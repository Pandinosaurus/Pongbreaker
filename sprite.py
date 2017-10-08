#Project : Pongbreaker
#File	 : player.py
#Author  : Remi Ratajczak
#Contact : Remi.Ratajczak@gmail.com

import os, pygame, sys, random
from colours import *

#A Sprite is an extension of a pygame.sprite.Sprite
#It has a size, a skin, a position and a speed
#It can move horizontally and vertically if
#its speeds in a given direction are not equal to 0
#The tickers are used to update the sprites
#It may be required to overload some functions
#in order to create/modify some functionalities
class Sprite(pygame.sprite.Sprite):
    def __init__(self, width = 0, height = 0, skinpath= "", posX=0, posY=0, speedX=0, speedY=0):
        #one needs to first set the size then the skin then the pos
        #this is required because the skin is set using the size and
        #the position is set using the bounding rectangle of the skin
        pygame.sprite.Sprite.__init__(self)
        self.setSize(width, height)
        self.setSkin(skinpath)
        self.setPos(posX, posY)
        self.setSpeed(speedX, speedY)
        self.tickermax = 1  
        self.ticker = 0

    def setSize(self, width, height):
        self.width =  width
        self.height = height
        self.size = (self.width, self.height)

    def setSkin(self, skinpath):
        self.skinpath = skinpath
        self.image = pygame.image.load(skinpath)
        self.image = pygame.transform.scale(self.image,self.size)
        self.rect = self.image.get_rect()

    def setPos(self, X, Y):
        self.setPosX(X)
        self.setPosY(Y)

    def setPosX(self, X):
        self.rect.x = X

    def setPosY(self, Y):
        self.rect.y = Y

    def getPosX(self):
        return self.rect.x

    def getPosY(self):
        return self.rect.y

    #We do not want our player to move verticaly
    #Hence we make sure it can't do
    def setSpeed(self, speedX = 0, speedY = 0):
        self.setSpeedX(speedX)
        self.setSpeedY(speedY)
   
    def setSpeedX(self,speedX = 0):
        self.speedX = speedX

    def setSpeedY(self,speedY = 0):
        self.speedY = speedY

    def getSpeedX(self):
        return self.speedX

    def getSpeedY(self):
        return self.speedY

    def moveRight(self):
        if self.ticker == 0:
            self.ticker = self.tickermax
            self.rect.x = self.rect.x + self.speedX

    def moveLeft(self):
        if self.ticker == 0:
            self.ticker = self.tickermax
            self.rect.x = self.rect.x - self.speedX

    def moveUp(self):
        if self.ticker == 0:
            self.ticker = self.tickermax
            self.rect.y = self.rect.y - self.speedY

    def moveDown(self):
        if self.ticker == 0:
            self.ticker = self.tickermax
            self.rect.y = self.rect.y + self.speedY

    def resize(self,width, height):
        self.setSize(self, width, height)
        self.image = pygame.transform.scale(self.image,self.size)
        self.rect = self.image.get_rect()
        
    def update(self):
        if self.ticker > 0:
            self.ticker -= 1
