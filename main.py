import pygame as pg
import methods

methods.InitPygame()

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
timerThing = 0.0
flag = False
leftFlag = False
rightFlag = False

background = pg.image.load("assets/test-image.png")
bgRect = background.get_rect()
bgRect2 = background.get_rect()

player = pg.Rect(100, (2*ymax)//3, 50, 50)
player2 = pg.Rect(100, ymax//3, 50, 50)

font = pg.font.SysFont(None, 24)

def GetAlternatingInputs(keys, value, flag):
    
    return value

running = True
while running:
    t = 0.001 * pg.time.get_ticks()
    dt = min(t-t0, maxdt)
    if dt > 0.0:
        clock.tick()
        t0 = t

        fpsImage = font.render("FPS: " + str(int(clock.get_fps())), True, (255, 255, 255))
        speedImage = font.render("Speed: " + str(value), True, (255, 255, 255))

        pg.event.pump()
        keys = pg.key.get_pressed()
        
        # for event in pg.event.get():
        #     if event.type == pg.quit():
        #         running = False
            # if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT and not leftFlag:
            #     rightFlag = True
            #     value -= 10
            # elif event.type == pg.KEYUP and event.key == pg.K_RIGHT:
            #     rightFlag = False
            # if event.type == pg.KEYDOWN and event.key == pg.K_LEFT and not rightFlag:
            #     leftFlag = True
            #     value -= 10
            # elif event.type == pg.KEYUP and event.key == pg.K_LEFT:
            #     leftFlag = False

        if keys[pg.K_LEFT] and keys[pg.K_RIGHT]:
            pass
        elif keys[pg.K_RIGHT] and flag:
            value -= 10
            flag = False
        elif keys[pg.K_LEFT] and not flag:
            value -= 10
            flag = True

        if keys[pg.K_ESCAPE]:
            running = False

        timerThing += dt
        if timerThing > 0.1:
            timerThing = 0.0
            if value < 0:
                value += 5
                value //= 1.1
            elif value > 0:
                value = 0

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
        pg.draw.rect(screen, (128, 0, 255), player)
        pg.draw.rect(screen, (0, 128, 255), player2)
        pg.display.flip()

pg.quit()