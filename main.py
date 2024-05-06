import pygame as pg

pg.init()
t0 = 0.001 * pg.time.get_ticks()

maxdt = 0.5


xmax = 1280
ymax = 720
reso = (xmax, ymax)
screen = pg.display.set_mode(reso)

velocity = 0
acceleration = 0
position = xmax//2

background = pg.image.load("assets/test-image.png")
bgRect = background.get_rect()

player = pg.Rect(100, ymax//2, 50, 50)

running = True
while running:
    t = 0.001 * pg.time.get_ticks()
    dt = min(t-t0, maxdt)
    if dt > 0.0:
        t0 = t

        pg.event.pump()
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            velocity += 10
        if keys[pg.K_LEFT]:
            velocity += -10
        if keys[pg.K_ESCAPE]:
            running = False

        velocity = velocity + acceleration * dt
        position = position + velocity * dt

        bgRect.centerx = position
        
        screen.blit(background, bgRect)
        pg.draw.rect(screen, (128, 0, 255), player)

        pg.display.flip()




    pass




pg.quit()