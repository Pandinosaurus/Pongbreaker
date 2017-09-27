import os, pygame, sys, random
from pygame.locals import *
from colours import *
from player import *

#ToDo :
#A lot...
#Make it clearer through OO
# - Use the ball class
# - Make the ball being a circle
# - Create a game class
#Make it more readable and extendable
# - Find a gracious way to manage the tickers
# - Use a configuration file ton manage the backgrounds
# - Redefine a STEP versus the SPEED and the VELOCITY (VX, VY)
# - Rename the PATH to make them more relevant (PATH -> skin)
# - Is there kind of a switch in Python? If true use it
# - Make isColliding clearer - both name, arguments and code
#Finish it
# - add randomly appearing block to break
# - add a second ball?
# - give bonuses through block?

def Game():    
    BACKGROUNDPATH= "./resources/backgrounds/sea.bmp"
    WIDTH = 600
    HEIGHT = 500
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    STEP = 2
    PLAYERWIDTH = WIDTH*15/100
    PLAYERHEIGHT = HEIGHT*5/50
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

    PLAYER1_PATH = "./resources/players/PandaDraw.png"
    PLAYER1 = Player(PLAYERWIDTH, 
                     PLAYERHEIGHT, 
                     WIDTH/2-PLAYERWIDTH, 
                     5, 
                     TICKERMAX, 
                     PLAYERSTEP, 
                     PLAYER1_PATH)

    PLAYER2_PATH = "./resources/players/SealDraw.png"
    PLAYER2 = Player(PLAYERWIDTH, 
                     PLAYERHEIGHT, 
                     WIDTH/2-PLAYERWIDTH, 
                     HEIGHT-5-PLAYERHEIGHT, #diff with player1
                     TICKERMAX, 
                     PLAYERSTEP, 
                     PLAYER2_PATH) #diff with player1


    PLAYERS = pygame.sprite.RenderUpdates()
    PLAYERS.add(PLAYER1)
    PLAYERS.add(PLAYER2)

    while RUNNING:
		#Activate the events so  you can read the key pressed
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                RUNNING = False
   
        #Allow continuous move every ticker frames
        keys = pygame.key.get_pressed()
        if len(keys) > 0:       
            if keys[pygame.K_RIGHT]:
                if PLAYER1.rect.x + PLAYER1.width + PLAYER1.step < WIDTH:
                    PLAYER1.moveRight()
            if keys[pygame.K_LEFT]:
                if PLAYER1.rect.x - PLAYERSTEP > 0:
                    PLAYER1.moveLeft()
            if keys[pygame.K_d]:
                if PLAYER2.rect.x + PLAYER2.width + PLAYER2.step < WIDTH:
                    PLAYER2.moveRight()
            if keys[pygame.K_q]:
                if PLAYER2.rect.x - PLAYERSTEP > 0:
                    PLAYER2.moveLeft()
            PLAYERS.update()


        #Move the ball
        #If ball touch ai...
        if isColliding((PLAYER2, PLAYER2.rect.x, PLAYER2.rect.y), (ball, ball_x, ball_y)):
            if ball_vx > 0:
                ball_vx = VX
                ball_vy = VY
            else:
                ball_vx = -VX
                ball_vy = VY
        #If the ball touched the player...
        elif isColliding((PLAYER1, PLAYER1.rect.x, PLAYER1.rect.y), (ball, ball_x, ball_y)):
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
            PLAYER2.setScore( PLAYER2.score + 1 )
        if ball_y + pygame.Surface.get_height(ball)+2 >= HEIGHT: #bottom
            ball_vy *= -1
            PLAYER1.setScore( PLAYER1.score + 1 )
        
        player_score_text = font.render(str(PLAYER1.score),True,cyan)
        ai_score_text = font.render(str(PLAYER2.score),True,red)

        #If it's time to update the ball, update its position using vx and vy
        if ball_move_ticker == 0:
            ball_move_ticker = ball_move_ticker_max
            ball_y -= ball_vy #velocity is just a way to say 'move it of a given number of pixels'
            ball_x -= ball_vx #velocity is just a way to say 'move it of a given number of pixels'
        
        if ball_move_ticker > 0:
            ball_move_ticker -= 1
        
        SCREEN.blit(background,(0,0))
        PLAYERS.draw(SCREEN)
        SCREEN.blit(ball,(ball_x,ball_y))
        SCREEN.blit(player_score_text,(5,5))
        SCREEN.blit(ai_score_text,(5, HEIGHT-5-ai_score_text.get_height()))
        pygame.display.flip()

def isColliding(obj1, obj2): # check if two bouding boxes are colliding
    rect1 = pygame.Rect(obj1[1], obj1[2], obj1[0].width, obj1[0].height)
    rect2 = pygame.Rect(obj2[1], obj2[2], pygame.Surface.get_bounding_rect(obj2[0])[2], pygame.Surface.get_bounding_rect(obj2[0])[3])
    return rect1.colliderect(rect2)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init(22050,-16,2,16)
    Game()
