import sys
import random
import pygame
from gameConstants import *
from menu import *


"""
Instances of this class represent a single square on an 8x8 chessboard.
Each square has the following attributes: 
- color (black or white) 
- position (eg: top left square is at position (1, 1))
- side length
- square (which is a pygame.Rect object which is used to detect if a 
  particular square is clicked)
- location (the location to assign to the topleft corner of the square
  attribute)
"""
class ChessSquare:
	color = 0, 0, 0
	position = 0, 0
	square = None
	sidelength = 0
	location = 0, 0
	def __init__(self, color, position, sidelength, location):
		self.color = color
		self.position = position
		self.sidelength = sidelength
		self.location = location
		self.square = pygame.Rect((self.location), (self.sidelength, self.sidelength))

	"""
	Draws the square (by invoking pygame.draw.rect) to the surface
	passed in the screen argument.
	"""
	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.square)

class Board:
	surface = None
	rect = None
	squareList = []
	pieceListWhite = []
	pieceListBlack = []
	currentPieceList = []
	waitingPieceList = []
	selectedPiece = None
	doubleUpPawn = None
	enPassantSpace = None
	highlightedSquares = []

	def __init__(self, surface, position, sideLength):
		self.surface = surface
		self.rect = pygame.draw.rect(surface, BLACK, ((position), (sideLength, sideLength)))
		squareLength = sideLength/8
		for i in range(0, 8):
			for j in range(0, 8):
				currentSquarePos = i*squareLength+position[0], j*squareLength+position[1]
				squarecolor = BROWN if (i+j)%2 == 0 else BLACK
				newSquare = ChessSquare(squarecolor, (j+1, i+1), squareLength, currentSquarePos)
				self.squareList.append(newSquare)
		
		self.setInitialPositions()
		for piece in self.pieceListWhite:
			piece.updatePotentialSpaces(self.pieceListWhite, self.pieceListBlack, False)
		for piece in self.pieceListBlack:
			piece.updatePotentialSpaces(self.pieceListBlack, self.pieceListWhite, False)
		self.currentPieceList = self.pieceListWhite
		self.waitingPieceList = self.pieceListBlack

	def setInitialPositions(self):
		#initialize white pieces
		for i in range(8):
			self.pieceListWhite.append(Pawn(whitePawnImage, self.getSquarebyPosition((7, i+1)), player1Color))
		self.pieceListWhite.append(Rook(whiteRookImage, self.getSquarebyPosition((8, 1)), player1Color))
		self.pieceListWhite.append(Rook(whiteRookImage, self.getSquarebyPosition((8, 8)), player1Color))
		self.pieceListWhite.append(Knight(whiteKnightImage, self.getSquarebyPosition((8, 2)), player1Color))
		self.pieceListWhite.append(Knight(whiteKnightImage, self.getSquarebyPosition((8, 7)), player1Color))
		self.pieceListWhite.append(Bishop(whiteBishopImage, self.getSquarebyPosition((8, 3)), player1Color))
		self.pieceListWhite.append(Bishop(whiteBishopImage, self.getSquarebyPosition((8, 6)), player1Color))
		self.pieceListWhite.append(Queen(whiteQueenImage, self.getSquarebyPosition((8, 4)), player1Color))
		self.pieceListWhite.append(King(whiteKingImage, self.getSquarebyPosition((8, 5)), player1Color))
		#initialize black pieces
		for i in range(8):
			self.pieceListBlack.append(Pawn(blackPawnImage, self.getSquarebyPosition((2, i+1)), player2Color))
		self.pieceListBlack.append(Rook(blackRookImage, self.getSquarebyPosition((1, 1)), player2Color))
		self.pieceListBlack.append(Rook(blackRookImage, self.getSquarebyPosition((1, 8)), player2Color))
		self.pieceListBlack.append(Knight(blackKnightImage, self.getSquarebyPosition((1, 2)), player2Color))
		self.pieceListBlack.append(Knight(blackKnightImage, self.getSquarebyPosition((1, 7)), player2Color))
		self.pieceListBlack.append(Bishop(blackBishopImage, self.getSquarebyPosition((1, 3)), player2Color))
		self.pieceListBlack.append(Bishop(blackBishopImage, self.getSquarebyPosition((1, 6)), player2Color))
		self.pieceListBlack.append(Queen(blackQueenImage, self.getSquarebyPosition((1, 4)), player2Color))
		self.pieceListBlack.append(King(blackKingImage, self.getSquarebyPosition((1, 5)), player2Color))

	def draw(self):
		for square in self.squareList:
			square.draw(self.surface)
		for piece in self.pieceListWhite:
			piece.draw(self.surface)
		for piece in self.pieceListBlack:
			piece.draw(self.surface)

	def getSquarebyPosition(self, position):
		for square in self.squareList:
			if position == square.position:
				return square
		return None

	def getSquarebyMousePosition(self, position):
		for square in self.squareList:
			if square.square.collidepoint(position):
				return square
		return None

	@staticmethod
	def isOccupied(pieceList, position):
		for piece in pieceList:
			if position == piece.position:
				return True
		return False

	@staticmethod
	def getPiecebyRank(pieceList, rank):
		for piece in pieceList:
			if piece.rank == rank:
				return piece
		return None

	@staticmethod
	def getPiecebyPosition(pieceList, position):
		for piece in pieceList:
			if piece.position == position:
				return piece
		return None

	def highlightMovableSquares(self, piece):
		self.highlightedSquares = []
		for space in piece.potentialSpaces:
			self.highlightedSquares.append(self.getSquarebyPosition(space))
		for square in self.highlightedSquares:
			color = YELLOW if (square.position[0] + square.position[1]) % 2 == 0 else YELLOW2
			square.color = color
			square.draw(self.surface)
			for piece in self.waitingPieceList:
				if square.position == piece.position:
					piece.draw(self.surface)
					break

	def unhighlightMovableSquares(self):
		for square in self.highlightedSquares:
			color = BROWN if (square.position[0] + square.position[1]) % 2 == 0 else BLACK
			square.color = color
			square.draw(self.surface)
			for piece in self.waitingPieceList:
				if square.position == piece.position:
					piece.draw(self.surface)
					break

	@staticmethod
	def getGameState(threateningPiece, currentPieceList, waitingPieceList):
		if Board.checked(threateningPiece, currentPieceList, waitingPieceList):
			pygame.mixer.music.load(checkSound)
			pygame.mixer.music.play()
		threateningPiece.updatePotentialSpaces(currentPieceList, waitingPieceList, False)
		waitingKingPosition = Board.getPiecebyRank(waitingPieceList, kingRank).position
		allOpponentSpaces = []
		for piece in waitingPieceList:
			piece.updatePotentialSpaces(waitingPieceList, currentPieceList, True)
			allOpponentSpaces += piece.potentialSpaces
		if len(allOpponentSpaces) == 0:
			if waitingKingPosition in threateningPiece.potentialSpaces:
				return CHECKMATE
			else:
				return STALEMATE
		return RUNNING

	@staticmethod
	def checked(threateningPiece, threateningPieceList, threatenedPieceList):
		threateningPiece.updatePotentialSpaces(threateningPieceList, threatenedPieceList, False)
		waitingKingPosition = Board.getPiecebyRank(threatenedPieceList, kingRank).position
		if waitingKingPosition in threateningPiece.potentialSpaces:
			return True
		return False

	def checkPawnPromotion(self, pawn, pawnPieceList):
		if pawn.rank != pawnRank: return
		if pawn.position[0] == 1 and pawn.color == player1Color or pawn.position[0] == 8 and pawn.color == player2Color:
			newPiece = None
			color = pawn.color
			newRank = launchPromotionMenu(self.surface, 600, 600, color)
			if newRank == PROMOTETOQUEEN:
				image = whiteQueenImage if color == player1Color else blackQueenImage
				newPiece = Queen(image, self.getSquarebyPosition(pawn.position), color)
			elif newRank == PROMOTETOROOK:
				image = whiteRookImage if color == player1Color else blackRookImage
				newPiece = Rook(image, self.getSquarebyPosition(pawn.position), color)
			elif newRank == PROMOTETOBISHOP:
				image = whiteBishopImage if color == player1Color else blackBishopImage
				newPiece = Bishop(image, self.getSquarebyPosition(pawn.position), color)
			elif newRank == PROMOTETOKNIGHT:
				image = whiteKnightImage if color == player1Color else blackKnightImage
				newPiece = Knight(image, self.getSquarebyPosition(pawn.position), color)
			pawnPieceList.remove(pawn)
			pawnPieceList.append(newPiece)
			self.selectedPiece = newPiece

	def checkEnPassant(self, pawn, pawnPieceList, opponentPieceList):
		potentialSpace = self.enPassantSpace
		if abs(pawn.position[0]-potentialSpace[0]) != 1 or abs(pawn.position[1]-potentialSpace[1]) != 1:
			return
		futureOpponentPieceList = opponentPieceList.copy()
		futureOpponentPieceList.remove(self.doubleUpPawn)
		if not pawn.leavesKingOpen(pawnPieceList, futureOpponentPieceList, potentialSpace):
			pawn.potentialSpaces.append(potentialSpace)

	def castle(self, king, rook, newKingPosition):
		oldRookSquare = self.getSquarebyPosition(rook.position)
		oldRookSquare.draw(self.surface)
		oldKingSquare = self.getSquarebyPosition(king.position)
		oldKingSquare.draw(self.surface)
		newKingSquare = self.getSquarebyPosition(newKingPosition)
		king.move(newKingSquare)
		if rook.position[1] > king.position[1]:
			newRookSquare = self.getSquarebyPosition((newKingPosition[0], newKingPosition[1]-1))
			rook.move(newRookSquare)
		else:
			newRookSquare = self.getSquarebyPosition((newKingPosition[0], newKingPosition[1]+1))
			rook.move(newRookSquare)
		self.unhighlightMovableSquares()
		king.draw(self.surface)
		rook.draw(self.surface)

	def reset(self):
		self.pieceListWhite = []
		self.pieceListBlack = []
		self.setInitialPositions()
		self.currentPieceList = self.pieceListWhite
		self.waitingPieceList = self.pieceListBlack
		self.selectedPiece = None

	def changeTurn(self):
		temp = self.currentPieceList
		self.currentPieceList = self.waitingPieceList
		self.waitingPieceList = temp
		self.selectedPiece = None

	def rotate(self):
		for piece in self.pieceListWhite:
			newSquare = self.getSquarebyPosition((9-piece.row, 9-piece.col))
			piece.setPosition(newSquare)
		for piece in self.pieceListBlack:
			newSquare = self.getSquarebyPosition((9-piece.row, 9-piece.col))
			piece.setPosition(newSquare)

	def playKillSound(self):
		randIndex = random.randrange(0, len(captureSounds))
		pygame.mixer.music.load(captureSounds[randIndex])
		pygame.mixer.music.play()

	def playPVP(self):
		while True:
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					endOption = launchEndMenu(screen, EXIT, self.currentPieceList[0].color,
					  self.waitingPieceList[0].color)
					if endOption == QUIT:
						pygame.quit()
						sys.exit()
					elif endOption == REMATCH:
						board.reset()
						board.draw()
						break
					elif endOption == MAINMENU:
						board.reset()
						return
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.doubleUpPawn and self.doubleUpPawn.color == self.currentPieceList[0].color:
						self.doubleUpPawn = None
						self.enPassantSpace = None
					clickpos = pygame.mouse.get_pos()
					clickedSquare = self.getSquarebyMousePosition(clickpos)
					if clickedSquare:
						clickedPosition = clickedSquare.position
						isMyPiece = False
						clickedPiece = Board.getPiecebyPosition(self.currentPieceList, clickedPosition)
						if clickedPiece: isMyPiece = True
						else:
							clickedPiece = Board.getPiecebyPosition(self.waitingPieceList, clickedPosition)
							isMyPiece = False
						if clickedPiece:
							if not self.selectedPiece:
								if isMyPiece:
									self.selectedPiece = clickedPiece
									selectedRank = self.selectedPiece.rank
									print("piece at ", clickedPiece.position, " selected!")
									clickedSquare.color = RED
									clickedSquare.draw(board.surface)
									clickedPiece.draw(board.surface)
									clickedSquare.color = BROWN if (clickedPosition[0]+clickedPosition[1])%2 == 0 else BLACK
									self.selectedPiece.updatePotentialSpaces(self.currentPieceList, self.waitingPieceList, True)
									if selectedRank == pawnRank and self.doubleUpPawn:
										if self.selectedPiece.color == player1Color:
											self.enPassantSpace = self.doubleUpPawn.position[0]-1, self.doubleUpPawn.position[1]
										else:
											self.enPassantSpace = self.doubleUpPawn.position[0]+1, self.doubleUpPawn.position[1]
										self.checkEnPassant(self.selectedPiece, self.currentPieceList, self.waitingPieceList)
									self.highlightMovableSquares(self.selectedPiece)
							elif self.selectedPiece == clickedPiece:
								self.selectedPiece = None
								print("piece at ", clickedPiece.position, " deselected!")
								clickedSquare.color = BROWN if (clickedPosition[0]+clickedPosition[1])%2 == 0 else BLACK
								clickedSquare.draw(board.surface)
								clickedPiece.draw(board.surface)
								self.unhighlightMovableSquares()
							else:
								if clickedPosition in self.selectedPiece.potentialSpaces:
									print("piece at ", self.selectedPiece.position, " kills piece at ", clickedPiece.position)
									self.playKillSound()
									self.waitingPieceList.remove(clickedPiece)
									oldSquare = board.getSquarebyPosition(self.selectedPiece.position)
									oldSquare.draw(board.surface)
									clickedSquare.draw(board.surface)
									self.unhighlightMovableSquares()
									self.selectedPiece.move(clickedSquare)
									self.checkPawnPromotion(self.selectedPiece, self.currentPieceList)
									self.selectedPiece.draw(board.surface)								
									#looking for checkmate!
									gameState = Board.getGameState(self.selectedPiece, self.currentPieceList, self.waitingPieceList)
									if gameState == CHECKMATE or gameState == STALEMATE:
										endOption = launchEndMenu(screen, gameState, self.currentPieceList[0].color, 
											self.waitingPieceList[0].color)
										if endOption == QUIT:
											pygame.quit()
											sys.exit()
										elif endOption == REMATCH:
											board.reset()
											board.draw()
											break
										elif endOption == MAINMENU:
											board.reset()
											return
									self.draw()									
									self.changeTurn()
								else:
									print(self.selectedPiece.potentialSpaces)
									print("piece at ", self.selectedPiece.position, " can't move there!")
						else:
							if self.selectedPiece:
								selectedRank = self.selectedPiece.rank
								#self.selectedPiece.updatePotentialSpaces(self.currentPieceList, self.waitingPieceList, True)
								#check to append possible enpassant capture move if selected piece is pawn and an enemypawn doubled up
								#last move
								if clickedPosition in self.selectedPiece.potentialSpaces:
									#if selected piece is a king and castling available and chosen
									if selectedRank == kingRank and clickedPosition in self.selectedPiece.castlingPositions:
										for rook in self.selectedPiece.rooksToCastle:
											if abs(rook.position[1]-clickedPosition[1]) <= 2: 
												self.castle(self.selectedPiece, rook, clickedPosition)
												break
									else:									
										if self.doubleUpPawn and clickedPosition == self.enPassantSpace:
											self.playKillSound()
											self.waitingPieceList.remove(self.doubleUpPawn)
											killedPawnSquare = self.getSquarebyPosition(self.doubleUpPawn.position)
											killedPawnSquare.draw(self.surface)
										oldSquare = board.getSquarebyPosition(self.selectedPiece.position)
										oldSquare.draw(board.surface)
										if selectedRank == pawnRank and abs(self.selectedPiece.row-clickedPosition[0]) == 2:
											self.doubleUpPawn = self.selectedPiece
										self.unhighlightMovableSquares()
										self.selectedPiece.move(clickedSquare)
										self.checkPawnPromotion(self.selectedPiece, self.currentPieceList)
										self.selectedPiece.draw(board.surface)
									#looking for checkmate!								
									gameState = Board.getGameState(self.selectedPiece, self.currentPieceList, self.waitingPieceList)
									if gameState == CHECKMATE or gameState == STALEMATE:
										endOption = launchEndMenu(screen, gameState, self.currentPieceList[0].color,
										  self.waitingPieceList[0].color)
										if endOption == QUIT:
											pygame.quit()
											sys.exit()
										elif endOption == REMATCH:
											board.reset()
											board.draw()
											break
										elif endOption == MAINMENU:
											board.reset()
											return
									self.draw()
									self.changeTurn()
								else:
									print(self.selectedPiece.potentialSpaces)
									print("piece at ", self.selectedPiece.position, " can't move there!")

"""
This class serves as the base class for all pieces (pawn, knight, etc.)
Each piece has the following attributes:
- sprite: the sprite used to draw the piece
- spriteGroup: the sprite group used to hold sprite
- position: the position of the square that the piece occupies
- color: color of the piece (either player1Color or player2Color)
- rank: rank of the piece (pawnRank, knightRank, etc.)
- potentialSpaces: a list of coordinate tuples of square positions
  that the square is able to legally move to
- hasMoved: becomes true once the piece has moved atleast once
"""
class Piece:
	sprite = None
	spriteGroup = None
	position = 0, 0
	row = 0
	col = 0
	color = ""
	rank = ""
	potentialSpaces = []
	hasMoved = False

	def __init__(self):
		pass

	"""
	Determines whether moving to a particular space (futurePosition)
	will leave the king of this piece open, thereby making that move
	illegal. myPieceList is the piece's pieceList and opponentPieceList
	is the opponent's. This function returns true if a move is illegal,
	and is used at the end of the updatePotentialSpaces method of all
	Piece derived classes to filter illegal moves.
	"""
	def leavesKingOpen(self, myPieceList, opponentPieceList, futurePosition):
		myKing = Board.getPiecebyRank(myPieceList, kingRank)
		originalKingPosition = myKing.position
		if Board.isOccupied(opponentPieceList, futurePosition):
			potentialKill = Board.getPiecebyPosition(opponentPieceList, futurePosition)
			#new opponent piece list if king kills piece
			futureOpponentPieceList = opponentPieceList.copy()
			futureOpponentPieceList.remove(potentialKill)
			#new my piece list for new king position
			currentPosition = self.position
			self.position = futurePosition
			self.row = futurePosition[0]
			self.col = futurePosition[1]
			for piece in futureOpponentPieceList:
				#if this king will be in opponent king's range
				if piece.rank == kingRank:
					if abs(myKing.position[0]-piece.position[0]) <= 1 and abs(myKing.position[1]-piece.position[1]) <= 1:
						myKing.position = originalKingPosition
						myKing.row = originalKingPosition[0]
						myKing.col = originalKingPosition[1]
						return True
				#all other pieces
				else:
					#save the current potential spaces of the opponent's piece
					currentPotentialSpaces = piece.potentialSpaces.copy()
					#generate potential spaces given the king kills the original piece
					piece.updatePotentialSpaces(futureOpponentPieceList, myPieceList, False)
					#store spaces
					if myKing.position in piece.potentialSpaces:
						self.position = currentPosition
						self.row = currentPosition[0]
						self.col = currentPosition[1]
						piece.potentialSpaces = currentPotentialSpaces
						return True
					#reassign original spaces
					piece.potentialSpaces = currentPotentialSpaces
			self.position = currentPosition
			self.row = currentPosition[0]
			self.col = currentPosition[1]
			return False
		else:
			currentPosition = self.position
			self.position = futurePosition
			self.row = futurePosition[0]
			self.col = futurePosition[1]
			for piece in opponentPieceList:
				#if this king will be in opponent king's range
				if piece.rank == kingRank:
					if abs(myKing.position[0]-piece.position[0]) <= 1 and abs(myKing.position[1]-piece.position[1]) <= 1:
						myKing.position = originalKingPosition
						myKing.row = originalKingPosition[0]
						myKing.col = originalKingPosition[1]
						return True
				#all other pieces
				else:
					#save the current potential spaces of the opponent's piece
					currentPotentialSpaces = piece.potentialSpaces.copy()
					#generate potential spaces given the king kills the original piece
					piece.updatePotentialSpaces(opponentPieceList, myPieceList, False)
					#store spaces
					if myKing.position in piece.potentialSpaces:
						self.position = currentPosition
						self.row = currentPosition[0]
						self.col = currentPosition[1]
						piece.potentialSpaces = currentPotentialSpaces
						return True
					#reassign original spaces
					piece.potentialSpaces = currentPotentialSpaces
			self.position = currentPosition
			self.row = currentPosition[0]
			self.col = currentPosition[1]
			return False

	""" Draws the piece's sprite """
	def draw(self, surface):
		self.spriteGroup.draw(surface)

	"""
	Moves a piece to the square passed to the newSquare argument.
	Will assign hasMoved attribute to True.
	"""
	def move(self, newSquare):
		self.position = newSquare.position
		self.row = self.position[0]
		self.col = self.position[1]
		self.sprite.rect.center = newSquare.square.center
		self.hasMoved = True

	"""
	Moves a piece to the square passed to the newSquare argument.
	Used exclusively in the board.rotate() method. Does not change
	the hasMoved attribute.
	"""
	def setPosition(self, newSquare):
		self.position = newSquare.position
		self.row = self.position[0]
		self.col = self.position[1]
		self.sprite.rect.center = newSquare.square.center

	"""
	Generates a new list of spaces that the piece can move to. Each
	Piece deriving class overrides this method, which is defined based
	on individual movesets. The piece's list of pieces and the piece list
	of the opponent must be passed as myPieceList and opponentPieceList,
	respectively. The checkMyKing is a boolean parameter that indicates
	whether or not to call the leavesKingOpen() method for each generated
	space. This is done when leavesKingOpen is True. checkMyKing is 
	supposed to be True only when updating the spaces of a piece that is 
	selected by a player and is intended to be moved. This function is 
	called in the leavesKingOpen() method for opponent pieces, where the 
	checkMyKing parameter is passed as False.
	"""
	def updatePotentialSpaces(self, myPieceList, opponentPieceList, checkMyKing):
		pass


"""
The following classes represent chess pieces and derive from the 
Piece class. No new attributes are declared for any of these classes,
with the exception of the King class which has two new attributes 
castlingPositions and rooksToCastle which both deal with castling.
Each class has a unique overriden updatePotentialSpaces() method
based on its moveset, which updates the potentialSpaces attribute.
"""
class Pawn(Piece):
	def __init__(self, image, initialSquare, color):
		Piece.__init__(self)
		self.image = image
		self.sprite = PieceSprite(image, initialSquare.square.center)
		self.spriteGroup = pygame.sprite.Group(self.sprite)
		self.position = initialSquare.position
		self.row = initialSquare.position[0]
		self.col = initialSquare.position[1]
		self.color = color
		self.rank = pawnRank
		self.initialPosition = self.position

	def updatePotentialSpaces(self, myPieceList, opponentPieceList, checkMyKing):
		self.potentialSpaces = []
		# Pawn can moveup or diagonal spaces if occupied by an opponent piece
		moveup = []
		moveDiagonals = []
		if self.color == player1Color:
			moveup.append((self.row-1, self.col))
			if not Board.isOccupied(myPieceList, moveup[0]) and not Board.isOccupied(opponentPieceList, moveup[0]):
				self.potentialSpaces.append(moveup[0])
			if not self.hasMoved:  # can move up 2 spaces if hasn't moved
				moveup.append((self.row-2,self.col))
				if not Board.isOccupied(myPieceList, moveup[1]) and not Board.isOccupied(opponentPieceList, moveup[1]):
					self.potentialSpaces.append(moveup[1])
			moveDiagonals = [(self.row-1, self.col+1), (self.row-1, self.col-1)]
		else:
			moveup.append((self.row+1, self.col))
			if not Board.isOccupied(myPieceList, moveup[0]) and not Board.isOccupied(opponentPieceList, moveup[0]):
				self.potentialSpaces.append(moveup[0])
			if not self.hasMoved:  # can move up 2 spaces if hasn't moved
				moveup.append((self.row+2,self.col))
				if not Board.isOccupied(myPieceList, moveup[1]) and not Board.isOccupied(opponentPieceList, moveup[1]):
					self.potentialSpaces.append(moveup[1])
			moveDiagonals = [(self.row+1, self.col+1), (self.row+1, self.col-1)]
		if Board.isOccupied(opponentPieceList, moveDiagonals[0]): self.potentialSpaces.append(moveDiagonals[0])
		if Board.isOccupied(opponentPieceList, moveDiagonals[1]): self.potentialSpaces.append(moveDiagonals[1])
		# if this piece is intended to be moved, check if moves leave king open
		if checkMyKing:
			for space in self.potentialSpaces.copy():
				if Piece.leavesKingOpen(self, myPieceList, opponentPieceList, space):
					self.potentialSpaces.remove(space)

class Rook(Piece):
	def __init__(self, image, initialSquare, color):
		Piece.__init__(self)
		self.image = image
		self.sprite = PieceSprite(image, initialSquare.square.center)
		self.spriteGroup = pygame.sprite.Group(self.sprite)
		self.position = initialSquare.position
		self.row = initialSquare.position[0]
		self.col = initialSquare.position[1]
		self.color = color
		self.rank = rookRank


	def updatePotentialSpaces(self, myPieceList, opponentPieceList, checkMyKing):
		self.potentialSpaces = []
		# all squares below
		for x in range(self.row+1, 9):
			pos = (x, self.col)
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		# all squares above
		for x in range(1, self.row):
			pos = (self.row-x, self.col)
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		# all squares left
		for x in range(1, self.col):
			pos = (self.row, self.col-x)
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		# all squares right
		for x in range(self.col+1, 9):
			pos = (self.row, x)
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		if checkMyKing:
			for space in self.potentialSpaces.copy():
				if Piece.leavesKingOpen(self, myPieceList, opponentPieceList, space):
					self.potentialSpaces.remove(space)

class Knight(Piece):
	def __init__(self, image, initialSquare, color):
		Piece.__init__(self)
		self.image = image
		self.sprite = PieceSprite(image, initialSquare.square.center)
		self.spriteGroup = pygame.sprite.Group(self.sprite)
		self.position = initialSquare.position
		self.row = initialSquare.position[0]
		self.col = initialSquare.position[1]
		self.color = color
		self.rank = knightRank

	def updatePotentialSpaces(self, myPieceList, opponentPieceList, checkMyKing):
		self.potentialSpaces = []
		movableSpaces = []
		movableSpaces.append((self.row+1, self.col+2))
		movableSpaces.append((self.row+1, self.col-2))
		movableSpaces.append((self.row-1, self.col+2))
		movableSpaces.append((self.row-1, self.col-2))
		movableSpaces.append((self.row+2, self.col+1))
		movableSpaces.append((self.row+2, self.col-1))
		movableSpaces.append((self.row-2, self.col+1))
		movableSpaces.append((self.row-2, self.col-1))
		for space in movableSpaces:
			if Board.isOccupied(myPieceList, space): pass
			elif Board.isOccupied(opponentPieceList, space): self.potentialSpaces.append(space)
			elif space[0]>0 and space[0]<9 and space[1]>0 and space[1]<9: self.potentialSpaces.append(space)
		if checkMyKing:
			for space in self.potentialSpaces.copy():
				if Piece.leavesKingOpen(self, myPieceList, opponentPieceList, space):
					self.potentialSpaces.remove(space)

class Bishop(Piece):
	def __init__(self, image, initialSquare, color):
		Piece.__init__(self)
		self.image = image
		self.sprite = PieceSprite(image, initialSquare.square.center)
		self.spriteGroup = pygame.sprite.Group(self.sprite)
		self.position = initialSquare.position
		self.row = initialSquare.position[0]
		self.col = initialSquare.position[1]
		self.color = color
		self.rank = bishopRank

	def updatePotentialSpaces(self, myPieceList, opponentPieceList, checkMyKing):
		self.potentialSpaces = []
		# up right diagonal
		bound = min(self.row-1, 8-self.col)
		for x in range(0, bound):
			pos = (self.row-(x+1), self.col+x+1)
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		# up left diagonal
		bound = min(self.row-1, self.col-1)
		for x in range(0, bound):
			pos = (self.row-(x+1), self.col-(x+1))
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		# down right diagonal
		bound = min(8-self.row, 8-self.col)
		for x in range(0, bound):
			pos = (self.row+x+1, self.col+x+1)
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		# down left diagonal
		bound = min(8-self.row, self.col-1)
		for x in range(0, bound):
			pos = (self.row+x+1, self.col-(x+1))
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		if checkMyKing:
			for space in self.potentialSpaces.copy():
				if Piece.leavesKingOpen(self, myPieceList, opponentPieceList, space):
					self.potentialSpaces.remove(space)

class Queen(Piece):
	def __init__(self, image, initialSquare, color):
		Piece.__init__(self)
		self.image = image
		self.sprite = PieceSprite(image, initialSquare.square.center)
		self.spriteGroup = pygame.sprite.Group(self.sprite)
		self.position = initialSquare.position
		self.row = initialSquare.position[0]
		self.col = initialSquare.position[1]
		self.color = color
		self.rank = queenRank

	def updatePotentialSpaces(self, myPieceList, opponentPieceList, checkMyKing):
		self.potentialSpaces = []
		# all squares below
		for x in range(self.row+1, 9):
			pos = (x, self.col)
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		# all squares above
		for x in range(1, self.row):
			pos = (self.row-x, self.col)
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		# all squares left
		for x in range(1, self.col):
			pos = (self.row, self.col-x)
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		# all squares right
		for x in range(self.col+1, 9):
			pos = (self.row, x)
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		# up right diagonal
		bound = min(self.row-1, 8-self.col)
		for x in range(0, bound):
			pos = (self.row-(x+1), self.col+x+1)
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		# up left diagonal
		bound = min(self.row-1, self.col-1)
		for x in range(0, bound):
			pos = (self.row-(x+1), self.col-(x+1))
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		# down right diagonal
		bound = min(8-self.row, 8-self.col)
		for x in range(0, bound):
			pos = (self.row+x+1, self.col+x+1)
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		# down left diagonal
		bound = min(8-self.row, self.col-1)
		for x in range(0, bound):
			pos = (self.row+x+1, self.col-(x+1))
			if Board.isOccupied(myPieceList, pos): break
			if Board.isOccupied(opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		if checkMyKing:
			for space in self.potentialSpaces.copy():
				if Piece.leavesKingOpen(self, myPieceList, opponentPieceList, space):
					self.potentialSpaces.remove(space)

class King(Piece):
	# New attributes, used for castling
	castlingPositions = []
	rooksToCastle = []
	def __init__(self, image, initialSquare, color):
		Piece.__init__(self)
		self.image = image
		self.sprite = PieceSprite(image, initialSquare.square.center)
		self.spriteGroup = pygame.sprite.Group(self.sprite)
		self.position = initialSquare.position
		self.row = initialSquare.position[0]
		self.col = initialSquare.position[1]
		self.color = color
		self.rank = kingRank

	def updatePotentialSpaces(self, myPieceList, opponentPieceList, checkMyKing):
		self.potentialSpaces = []
		self.castlingPositions = []
		movableSpaces = []
		movableSpaces.append((self.row+1, self.col))
		movableSpaces.append((self.row+1, self.col+1))
		movableSpaces.append((self.row+1, self.col-1))
		movableSpaces.append((self.row, self.col+1))
		movableSpaces.append((self.row, self.col-1))
		movableSpaces.append((self.row-1, self.col))
		movableSpaces.append((self.row-1, self.col+1))
		movableSpaces.append((self.row-1, self.col-1))
		for space in movableSpaces:
			if space[0] >= 1 and space[0] <= 8 and space[1] >= 1 and space[1] <= 8:
				if Board.isOccupied(myPieceList, space): 
					pass
				else:
					if not Piece.leavesKingOpen(self, myPieceList, opponentPieceList, space):
						self.potentialSpaces.append(space)
		# not CheckMyKing to prevent recursion between kings 
		# when checking castling
		if not checkMyKing: return
		if not self.canCastle(myPieceList, opponentPieceList): 
			self.castlingPositions = []
			self.rooksToCastle = []
		
	"""
	Checks if the king can castle. Appends possible castling positions
	and corresponding rooks to self.castlingPositions and 
	self.rooksToCastle. Returns true if anything was appended to the 
	mentioned lists (there are castling positions available).
	"""
	def canCastle(self, myPieceList, opponentPieceList):
		if self.hasMoved: return False
		for piece in opponentPieceList:
			if Board.checked(piece, opponentPieceList, myPieceList): return False
		myRookList = []
		for piece in myPieceList:
			if piece.rank == rookRank and not piece.hasMoved: myRookList.append(piece)
		originalPosition = self.position
		for rook in myRookList.copy():
			if rook.position[1] > self.position[1]:
				for i in range(rook.position[1] - originalPosition[1] - 1):
					checkPosition = originalPosition[0], originalPosition[1]+i+1
					if Board.isOccupied(myPieceList, checkPosition) or Board.isOccupied(opponentPieceList, checkPosition): 
						myRookList.remove(rook)
						break
					if Piece.leavesKingOpen(self, myPieceList, opponentPieceList, checkPosition): 
						myRookList.remove(rook)
						break
				if rook in myRookList: 
					self.castlingPositions.append((originalPosition[0], originalPosition[1]+2))
					self.potentialSpaces.append((originalPosition[0], originalPosition[1]+2))
			else:
				for i in range(originalPosition[1] - rook.position[1] - 1):
					checkPosition = originalPosition[0], originalPosition[1]-(i+1)
					if Board.isOccupied(myPieceList, checkPosition) or Board.isOccupied(opponentPieceList, checkPosition): 
						myRookList.remove(rook)
						break
					if Piece.leavesKingOpen(self, myPieceList, opponentPieceList, checkPosition): 
						myRookList.remove(rook)
						break
				if rook in myRookList: 
					self.castlingPositions.append((originalPosition[0], originalPosition[1]-2))
					self.potentialSpaces.append((originalPosition[0], originalPosition[1]-2))
		if len(myRookList) == 0: return False
		self.rooksToCastle = myRookList
		return True


"""
End of Piece classes.
"""

"""
Simple Sprite class deriving the abstract base class 
pygame.sprite.Sprite used for the sprite attribute of
Piece classes. A center argument is passed to the constructor 
to assign an initial location to the sprite.
"""
class PieceSprite(pygame.sprite.Sprite):
	def __init__(self, image, center):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = center

pygame.init()

screenWidth = 600
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_icon(whiteKnightImage)
pygame.display.set_caption(screenCaption)
screen.fill(GREY)
boardLength = screenHeight
boardpos = (screenWidth-screenHeight)/2, 0
board = Board(screen, (boardpos), boardLength)
while True:
	selectedOption = launchStartMenu(screen, screenWidth, screenHeight)
	if selectedOption == PLAYERVSPLAYER:
		board.draw()
		board.playPVP()