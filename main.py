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

background = pg.image.load("assets/test-image.png")
bgRect = background.get_rect()
bgRect2 = background.get_rect()

font = pg.font.SysFont(None, 24)

dir = "assets/trash"
sprites = []
for file in os.listdir(dir):
    sprites.append(pg.image.load(os.path.join(dir,file)))

running = True
trash = [Obstacle(sprites,np.array([2*xmax,randrange(0, ymax-100, 50)]), 0)]
trashinterval = xmax

player = Player()
fps = Text('fps', None, 24, (255, 255, 255))
speed = Text('speed', None, 24, (255, 255, 255))

minvel = 500

while running:
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

        player.vel[1] = 0
        if (pressedKeys.right and pressedKeys.left) or (pressedKeys.left and pressedKeys.d) or (pressedKeys.right and pressedKeys.a) or (pressedKeys.a and pressedKeys.d):
            pass
        elif pressedKeys.right and pressedKeys.d:
            if not flag:
                player.vel[0] -= 50
                startTime = pg.time.get_ticks()
            flag = True
            player.vel[1] = startTime*100/(pg.time.get_ticks())
        elif pressedKeys.left and pressedKeys.a:
            if flag:
                player.vel[0] -= 50
                startTime = pg.time.get_ticks()
            flag = False
            player.vel[1] = -startTime*100/(pg.time.get_ticks())

        timeStep += dt
        if timeStep > 0.1:
            timeStep = 0.0
            if player.vel[0] < -minvel:
                player.vel[0] += minvel
                player.vel[0] //= 1.1
            elif player.vel[0] > -minvel:
                player.vel[0] = -minvel     

        player.pos = player.pos + player.vel * dt

        bgRect.left = player.pos[0] % xmax - xmax
        bgRect2.left = player.pos[0] % xmax
        
        screen.blit(background, bgRect)
        screen.blit(background, bgRect2)

        for obj in trash:
            obj.pos[0] = xmax-(obj.initialpos-player.pos[0])
            obj.draw(screen)
            # collide = pg.Rect.colliderect(player.hitbox, obj.hitbox)
            collide = obj.mask.overlap(player.mask,(100 - obj.pos[0], player.pos[1] - obj.pos[1]))

            if collide: 
                obj.color = (0,255,0)
 
        dist = (xmax-(obj.initialpos-player.pos[0]))
        if (xmax - trash[-1].pos[0] > trashinterval):
            trash.append(Obstacle(sprites,np.array([xmax,randrange(0, ymax-100, 50)]), player.pos[0]))

        player.draw(screen)

        fps.draw(clock.get_fps(), (20, 20), screen)
        speed.draw(np.linalg.norm(player.vel), (xmax-100, 20), screen)

        pg.display.flip()

pg.quit()