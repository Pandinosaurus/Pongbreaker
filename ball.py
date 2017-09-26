import pygame, os, sys
from pygame.locals import *
from colours import *

class ball(pygame.Surface):
    self = pygame.Surface((WIDTH/20,HEIGHT/20))
    ball_x, ball_y = WIDTH/2-(WIDTH/20)/2, HEIGHT/2-(HEIGHT/20)/2
    ball_vx, ball_vy= VX, VY
    ball_move_ticker = 0
    ball_move_ticker_max = TICKERMAX
    ball.fill(yellow,(0,0,100,25))