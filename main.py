import pygame as pg

pg.init()
clock = pg.time.Clock()

pg.display.set_caption("Balls")

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

background = pg.image.load("assets/test-image.png")
bgRect = background.get_rect()
bgRect2 = background.get_rect()

player = pg.Rect(100, ymax//2, 50, 50)

font = pg.font.SysFont(None, 24)

running = True
while running:
    t = 0.001 * pg.time.get_ticks()
    dt = min(t-t0, maxdt)
    if dt > 0.0:
        clock.tick()

        t0 = t

        fpsImage = font.render(str(int(clock.get_fps())), True, (255, 255, 255))

        pg.event.pump()
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            velocity += -10
        if keys[pg.K_LEFT]:
            velocity += 10
        if keys[pg.K_ESCAPE]:
            running = False

        velocity = velocity + acceleration * dt
        position = position + velocity * dt

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
        pg.draw.rect(screen, (128, 0, 255), player)

        pg.display.flip()

pg.quit()