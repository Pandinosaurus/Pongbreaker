#Project : Pongbreaker
#File	 : player.py
#Author  : Remi Ratajczak
#Contact : Remi.Ratajczak@gmail.com

import os, pygame, sys, random
from colours import *

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, posX, posY, tickermax, step, skinpath, file = None):
        #A player is a sprite that can be updated
        pygame.sprite.Sprite.__init__(self)

        #Init size, position, speed, score and skin
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.skinpath = skinpath
        self.image = pygame.image.load(skinpath)
        self.image = pygame.transform.scale(self.image,self.size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = posX, posY
        self.ticker = 0
        self.tickermax = max(tickermax,1)
        self.step = step
        self.score = 0

    def moveRight(self):
        if self.ticker == 0:
            self.ticker = self.tickermax
            self.rect.x = self.rect.x + self.step

    def moveLeft(self):
        if self.ticker == 0:
            self.ticker = self.tickermax
            self.rect.x = self.rect.x - self.step

    def setScore(self, score):
        self.score = score

    def update(self):
        if self.ticker > 0:
            self.ticker -= 1