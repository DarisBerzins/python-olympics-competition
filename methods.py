import numpy as np
import pygame as pg
from random import randrange
import os

class pressedKeys():
    left = False
    right = False
    a = False
    d = False

class animatedSurface():
    sprites = []
    def __init__(self,folderdir, delay):
        for file in os.listdir(folderdir):
            self.sprites.append(pg.image.load(os.path.join(folderdir,file)))
        self.counter = 0
        self.frames = 0
        self.delay = delay
    def update(self):
        current = self.sprites[self.counter]
        self.frames += 1
        if self.frames >= self.delay:
            self.frames = 0
            self.counter += 1
        if self.counter > len(self.sprites)-1:
            self.counter = 0
        return current
        
        

class Player():
    pos = np.array([0, 300])
    vel = np.array([0, 0])
    folderdir = 'assets/kayak'
    sprites = []
    frame = 0
    for file in os.listdir(folderdir):
        sprites.append(pg.transform.scale_by(pg.image.load(os.path.join(folderdir, file)), 2.2))
    hitboxSprite = pg.image.load("assets/kayak-no-paddles.png")
    hitbox = hitboxSprite.get_rect()
    mask = pg.mask.from_surface(hitboxSprite)
    # hitbox.height -= 20
    def draw(self,screen):
        self.hitbox.topleft = (100, self.pos[1])
        # pg.draw.rect(screen, (255, 0, 0), self.hitbox)
        screen.blit(self.sprites[self.frame],(100, self.pos[1])) #store the position in the class lol (do it)!!!!!!!!!!!!!!!!!!!!!11
        
        # screen.blit(self.mask,(100, self.pos[1]))

class Obstacle():
    # sprite = [pg.image.load("assets/rat.png"), pg.image.load("assets/")]  
    color = (255, 0, 0)
    def __init__(self,sprites,sounds,pos,initialpos):
        self.random = randrange(0,len(sprites))
        self.sprite = sprites[self.random]
        self.sprite = pg.transform.scale_by(self.sprite, 1)
        self.pos = pos
        self.initialpos = initialpos
        self.hitbox = self.sprite.get_rect()
        self.mask = pg.mask.from_surface(self.sprite)
        self.sounded = False
    
    # def move(self,dt):
    #     self.x += self.v*dt
    def draw(self,screen):
        self.hitbox.topleft = self.pos
        # pg.draw.rect(screen, self.color, self.hitbox)
        screen.blit(self.sprite,self.pos)
    
        # screen.blit(self.mask, self.pos)

class Text():
    def __init__(self, type: str, font, fontSize: int, color):
        self.type = type
        self.font = pg.font.SysFont(font, fontSize)
        self.color = color

    def draw(self, value, position, screen):
        if self.type == 'fps':
            self.image = self.font.render("FPS: " + str(int(value)), True, self.color)
        elif self.type == 'speed':
            self.image = self.font.render("Speed: " + str(int(value)), True, self.color)
        screen.blit(self.image, position)

#methods
def InitPygame():
    pg.init()
    pg.display.set_caption("THE MOST FRENCH EXPERIENCE")
    icon = pg.image.load('assets/french_flag.png')
    pg.display.set_icon(icon)
