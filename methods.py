import pygame as pg

#methods
def InitPygame():
    pg.init()
    pg.display.set_caption("Balls")

def GetAlternatingInputs(keys, value, flag):
    if keys[pg.K_RIGHT] and flag:
        value -= 10
        flag = False
    elif keys[pg.K_LEFT] and not flag:
        value -= 10
        flag = True
    return value
        



#functions
def placeholder():
    return True
    