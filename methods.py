import numpy as np
import pygame as pg
from random import randrange
import os

class pressedKeys():
    left = False
    right = False
    a = False
    d = False

class Player():
    pos = np.array([0, 0])
    vel = np.array([0, 0])
    frame = 0
    if frame == 0:
        sprite = pg.image.load("assets/testboat.png")
    elif frame == 1:
        pass #make this the right stroke sprite
    elif frame == 2:
        pass #make this the left stroke sprite
    elif frame == 3:
        pass #make this the destroyed boat sprite
    hitbox = sprite.get_rect()
    
    def draw(self,screen):
        self.hitbox = self.sprite.get_rect()
        screen.blit(self.hitbox,(self.x,self.y))
        screen.blit(self.sprite,(self.x,self.y)) #store the position in the class lol (do it)!!!!!!!!!!!!!!!!!!!!!11

class Obstacle():
    # sprite = [pg.image.load("assets/rat.png"), pg.image.load("assets/")]  
    def __init__(self,sprites,x,y,v):
        self.sprite = sprites[randrange(0,len(sprites)-1)]
        self.sprite = pg.transform.scale(self.sprite, (200,200))
        self.x = x
        self.y = y
        self.v = v
        self.hitbox = self.sprite.get_rect()
        
    def move(self,dt):
        self.x += self.v*dt
    def draw(self,screen):
        self.hitbox = self.sprite.get_rect()
        screen.blit(self.hitbox,(self.x,self.y))
        screen.blit(self.sprite,(self.x,self.y))

#methods
def InitPygame():
    pg.init()
    pg.display.set_caption("Balls")

#functions
def placeholder():
    return True
    