import sys, pygame

pygame.init()

screenHeight = screenWidth = 600

# consider using Sprite class and group for chess squares
class ChessSquare:
	color = 0, 0, 0
	position = 0, 0
	square = None
	sidelength = 0
	def __init__(self, color, position, sidelength):
		self.color = color
		self.position = position
		self.sidelength = sidelength

	def draw(self, screen, location):
		self.square = pygame.draw.rect(screen, self.color, ((location), (self.sidelength, self.sidelength)))

WHITE = 255, 255, 255
BLACK = 0, 0, 0
BROWN = 185, 156, 107
RED = 255, 0, 0
BLUE = 0, 0, 255
screen = pygame.display.set_mode((screenHeight, screenWidth))
screen.fill(WHITE)

boardHeight = boardWidth = screenHeight - 100
boardpos = (screenWidth-boardWidth)/2, (screenHeight-boardHeight)/2
board = pygame.draw.rect(screen, BLACK, ((boardpos), (boardWidth, boardHeight)))
squareLength = boardHeight/8
squareList = []
for i in range(0, 8):
	for j in range(0, 8):
		currentSquarePos = i*squareLength+boardpos[0], j*squareLength+boardpos[1]
		squarecolor = BROWN if (i+j)%2 == 0 else BLACK
		newSquare = ChessSquare(squarecolor, (j+1, i+1), squareLength)
		newSquare.draw(screen, currentSquarePos)
		squareList.append(newSquare)

temp = squareList[7].square.copy()
pieceRow = 8
pieceCol = 1
piece = temp.copy() 
piece.width = 20
piece.height = 20
piece.move_ip(temp.centerx - piece.centerx, temp.centery - piece.centery)

piece2Row = 1
piece2Col = 8
temp = squareList[56].square.copy()
piece2 = temp.copy()
piece2.width = 20
piece2.height = 20
piece2.move_ip(temp.centerx - piece2.centerx, temp.centery - piece2.centery)

pygame.draw.rect(screen, RED, piece)
pygame.draw.rect(screen, BLUE, piece2)

pieceList = [(8, 1), (1, 8)]
pieceSelected = False
piece2Selected = False
while True:
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			clickpos = pygame.mouse.get_pos()
			clickedSquare = None
			for square in squareList:
				if square.square.collidepoint(clickpos):
					clickedSquare = square
					break
			if clickedSquare:
				if clickedSquare.position in pieceList:
					pieceNumber = pieceList.index(clickedSquare.position)
					if not pieceSelected and not piece2Selected:
						if pieceNumber == 0:
							pieceSelected = True
							piece2Selected = False
							print("piece 1 selected!")
						else:
							piece2Selected = True
							pieceSelected = False
							print("piece 2 selected!")
					else:
						if pieceSelected and pieceNumber == 0:
							pieceSelected = False
							print("piece 1 deselected!")
						elif piece2Selected and pieceNumber == 1:
							piece2Selected = False
							print("piece 2 deselected!")
						#move a previously selected piece onto another piece
						elif pieceSelected and pieceNumber == 1:
							#pieceSelected = False
							pass
						elif piece2Selected and pieceNumber == 0:
							#piece2Selected = False
							pass
				#move a previously selected piece to an empty space
				elif pieceSelected: 
					temp = clickedSquare.square.copy()
					piece.move_ip(temp.centerx - piece.centerx, temp.centery - piece.centery)
					pieceList.remove((pieceRow, pieceCol))
					currentSquare = ((pieceRow-1) + (pieceCol-1)*8)
					squaretoFill = squareList[currentSquare]
					squaretoFill.draw(screen, squaretoFill.square.topleft)
					pygame.draw.rect(screen, RED, piece)
					pieceRow = clickedSquare.position[0]
					pieceCol = clickedSquare.position[1]
					pieceList.insert(0, (pieceRow, pieceCol))
					pieceSelected = False
				elif piece2Selected: 
					temp = clickedSquare.square.copy()
					piece2.move_ip(temp.centerx - piece2.centerx, temp.centery - piece2.centery)
					pieceList.remove((piece2Row, piece2Col))
					currentSquare = ((piece2Row-1) + (piece2Col-1)*8)
					squaretoFill = squareList[currentSquare]
					squaretoFill.draw(screen, squaretoFill.square.topleft)
					pygame.draw.rect(screen, BLUE, piece2)
					piece2Row = clickedSquare.position[0]
					piece2Col = clickedSquare.position[1]
					pieceList.insert(1, (piece2Row, piece2Col))
					piece2Selected = False



