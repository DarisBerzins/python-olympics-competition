import pygame as pg
from methods import *
import os
from random import randrange, randint

InitPygame()

clock = pg.time.Clock()

xmax = 1280
ymax = 720
reso = (xmax, ymax)
screen = pg.display.set_mode(reso)

enableMusic = True

background = animatedSurface("assets/bg", 20) #initialize the animation for the background
bg = background.update()
bgRect = bg.get_rect()
bgRect2 = bg.get_rect()

font = pg.font.SysFont(None, 24)
pixel_font = "assets/power_pixel-7.ttf"

textBoxes = []

gameSound = pg.mixer.Sound('assets/sounds/background-music.wav')
gameSound.set_volume(0.25)

menuSound = pg.mixer.Sound('assets/sounds/menu-music.wav')
menuSound.set_volume(0.25)

trashSprites = []
for file in os.listdir("assets/trash"):
    trashSprites.append(pg.image.load(os.path.join("assets/trash",file)))

trashSounds = []
for file in os.listdir("assets/trash_sounds"):
    snd = pg.mixer.Sound(os.path.join("assets/trash_sounds",file))
    snd.set_volume(0.25)
    trashSounds.append(snd)

boostSprites = []
for file in os.listdir("assets/boosts"):
    boostSprites.append(pg.image.load(os.path.join("assets/boosts", file)))

boostSounds = []
for file in os.listdir("assets/boost_sounds"):
    snd = pg.mixer.Sound(os.path.join("assets/boost_sounds", file))
    snd.set_volume(0.25)
    boostSounds.append(snd)

keysNsprites = boatState(xmax, ymax)

flag = False

t0 = 0.001 * pg.time.get_ticks()
maxdt = 0.5

running = True

game = False
menu = False
scorebd = False
intro = True

enteredGame = True
enteredMenu = True
enteredScorebd = True

pulseEnter = True

exitingScoreboard = False

dM_run = True

menubg = pg.image.load("assets/cover/" + os.listdir("assets/cover")[0])
highscoresbg = pg.image.load("assets/cover/" + os.listdir("assets/cover")[1])
introbg = pg.image.load("assets/cover/" + os.listdir("assets/cover")[2])

menu_keys = menuKeys()
select = 0
pressed = False
firstTimeInMenu = True

def setMenu():
    global menu, game, scorebd, enteredMenu, select, exitingScoreboard
    if scorebd:
        exitingScoreboard = True
    select = 0
    enteredMenu = True
    menu = True
    game = False
    scorebd = False
    gameSound.stop()

def setGame():
    global menu, game, scorebd, enteredGame, select
    select = 0
    game = True
    enteredGame = True
    menu = False
    scorebd = False
    gameSound.stop()

def setScorebd():
    global menu, game, scorebd, enteredScorebd, select
    select = 0
    enteredScorebd = True
    scorebd = True
    menu = False
    game = False

buttons = [button(400,50,(xmax/2,ymax/2-70),"START",pixel_font,32,(255,0,0),(0,255,0),setGame),
           button(400,50,(xmax/2,ymax/2),"SCOREBOARD",pixel_font,32,(255,0,0),(0,255,0),setScorebd),
           button(400,50,(xmax/2,ymax/2+70),"QUIT",pixel_font,32,(255,0,0),(0,255,0),quit)]

deadbuttons = [button(400,50,(xmax/2,ymax/2),"RESTART",pixel_font,32,(255,0,0),(0,255,0), setGame),
           button(400,50,(xmax/2,ymax/2+80),"MAIN MENU",pixel_font,32,(255,0,0),(0,255,0),setMenu)]

def initGame():
    global trash, trashIntervalMultiplier, trashInterval, boosters, boostIntervalMultiplier, boostInterval, player, fps, speed, angleText, startfinish, runtime, runtimeText, finishText, border, speedBoostOnPress, speedBoostOnBooster, angularVelocity, trailSpeed, resetTime, resetTimer, firstReset, allowAnyKey, textBoxCreated, pastFinish, select, pressed, flag, pulseEnter
    trash = [Obstacle(trashSprites,np.array([2.5*xmax,randrange(0, ymax-100, 50)]), 0)]
    trashIntervalMultiplier = 0.6
    trashInterval = randint(xmax//2, xmax//0.5) * trashIntervalMultiplier

    boosters = [Powerup(boostSprites, np.array([2.5*xmax, randrange(0, ymax-100, 50)]), 0)]
    boostIntervalMultiplier = 1.5
    boostInterval = randint(xmax//2, xmax//0.5) * boostIntervalMultiplier

    player = Player()
    
    fps = Text('fps', None, 24, colors.white)
    speed = Text('speed', None, 24, colors.white)
    angleText = Text('angle', None, 24, colors.white)

    startfinish = startNfinish(-1000, 10000, pg.image.load('assets/start_line.png'), pg.image.load('assets/finish_line.png'), xmax, ymax)
    runtime = 0
    runtimeText = Text('Runtime', pixel_font, 32, colors.selectedButtonColor)
    finishText = Text("string", pixel_font, 32, colors.selectedButtonColor)

    border = Borders('assets/borders.png')

    speedBoostOnPress = 350
    speedBoostOnBooster = 1000
    angularVelocity = 1.8
    trailSpeed = 400
    resetTime = 500 #milliseconds
    resetTimer = -1
    firstReset = True
    allowAnyKey = True
    textBoxCreated = False
    pastFinish = False
    flag = False
    if enableMusic: gameSound.play(-1)
    keysNsprites.stopInputs = False
    select = 0
    pressed = False

def gameFrame():
    global trash, trashIntervalMultiplier, trashInterval, boosters, boostIntervalMultiplier, boostInterval, player, fps, speed, angleText, startfinish, runtime, runtimeText, finishText, border, speedBoostOnPress, speedBoostOnBooster, angularVelocity, trailSpeed, resetTime, resetTimer, firstReset, allowAnyKey, textBoxCreated, pastFinish, select, pressed, flag, pulseEnter
    player.polarVel[0] = np.linalg.norm(player.vel)
    player.polarVel[1] = np.arctan2(player.vel[1], -player.vel[0])

    if not (pastFinish or player.dead):
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

    player.frame = keysNsprites.selectSprite()

    for obj in boosters:
        obj.pos[0] = xmax-(obj.initialpos-player.pos[0]) #trash movement
        dx = player.hitbox.left - obj.hitbox.left
        dy = player.hitbox.top - obj.hitbox.top
        collide = obj.mask.overlap(player.mask, (dx, dy))
        if collide: 
            if not obj.used:
                player.polarVel[0] += speedBoostOnBooster
                boostSounds[obj.random].play()
            obj.used = True
            

    player.vel[0] = -np.cos(player.polarVel[1])*player.polarVel[0]
    player.vel[1] = np.sin(player.polarVel[1])*player.polarVel[0]

    player.accel -= player.vel
    if player.dead:
        player.accel -= player.vel * 6

    player.vel = player.vel + player.accel * dt
    player.pos = player.pos + player.vel * dt

    player.accel = np.array([0.0,  0.0])

    bgRect.left = player.pos[0] % xmax - xmax
    bgRect2.left = player.pos[0] % xmax - 10
    
    bg = background.update()
    screen.blit(bg, bgRect)
    screen.blit(bg, bgRect2)

    for a in boosters: a.draw(screen)

    for obj in trash:
        obj.pos[0] = xmax-(obj.initialpos-player.pos[0]) #trash movement
        obj.draw(screen, xmax)
        dx = player.hitbox.left - obj.hitbox.left
        dy = player.hitbox.top - obj.hitbox.top
        collide = obj.mask.overlap(player.mask, (dx, dy))
        if collide: 
            player.dead = True
            if not obj.sounded:
                trashSounds[obj.random].play()
                obj.sounded = True
        else:
            obj.sounded = False

    border.update(player.pos[0], xmax)
    if border.mask.overlap(player.mask, (player.hitbox.left, player.hitbox.top)):
        player.dead = True

    if player.dead or player.pos[0] < startfinish.finishpos:
        keysNsprites.stopInputs = True
        
    if (xmax - trash[-1].pos[0] > trashInterval):
        trash.append(Obstacle(trashSprites,np.array([3.5*xmax,randrange(150, ymax-100, 50)]), player.pos[0] - 100))
        trashInterval = randint(xmax//2, xmax//0.5) * trashIntervalMultiplier

    if (xmax - boosters[-1].pos[0] > boostInterval):
        boosters.append(Powerup(boostSprites,np.array([3.5*xmax,randrange(150, ymax-100, 50)]), player.pos[0] - 100))
        boostInterval = randint(xmax//2, xmax//0.5) * boostIntervalMultiplier

    player.draw(screen)
    startfinish.draw(screen, player.pos[0], xmax)
    keysNsprites.drawKeypressIndicators(screen)

    fps.draw(clock.get_fps(), (50, 20), screen)
    speed.draw(np.linalg.norm(player.vel), (xmax-50, 20), screen)
    angleText.draw(player.angle, (20, ymax-20), screen)

    runtimeText.draw(runtime, (xmax/2,60), screen)
    
    if player.pos[0]<startfinish.finishpos:
        pastFinish = True
        keysNsprites.a = False
        keysNsprites.d = False
        keysNsprites.left = False
        keysNsprites.right = False
        
        end_rect = pg.Rect(0,0,600,200)
        end_rect.center = (xmax/2,ymax/2)
        pg.draw.rect(screen, colors.white, end_rect)
        finishText.draw("Finish!!", (xmax/2,ymax/2-50), screen)
        finishText.draw("Press enter to submit",(xmax/2,ymax/2+50), screen)
        finishText.draw("and quit to main menu",(xmax/2,ymax/2+80), screen)
        for i in textBoxes: i.draw(screen)
        
        if not textBoxCreated:
            textBoxes.append(textBox(300, 60, xmax//2, ymax//2, "assets/power_pixel-7.ttf", 36))
            textBoxCreated = True
        if textBoxes[-1].returned:
            with open("scores.csv","a") as f:
                f.write(textBoxes[-1].getText() + "," + str(round(runtime,3)) + "\n")
                
            textBoxes.remove(textBoxes[-1])
            textBoxCreated = False
            setMenu()
            pulseEnter = False
            
    elif player.dead:
        if menu_keys.enter and pulseEnter:
            pulseEnter = False
            deadbuttons[select].execute()
        
        dead_surf = pg.Surface((650,325))
        dead_surf.set_alpha(128)
        dead_rect = dead_surf.get_rect()
        dead_rect.center = (xmax/2,ymax/2)
        screen.blit(dead_surf,dead_rect)
        finishText.draw("you crashed and drowned", (xmax//2, ymax//2-100), screen) 
        finishText.draw("in the Seine River :(", (xmax//2, ymax//2-70), screen) 

        if menu_keys.up: select-=1; menu_keys.up = False
        elif menu_keys.down: select+=1; menu_keys.down = False
        
        if select == len(deadbuttons): select = 0
        if select < 0: select = len(deadbuttons)-1    

        for but in deadbuttons:
            but.draw(screen)
            but.buttoncolor = colors.unSelectedButtonColor
        deadbuttons[select].buttoncolor = colors.selectedButtonColor
        
    elif player.pos[0]<startfinish.startpos and player.pos[0]>startfinish.finishpos:
        runtime +=dt

def exitGame():
    if enableMusic: gameSound.stop()


def initScoreboard():
    global scores
    scores = []
    with open("scores.csv","r") as f:
        for line in f:
            score = line.strip("\n").split(",")
            score[-1] = float(score[-1])
            scores.append(score)
    
    scoreboard_rect = pg.Rect(0,0,500,400)
    scoreboard_rect.center = (xmax/2,ymax/2)
    pg.draw.rect(screen, colors.white, scoreboard_rect)
    scores.sort(key = lambda x: x[1])
    scores = scores[0:min(len(scores),10)]

def scoreboardFrame():
    step = 100
    pos = 1
    
    for event in pg.event.get(pump=True):
        if event.type == pg.QUIT or menu_keys.escape:
            dM = False
            menu_keys.escape = False

        if event.type == pg.KEYDOWN:
            match event.key:
                case pg.K_UP: menu_keys.up = True
                case pg.K_DOWN: menu_keys.down = True
                case pg.K_ESCAPE: menu_keys.escape = True; 

        if event.type == pg.KEYUP:
            match event.key:
                case pg.K_UP: menu_keys.up = False
                case pg.K_DOWN: menu_keys.down = False
    screen.blit(highscoresbg,(0,0))
    for line in scores:
        txt = Text("string", "assets/power_pixel-7.ttf", 24, colors.black)
        txt.draw(str(pos)+". "+line[0]+" "+str(line[1]), (xmax/2, step+100),screen)
        step += 25
        pos += 1


def initMenu():
    global enableMusic, exitingScoreboard
    if enableMusic and not exitingScoreboard: 
        menuSound.play(-1)
        exitingScoreboard = False

def menuFrame():
    global select, pulseEnter
    if menu_keys.enter and pulseEnter:
        pulseEnter = False
        if select == 0: 
            if enableMusic: menuSound.stop()
        buttons[select].execute()

    if menu_keys.up: select-=1; menu_keys.up = False
    elif menu_keys.down: select+=1; menu_keys.down = False
    
    if select == len(buttons): select = 0
    if select < 0: select = len(buttons)-1    
    
    screen.blit(menubg, (0,0))
    for but in buttons:
        but.draw(screen)
        but.buttoncolor = colors.unSelectedButtonColor
    buttons[select].buttoncolor = colors.selectedButtonColor


while running:
    t = 0.001 * pg.time.get_ticks()
    dt = min(t-t0, maxdt)
    if dt > 0.0:
        clock.tick()
        t0 = t
        #====================================================== INPUTS
        for event in pg.event.get(pump=True):
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                if menu:
                    running = False
                else:
                    setMenu()
            
            for i in textBoxes: i.handleEvent(event)

            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_RIGHT: keysNsprites.right = True
                    case pg.K_LEFT: keysNsprites.left = True
                    case pg.K_d: keysNsprites.d = True
                    case pg.K_a: keysNsprites.a = True
                    case pg.K_ESCAPE: menu_keys.escape = True
                    case pg.K_RETURN: menu_keys.enter = True
                    case pg.K_UP: menu_keys.up = True
                    case pg.K_DOWN: menu_keys.down = True
            
            if event.type == pg.KEYUP:
                match event.key:
                    case pg.K_RIGHT: keysNsprites.right = False
                    case pg.K_LEFT: keysNsprites.left = False
                    case pg.K_d: keysNsprites.d = False
                    case pg.K_a: keysNsprites.a = False
                    case pg.K_RETURN: menu_keys.enter = False; pulseEnter = True
                    case pg.K_UP: menu_keys.up = False
                    case pg.K_DOWN: menu_keys.down = False
        #============================================================= INPUTS
        if intro:
            screen.blit(introbg, screen.get_rect())

        if menu:
            if enteredMenu:
                enteredMenu = False
                initMenu() #First time run
            menuFrame() #everything in menu

        if game:
            if enteredGame:
                enteredGame = False
                initGame()
            gameFrame()
            if not game:
                exitGame()
        
        if scorebd:
            if enteredScorebd:
                enteredScorebd = False
                initScoreboard()
            scoreboardFrame()

        pg.display.flip()

pg.quit()