import pygame
import random
import math

from pygame import mixer


#Initialize the pygame
pygame.init()

#Create the window
screen = pygame.display.set_mode((800,600))

#create Background Image
background = pygame.image.load("grass.jpg")

#Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10


#Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',64)
over_font_space = pygame.font.Font('freesansbold.ttf',40)
score_font = pygame.font.Font('freesansbold.ttf',50)



def showScore(x,y):
	score = font.render("Score :" + str(score_value), True, (255,255,255))
	screen.blit(score, (x, y))


def game_over_text():
	screen.fill((255,255,255))
	screen.blit(background, (0,0))
	over_text = over_font.render("GAME OVER", True, (255, 255, 255))
	score_text = score_font.render("Your score is: "+ str(score_value), True, (255, 255, 255))
	over_text_space = over_font_space.render("Press any key to Start New Game", True, (255, 255, 255))

	screen.blit(over_text, (200,250))
	screen.blit(score_text, (150, 300))
	screen.blit(over_text_space, (80,350))

#Title and Icon
pygame.display.set_caption("Reduct Video Game")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)


#Food
foodImg = pygame.image.load("worm.png")
foodX = random.randint(50,550)
foodY = random.randint(50, 350)
foodX_change = 0
foodY_change = 0



#Player
playerImg = pygame.image.load("ant.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


#Bomb
bombImg = []
bombX = []
bombY = []
bombX_change = []
bombY_change = []
num_of_bomb = 8


for i in range(num_of_bomb):
	bombImg.append(pygame.image.load("b.gif"))
	bombX.append(random.randint(50,550))
	bombY.append(random.randint(50, 350))
	bombX_change.append(2) 
	bombY_change.append(1)


def bomb(x,y,i):
	screen.blit(bombImg[i],(x,y))
		


def food(x, y):
	screen.blit(foodImg, (x, y))

def player(x, y):
	screen.blit(playerImg, (x, y))


def isCollision(foodX, foodY, playerX, playerY):
	distance = math.sqrt((math.pow(foodX-playerX,2)) + (math.pow(foodY-playerY, 2)))
	if distance < 35:
		return True


	else:
		return False

def isDead(bombX, bombY, playerX, playerY, i):


	distance = math.sqrt((math.pow(bombX-playerX,2)) + (math.pow(bombY-playerY, 2)))
	if distance < 35:
		return True
	else:
		return False


def game_loop():
#Game Loop

	global playerY, playerX, foodY, foodX, playerX_change, playerY_change, bombX, bombY, score_value, playerImg
	running = True


	while running:

		screen.fill((255,255,255))
		screen.blit(background, (0,0)) 

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		
			#If keystroke is pressed check:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					playerImg = pygame.image.load("antl.png")
					playerX_change = -5
				if event.key == pygame.K_RIGHT:
					playerImg = pygame.image.load("antr.png")
					playerX_change = 5
				if event.key == pygame.K_DOWN:
					playerImg = pygame.image.load("antd.png")
					playerY_change = 5
				if event.key == pygame.K_UP:
					playerImg = pygame.image.load("ant.png")
					playerY_change = -5
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
					playerX_change = 0
					playerY_change = 0
		
		playerX += playerX_change
		playerY += playerY_change

		if playerX <=0:
			playerX = 736
		elif playerX >= 736:
			playerX = 0
		elif playerY <=0:
			playerY = 584
		elif playerY >= 584:
			playerY = 0


		#collision
		collision = isCollision(foodX, foodY, playerX, playerY)

		if collision:
			score_value += 1
			collision_sound = mixer.Sound('sallow.wav')
			collision_sound.play()
			foodX = random.randint(0,750)
			foodY = random.randint(0, 550)

		for i in range(num_of_bomb):



			#change position of bomb
			bombX[i] += bombX_change[i]
			bombY[i] += bombY_change[i]

			if bombX[i] <=0:
				bombX[i] = 736
			elif bombX[i] >= 736:
				bombX[i] = 0
			elif bombY[i] <=0:
				bombY[i] = 584
			elif bombY[i] >= 584:
				bombY[i] = 0

			dead_status = isDead(bombX[i], bombY[i], playerX, playerY,i)

			if dead_status:
				game_over_text()
				for i in range(num_of_bomb):
					bombX_change[i] = 0
					bombY_change[i] = 0
				
				
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						score_value = 0
						playerX = 370
						playerY = 480
						for i in range(num_of_bomb):
							bombX[i] = random.randint(50,550)
							bombY[i] = random.randint(50,350)

							bombX_change[i] = 2
							bombY_change[i] = 1
					if event.type == pygame.KEYUP:
						
						game_loop()


			bomb(bombX[i], bombY[i], i)
				


		showScore(textX, textY)
		food(foodX,foodY)
		player(playerX, playerY)
		
		pygame.display.update()



game_loop()