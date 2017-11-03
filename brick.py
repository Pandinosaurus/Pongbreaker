#Project : Pongbreaker
#File	 : brick.py
#Author  : Remi Ratajczak
#Contact : Remi.Ratajczak@gmail.com

import pygame, os, sys
from pygame.locals import *
from colours import *
from sprite import *

class Brick(Sprite):
    def __init__(self, width = 0, height = 0, skinpath = "", posX = 0, posY = 0, speedX = 0, speedY = 0):  
        Sprite.__init__(self, width, height, skinpath, posX, posY, speedX, speedY)
        self.maxLives = 3;
        self.setLives(self.maxLives)

    def setSkin(self,skinpath=""):
        self.setOrientation()
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def setOrientation(self):
        if randint(0,1) == 1: #1 corresponds to blue AND vertical
            self.setVertical()
        else:
            self.setHorizontal()

    def setVertical(self):
        if self.width > self.height:
            tmp = self.width
            self.width = self.height
            self.height = tmp
        self.setColor(purple)

    def setHorizontal(self):
        if self.height > self.width:
            tmp = self.height
            self.height = self.width
            self.width = tmp
        self.setColor(yellow)

    def setLives(self, lives):
        self.lives = lives
        if self.lives == 3:
            self.setColor(blue)
        if self.lives == 2:
            self.setColor(yellow)
        if self.lives == 1:
            self.setColor(red)

    
    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color