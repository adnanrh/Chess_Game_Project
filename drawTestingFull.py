import sys, pygame
from ChessBoard import *
from gameConstants import *
from menu import *

pygame.init()

screenWidth = 600
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_icon(whiteKnightImage)
pygame.display.set_caption(screenCaption)
screen.fill(GREY)
selectedOption = launchStartMenu(screen, screenWidth, screenHeight)
if not selectedOption == PLAYERVSPLAYER:
	pygame.quit()
	sys.exit()

boardLength = screenHeight
boardpos = (screenWidth-screenHeight)/2, 0

board = Board(screen, (boardpos), boardLength)

board.draw()
currentPieceList = board.pieceListWhite
waitingPieceList = board.pieceListBlack
selectedPiece = None
while True:
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			clickpos = pygame.mouse.get_pos()
			clickedSquare = board.getSquarebyMousePosition(clickpos)
			if clickedSquare:
				clickedPosition = clickedSquare.position
				isMyPiece = False
				clickedPiece = Board.getPiecebyPosition(currentPieceList, clickedPosition)
				if clickedPiece: isMyPiece = True
				else:
					clickedPiece = Board.getPiecebyPosition(waitingPieceList, clickedPosition)
					isMyPiece = False
				if clickedPiece:
					if not selectedPiece:
						if isMyPiece:
							selectedPiece = clickedPiece
							print("piece at ", clickedPiece.position, " selected!")
							clickedSquare.color = YELLOW
							clickedSquare.draw(board.surface)
							clickedPiece.draw(board.surface)
							clickedSquare.color = BROWN if (clickedPosition[0]+clickedPosition[1])%2 == 0 else BLACK
					elif selectedPiece == clickedPiece:
						selectedPiece = None
						print("piece at ", clickedPiece.position, " deselected!")
						clickedSquare.color = BROWN if (clickedPosition[0]+clickedPosition[1])%2 == 0 else BLACK
						clickedSquare.draw(board.surface)
						clickedPiece.draw(board.surface)
					else:
						selectedPiece.updatePotentialSpaces(currentPieceList, waitingPieceList, True)
						if clickedPosition in selectedPiece.potentialSpaces:
							print("piece at ", selectedPiece.position, " kills piece at ", clickedPiece.position)
							waitingPieceList.remove(clickedPiece)
							oldSquare = board.getSquarebyPosition(selectedPiece.position)
							oldSquare.draw(board.surface)
							clickedSquare.draw(board.surface)
							selectedPiece.move(clickedSquare)
							selectedPiece.draw(board.surface)
							#looking for checkmate!
							if Board.checkMated(selectedPiece, currentPieceList, waitingPieceList):
								print("Checkmate!")
								endOption = launchEndMenu(screen, currentPieceList[0].color, waitingPieceList[0].color)
								if endOption == QUIT:
									pygame.quit()
									sys.exit()
								elif endOption == REMATCH:
									board.reset()
									board.draw()
									currentPieceList = board.pieceListWhite
									waitingPieceList = board.pieceListBlack
									selectedPiece = None
									break
							swapper = currentPieceList
							currentPieceList = waitingPieceList
							waitingPieceList = swapper
							selectedPiece = None
						else:
							print("piece at ", selectedPiece.position, " can't move there!")
				else:
					if selectedPiece:
						selectedPiece.updatePotentialSpaces(currentPieceList, waitingPieceList, True)
						print(selectedPiece.potentialSpaces)
						if clickedPosition in selectedPiece.potentialSpaces:
							print("piece at ", selectedPiece.position, " moves to ", clickedPosition)
							oldSquare = board.getSquarebyPosition(selectedPiece.position)
							oldSquare.draw(board.surface)
							selectedPiece.move(clickedSquare)
							selectedPiece.draw(board.surface)
							#looking for checkmate!
							if Board.checkMated(selectedPiece, currentPieceList, waitingPieceList):
								print("Checkmate!")
								endOption = launchEndMenu(screen, currentPieceList[0].color, waitingPieceList[0].color)
								if endOption == QUIT:
									pygame.quit()
									sys.exit()
								elif endOption == REMATCH:
									board.reset()
									board.draw()
									currentPieceList = board.pieceListWhite
									waitingPieceList = board.pieceListBlack
									selectedPiece = None
									break
							swapper = currentPieceList
							currentPieceList = waitingPieceList
							waitingPieceList = swapper
							selectedPiece = None
						else:
							print("piece at ", selectedPiece.position, " can't move there!")



