'''Author: Juan Marron

Image sources:
Asteroids: small pieces of a photo on nssdc.gsfc.nasa.gov
Lava is a piece cut from a picture of the sun on this website: http://cindeepthoughts.com/category/sun/
Created the mech character myself on charas-project.net

Notes:
	Think about creating a scrolling background using Parallax (get it from github)
	Add a little health bar to the mech in the future
	Also add a class of sprite that if collided with the mech will give it health
	Have a Game over screen, with your score and the highscore so people can hate themselves
	for not getting it

'''

import pygame, sys, random
from pygame.locals import *


class Mech(pygame.sprite.Sprite):
	# start variable gives the user 111 microseconds of delay between 
	# starting the game, and gravity starting to take effect. Meaning
	# after the game starts, the mech isn't affected by gravity for a
	# small period of time so that the user can get ready a bit
	start = 0	
	invincible = False
	# time_out is a timer for the invincibility. After 100 frames, the mech is no longer invincible
	time_out = 0
	def __init__(self, X, Y):
		pygame.sprite.Sprite.__init__(self)
		self.X = X
		self.Y = Y
		self.Xspeed = 0
		self.Yspeed = 0
		self.image = pygame.image.load('mech.png')
		self.rect = self.image.get_rect()

		self.hp = 15
	def update(self, jetpack=False):
		self.start += 1	
		if jetpack and not self.invincible:
			self.image = pygame.image.load('jetpack.png')
			self.position = (self.X, self.Y)
			self.rect = self.image.get_rect()
			self.rect.center = self.position
		if not jetpack and not self.invincible:
			self.image = pygame.image.load('mech.png')
			self.position = (self.X, self.Y)
			self.rect = self.image.get_rect()
			self.rect.center = self.position
		if self.invincible:
			if jetpack:
				self.image = pygame.image.load('jetpack_inv.png')
				self.position = (self.X, self.Y)
				self.rect = self.image.get_rect()
				self.rect.center = self.position
			else:
				self.image = pygame.image.load('mech_inv.png')
				self.position = (self.X, self.Y)
				self.rect = self.image.get_rect()
				self.rect.center = self.position

		if self.invincible:
			self.time_out += 1
		if self.invincible and self.time_out >= 300:
			self.invincible = False
			self.time_out = 0
	#The parameter for this function is the list of pressed keys
	def move(self, keys_pressed):
		global gravity
		if (keys_pressed[K_UP]) and self.Y >= 30:
			self.Y -= 12
			# Need to reset the following to zero because if the user presses K_UP, then the
			# speed of gravity when K_UP is released will be zero.
			gravity = 0
		if (keys_pressed[K_DOWN]) and self.Y <= win.get_height() - 30:
			self.Y += 12
		if (keys_pressed[K_RIGHT]):
			if self.X >= win.get_width():
				self.X = 0
			self.X += 12
		if (keys_pressed[K_LEFT]):
			if self.X <= 30:
				self.X = win.get_width()
			self.X -= 12

		if (self.Y <= (win.get_height() - 30)) and self.start >= 10:
			self.Y += gravity	
			gravity += 2
			# Set a terminal velocity, otherwise the fall can get pretty fast
			if gravity > 30:
				gravity = 30	
class PowerUp(pygame.sprite.Sprite):		
	def __init__(self, image, invincibility_pwrup=False):
		pygame.sprite.Sprite.__init__(self)	
		self.invincibility_pwrup = invincibility_pwrup
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.Y = 0
		self.X = random.randint(1, win.get_width()-10)	
		self.speed = random.randint(5, 10)

	def update(self, hit_list, mech):
		if self in hit_list:
			if self.invincibility_pwrup:
				mech.invincible = True
				self.kill()
			elif not self.invincibility_pwrup:
				mech.hp += 5
				self.kill()
		
		self.Y += self.speed
		if self.Y >= win.get_height():
			self.kill()

		self.rect = self.image.get_rect()
		self.rect.center = (self.X, self.Y)

class Collider(pygame.sprite.Sprite):
	# start variable is for a bit of a delay between the time when the user opens the game and the asteroids actually start
	# falling
	start = 0
	def __init__(self, image, lava=False):
		self.lava = lava
		if self.lava:
			pygame.sprite.Sprite.__init__(self)
			self.image = pygame.image.load(image)
			self.rect = self.image.get_rect()
			self.Y = win.get_height()
			self.X = win.get_width()/2
		if not self.lava:
			self.speed = random.randint(5, 25)
			pygame.sprite.Sprite.__init__(self)
			self.image = pygame.image.load(image)
			self.rect = self.image.get_rect()
			self.Y = 0
			self.X = random.randint(1, win.get_width()-10)
	def update(self, hit_list, mech):
		self.start += 1
		if not self.lava and self.start >= 15:
			self.Y += self.speed
		self.rect = self.image.get_rect()
		self.rect.center = (self.X, self.Y)
		if self in hit_list:
			if not mech.invincible:
				win.fill(RED)
				mech.hp -= 1
			elif not self.lava:
				self.X = random.randint(1, win.get_width()-10)
				self.Y = 0
			if mech.hp == 0:
				if score > int(current_high_score):
					high_score.write(str(score))
					high_score.close()
				else:
					high_score.write(current_high_score)
					high_score.close()
				game_over()
			
				
	def send_up(self):
		if not self.lava:
			self.speed = random.randint(5, 25)
			self.Y = 0
			self.X = random.randint(1, win.get_width()-10)

def game_over():
	back_to_game = False
	while True:	
		win.fill(BLACK)
		keys_pressed = pygame.key.get_pressed()
		
		# Going back to the game needs some more revision
		'''if back_to_game:
			break'''
		g_over = FONT.render("GAME OVER!", 1, RED)
		if int(current_high_score) > score:
			your_score = FONT.render("Your score was: " + str(score), 1, RED)
			your_high_score = FONT.render("High score is: " + str(current_high_score), 1, RED)
		else:
			your_score = FONT.render("Your score was: " + str(score) + " That's a new high score!", 1, RED)
			your_high_score = FONT.render("High score is: " + str(score), 1, RED)		
		'''play_again = FONT.render("Would you like to play again? y/n", 1, RED)'''
		exit_game_label = FONT.render("Hit ESC to exit", 1, RED)
	
		win.blit(g_over, (win.get_width()/3, win.get_height()/2))
		win.blit(your_score, (win.get_width()/3, win.get_height()/2 + 20))
		win.blit(your_high_score, (win.get_width()/3, win.get_height()/2 + 40))	
		win.blit(exit_game_label, (win.get_width()/3, win.get_height()/2 + 60))
		
		'''if 1 in keys_pressed:
			quit_all()'''
		for event in pygame.event.get():
			if event.type == QUIT:
				quit_all()
			'''if event.key == K_y:
				back_to_game = True
				quit_all()'''
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					quit_all()
		pygame.display.flip()
		fps.tick(30)		
def quit_all():
	pygame.quit()
	sys.exit()

pygame.init()
fps = pygame.time.Clock()

FONT = pygame.font.SysFont(None, 20)
RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 255, 255)
BLACK = pygame.Color(0, 0, 0)

win = pygame.display.set_mode((790, 790), DOUBLEBUF)
pygame.display.set_caption('Jet Mech')

# Global variable for gravity
gravity = 0

# Highest score is saved in a file in the directory. If the file does not exist (first time playing the game),
# then the file is created. Otherwise it is loaded up, and the high score from there is parsed out. 
# If the high score from the current session exceeds the last high score, the new high score gets written into
# the file. In the future, might include more than one highscore (like top 3 or something)
# Note that if the game crashes for any reason the HighScore gets erased :( Need to find a way around that.
try:
	high_score = open("HighScore.txt", 'r+')
# If file doesn't exist, create it with a dummy value of 0, then revert the stream back to read mode
except IOError:
	high_score = open("HighScore.txt", 'w')
	high_score.write("0")
	high_score.close()
	high_score = open("HighScore.txt", 'r')

current_high_score = high_score.readline()
if not current_high_score:
	current_high_score = 0
high_score.close()
high_score = open("HighScore.txt", 'w')

#Initialize the score. Score just gets incremented once every time the game loop runs.
score = 1
time = 1

# Initialize mech sprite and add it to a sprite group
mech = Mech(win.get_width()/2, win.get_height()*3/4)
mech_group = pygame.sprite.Group()
mech_group.add(mech)

# Initialize collider sprites and add them to a sprite group
colliders = [
	Collider('ast1.png'),
	Collider('ast2.png'),
	Collider('lava.png', True),	
]
collider_group = pygame.sprite.Group()
for element in colliders:
	collider_group.add(element)
# Create the group that will contain the powerups
# A powerup will be created around every 4000 frames
pwr_group = pygame.sprite.Group()

# First screen
menu = 0
while True:	
	for event in pygame.event.get():
		if event.type == QUIT:
			high_score.write(current_high_score)
			quit_all()	
		if event.type == KEYDOWN:
			if event.key == K_RETURN:
				menu = 1
			
			if event.key == K_SPACE:
				menu = 1
	
	title = pygame.image.load('title_screen.png')
	win.blit(title, (0,0))

	pygame.display.flip()
	fps.tick(30)
	
	if menu:
		break
# Game loop
first = True
while True:
	keys = pygame.key.get_pressed()
	mech.move(keys)

	# If an asteroid has reached the bottom, send it back to the top and reassign it an x value.
	# This way I don't need to create new Collider objects
	for element in colliders:	
		if element.Y > win.get_height()-55:
			element.send_up()

	# Get a new asteroid to increase the difficulty
	# Asteroid type is random
	# Limit is 9 asteroids, otherwise it becomes impossible	
	if time%400 == 0 and len(colliders) <= 9:
		r = random.randint(1, 3)
		if r == 1:
			colliders.append(Collider('ast1.png'))
		if r == 2:
			colliders.append(Collider('ast2.png'))
		if r == 3:
			colliders.append(Collider('ast3.png'))
		collider_group.add(colliders[-1])

	# As the game gets harder, hp powerups get scarcer
	increment = 1000
	if time%increment == 0:
		pwrup = PowerUp('pwrup.png')
		pwr_group.add(pwrup)
		increment += 1000
	if time%1500 == 0:
		pwrup = PowerUp('inv.png', True)
		pwr_group.add(pwrup)


	for event in pygame.event.get():
		if event.type == QUIT:
			high_score.write(current_high_score)
			quit_all()	
	
	win.fill(BLUE)
	
	score += 3
	time += 1
	# For some reason, on the first time collisions is called, it detects that the mech is colliding with all asteroids
	# even though that is not the case
	collisions = pygame.sprite.spritecollide(mech, collider_group, False)
	collide_with_powerup = pygame.sprite.spritecollide(mech, pwr_group, False)

	if not first:
		collider_group.update(collisions, mech)
		collider_group.draw(win)
		pwr_group.update(collide_with_powerup, mech)	
		pwr_group.draw(win)
	
	if keys[K_UP]:
		# Calling update(True) displays the mech with the jetpack.
		mech_group.update(True)
		mech_group.draw(win)
	else:
		mech_group.update()
		mech_group.draw(win)
		
	# Display the score, hp, and high score	
	hscore = FONT.render("High Score: " + str(current_high_score), 1, BLACK)
	win.blit(hscore, (win.get_width() - 200, 30))
	mech_hp = FONT.render("HP: " + str(mech.hp) + " Score: " + str(score), 1, BLACK)
	win.blit(mech_hp, (win.get_width() - 200, 70))
	
	
	first = False
	pygame.display.flip()
	fps.tick(30)	
