#Project : Pongbreaker
#File	 : player.py
#Author  : Remi Ratajczak
#Contact : Remi.Ratajczak@gmail.com
#ToDo : add dictionary mapping for switch like behavior : https://www.pydanny.com/why-doesnt-python-have-switch-case.html

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
        self.move = ""

    def setSize(self, width, height):
        self.width =  int(width)
        self.height = int(height)
        self.size = (self.width, self.height)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getSize(self):
        return self.size

    def setSkin(self, skinpath):
        self.skinpath = skinpath
        if skinpath is not "": #should add a better condition
            self.image = pygame.image.load(skinpath)
            self.image = pygame.transform.scale(self.image,self.size)
            self.rect = self.image.get_rect()        
        else:
            self.rect = pygame.Rect(0,0,0,0)

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

    #Single move in 2D
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

    #Combined move in 2D
    def moveUpLeft(self):
        if self.ticker == 0:
            self.ticker = self.tickermax
            self.rect.x = self.rect.x - self.speedX
            self.rect.y = self.rect.y - self.speedY

    def moveUpRight(self):
        if self.ticker == 0:
            self.ticker = self.tickermax
            self.rect.x = self.rect.x + self.speedX
            self.rect.y = self.rect.y - self.speedY

    def moveDownLeft(self):
        if self.ticker == 0:
            self.ticker = self.tickermax
            self.rect.x = self.rect.x - self.speedX
            self.rect.y = self.rect.y + self.speedY

    def moveDownRight(self):
        if self.ticker == 0:
            self.ticker = self.tickermax
            self.rect.x = self.rect.x + self.speedX
            self.rect.y = self.rect.y + self.speedY

    #For external
    def defineMove(self,move=""):
        self.move = move

    def invertMove(self):
        if self.move == "Up":
            self.defineMove("Down")
        elif self.move == "Down":
            self.defineMove("Up")
        elif self.move == "Right":
            self.defineMove("Left")
        elif self.move == "Left":
            self.defineMove("Right")
        elif self.move == "UpRight":
            self.defineMove("DownLeft")
        elif self.move == "UpLeft":
            self.defineMove("DownRight")
        elif self.move == "DownRight":
            self.defineMove("UpLeft")
        elif self.move == "DownLeft":
            self.defineMove("UpRight")

    def reflectMoveAlongX(self):
        if self.move == "Up":
            self.defineMove("Down")
        elif self.move == "Down":
            self.defineMove("Up")
        elif self.move == "Right":
            self.defineMove("Left")
        elif self.move == "Left":
            self.defineMove("Right")
        elif self.move == "UpRight":
            self.defineMove("DownRight")
        elif self.move == "UpLeft":
            self.defineMove("DownLeft")
        elif self.move == "DownRight":
            self.defineMove("UpRight")
        elif self.move == "DownLeft":
            self.defineMove("UpLeft")

    def reflectMoveAlongY(self):
        if self.move == "Up":
            self.defineMove("Down")
        elif self.move == "Down":
            self.defineMove("Up")
        elif self.move == "Right":
            self.defineMove("Left")
        elif self.move == "Left":
            self.defineMove("Right")
        elif self.move == "UpRight":
            self.defineMove("UpLeft")
        elif self.move == "UpLeft":
            self.defineMove("UpRight")
        elif self.move == "DownRight":
            self.defineMove("DownLeft")
        elif self.move == "DownLeft":
            self.defineMove("DownRight")

    def moveIt(self):
        if self.move == "Up":
            self.moveUp()
        elif self.move == "Down":
            self.moveDown()
        elif self.move == "Right":
            self.moveRight()
        elif self.move == "Left":
            self.moveLeft()
        elif self.move == "UpRight":
            self.moveUpRight()
        elif self.move == "UpLeft":
            self.moveUpLeft()
        elif self.move == "DownRight":
            self.moveDownRight()
        elif self.move == "DownLeft":
            self.moveDownLeft()

    def getMove(self):
        return self.move

    def resize(self,width, height):
        self.setSize(self, width, height)
        self.image = pygame.transform.scale(self.image,self.size)
        self.rect = self.image.get_rect()
        
    def update(self):
        if self.ticker > 0:
            self.ticker -= 1
