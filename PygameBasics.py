import pygame

pygame.init()

sh = 300
sl = 600

win = pygame.display.set_mode((sl, sh))
pygame.display.set_caption('Caption')

clock = pygame.time.Clock()


run = True
while run:
	win.fill((125,125,125))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False


	clock.tick(30)
	pygame.display.update()

pygame.quit()