class Piece:
	sprite = None
	position = 0, 0
	row = 0
	col = 0
	color = ""
	rank = ""
	potentialSpaces = []

	def __init__(self):
		pass

	def isOccupied(self, pieceList, position):
		for piece in pieceList:
			if position == piece.position:
				return True
		return False

	def updatePotentialSpaces(self, myPieceList, opponentPieceList):
		pass

#derived piece classes
class Pawn(Piece):
	def __init__(self, row, col, color):
		Piece.__init__(self)
		self.position = (row, col)
		self.row = row
		self.col = col
		self.color = color
		self.rank = "Pawn"

	def updatePotentialSpaces(self, myPieceList, opponentPieceList):
		self.potentialSpaces = []
		moveup = (self.row-1, self.col)
		moveDiagonals = [(self.row-1, self.col+1), (self.row-1, self.col-1)]
		canMoveup = True
		for piece in myPieceList:
			if moveup == piece.position:
				canMoveup = False
				break
		if canMoveup:
			self.potentialSpaces.append(moveup)
		for piece in opponentPieceList:
			if moveDiagonals[0] == piece.position:
				self.potentialSpaces.append(moveDiagonals[0])
			if moveDiagonals[1] == piece.position:
				self.potentialSpaces.append(moveDiagonals[1])

class Rook(Piece):
	def __init__(self, row, col, color):
		Piece.__init__(self)
		self.position = (row, col)
		self.row = row
		self.col = col
		self.color = color
		self.rank = "Rook"

	def updatePotentialSpaces(self, myPieceList, opponentPieceList):
		self.potentialSpaces = []
		#all squares below, shorten code using position checking function in Player class
		for x in range(self.row+1, 9):
			exit = False
			pos = (x, self.col)
			for piece in myPieceList:
				if pos == piece.position:
					exit = True
					break
			for piece in opponentPieceList:
				if pos == piece.position:
					self.potentialSpaces.append(pos)
					exit = True
					break
			if exit:
				break
			self.potentialSpaces.append(pos)
		#all squares above
		for x in range(1, self.row):
			exit = False
			pos = (self.row-x, self.col)
			for piece in myPieceList:
				if pos == piece.position:
					exit = True
					break
			for piece in opponentPieceList:
				if pos == piece.position:
					self.potentialSpaces.append(pos)
					exit = True
					break
			if exit:
				break
			self.potentialSpaces.append(pos)
		#all squares left
		for x in range(1, self.col):
			exit = False
			pos = (self.row, self.col-x)
			for piece in myPieceList:
				if pos == piece.position:
					exit = True
					break
			for piece in opponentPieceList:
				if pos == piece.position:
					self.potentialSpaces.append(pos)
					exit = True
					break
			if exit:
				break
			self.potentialSpaces.append(pos)
		#all squares right
		for x in range(self.col+1, 9):
			exit = False
			pos = (self.row, x)
			for piece in myPieceList:
				if pos == piece.position:
					exit = True
					break
			for piece in opponentPieceList:
				if pos == piece.position:
					self.potentialSpaces.append(pos)
					exit = True
					break
			if exit:
				break
			self.potentialSpaces.append(pos)

class Knight(Piece):
	def __init__(self, row, col, color):
		Piece.__init__(self)
		self.position = (row, col)
		self.row = row
		self.col = col
		self.color = color
		self.rank = "Knight"

	def updatePotentialSpaces(self, myPieceList, opponentPieceList):
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
			add = True
			for piece in myPieceList:
				if space == piece.position:
					add = False
					break
			for piece in opponentPieceList:
				if space == piece.position:
					break
			if add:
				self.potentialSpaces.append(space)

class Bishop(Piece):
	def __init__(self, row, col, color):
		Piece.__init__(self)
		self.position = (row, col)
		self.row = row
		self.col = col
		self.color = color
		self.rank = "Bishop"

	def updatePotentialSpaces(self, myPieceList, opponentPieceList):
		self.potentialSpaces = []
		#up right diagonal
		bound = min(self.row-1, 8-self.col)
		for x in range(0, bound):
			pos = (self.row-(x+1), self.col+x+1)
			if Piece.isOccupied(self, myPieceList, pos): break
			if Piece.isOccupied(self, opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		#up left diagonal
		bound = min(self.row-1, self.col-1)
		for x in range(0, bound):
			pos = (self.row-(x+1), self.col-(x+1))
			if Piece.isOccupied(self, myPieceList, pos): break
			if Piece.isOccupied(self, opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		#down right diagonal
		bound = min(8-self.row, 8-self.col)
		for x in range(0, bound):
			pos = (self.row+x+1, self.col+x+1)
			if Piece.isOccupied(self, myPieceList, pos): break
			if Piece.isOccupied(self, opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		#down left diagonal
		bound = min(8-self.row, self.col-1)
		for x in range(0, bound):
			pos = (self.row+x+1, self.col-(x+1))
			if Piece.isOccupied(self, myPieceList, pos): break
			if Piece.isOccupied(self, opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)

class Queen(Piece):
	def __init__(self, row, col, color):
		Piece.__init__(self)
		self.position = (row, col)
		self.row = row
		self.col = col
		self.color = color
		self.rank = "Queen"

	def updatePotentialSpaces(self, myPieceList, opponentPieceList):
		self.potentialSpaces = []
		#all squares below
		for x in range(self.row+1, 9):
			pos = (x, self.col)
			if Piece.isOccupied(self, myPieceList, pos): break
			if Piece.isOccupied(self, opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		#all squares above
		for x in range(1, self.row):
			pos = (self.row-x, self.col)
			if Piece.isOccupied(self, myPieceList, pos): break
			if Piece.isOccupied(self, opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		#all squares left
		for x in range(1, self.col):
			pos = (self.row, self.col-x)
			if Piece.isOccupied(self, myPieceList, pos): break
			if Piece.isOccupied(self, opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		#all squares right
		for x in range(self.col+1, 9):
			pos = (self.row, x)
			if Piece.isOccupied(self, myPieceList, pos): break
			if Piece.isOccupied(self, opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		#up right diagonal
		bound = min(self.row-1, 8-self.col)
		for x in range(0, bound):
			pos = (self.row-(x+1), self.col+x+1)
			if Piece.isOccupied(self, myPieceList, pos): break
			if Piece.isOccupied(self, opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		#up left diagonal
		bound = min(self.row-1, self.col-1)
		for x in range(0, bound):
			pos = (self.row-(x+1), self.col-(x+1))
			if Piece.isOccupied(self, myPieceList, pos): break
			if Piece.isOccupied(self, opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		#down right diagonal
		bound = min(8-self.row, 8-self.col)
		for x in range(0, bound):
			pos = (self.row+x+1, self.col+x+1)
			if Piece.isOccupied(self, myPieceList, pos): break
			if Piece.isOccupied(self, opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)
		#down left diagonal
		bound = min(8-self.row, self.col-1)
		for x in range(0, bound):
			pos = (self.row+x+1, self.col-(x+1))
			if Piece.isOccupied(self, myPieceList, pos): break
			if Piece.isOccupied(self, opponentPieceList, pos):
				self.potentialSpaces.append(pos)
				break
			self.potentialSpaces.append(pos)

class King(Piece):
	def __init__(self, row, col, color):
		Piece.__init__(self)
		self.position = (row, col)
		self.row = row
		self.col = col
		self.color = color
		self.rank = "King"

	def updatePotentialSpaces(self, myPieceList, opponentPieceList):
		self.potentialSpaces = []
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
			if Piece.isOccupied(self, myPieceList, space): pass
			#if king can kill a particular piece, must check if threathened in new space...
			elif Piece.isOccupied(self, opponentPieceList, space):
				potentialKill = None
				for piece in opponentPieceList:
					if space == piece.position:
						potentialKill = piece
						break
				#new opponent piece list if king kills piece
				futureOpponentPieceList = opponentPieceList.copy()
				futureOpponentPieceList.remove(potentialKill)
				#new my piece list for new king position
				futureMyPieceList = myPieceList.copy()
				futureMyPieceList.remove(self)
				futureKing = King(space[0], space[1], self.color)
				futureMyPieceList.append(futureKing)
				futureOpponentSpaces = []
				for piece in futureOpponentPieceList:
					#save the current potential spaces of the opponent's piece
					currentPotentialSpaces = piece.potentialSpaces.copy()
					#generate potential spaces given the king kills the original piece
					piece.updatePotentialSpaces(futureOpponentPieceList, futureMyPieceList)
					#store spaces
					futureOpponentSpaces += piece.potentialSpaces
					#reassign original spaces
					piece.potentialSpaces = currentPotentialSpaces
				if space not in futureOpponentSpaces:
					self.potentialSpaces.append(space)
			#check if king is threatened in potential empty spaces
			elif space[0]>0 and space[0]<9 and space[1]>0 and space[1]<9: 
				futureMyPieceList = myPieceList.copy()
				futureMyPieceList.remove(self)
				futureKing = King(space[0], space[1], self.color)
				futureMyPieceList.append(futureKing)
				futureOpponentSpaces = []
				for piece in opponentPieceList:
					#save the current potential spaces of the opponent's piece
					currentPotentialSpaces = piece.potentialSpaces.copy()
					#generate potential spaces given the king kills the original piece
					piece.updatePotentialSpaces(opponentPieceList, futureMyPieceList)
					#store spaces
					futureOpponentSpaces += piece.potentialSpaces
					#reassign original spaces
					piece.potentialSpaces = currentPotentialSpaces
				if space not in futureOpponentSpaces:
					self.potentialSpaces.append(space)


color1 = "White"
color2 = "Black"

myPieceList = [Queen(5, 3, color1), King(2, 6, color1), Rook(6, 6, color1)]
opponentPieceList = [Bishop(3, 5, color2), Pawn(4, 4, color2), Knight(7, 4, color2), Rook(8, 5, color2), Bishop(3, 8, color2)]

for x in range(len(opponentPieceList)):
	opponentPieceList[x].updatePotentialSpaces(opponentPieceList, myPieceList)

for x in range(len(myPieceList)):
	myPieceList[x].updatePotentialSpaces(myPieceList, opponentPieceList)

for x in range(len(myPieceList)):
	myPieceList[x].updatePotentialSpaces(myPieceList, opponentPieceList)

for x in range(len(myPieceList)):
	print(myPieceList[x].color, myPieceList[x].rank, myPieceList[x].potentialSpaces)

for x in range(len(opponentPieceList)):
	print(opponentPieceList[x].color, opponentPieceList[x].rank, opponentPieceList[x].potentialSpaces)