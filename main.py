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

velocity = 0
acceleration = 0
position = 0
position2 = xmax
value = 0
vert = 0
timerThing = 0.0
flag = False
leftFlag = False
rightFlag = False

class pressedKeys():
    left = False
    right = False
    a = False
    d = False

background = pg.image.load("assets/test-image.png")
bgRect = background.get_rect()
bgRect2 = background.get_rect()

font = pg.font.SysFont(None, 24)

dir = "assets/trash"
sprites = []
for file in os.listdir(dir):
    sprites.append(pg.image.load(os.path.join(dir,file)))

running = True
trash = []
while running:
    t = 0.001 * pg.time.get_ticks()
    dt = min(t-t0, maxdt)
    if dt > 0.0:
        clock.tick()
        t0 = t

        fpsImage = font.render("FPS: " + str(int(clock.get_fps())), True, (255, 255, 255))
        speedImage = font.render("Speed: " + str(value), True, (255, 255, 255))

        for event in pg.event.get(pump=True):
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False
            
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_RIGHT: pressedKeys.right = True
                    case pg.K_LEFT: pressedKeys.left = True
                    case pg.K_d: pressedKeys.d = True
                    case pg.K_a: pressedKeys.a = True
            
            if event.type == pg.KEYUP:
                match event.key:
                    case pg.K_RIGHT: pressedKeys.right = False
                    case pg.K_LEFT: pressedKeys.left = False
                    case pg.K_d: pressedKeys.d = False
                    case pg.K_a: pressedKeys.a = False
        if (pressedKeys.right and pressedKeys.left) or (pressedKeys.left and pressedKeys.d) or (pressedKeys.right and pressedKeys.a) or (pressedKeys.a and pressedKeys.d):
            pass
        elif pressedKeys.right and pressedKeys.d:
            if not flag:
                value -= 20
            flag = True
            vert += 1
        elif pressedKeys.left and pressedKeys.a:
            if flag:
                value -= 20
            flag = False
            vert -= 1

        timerThing += dt
        if timerThing > 0.1:
            timerThing = 0.0
            if value < -5:
                value += 5
                value //= 1.1
            elif value > -5:
                value = -5     
        
        position = position + value * dt
        position2 = position + xmax
        bgRect.left = position
        bgRect2.left = position2
        
        if position > xmax:
            position = 0
        elif position < -xmax:
            position = 0
        
        screen.blit(background, bgRect)
        screen.blit(background, bgRect2)

        screen.blit(fpsImage, (20, 20))
        screen.blit(speedImage, (xmax-100, 20))

        screen.blit(Player.surf, (100, 2*ymax//3 + vert))
        
        if position%50==0:
            trash.append(Obstacle(sprites,xmax,randrange(0, ymax-100, 100),-5))
        for obj in trash:
            obj.v = value
            obj.move(dt)
            obj.draw(screen)

        pg.display.flip()

pg.quit()




