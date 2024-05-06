import pygame as pg

pg.init()
t0 = 0.001 * pg.time.get_ticks()

maxdt = 0.5


xmax = 720
ymax = 480
reso = (xmax, ymax)
screen = pg.display.set_mode(reso)

ax = 0
ay = 0
vx = 0
vy = 0
sx = xmax//2
sy = ymax//2

player = pg.Rect(sx, sy, 50, 50)

running = True
while running:
    t = 0.001 * pg.time.get_ticks()
    dt = min(t-t0, maxdt)
    if dt > 0.0:
        t0 = t

        pg.draw.rect(screen, (255, 255, 255), screen.get_rect())

        pg.event.pump()
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            vy += -1
        if keys[pg.K_DOWN]:
            vy += 1
        if keys[pg.K_RIGHT]:
            vx += 1
        if keys[pg.K_LEFT]:
            vx += -1
        if keys[pg.K_ESCAPE]:
            running = False

        vx = vx + ax * dt
        vy = vy + ay * dt
        sx = sx + vx * dt
        sy = sy + vy * dt

        player.centerx = sx
        player.centery = sy
        
        pg.draw.rect(screen, (0, 0, 255), player)
        pg.display.flip()




    pass




pg.quit()