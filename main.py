import pygame as pg
from methods import *
import os
from random import randrange

InitPygame()

clock = pg.time.Clock()

t0 = 0.001 * pg.time.get_ticks()
maxdt = 0.5

xmax = 1280
ymax = 720
reso = (xmax, ymax)
screen = pg.display.set_mode(reso)

timeStep = 0.0
flag = False
startTime = 0

background = animatedSurface("assets/bg", 20) #initialize the animation for the background
bg = background.update()
bgRect = bg.get_rect()
bgRect2 = bg.get_rect()

font = pg.font.SysFont(None, 24)

sprites = []
for file in os.listdir("assets/trash"):
    sprites.append(pg.image.load(os.path.join("assets/trash",file)))

sounds = []
for file in os.listdir("assets/trash_sounds"):
    snd = pg.mixer.Sound(os.path.join("assets/trash_sounds",file))
    snd.set_volume(0.25)
    sounds.append(snd)

running = True
deathMenu = False
trash = [Obstacle(sprites,sounds,np.array([2.5*xmax,randrange(0, ymax-100, 50)]), 0)]
trashinterval = xmax

player = Player()
keysNsprites = boatState()
fps = Text('fps', None, 24, (255, 255, 255))
speed = Text('speed', None, 24, (255, 255, 255))
angleText = Text('angle', None, 24, (255, 255, 255))

startfinish = startNfinish(-1000, 10000)
runtime = 0
runtimeText = Text('Runtime', "assets/power_pixel-7.ttf", 32, (255,0,0))
finishText = Text("string", "assets/power_pixel-7.ttf", 32, (255,0,0))

minvel = 5
speedBoostOnPress = 350
angularVelocity = 1.8
trailSpeed = 400
resetTime = 500 #milliseconds
resetTimer = -1
firstReset = True
allowAnyKey = True

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

        if (keysNsprites.right and keysNsprites.left) or (keysNsprites.left and keysNsprites.d) or (keysNsprites.right and keysNsprites.a) or (keysNsprites.a and keysNsprites.d):
            # player.frame = 0
            player.polarVel[0] -= min(speedBoostOnPress//6, player.polarVel[0]//8)
        elif keysNsprites.right and keysNsprites.d:
            if not flag or allowAnyKey:
                allowAnyKey = False
                player.polarVel[0] += speedBoostOnPress
                # player.frame = 1
            flag = True
            player.polarVel[1] += angularVelocity * dt
        elif keysNsprites.left and keysNsprites.a:
            if flag or allowAnyKey:
                allowAnyKey = False
                player.polarVel[0] += speedBoostOnPress
                # player.frame = 2
            flag = False
            player.polarVel[1] -= angularVelocity * dt
        else:
            # player.frame = 0
            pass
        
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

        if player.polarVel[0] >= 400:
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
            # collide = pg.Rect.colliderect(player.hitbox, obj.hitbox)
            collide = obj.mask.overlap(player.mask,(200 - obj.pos[0], player.pos[1] - obj.pos[1]))

            if collide: 
                obj.color = (0,255,0)
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
        
        # startfinish.draw(screen)

        fps.draw(clock.get_fps(), (50, 20), screen)
        speed.draw(np.linalg.norm(player.vel), (xmax-50, 20), screen)
        angleText.draw(player.angle, (20, ymax-20), screen)

        runtimeText.draw(runtime, (xmax/2,40), screen)

        if player.pos[0]<startfinish.startpos and player.pos[0]>startfinish.finishpos:
            runtime +=dt
        elif player.pos[0]<startfinish.finishpos:
            finishText.draw("Congrats lol ur time is: " + str(runtime), (xmax/2,ymax/2), screen)
            pg.display.update()
            playerName = input("UR NAME HERE (FOR NOW) ")
            f = open("scores.txt","a")
            f.write("\n" + playerName + "\t" + str(round(runtime,3)))
            f.close()
            running = False
            dM_run = True

def deathMenu(dM):
    scores = []
    f = open("scores.txt","r")
    for line in f:
        elements = line.split()
        print(elements)
        score = [elements[0], float(elements[1])]
        scores.append(score)
    f.close()
    
    scores.sort(key = lambda x: x[1])
    print(scores)

    while dM:
        for event in pg.event.get(pump=True):
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    dM = False
                
                if event.type == pg.KEYDOWN:
                    match event.key:
                        case pg.K_UP: keysNsprites.right = True
                        case pg.K_DOWN: keysNsprites.d = True
                
                if event.type == pg.KEYUP:
                    match event.key:
                        case pg.K_UP: keysNsprites.right = False
                        case pg.K_DOWN: keysNsprites.left = False
               
        # pg.draw.rect(screen, (40,40,40), pg.Rect(200,200,200,200))
        pg.display.update()

deathMenu(dM_run)

pg.quit()