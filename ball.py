#Project : Pongbreaker
#File	 : ball.py
#Author  : Remi Ratajczak
#Contact : Remi.Ratajczak@gmail.com

import pygame, os, sys
from pygame.locals import *
from colours import *
from sprite import *

class Ball(Sprite):
    def __init__(self, width = 0, height = 0, skinpath = "", posX = 0, posY = 0, speedX = 0, speedY = 0):  
        Sprite.__init__(self, width, height, skinpath, posX, posY, speedX, speedY)
        self.move = "UpRight"

    def setSkin(self,skinpath=""):
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(yellow)
        pygame.draw.ellipse(self.image, yellow, [0,0, self.width, self.height])
        self.rect = self.image.get_rect()