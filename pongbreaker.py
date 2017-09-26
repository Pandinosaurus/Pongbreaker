import pygame, os, sys
from pygame.locals import *
from colours import *

def Game():    
    BACKGROUNDPATH= "./resources/backgrounds/sea.bmp"
    WIDTH = 400
    HEIGHT = 500
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    PLAYERWIDTH = WIDTH*15/100
    PLAYERHEIGHT = HEIGHT*5/100
    STEP = 2
    PLAYERSTEP = 2 * STEP
    VX, VY = 1*STEP, 1.5*STEP
    RUNNING = True
    TICKERMAX = 1

    #Set the background surface using pygame
    background = pygame.image.load(BACKGROUNDPATH)
    #Transform it so it is scaled to the current screen
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    #Set video system so it is fast to render the image
    background = background.convert()
    #Set the font to use in the game / NB: you can define multiple fonts
    font = pygame.font.SysFont('Arial',24, True)
    
    ball = pygame.Surface((WIDTH/20,HEIGHT/20))
    ball_x, ball_y = WIDTH/2-(WIDTH/20)/2, HEIGHT/2-(HEIGHT/20)/2
    ball_vx, ball_vy= VX, VY
    ball_move_ticker = 0
    ball_move_ticker_max = TICKERMAX
    ball.fill(yellow,(0,0,100,25))

    player = pygame.Surface((PLAYERWIDTH, PLAYERHEIGHT))
    player_x, player_y = WIDTH/2-PLAYERWIDTH, HEIGHT/15
    player_move_ticker = 0
    player_move_ticker_max = TICKERMAX #allow to move every TICKERMAX+1 frames so that it does not move too fast
    player_score = 0
    player_color = cyan
    player.fill(player_color,(0,0,100,25))

    ai = pygame.Surface((PLAYERWIDTH, PLAYERHEIGHT))
    ai_x, ai_y = WIDTH/2-PLAYERWIDTH, HEIGHT-HEIGHT/15
    ai_move_ticker = 0
    ai_move_ticker_max = TICKERMAX #allow to move every TICKERMAX+1 frames so that it does not move too fast
    ai_score = 0
    ai_color = red
    ai.fill(ai_color,(0,0,100,25))

    while RUNNING:
		#Activate the events so  you can read the key pressed
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if player_x - PLAYERSTEP > 0:
                        player_x = player_x - PLAYERSTEP
                if event.key == pygame.K_RIGHT:
                    if player_x + PLAYERWIDTH + PLAYERSTEP < WIDTH:
                        player_x = player_x + PLAYERSTEP
   
        #Allow continuous move every ticker frames
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if player_x + PLAYERWIDTH + PLAYERSTEP < WIDTH:
                if player_move_ticker == 0:
                    player_move_ticker = player_move_ticker_max
                    player_x = player_x + PLAYERSTEP
        if keys[pygame.K_LEFT]:
            if player_x - PLAYERSTEP > 0:
                if player_move_ticker == 0:
                    player_move_ticker = player_move_ticker_max
                    player_x = player_x - PLAYERSTEP
        if keys[pygame.K_d]:
            if ai_x + PLAYERWIDTH + PLAYERSTEP < WIDTH:
                if ai_move_ticker == 0:
                    ai_move_ticker = ai_move_ticker_max
                    ai_x = ai_x + PLAYERSTEP
        if keys[pygame.K_q]:
            if ai_x - PLAYERSTEP > 0:
                if ai_move_ticker == 0:
                    ai_move_ticker = ai_move_ticker_max
                    ai_x = ai_x - PLAYERSTEP

        #Move the ball
        #If the ball touche the ai...
        if isColliding((ai, ai_x, ai_y), (ball, ball_x, ball_y)):
            if ball_vx > 0:
                ball_vx = VX
                ball_vy = VY
            else:
                ball_vx = -VX
                ball_vy = VY
        #If the ball touched the player...
        elif isColliding((player, player_x, player_y), (ball, ball_x, ball_y)):
            if ball_vx > 0:
                ball_vx = VX
                ball_vy = -VY
            else:
                ball_vx = -VX
                ball_vy = -VY

        #If the ball touched a wall, inverse motion of the ball
        if ball_x-2 <= 0: #left
            ball_vx *= -1 
        if ball_x + pygame.Surface.get_width(ball)+2 >= WIDTH: #right
            ball_vx *= -1  
        if ball_y-2 <= 0: #top
            ball_vy *= -1
            ai_score = ai_score + 1
        if ball_y + pygame.Surface.get_height(ball)+2 >= HEIGHT: #bottom
            ball_vy *= -1
            player_score = player_score + 1
        #If it's time to update the ball, update its position using vx and vy
        if ball_move_ticker == 0:
            ball_move_ticker = ball_move_ticker_max
            ball_y -= ball_vy #velocity is just a way to say 'move it of a given number of pixels'
            ball_x -= ball_vx #velocity is just a way to say 'move it of a given number of pixels'
        
        if player_move_ticker > 0:
            player_move_ticker -= 1
        if ai_move_ticker > 0:
            ai_move_ticker -= 1
        if ball_move_ticker > 0:
            ball_move_ticker -= 1

        player_score_text = font.render(str(player_score),True,player_color)
        ai_score_text = font.render(str(ai_score),True,ai_color)
        SCREEN.blit(background,(0,0))
        SCREEN.blit(player,(player_x,player_y))
        SCREEN.blit(ball,(ball_x,ball_y))
        SCREEN.blit(ai, (ai_x,ai_y)) 
        SCREEN.blit(player_score_text,(5,5))
        SCREEN.blit(ai_score_text,(5, HEIGHT-5-2*ai_score_text.get_height()))
        pygame.display.flip()

def isColliding(obj1, obj2): # checks if two surfaces are collliding
    rect1 = pygame.Rect(obj1[1], obj1[2], pygame.Surface.get_bounding_rect(obj1[0])[2], pygame.Surface.get_bounding_rect(obj1[0])[3])
    rect2 = pygame.Rect(obj2[1], obj2[2], pygame.Surface.get_bounding_rect(obj2[0])[2], pygame.Surface.get_bounding_rect(obj2[0])[3])
    return rect1.colliderect(rect2)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init(22050,-16,2,16)
    Game()
