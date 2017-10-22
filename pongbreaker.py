import os, pygame, sys, random
from pygame.locals import *
from colours import *
from player import *
from ball import *
from brick import *
from random import randint

#ToDo :
#Finish it
# - add randomly appearing block to break
# - add a second ball?
# - give bonuses/maluses through the block?
#Add design patterns
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
        self.setBricks()

    def setParams(self):
        self.setScreenSize(700,500)
        self.setGameSpeed(4)
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
       	self.ball.setSpeed(1*self.gameSpeed, 0.8*self.gameSpeed) #the 1 and 0.5 coefficients can be use as angle definitions
        self.ball.setSkin()
        self.ball.setPos(self.screenWidth/2 - self.ball.width/2, 
                         self.screenHeight/2 - self.ball.height/2)
        self.ball.defineMove("UpRight")

        self.balls = pygame.sprite.RenderUpdates()
        self.balls.add(self.ball)

    #Set bricks
    def setBricks(self):
        self.initBricks()
        self.setNumberOfBricksToAdd(10)
        self.addBricks()

    def initBricks(self):
        self.bricks = pygame.sprite.RenderUpdates()
        self.numberOfBricks = 0

    def setNumberOfBricksToAdd(self, number):
        self.numberOfBricksToAdd = number

    def addBricks(self, number = 0):
        if number > 0:
            setNumberOfBricksToAdd(number)

        maxTrials = self.numberOfBricksToAdd*2 #avoid infinite loop in case of constant overlaping
        while self.numberOfBricksToAdd > 0 and maxTrials > 0:
            brick = Brick(self.screenWidth/15, self.screenWidth/30)
            brick.setSkin()
            brick.setPos(randint(brick.getWidth(), 
                                 self.screenWidth-brick.getWidth()), 
                         randint(self.player1.getPosY() + self.player1.getHeight() + brick.getHeight(),
                                 self.player2.getPosY() - self.player2.getHeight() - brick.getHeight()))
            overlap = False
            for br in self.bricks:
                if isColliding(br, brick):
                   overlap = True
                   break
            if overlap == False:
                self.bricks.add(brick)
                self.numberOfBricksToAdd -= 1
                self.numberOfBricks += 1

            maxTrials -=1

    def run(self):
        self.running = True
        while self.running:
            self.checkQuit()
            self.movePlayers()
            self.moveBalls()
            self.players.update()
            self.balls.update()
            self.display()

    def checkQuit(self):
        # Activate the events so  you can read the key pressed
        # Check if the user want to quit the game
        # Stop running it if necessary
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                self.running = False

    def movePlayers(self):
        # Allow continuous move by get the key pressed
        # The motion period may be reduced using tickers
        keys = pygame.key.get_pressed() 
        if len(keys) > 0:       
            if keys[pygame.K_RIGHT]:
                if self.player1.getPosX() + self.player1.getWidth() + self.player1.getSpeedX() < self.screenWidth:
                    self.player1.defineMove("Right") #we call defineMove then moveIt instead of moveRight for consistency with the ball 
                    self.player1.moveIt()
            if keys[pygame.K_LEFT]:
                if self.player1.getPosX() - self.player1.getSpeedX() > 0:
                    self.player1.defineMove("Left")
                    self.player1.moveIt()
            if keys[pygame.K_d]:
                if self.player2.getPosX() + self.player2.getWidth() + self.player2.getSpeedX() < self.screenWidth:
                    self.player2.defineMove("Right")
                    self.player2.moveIt()
            if keys[pygame.K_q]:
                if self.player2.getPosX() - self.player2.getSpeedX() > 0:
                    self.player2.defineMove("Left")
                    self.player2.moveIt()

    def moveBalls(self):      
        if(self.checkCollidingPlayers()):
            self.ball.moveIt()
            return
        self.checkIfBallIsCollidingABrick()
        self.checkCollidingBorders()
        self.ball.moveIt()

    def checkCollidingPlayers(self):
        ballMove = self.ball.getMove()
        if self.checkIfBallIsBetweenPlayers():
            if isColliding(self.player1,self.ball):
                if ballMove == "Up" or ballMove == "UpRight" or ballMove == "UpLeft":
                    self.ball.reflectMoveAlongX()
                    return True
            elif isColliding(self.player2,self.ball):
                if ballMove == "Down" or ballMove == "DownRight" or ballMove == "DownLeft":
                    self.ball.reflectMoveAlongX()
                    return True
        return False

    def checkIfBallIsBetweenPlayers(self):
        if self.ball.getPosY() >= self.player1.getPosY() + self.player1.getHeight()/2:
            if self.ball.getPosY() < self.player2.getPosY():
                return True
        return False

    def checkIfBallIsCollidingABrick(self):
        for brick in self.bricks:
            if isColliding(self.ball, brick):
                self.ball.reflectMoveAlongX()
                break

    def checkCollidingBorders(self):
        if self.ball.getPosX() <= 0:
            self.ball.setPosX = 0
            self.ball.reflectMoveAlongY()
        elif self.ball.getPosX()+self.ball.getWidth() >= self.screenWidth:
            self.ball.setPosX = self.screenWidth-self.ball.getWidth()
            self.ball.reflectMoveAlongY()

        if self.ball.getPosY() <= 0:
            self.ball.setPosY = 0
            self.ball.reflectMoveAlongX()
            self.player2.incrementScore()
        elif self.ball.getPosY()+self.ball.getHeight() >= self.screenHeight:
            self.ball.setPosY = self.screenHeight-self.ball.getHeight()
            self.ball.reflectMoveAlongX()
            self.player1.incrementScore()

    def display(self):
        player1_score_text = self.mainFont.render(str(self.player1.getScore()),True,cyan)
        player2_score_text = self.mainFont.render(str(self.player2.getScore()),True,red)
        self.screen.blit(self.background,(0,0))
        self.screen.blit(player1_score_text,(5,5))
        self.screen.blit(player2_score_text,(5, self.screenHeight-5-player2_score_text.get_height()))
        self.players.draw(self.screen)
        self.balls.draw(self.screen)
        self.bricks.draw(self.screen)
        pygame.display.flip()

def isColliding(obj1, obj2): # check if two bouding boxes are colliding
    rect1 = pygame.Rect(obj1.getPosX(), obj1.getPosY(), obj1.getWidth(), obj1.getHeight())
    rect2 = pygame.Rect(obj2.getPosX(), obj2.getPosY(), obj2.getWidth(), obj2.getHeight())
    return rect1.colliderect(rect2)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init(22050,-16,2,16)
    test = Gaming.Instance()
    test.run()
