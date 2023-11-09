import pygame
import time
import random
pygame.init()
WIDTH  = 800
HEIGHT = 600
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))

#Variables used in multiple functions are declared here#
score = 0
black = ( 0, 0, 0)
green = (34,139,34)
textcolor = (200, 120, 80)
textcolor2 = (139,0,0)
white = ( 255, 255, 255)

#Assets are loaded here#
block = pygame.image.load("image/block.jpg")
background = pygame.image.load("image/graveyard.png")
myfont = pygame.font.SysFont("monospace", 16)
losefont = pygame.font.Font("image/fofbb_reg.ttf", 40)

#player sprite images are loaded and saved to a list here#
charPic =[0]*4
for i in range(4):
    charPic[i] = pygame.image.load("image/pic" + str(i) + ".bmp")

#function that draws the loading screen accepts an image as an argument which it displays as the loading screen image#     
def splashScreen(image):
    pygame.mixer.music.pause()
    pygame.mixer.music.load("sounds/menuMusic.wav")
    pygame.mixer.music.play(-1)
    while True:
        gameWindow.blit(image, [0,0])#draws background image
        pygame.display.update()
        pygame.event.get()                  
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_a]: #checks for input to start the game
            break
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
    return True   
    pygame.display.update()

#main function that displays the actual gameplay accepts two arguments that are two functions#
#the first function draws the game display#
#the second function checks for collisions between the sprite and the obstacles"
def gameScreen(drawgame,collisioncheck):
    #load and play the music#
    pygame.mixer.music.load("sounds/gamemusic.wav")
    pygame.mixer.music.play(-1)
    collisionSound = pygame.mixer.Sound("sounds/slap.ogg")
    #declare variables used in this function#
    clock = pygame.time.Clock()
    FPS = 100
    start = time.time()
    lose = False
    scoretimer = time.time()
    obstacles = [] #list that contains the specs of all of the obstacles#
    score = 0
    charX = 100
    charY = HEIGHT/2
    vx = 0
    vy = 0
    speed = 4
    gravity = 0.2
    noi = 3 #used for the animation timing#
    charPicNum = 0 #variable that contains the current sprite image being displayed#
    nextRightPic = [1, 2, 1, 0] #list used to iterate through the images for animation#
    start_frame = time.time()
    frames_per_second = 10
    obstacles.append(genObstacle(HEIGHT))

    #game loop that runs the gameplay functions#
    while True: 
        now = time.time()
        #creates obstacles periodically, the length of the periods are random#
        if now - start > random.randint(3, 8):
            obstacles.append(genObstacle(HEIGHT))
            start = now
        #adds to the player's score periodically, the longer the player doesn't collide with anything the higher the score#
        if now - scoretimer > 2:
            score += 1
            scoretimer = time.time()
        #render the score to be displayed by the drawgame() function#
        scoretext = myfont.render("Score = "+str(score),1, textcolor)

        #checks for collisions using the collisioncheck() function#
        #if the function returns false indicating that there has been a collision, the gameScreen() function will return False so the program will exit the gamescreen#
        #furthermore it will set the lose variable to True so the drawgame() function will display the player's final score on the screen and inform them they lost#
        if collisioncheck(obstacles, charX, charY) == False:
            collisionSound.play(0) #plays the sound indicating they have hit something#
            lose = True
            drawgame(charPicNum, obstacles,scoretext,lose, score, charX, charY)
            pygame.time.delay(2000) #freezes the screen so the player can see that they have lost#
            return False
        #ensures the player sprite does not go higher than the gamescreen#
        elif charY < 0:
            charY = 1
        #checks if the player hits the ground and will follow the same protocol as it would if a collision occurs#
        elif charY > 570:
            collisionSound.play(0)
            lose = True
            drawgame(charPicNum, obstacles,scoretext,lose, score, charX, charY)
            pygame.time.delay(2000)
            return False
        clock.tick(FPS)
        #changes the players position to simulate gravity and to display responsiveness to the player's inputs#
        vy = gravity + vy 
        charX = charX + vx
        charY = charY + vy
        pygame.event.get()                  
        #checks to see if the player presses escape at which point it will exit the gamescreen and displays the loading screen#
        keys = pygame.key.get_pressed()                                         
        if keys[pygame.K_ESCAPE]:
             return False
        #checks if the player presses the upper arrow key if true, the sprite will move upwards and its image changes# 
        elif keys[pygame.K_UP]:
            vy = -speed
            charPicNum = 3
        #if no keys are pressed the following line of code will animate the sprite by changing the sprite image number#
        else:
            charPicNum = int((time.time() - start_frame) * frames_per_second % noi) #this code ensures that the images are not iterated through too quickly and creates a seperate FPS for images only#
        drawgame(charPicNum, obstacles,scoretext,lose, score, charX, charY)
#function that generates obstacles, the obstacles specs are saved as a list which are indexed within another list#
#accepts one argument which is the Height of the frame#
def genObstacle(Height):
    x = 750 #xposition of obstacles#
    y1 = 0 #yposition of the top obstacles#
    h = random.randint(100, 400) # height for top obstacle#
    
    h2 = random.randint(400,465) - h #height for bottom obstacle#
    y2 = Height - h2 #yposition for bottom obstacle#
    w = 50 #width of both obstacles#
    return [x,[y1, y2], w, [h, h2]] #returns the specs of the obstacles and saves it as a list which is indexed within the obstacles[] list#
#function that checks for collsions#
#accepts three arguments, the first being the list of obstacle specs that are generated by the genObstacle() function#
#the second and third argument are the x and y positions of the player sprite respectively#
#this function iterates through the obstacle list which the obstacles' specs are saved in to check if it collides with the player#
#the collide rect function checks if the player's rect values which is its x, y, width, and height collide with the obstacle that is currently being iterated#
#if a collsion is detected it will return False#
def checkCollision(obstaclelist,x, y):
    for i in range(len(obstaclelist)):
        obstacle = pygame.Rect(obstaclelist[i][0], obstaclelist[i][1][0], obstaclelist[i][2], obstaclelist[i][3][0])#loads the spec of the top obstacle#
        obstacle2 = pygame.Rect(obstaclelist[i][0], obstaclelist[i][1][1], obstaclelist[i][2], obstaclelist[i][3][1])#loads the spec of the bottom obstacle#
        if obstacle.colliderect(x, y, 30, 30) or obstacle2.colliderect(x, y, 30, 30): #checks collision between sprite and bottom or top obstacle#
            return False #returns false indicating collision#
#function that draws the game window#
#accepts 7 arguments#
#first argument is the current picture number of the sprite that should be displayed#
#second argument is the obstacle list that contains all of the obstacles specs, #
#this function iterates through all of the obstacles and decreases their x-values by one#
#therefore when the obstacles are redrawn it appears as though they are moving to the left towards the sprite.#
#the third argument is the graphics of the player's score so it can draw them onto the game screen#
#the fourth argument is the variable that it indicates if a player has lost#
#if lose == True indicating the player has lost this function will display the losetext graphics which informs the player they have lost and displays their final score#
#the fifth argument is the current score and the sixth and seventh are the player's x and y values respectively#
def redrawGameWindow(picNum, obstacles,scoretext,lose, score, X, Y):
    losetext = losefont.render("You Lose! Final Score: "+str(score),1, textcolor2)
    gameWindow.blit(background, [0,0])
    gameWindow.blit(charPic[picNum],(X, Y))
    for i in range(len(obstacles)):
        pygame.draw.rect(gameWindow, green, (obstacles[i][0], obstacles[i][1][0], obstacles[i][2], obstacles[i][3][0]))#draws top obstacle#
        pygame.draw.rect(gameWindow, green, (obstacles[i][0], obstacles[i][1][1], obstacles[i][2], obstacles[i][3][1]))#draws bottom obstacle#
        obstacles[i][0] -= 1 #moves both obstacles to the left one pixel#
    if lose == True:#checks if the player has lost
        gameWindow.blit(losetext, (200, HEIGHT/2))#indicates the player has lost#
    gameWindow.blit(scoretext, (5, 10))

    pygame.display.update()
    
loadimg = pygame.image.load("image/splashscreen.jpg")

#This loop is responsible for transitioning between the game screen and the loading screen#  
play = False #variable responsible for transitioning between game screen and loading screen, if false it displays the loading screen, and if true it displays the game screen#
while True:
    while play == True:
        play = gameScreen(redrawGameWindow, checkCollision)
    while play == False:
        play = splashScreen(loadimg)
pygame.quit()
