import numpy as np
import pygame as pg
from random import randrange
import os

class boatState():
    
    def __init__(self):
        self.left = False
        self.right = False
        self.a = False
        self.d = False
        self.trailState = False
    
    def selectSprite(self): #0 is left, 1 is none, 2 is right
        if self.right == self.left: self.rearState = 1
        elif self.left: self.rearState = 2
        elif self.right: self.rearState = 0

        if self.a == self.d: self.frontState = 1
        elif self.a: self.frontState = 2
        elif self.d: self.frontState = 0

        if self.trailState:
            # print(3 * self.rearState + self.frontState + 1, self.trailState)
            return 3 * self.rearState + self.frontState + 1
        else:
            # print(10 + 3 * self.rearState + self.frontState, self.trailState)
            return 10 + 3 * self.rearState + self.frontState

class animatedSurface():
    sprites = []
    def __init__(self, folderdir, delay):
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
    pos = np.array([0.0, 300.0])
    vel = np.array([-1.0, 0.0])
    accel = np.array([0.0, 0.0])
    polarVel = np.array([0.0, 0.0])
    mass = 1
    folderdir = 'assets/kayak'
    sprites = []
    rotatedSprites = []
    rotatedHitboxes = []
    angle = 20
    frame = 0
    for file in os.listdir(folderdir):
        sprites.append(pg.transform.scale_by(pg.image.load(os.path.join(folderdir, file)), 2.2))
    for i in range(len(sprites)):
        tempList = []
        for angleRange in range(0, 361):
            tempList.append(pg.transform.rotate(sprites[i], angleRange))
        rotatedSprites.append(tempList)
    
    hitboxSprite = pg.image.load("assets/kayak-no-paddles.png")
    hitbox = hitboxSprite.get_rect()
    for i in range(0, 361):
        rotatedHitboxes.append(pg.transform.rotate(hitboxSprite, i))
    mask = pg.mask.from_surface(hitboxSprite)
    # hitbox.height -= 20
    def draw(self,screen):
        
        self.angle = -int(np.degrees(np.arctan2(self.vel[1], -self.vel[0])))
        self.hitbox = self.rotatedSprites[self.frame][self.angle].get_rect()
        self.hitbox.center = (200, self.pos[1])
        self.mask = pg.mask.from_surface(self.rotatedHitboxes[self.angle])
        # pg.draw.rect(screen, (255, 0, 0), self.hitbox)
        if self.frame == 0: self.angle = 0
        screen.blit(self.rotatedSprites[self.frame][self.angle], self.hitbox)  
        # print(self.vel)      
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

class startNfinish():
    def __init__(self, startpos, lengthofTrack):
        self.startpos = startpos
        self.finishpos = self.startpos - lengthofTrack
        # self.initialpos = initialpos
    def draw(self, screen):
        pg.draw.rect(screen, (255,0,0), pg.Rect(self.startpos,0,100,screen.get_size()[0])) #doesn't work
    
    


class Text():
    def __init__(self, type: str, font, fontSize: int, color):
        self.type = type
        self.font = pg.font.Font(font, fontSize)
        self.color = color

    def draw(self, value, position, screen):
        if self.type == 'fps':
            self.image = self.font.render("FPS: " + str(int(value)), True, self.color)
        elif self.type == 'speed':
            self.image = self.font.render("Speed: " + str(int(value)), True, self.color)
        elif self.type == 'angle':
            self.image = self.font.render("Angle: " + str(int(value)), True, self.color)
        elif self.type == 'Runtime':
            self.image = self.font.render("Run time: " + str(round(value,3)), True, self.color)
        elif self.type == 'string':
            self.image = self.font.render(value, True, self.color)
        self.rect = self.image.get_rect(center = position)
        screen.blit(self.image, self.rect)

#methods
def InitPygame():
    pg.init()
    pg.display.set_caption("THE MOST FRENCH EXPERIENCE")
    icon = pg.image.load('assets/french_flag.png')
    pg.display.set_icon(icon)