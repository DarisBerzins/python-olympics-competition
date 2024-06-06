import pygame as pg
from methods import *
import os
from random import randrange

InitPygame()

clock = pg.time.Clock()

xmax = 1280
ymax = 720
reso = (xmax, ymax)
screen = pg.display.set_mode(reso)

background = animatedSurface("assets/bg", 20) #initialize the animation for the background
bg = background.update()
bgRect = bg.get_rect()
bgRect2 = bg.get_rect()

font = pg.font.SysFont(None, 24)

textBoxes = []

sprites = []
for file in os.listdir("assets/trash"):
    sprites.append(pg.image.load(os.path.join("assets/trash",file)))

sounds = []
for file in os.listdir("assets/trash_sounds"):
    snd = pg.mixer.Sound(os.path.join("assets/trash_sounds",file))
    snd.set_volume(0.25)
    sounds.append(snd)

dM_run = True

menu = True
menubg = pg.image.load("assets/cover/" + os.listdir("assets/cover")[0])
highscoresbg = pg.image.load("assets/cover/" + os.listdir("assets/cover")[1])

def runGame():

    t0 = 0.001 * pg.time.get_ticks()
    maxdt = 0.5

    flag = False

    running = True
    
    trash = [Obstacle(sprites,sounds,np.array([2.5*xmax,randrange(0, ymax-100, 50)]), 0)]
    trashinterval = xmax
    
    player = Player()
    keysNsprites = boatState(xmax, ymax)
    fps = Text('fps', None, 24, (255, 255, 255))
    speed = Text('speed', None, 24, (255, 255, 255))
    angleText = Text('angle', None, 24, (255, 255, 255))

    startfinish = startNfinish(-1000, 10000)
    runtime = 0
    runtimeText = Text('Runtime', "assets/power_pixel-7.ttf", 32, (255,0,0))
    finishText = Text("string", "assets/power_pixel-7.ttf", 32, (255,0,0))

    speedBoostOnPress = 350
    angularVelocity = 1.8
    trailSpeed = 400
    resetTime = 500 #milliseconds
    resetTimer = -1
    firstReset = True
    allowAnyKey = True
    textBoxCreated = False
    pastFinish = False

    while running:
        pg.display.flip()
        t = 0.001 * pg.time.get_ticks()
        dt = min(t-t0, maxdt)
        if dt > 0.0:
            clock.tick()
            t0 = t

            for event in pg.event.get(pump=True):
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    running = False
                
                for i in textBoxes: i.handleEvent(event)

                if not pastFinish:
                    if event.type == pg.KEYDOWN:
                        match event.key:
                            case pg.K_RIGHT: keysNsprites.right = True
                            case pg.K_LEFT: keysNsprites.left = True
                            case pg.K_d: keysNsprites.d = True
                            case pg.K_a: keysNsprites.a = True
                    
                    if event.type == pg.KEYUP:
                        match event.key:
                            case pg.K_RIGHT: keysNsprites.right = False
                            case pg.K_LEFT: keysNsprites.left = False
                            case pg.K_d: keysNsprites.d = False
                            case pg.K_a: keysNsprites.a = False

            player.polarVel[0] = np.linalg.norm(player.vel)
            player.polarVel[1] = np.arctan2(player.vel[1], -player.vel[0])

            if not pastFinish:
                if (keysNsprites.right and keysNsprites.left) or (keysNsprites.left and keysNsprites.d) or (keysNsprites.right and keysNsprites.a) or (keysNsprites.a and keysNsprites.d):
                    player.polarVel[0] -= min(speedBoostOnPress//4, player.polarVel[0]//6)
                elif keysNsprites.right and keysNsprites.d:
                    if not flag or allowAnyKey:
                        allowAnyKey = False
                        player.polarVel[0] += speedBoostOnPress
                    flag = True
                    player.polarVel[1] += angularVelocity * dt
                elif keysNsprites.left and keysNsprites.a:
                    if flag or allowAnyKey:
                        allowAnyKey = False
                        player.polarVel[0] += speedBoostOnPress
                    flag = False
                    player.polarVel[1] -= angularVelocity * dt
            
            if not any([keysNsprites.left, keysNsprites.right, keysNsprites.a, keysNsprites.d]):
                if firstReset:
                    resetTimer = pg.time.get_ticks()
                    firstReset = False
                currentDelta = pg.time.get_ticks() - resetTimer
            else:
                firstReset = True
                currentDelta = 0
            if not any([keysNsprites.left, keysNsprites.right, keysNsprites.a, keysNsprites.d]) and currentDelta > resetTime:
                allowAnyKey = True

            if player.polarVel[0] >= trailSpeed:
                keysNsprites.trailState = True
            else: keysNsprites.trailState = False
            # print(keysNsprites.left, keysNsprites.right, keysNsprites.a, keysNsprites.d, keysNsprites.trailState)
            player.frame = keysNsprites.selectSprite()

            player.vel[0] = -np.cos(player.polarVel[1])*player.polarVel[0]
            player.vel[1] = np.sin(player.polarVel[1])*player.polarVel[0]

            player.accel -= player.vel

            player.vel = player.vel + player.accel * dt
            player.pos = player.pos + player.vel * dt

            player.accel = np.array([0.0,  0.0])

            bgRect.left = player.pos[0] % xmax - xmax
            bgRect2.left = player.pos[0] % xmax
            
            bg = background.update()
            screen.blit(bg, bgRect)
            screen.blit(bg, bgRect2)

            for obj in trash:
                obj.pos[0] = xmax-(obj.initialpos-player.pos[0]) #trash movement
                obj.draw(screen)
                dx = player.hitbox.left - obj.hitbox.left
                dy = player.hitbox.top - obj.hitbox.top
                collide = obj.mask.overlap(player.mask, (dx, dy))
                if collide: 
                    if not obj.sounded:
                        sounds[obj.random].play()
                        obj.sounded = True
                else:
                    obj.sounded = False
                
    
            dist = (xmax-(obj.initialpos-player.pos[0]))
            if (xmax - trash[-1].pos[0] > trashinterval):
                trash.append(Obstacle(sprites,sounds,np.array([2.5*xmax,randrange(0, ymax-100, 50)]), player.pos[0]))
            # print(player.pos)

            player.draw(screen)
            keysNsprites.drawKeypressIndicators(screen)
            
            # startfinish.draw(screen)

            fps.draw(clock.get_fps(), (50, 20), screen)
            speed.draw(np.linalg.norm(player.vel), (xmax-50, 20), screen)
            angleText.draw(player.angle, (20, ymax-20), screen)

            for i in textBoxes: i.draw(screen)

            runtimeText.draw(runtime, (xmax/2,40), screen)

            if player.pos[0]<startfinish.startpos and player.pos[0]>startfinish.finishpos:
                runtime +=dt
            elif player.pos[0]<startfinish.finishpos:
                pastFinish = True
                keysNsprites.a = False
                keysNsprites.d = False
                keysNsprites.left = False
                keysNsprites.right = False

                finishText.draw("Congrats lol ur time is: " + str(runtime), (xmax/2,ymax/2), screen)
                pg.display.update()
                if not textBoxCreated:
                    textBoxes.append(textBox(200, 40, xmax//2, ymax//2, "assets/power_pixel-7.ttf", 36))
                    textBoxCreated = True
                if textBoxes[-1].returned:
                    f = open("scores.txt","a")
                    f.write("\n" + textBoxes[-1].getText() + "\t" + str(round(runtime,3)))
                    f.close()
                    textBoxes.remove(textBoxes[-1])
                    textBoxCreated = False
                    running = False
    return True #when the game is over occurs

def deathMenu(dM):
    scores = []
    f = open("scores.txt","r")
    for line in f:
        elements = line.split("\t")
        # print(elements)
        score = [elements[0], float(elements[1])]
        scores.append(score)
    f.close()
    scoreboard_rect = pg.Rect(0,0,600,600)
    scoreboard_rect.center = (xmax/2,ymax/2)
    pg.draw.rect(screen, (255,255,255), scoreboard_rect)
    scores.sort(key = lambda x: x[1])
    # print(scores)
    step = 100
    pos = 1
    for line in scores:
        txt = Text("string", "assets/power_pixel-7.ttf", 16, (0,0,0))
        txt.draw(str(pos)+". "+line[0]+" "+str(line[1]), (xmax/2, step),screen)
        step += 25
        pos += 1
    
    while dM:
        for event in pg.event.get(pump=True):
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                dM = False
            
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_UP: menuKeys.up = True
                    case pg.K_DOWN: menuKeys.down = True
            
            if event.type == pg.KEYUP:
                match event.key:
                    case pg.K_UP: menuKeys.up = False
                    case pg.K_DOWN: menuKeys.down = False

        pg.display.update()


while menu:
    for event in pg.event.get(pump=True):        
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            menu = False
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if runGame():
                    deathMenu(dM_run)
            match event.key:
                case pg.K_UP: menuKeys.up = True
                case pg.K_DOWN: menuKeys.down = True
    
    menuRect = pg.Rect(0,0,600,200)
    menuRect.center = (xmax/2,ymax/2)
    
    screen.blit(menubg, (0,0))
    pg.draw.rect(screen, (200,200,200), menuRect)
    
    pg.display.flip()
    # runGame()

pg.quit()