import os, pygame, sys, random
from pygame.locals import *
from colours import *
from player import *
from ball import *

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
# - give bonuses/maluses through the block?
#Add design patterns
# - singleton for the game
# - factory for the blocks/bricks



#A singleton class
#source for comparison : https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
#source for the code : https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.
    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.
    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.
    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.
        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class Gaming(Singleton):
    def __init__(self):
        pygame.mixer.init(22050,-16,2,16)
        pygame.init()
        self.setIcon()
        self.reset()

    def setIcon(self):
        self.icon = pygame.image.load("./resources/players/PandaDraw.png")
        self.icon = pygame.transform.rotate(self.icon,-90)
        pygame.display.set_icon(self.icon)

    def reset(self):
        self.setParams()
        self.setScreen()
        self.setBackground()
        self.setPlayers()
        self.setBall()

    def setParams(self):
        self.setScreenSize(600,500)
        self.setGameSpeed(2)
        self.setGameState(False)
        self.setGameFPS(60)
        self.setFonts('Arial',24)
        
    def setScreenSize(self, width, height):
        self.screenWidth = width
        self.screenHeight = height

    def setGameSpeed(self, speed):
        self.gameSpeed = speed #should be const and private

    def setGameState(self, running):
        self.running = running

    def setGameFPS(self, FPS):
        self.FPS = 60    

    def setFonts(self, fontType, fontSize):
        self.mainFont = pygame.font.SysFont(fontType,
                                            fontSize, 
                                            True)

    def setScreen(self):
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))

    def setBackground(self):
        self.backgroundPath = "./resources/backgrounds/sea.bmp"
        self.background = pygame.image.load(self.backgroundPath)
        self.background = pygame.transform.scale(self.background, 
                                                 (self.screenWidth, self.screenHeight))
        self.background = self.background.convert()

    #This is a 1 to 2 players game only - an AI can replace a player
    #Players can only move horizontally - speed is in 1 direction
    #Note that the players could be fully initialized using the constructor
    #But things are clearer like that
    def setPlayers(self):
        self.player1 = Player()
        self.player2 = Player()
        self.setPlayersSize(self.screenWidth  * 0.15, self.screenHeight * 0.1)
        self.setPlayersSpeed(self.gameSpeed, 0)
        self.setPlayersSkins()
        self.setPlayersInitPos()

        self.players = pygame.sprite.RenderUpdates()
        self.players.add(self.player1)
        self.players.add(self.player2)

    def setPlayersSize(self, width, height):
        self.player1.setSize(width, height)
        self.player2.setSize(width, height)

    def setPlayersSpeed(self,speedX = 0, speedY = 0):
        self.player1.setSpeed(speedX,speedY)
        self.player2.setSpeed(speedX,speedY)

    def setPlayersInitPos(self):
        X1 = self.screenWidth/2 - self.player1.width/2
        Y1 = 5
        self.player1.setPos(X1,Y1)

        X2 = self.screenWidth/2 - self.player2.width/2
        Y2 = self.screenHeight - self.player2.height - 5
        self.player2.setPos(X2,Y2)

    def setPlayersSkins(self):
        self.player1.setSkin("./resources/players/PandaDraw.png")
        self.player2.setSkin("./resources/players/SealDraw.png")

    #There is only one ball at the moment
    #A ball can move in a 2D plan
    def setBall(self):
        self.ball = Ball()
        self.ball.setSize(self.screenWidth/25, self.screenWidth/25)
       	self.ball.setSpeed(1*self.gameSpeed, 0.5*self.gameSpeed) #the 1 and 0.5 coefficients can be use as angle definitions
        self.ball.setSkin()
        self.ball.setPos(self.screenWidth/2 - self.ball.width/2, 
                         self.screenHeight/2 - self.ball.height/2)
        self.ball.defineMove("UpRight")

        self.balls = pygame.sprite.RenderUpdates()
        self.balls.add(self.ball)

    def run(self):
        count = 100
        while True:

            #Play with the players
            self.player1.moveLeft()
            self.player2.moveRight()
            
            #Play with the ball
            if count > 5:
                self.ball.defineMove("UpRight")
                count = count - 1
            else:
                self.ball.defineMove("UpLeft")

            self.ball.moveIt()

            #Update the positions
            self.players.update()
            self.balls.update()

            #Show everything on the screen
            self.screen.blit(self.background,(0,0))
            self.players.draw(self.screen)
            self.balls.draw(self.screen)
            pygame.display.flip()


def Game():    
    BACKGROUNDPATH= "./resources/backgrounds/desert.bmp"
    WIDTH = 600
    HEIGHT = 500
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    STEP = 5
    PLAYERWIDTH = WIDTH*15/100
    PLAYERHEIGHT = HEIGHT*5/50
    PLAYERSTEP = 2 * STEP
    VX, VY = 1*STEP, 1.5*STEP
    RUNNING = True
    TICKERMAX = 0
    FPS= 60

    #Set the background surface using pygame
    background = pygame.image.load(BACKGROUNDPATH)
    #Transform it so it is scaled to the current screen
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    #Set video system so it is fast to render the image
    background = background.convert()
    #Set the font to use in the game / NB: you can define multiple fonts
    font = pygame.font.SysFont('Arial',24, True)


    PLAYER1_PATH = "./resources/players/PandaDraw.png"
    PLAYER1 = Player(PLAYERWIDTH, 
                     PLAYERHEIGHT,
                     PLAYER1_PATH, 
                     WIDTH/2-PLAYERWIDTH, 
                     5, 
                     PLAYERSTEP)

    PLAYER2_PATH = "./resources/players/SealDraw.png"
    PLAYER2 = Player(PLAYERWIDTH, 
                     PLAYERHEIGHT, 
                     PLAYER2_PATH,
                     WIDTH/2-PLAYERWIDTH, 
                     HEIGHT-5-PLAYERHEIGHT, #diff with player1 
                     PLAYERSTEP) #diff with player1


    PLAYERS = pygame.sprite.RenderUpdates()
    PLAYERS.add(PLAYER1)
    PLAYERS.add(PLAYER2)

    ball = pygame.Surface((WIDTH/20,HEIGHT/20))
    ball_x, ball_y = WIDTH/2-(WIDTH/20)/2, HEIGHT/2-(HEIGHT/20)/2
    ball_vx, ball_vy= VX, VY
    ball_move_ticker = 0
    ball_move_ticker_max = TICKERMAX
    ball.fill(yellow,(0,0,100,25))
    
    # Init the clock
    clock = pygame.time.Clock()

    while RUNNING:
        # Make sure the maximal FPS is set to 60
        clock.tick(FPS)

		# Activate the events so  you can read the key pressed
        # Check if the user want to quit the game
        # Stop running it if necessary
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                RUNNING = False
   
        # Allow continuous move by get the key pressed
        # The motion period may be reduced using tickers
        # 
        keys = pygame.key.get_pressed()
        if len(keys) > 0:       
            if keys[pygame.K_RIGHT]:
                if PLAYER1.rect.x + PLAYER1.width + PLAYER1.speedX < WIDTH:
                    PLAYER1.moveRight()
            if keys[pygame.K_LEFT]:
                if PLAYER1.rect.x - PLAYERSTEP > 0:
                    PLAYER1.moveLeft()
            if keys[pygame.K_d]:
                if PLAYER2.rect.x + PLAYER2.width + PLAYER2.speedX < WIDTH:
                    PLAYER2.moveRight()
            if keys[pygame.K_q]:
                if PLAYER2.rect.x - PLAYERSTEP > 0:
                    PLAYER2.moveLeft()
            PLAYERS.update()


        #Move the ball
        #If ball touch ai...
        if isColliding((PLAYER2, PLAYER2.getPosX(), PLAYER2.getPosY()), (ball, ball_x, ball_y)):
            if ball_vx > 0:
                ball_vx = VX
                ball_vy = VY
            else:
                ball_vx = -VX
                ball_vy = VY
        #If the ball touched the player...
        elif isColliding((PLAYER1, PLAYER1.getPosX(), PLAYER1.getPosY()), (ball, ball_x, ball_y)):
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
    test = Gaming.Instance()
    test.run()
