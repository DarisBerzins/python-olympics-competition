import numpy as np
import pygame as pg
from random import randrange
import os

class Player():
    pos = np.array([0, 0])
    vel = np.array([0, 0])
    frame = 0
    if frame == 0:
        surf = pg.image.load("assets/testboat.png")
    elif frame == 1:
        pass #make this the right stroke sprite
    elif frame == 2:
        pass #make this the left stroke sprite
    elif frame == 3:
        pass #make this the destroyed boat sprite

class Obstacle():
    # sprite = [pg.image.load("assets/rat.png"), pg.image.load("assets/")]  
    def __init__(self,sprites,x,y,v):
        self.sprite = sprites[randrange(0,len(sprites)-1)]
        self.sprite = pg.transform.scale(self.sprite, (200,200))
        self.x = x
        self.y = y
        self.v = v
    def move(self,dt):
        self.x += self.v*dt

    def draw(self,screen):
        screen.blit(self.sprite,(self.x,self.y))

#methods
def InitPygame():
    pg.init()
    pg.display.set_caption("Balls")

#functions
def placeholder():
    return True
    