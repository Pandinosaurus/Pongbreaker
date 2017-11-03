#Project : Pongbreaker
#File	 : main.py
#Author  : Remi Ratajczak
#Contact : Remi.Ratajczak@gmail.com

import os, pygame, sys, random
from pygame.locals import *
from game import *

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init(22050,-16,2,16)
    test = PongbreakerGame.Instance()
    test.run()
