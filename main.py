import pygame
import random
import math
from pygame import mixer

#initialise pygame
pygame.init()

#create the screen and set dimensions
screen = pygame.display.set_mode((800,600))

#load background image
background = pygame.image.load('bgimg.png')

#background music
mixer.music.set_volume(0.3)
mixer.music.load('background.wav')
mixer.music.play(-1)

#title
pygame.display.set_caption('   '.join([x for x in 'HAMMERDESTRUCTION']))

#player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

#alien
num_of_aliens = 6
alienImg = [pygame.image.load('alien.png') for i in range(num_of_aliens)]
alienX = [random.randint(50, 650) for i in range(num_of_aliens)]
alienY = [random.randint(50, 150) for i in range(num_of_aliens)]
alienX_change = [4 for i in range(num_of_aliens)]
alienY_change = [40 for i in range(num_of_aliens)]

#bullet, has two states
#'ready'; you can't see bullet on screen
#'fire'; bullet visibly moving on screen
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 6
bullet_state = 'ready'

#score
score_value = 0
font = pygame.font.Font('broken15.ttf', 64)
textX = 10
textY = 10

#game over text
game_over_font = pygame.font.Font('broken15.ttf', 128)

def show_score(x, y):
	score = font.render('Score : ' + str(score_value), True, (225, 10, 10))
	screen.blit(score, (x, y))

def game_over_text():
	game_end_text = game_over_font.render('GAME OVER', True, (0, 225, 0))
	screen.blit(game_end_text, (200, 250))

def player(x, y):
	screen.blit(playerImg, (x, y))

def alien(x, y, i):
	screen.blit(alienImg[i], (x, y))

def fire_bullet(x, y):
	global bullet_state
	bullet_state = 'fire'
	screen.blit(bulletImg, (x + 16, y + 10))

def collisionOccuring(alienX, alienY, bulletX, bulletY):
	distance = math.sqrt((alienX - bulletX)**2 + (alienY - bulletY)**2)
	if distance < 50:
		return True
	return False
	
#game loop
running = True
while running:
	
	#background image
	screen.blit(background, (0, 0))
	
	#check if game is quit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
		#event where keystroke is pressed
		#check whether left arrow or right arrow
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change -= 5
			if event.key == pygame.K_RIGHT:
				playerX_change += 5
			if event.key == pygame.K_UP:
				if bullet_state == 'ready':
					bullet_sound = mixer.Sound('throw.wav')
					bullet_sound.play()
					
					#set bullet's x position as current players current
					#x-position value
					bulletX = playerX
					fire_bullet(bulletX, bulletY)
					
	#stop moving player when keypress ceases
	if event.type == pygame.KEYUP:
		if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
			playerX_change = 0
			
	#update player's horiz. position based on key press
	playerX += playerX_change
		
	#draw player at new position
	player(playerX, playerY)
	
	#enforce boundaries on player movement
	if playerX < 50:	#50px inside border
		playerX = 50
	elif playerX > 650:	#50px inside border and accounting for
		playerX = 650	#width of the player; 100px
		
	#iterate over aliens to check for game over, to move aliens appropriately
	#and to check if aliens have been shot
	for i in range(num_of_aliens):
		
		#check if game over due to alien's proximity to player
		proximity = math.sqrt((alienX[i] - playerX)**2 + (alienY[i] - playerY)**2)
		if proximity < 91 or alienY[i] > 480:
			for j in range(num_of_aliens):
				alienY[j] = 2000
			game_over_text()
			break
		
		#move alien horizontally
		alienX[i] += alienX_change[i]
		
		#enforce boundaries on alien movement
		if alienX[i] <= 50:	#50px inside border
			
			#set horizontal velocity
			alienX_change[i] = 4
			
			#adjust vertical position instantaneously
			alienY[i] += alienY_change[i]
			
		elif alienX[i] >= 650:	#50px inside border and accounting for
			#set horizontal velocity
			alienX_change[i] = -4	#width of the alien; 100px
			
			#adjust vertical position instantaneously
			alienY[i] += alienY_change[i]
			
		#collision
		if collisionOccuring(alienX[i], alienY[i], bulletX, bulletY):
			explosion_sound = mixer.Sound('explosion.wav')
			explosion_sound.play()
			bulletY = 480
			bullet_state = 'ready'
			score_value += 1
			alienX[i] = random.randint(50, 650)
			alienY[i] = random.randint(50, 150)
		
		#draw aliens at new required coords
		alien(alienX[i], alienY[i], i)
		
	#move bullet
	if bulletY < 0:
			bulletY = 480
			bullet_state = 'ready'
	if bullet_state == 'fire':
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change		
	
	#update display
	player(playerX, playerY)
	show_score(textX, textY)
	pygame.display.update()

pygame.quit()
