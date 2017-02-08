import sys, pygame

screenHeight = screenWidth = 400

WHITE = 255, 255, 255
BLACK = 0, 0, 0
BROWN = 185, 156, 107
screen = pygame.display.set_mode((screenHeight, screenWidth))
screen.fill(WHITE)
pygame.init()

class MySprite(pygame.sprite.Sprite):
	def __init__(self, image, posx, posy):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (posx, posy)

testSprite = pygame.image.load("index.png")
mainSprite = MySprite(testSprite, 20, 20)
myGroup = pygame.sprite.Group()
myGroup.add(mainSprite)
myGroup.draw(screen)



while True:
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			clickpos = pygame.mouse.get_pos()
			screen.fill(WHITE)
			screen.blit(testSprite, clickpos)


