import sys, pygame, os
from gameConstants import *

pygame.init()

class menuItem(pygame.sprite.Sprite):
	mouseisOver = False
	font = None
	text = ''
	def __init__(self, image, center, text=None, font=None):
		pygame.sprite.Sprite.__init__(self)
		self.font = font
		self.text = text
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = center

	def changeState(self, mousepos):
		oldMouseState = self.mouseisOver
		self.mouseisOver = True if self.rect.collidepoint(mousepos) else False
		if self.mouseisOver == oldMouseState:
			return False
		elif self.mouseisOver:
			self.image = self.font.render(self.text, 1, YELLOW)
		elif not self.mouseisOver:
			self.image = self.font.render(self.text, 1, WHITE)
		return True

	def clicked(self, mousepos):
		return self.rect.collidepoint(mousepos)

def launchStartMenu(surface, surfaceWidth, surfaceHeight):
	pygame.mixer.music.load(startMusic)
	pygame.mixer.music.play(-1)
	titleSpriteGroup = pygame.sprite.Group()
	titleSpriteGroup.add(menuItem(titleDisplay, titlePosition, titleText, title))
	optionsSpriteGroup = pygame.sprite.Group()
	optionsSpriteGroup.add(menuItem(option1Display, option1Position, option1Text, option))
	optionsSpriteGroup.add(menuItem(option2Display, option2Position, option2Text, option))
	optionsSpriteGroup.add(menuItem(option3Display, option3Position, option3Text, option))
	squareLength = surfaceWidth/8
	for i in range(8):
		for j in range(8):
			color = BROWN if (i+j)%2 == 0 else BLACK
			pygame.draw.rect(surface, color, ((i*squareLength, j*squareLength), (squareLength, squareLength)))
	titleSpriteGroup.draw(surface)
	optionsSpriteGroup.draw(surface)
	while True:
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEMOTION:
				for sprite in optionsSpriteGroup.sprites():
					if sprite.changeState(event.pos):
						spriteToUpdate = pygame.sprite.Group()
						spriteToUpdate.add(sprite)
						spriteToUpdate.draw(surface)
						break
			elif event.type == pygame.MOUSEBUTTONDOWN:
				for sprite in optionsSpriteGroup.sprites():
					if sprite.clicked(event.pos):
						if sprite.text == option1Text: 
							pygame.mixer.music.stop()
							return PLAYERVSPLAYER
						# sprite.text == option2Text: return PLAYERVSCOMP
						#elif sprite.text == option3Text: return COMPVSCOMP

def launchEndMenu(surface, endCondition, currentPlayercolor, waitingPlayercolor):
	endtext = ''
	if endCondition == CHECKMATE:
		endtext = currentPlayercolor + ' checkmates ' + waitingPlayercolor + '!'
	elif endCondition == STALEMATE:
		endtext = 'Draw by Stalemate!'
	if endCondition != EXIT:
		pygame.mixer.music.load(endMusic)
		pygame.mixer.music.play(-1)
	endDisplay = endTitle.render(endtext, 1, GREEN)
	titleSpriteGroup = pygame.sprite.Group()
	titleSpriteGroup.add(menuItem(endDisplay, titlePosition, endtext, endTitle))
	optionsSpriteGroup = pygame.sprite.Group()
	optionsSpriteGroup.add(menuItem(option4Display, option4Position, option4Text, option))
	optionsSpriteGroup.add(menuItem(option5Display, option5Position, option5Text, option))
	optionsSpriteGroup.add(menuItem(option6Display, option6Position, option6Text, option))
	titleSpriteGroup.draw(surface)
	optionsSpriteGroup.draw(surface)
	while True:
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEMOTION:
				for sprite in optionsSpriteGroup.sprites():
					if sprite.changeState(event.pos):
						spriteToUpdate = pygame.sprite.Group()
						spriteToUpdate.add(sprite)
						spriteToUpdate.draw(surface)
						break
			elif event.type == pygame.MOUSEBUTTONDOWN:
				for sprite in optionsSpriteGroup.sprites():
					if sprite.clicked(event.pos):
						pygame.mixer.music.stop()
						if sprite.text == option4Text: return REMATCH
						elif sprite.text == option5Text: return MAINMENU
						elif sprite.text == option6Text: return QUIT


def launchPromotionMenu(surface, surfaceWidth, surfaceHeight, color):
	itemList = []
	if color == player1Color:
		itemList = [whiteRookImage, whiteKnightImage, whiteBishopImage, whiteQueenImage]
	else:
		itemList = [blackRookImage, blackKnightImage, blackBishopImage, blackQueenImage]

	headingText = 'Pawn Promoted!'
	headingDisplay = endTitle.render(headingText, 1, GREEN)
	headingSpriteGroup = pygame.sprite.Group()
	headingSpriteGroup.add(menuItem(headingDisplay, titlePosition, headingText, endTitle))
	optionsSpriteGroup = pygame.sprite.Group()
	firstItemPosition = surfaceWidth/5, surfaceHeight/2
	optionDistance = surfaceWidth/5
	i = 0
	for item in itemList:
		position = firstItemPosition[0]+i*optionDistance, firstItemPosition[1]
		optionsSpriteGroup.add(menuItem(item, position))
		i = i+1
	headingSpriteGroup.draw(surface)
	optionsSpriteGroup.draw(surface)
	while True:
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				for sprite in optionsSpriteGroup.sprites():
					if sprite.clicked(event.pos):
						if sprite.image == whiteRookImage or sprite.image == blackRookImage: return PROMOTETOROOK
						elif sprite.image == whiteKnightImage or sprite.image == blackKnightImage: return PROMOTETOKNIGHT
						elif sprite.image == whiteBishopImage or sprite.image == blackBishopImage: return PROMOTETOBISHOP
						elif sprite.image == whiteQueenImage or sprite.image == blackQueenImage: return PROMOTETOQUEEN
