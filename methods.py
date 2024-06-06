import numpy as np
import pygame as pg
from random import randrange
import os


class boatState():
    
    def __init__(self, xmax, ymax):
        self.left = False
        self.right = False
        self.a = False
        self.d = False
        self.trailState = False

        self.sprites = []
        self.rects = []
        for file in os.listdir("assets/keys"):
            self.sprites.append(pg.transform.scale_by(pg.image.load(os.path.join("assets/keys", file)), 3))

        for sprite in self.sprites:
            self.rects.append(sprite.get_rect())
        
        for i in range(len(self.rects)):
            if i == 0 or i == 4:
                self.rects[i].bottomleft = (50, ymax-50)
            elif i == 1 or i == 5:
                self.rects[i].bottomleft = (50 + self.rects[i].width + 5, ymax-50)
            elif i == 2 or i == 6:
                self.rects[i].bottomright = (xmax - 50 - self.rects[i].width - 5, ymax-50)
            elif i == 3 or i == 7:
                self.rects[i].bottomright = (xmax - 50, ymax - 50)

    
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
        
    def drawKeypressIndicators(self, screen):
        if not self.a: drawFromLists(screen, self.sprites, self.rects, 0)
        else: drawFromLists(screen, self.sprites, self.rects, 4)
        if not self.d: drawFromLists(screen, self.sprites, self.rects, 1)
        else: drawFromLists(screen, self.sprites, self.rects, 5)
        if not self.left: drawFromLists(screen, self.sprites, self.rects, 2)
        else: drawFromLists(screen, self.sprites, self.rects, 6)
        if not self.right: drawFromLists(screen, self.sprites, self.rects, 3)
        else: drawFromLists(screen, self.sprites, self.rects, 7)
        
class menuKeys():
    up = False
    down = False

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

class textBox():

    def __init__(self, width: int, height: int, x: int, y: int, font, fontSize: int):
        self.initWidth = width
        self.initHeight = height
        self.font = pg.font.Font(font, fontSize)
        self.textColor = (255, 255, 255)
        self.activeColor = (128, 0, 0)
        self.inactiveColor = (80, 80, 80)
        self.currentColor = self.inactiveColor
        self.rect = pg.Rect(x, y, width, height)
        self.text = ''
        self.returned = False
        self.textSurface = self.font.render(self.text, True, self.textColor)
        self.writing = False

    def handleEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and not self.returned:
                self.writing = True
                self.currentColor = self.activeColor
            else: 
                self.writing = False
                self.currentColor = self.inactiveColor

        elif event.type == pg.KEYDOWN and self.writing:
            if event.key == pg.K_RETURN:
                self.writing = False
                self.returned = True
            elif event.type == pg.K_BACKSPACE or event.key == 8:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        self.textSurface = self.font.render(self.text, True, self.textColor)

    def getText(self):
        if self.returned:
            self.returned = False
            t = self.text
            self.text = ''
            return t
        else: return None


    def draw(self, screen):
        self.rect.width = max(self.initWidth, self.textSurface.get_width() + 10)

        pg.draw.rect(screen, self.currentColor, self.rect)
        screen.blit(self.textSurface, (self.rect.x + 5, self.rect.y + 5))

#methods
def InitPygame():
    pg.init()
    pg.display.set_caption("THE MOST FRENCH EXPERIENCE")
    icon = pg.image.load('assets/french_flag.png')
    pg.display.set_icon(icon)

def drawFromLists(screen, sprite, rect, index):
    screen.blit(sprite[index], rect[index])