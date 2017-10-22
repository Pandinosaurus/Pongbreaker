#Project : Pongbreaker
#File	 : player.py
#Author  : Remi Ratajczak
#Contact : Remi.Ratajczak@gmail.com

import os, pygame, sys, random
from colours import *
from sprite import *

#A Player is a Sprite
#It can move horizontally but not vertically
#It also has a score
class Player(Sprite):
    def __init__(self, width = 0, height = 0, skinpath = "", posX = 0, posY = 0, speedX = 0, speedY = 0):  
        Sprite.__init__(self, width, height, skinpath, posX, posY, speedX, speedY)      
        self.setScore(0)

    def setScore(self, score):
        self.score = score

    def getScore(self):
        return self.score

    def incrementScore(self, incrementValue=1):
        self.score += incrementValue

    def decrementScore(self, decrementValue=1):
        self.score -= decrementValue