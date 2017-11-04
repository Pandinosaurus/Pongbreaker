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
        #A ball is a sprite 
        Sprite.__init__(self, width, height, skinpath, posX, posY, speedX, speedY)
        #Define the initial move of the ball
        self.move = "UpRight"
        #Set the color of the ball
        self.setColor(cyan)
        #Set the surface for the ball
        self.setSurface() 
        #Set the shape of the ball
        self.setShape() 

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def setSurface(self):
        #Set the surface as a transparent square
        self.height = max(self.width, self.height)
        self.width = self.height
        self.image = pygame.Surface([self.width,self.height], pygame.SRCALPHA, 32) 
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def setShape(self):
        if self.width == 0:
            self.width = 10
        if self.height == 0:
            self.height = 10
        if self.width != self.height:
            self.setSurface()
        #Make sure the ball is shaped inside a square 
        self.radius = self.width / 2 #a ball is a circle first
        self.lineWidth = self.radius / 2 #how thick the border of the ball will be - should by < radius - if set to zero the object will be filled with self.color

    def setSkin(self,skinpath=""):
        self.setSurface() #in case it has not been made before
        self.setShape() #in case it has not been made before
        self.setColor(cyan) #in case it has not been made before
        x,y = self.width/2,self.height/2
        pygame.draw.circle(self.image, self.color, (x,y), self.radius, self.lineWidth)