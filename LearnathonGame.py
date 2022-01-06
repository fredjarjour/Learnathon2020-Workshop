import pygame, random

pygame.init()

sh = 300
sl = 600

win = pygame.display.set_mode((sl, sh))
pygame.display.set_caption('No Internet')

clock = pygame.time.Clock()

class Dinosaur(object):
	def __init__(self):
		self.w = 35
		self.h = 50
		self.x = 100
		self.y = sh-150
		self.jump_inc = 0
		self.jumping = False
		self.crouching = False
		self.run_img = [pygame.image.load("walk1.png"), pygame.image.load("walk2.png")]
		self.crouch_img = [pygame.image.load("crouch1.png"), pygame.image.load("crouch2.png")]
		self.jump_img = pygame.image.load("jump.png")
		self.run_inc = 0
		self.crouch_inc = 0
		self.bullets = []
		self.shot_inc = 0

	def draw(self):
		#pygame.draw.rect(win, (125,125,125), (self.x, self.y, self.w, self.h))
		#pygame.draw.rect(win, (255,0,0), (self.x, self.y, self.w, self.h), 1)

		if self.jumping:
			win.blit(self.jump_img, (self.x, self.y))

		elif self.crouching:
			win.blit(self.crouch_img[self.crouch_inc//5], (self.x, self.y))

			if self.crouch_inc == 9:
				self.crouch_inc = -1
			self.crouch_inc += 1

		else:
			win.blit(self.run_img[self.run_inc//5], (self.x, self.y))

			if self.run_inc == 9:
				self.run_inc = -1
			self.run_inc += 1


	def move(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP] and not self.jumping and not self.crouching:
			self.jumping = True

		if keys[pygame.K_DOWN] and not self.jumping:
			self.crouching = True
			self.w = 50
			self.h = 25
			self.y = sh - 125
		elif not self.jumping:
			self.crouching = False
			self.y = sh - 150
			self.w = 35
			self.h = 50

		if self.jumping:
			if self.jump_inc <= 20:
				self.y -= (10 - self.jump_inc)*2
				self.jump_inc += 1
			else:
				self.jump_inc = 0
				self.jumping = False
		if score >= 100:
			if keys[pygame.K_SPACE] and self.shot_inc == 0:
				self.bullets.append(Bullet())
				self.shot_inc = 10

			if self.shot_inc > 0:
				self.shot_inc -= 1

			for bullet in self.bullets:
				if bullet.x >= sl:
					self.bullets.remove(bullet)
			



class Cactus(object):
	def __init__(self):
		self.image = pygame.image.load("cactus.png")
		if random.randint(1,2) == 1:
			self.w = 25
			self.h = 50
			self.big = True
		else:
			self.w = 48
			self.h = 25
			self.big = False
			self.image = pygame.transform.scale(self.image, (12, self.h))

		self.y = (sh-100) - self.h
		self.x = sl
		self.type = "cactus"

	def draw(self):
		#pygame.draw.rect(win, (0,0,0), (self.x, self.y, self.w, self.h))
		#pygame.draw.rect(win, (255,0,0), (self.x, self.y, self.w, self.h), 1)

		if self.big:
			win.blit(self.image, (self.x, self.y))
		else:
			win.blit(self.image, (self.x, self.y))
			win.blit(self.image, (self.x+12, self.y))
			win.blit(self.image, (self.x+24, self.y))
			win.blit(self.image, (self.x+36, self.y))


	def hit(self):
		if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(pygame.Rect(player.x, player.y, player.w, player.h)):
			return True
		return False



class Bird(object):
	def __init__(self):
		self.w = 50
		self.h = 25
		self.y = (sh - 100) - (self.h + 10) * random.randint(1,3)
		self.x = sl
		self.flying = [pygame.image.load("bird1.png"), pygame.image.load("bird2.png")]
		self.fly_inc = 0
		self.type = "bird"

	def draw(self):
		#pygame.draw.rect(win, (0,0,0), (self.x, self.y, self.w, self.h))
		#pygame.draw.rect(win, (255,0,0), (self.x, self.y, self.w, self.h), 1)
		win.blit(self.flying[self.fly_inc//10], (self.x, self.y))

		if self.fly_inc == 19:
			self.fly_inc = -1
		self.fly_inc += 1


	def hit(self):
		if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(pygame.Rect(player.x, player.y, player.w, player.h)):
			return True
		return False 


class Bullet(object):
	def __init__(self):
		self.x = player.x + 25
		self.y = player.y + 25
		self.vel = 5
		self.w = 9
		self.h = 5
		self.image = pygame.image.load("fireball.png")

	def draw(self):
		#pygame.draw.rect(win, (255,0,0), (self.x, self.y, self.size, self.size))
		win.blit(self.image, (int(self.x), int(self.y)))

	

	

play = True
while play:
	score = 0
	player = Dinosaur()


	enemies = []
	inc = 0
	game_speed = 1
	score_inc = 0


	#MAINLOOP
	run = True
	end = True
	while run:
		win.fill((255,255,255))
		pygame.draw.rect(win, (0,0,0), (0, sh-100, sl, 100))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				end = False
				run = False
				play = False

		inc += 1 * game_speed
		if inc >= 100:
			if random.randint(1,2) == 1 and score >= 100:
				enemies.append(Bird())
			else:
				enemies.append(Cactus())
			game_speed += 0.1
			inc = 0
		

		if score_inc <= 5:
			score_inc += 1 * game_speed
		else:
			score_inc = 0
			score += 1

		for enemy in enemies:
			enemy.x -= 5 * game_speed
			enemy.draw()
			if enemy.hit():
				run = False
			if enemy.x + enemy.w == 0:
				enemies.remove(enemy)
			for bullet in player.bullets:
				if pygame.Rect(bullet.x, bullet.y, bullet.w, bullet.h).colliderect(pygame.Rect(enemy.x, enemy.y, enemy.w, enemy.h)):
					if enemy.type == "bird":
						enemies.remove(enemy)
						player.bullets.remove(bullet)

		for bullet in player.bullets:
			bullet.draw()
			bullet.x += bullet.vel *game_speed

		player.draw()
		player.move()


		font = pygame.font.SysFont('comicsans', 40)
		smaller_font = pygame.font.SysFont('comicsans', 30)
		text = font.render(str(score), 1, (0,0,0))
		win.blit(text,(sl - text.get_width() - 10, 10))


		if score <= 20:
			controls = smaller_font.render("Press up to jump and down to crouch", 1, (0,0,0))
			win.blit(controls, (10, 10))

		if 100 <= score <= 125:
			unlocked_fire = smaller_font.render("You can now shoot birds with spacebar!", 1, (0,0,0))
			win.blit(unlocked_fire, (10, 10))

		pygame.display.update()
		clock.tick(30)


	while end:
		win.fill((0,0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				end = False
				play = False


		font = pygame.font.SysFont('comicsans', 50)
		final_score = font.render("Your score: " + str(score), 1, (255,255,255))
		exit_game = font.render("Click anywhere to restart", 1, (255,255,255))
		win.blit(final_score, (sl/2 - final_score.get_width()/2, sh/4))
		win.blit(exit_game, (sl/2 - exit_game.get_width()/2, sh* 2/3))


		if pygame.mouse.get_pressed()[0]:
			end = False

		pygame.display.update()


pygame.quit()