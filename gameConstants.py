import sys, pygame, os
pygame.font.init()

WHITE = 255, 255, 255
BLACK = 128, 70, 27
BROWN = 185, 156, 107
GREY = 105, 105, 105
YELLOW = 255, 255, 0
YELLOW2 = 255, 255, 102
GREEN = 0, 255, 0
RED = 255, 0, 0
player1Color = "White"
player2Color = "Black"
screenCaption = "Chess"
whitePawnImage = pygame.image.load(os.path.join('chessSprites','WhitePawn.png'))
whiteRookImage = pygame.image.load(os.path.join('chessSprites','WhiteRook.png'))
whiteKnightImage = pygame.image.load(os.path.join('chessSprites','WhiteKnight.png'))
whiteBishopImage = pygame.image.load(os.path.join('chessSprites','WhiteBishop.png'))
whiteQueenImage = pygame.image.load(os.path.join('chessSprites','WhiteQueen.png'))
whiteKingImage = pygame.image.load(os.path.join('chessSprites','WhiteKing.png'))
blackPawnImage = pygame.image.load(os.path.join('chessSprites','BlackPawn.png'))
blackRookImage = pygame.image.load(os.path.join('chessSprites','BlackRook.png'))
blackKnightImage = pygame.image.load(os.path.join('chessSprites','BlackKnight.png'))
blackBishopImage = pygame.image.load(os.path.join('chessSprites','BlackBishop.png'))
blackQueenImage = pygame.image.load(os.path.join('chessSprites','BlackQueen.png'))
blackKingImage = pygame.image.load(os.path.join('chessSprites','BlackKing.png'))
pawnRank = "Pawn"
rookRank = "Rook"
knightRank = "Knight"
bishopRank = "Bishop"
queenRank = "Queen"
kingRank = "King"
titleText = 'CHESS'
option1Text = 'Player vs. Player'
option2Text = 'Player vs. Computer (Coming Soon)'
option3Text = 'Computer vs. Computer (Coming Soon)'
option4Text = 'Rematch'
option5Text = 'Main Menu'
option6Text = 'Exit'

PLAYERVSPLAYER = 1
PLAYERVSCOMP = 2
COMPVSCOMP = 3
REMATCH = 4
MAINMENU = 5
QUIT = 6
PROMOTETOROOK = 7
PROMOTETOKNIGHT = 8
PROMOTETOBISHOP = 9
PROMOTETOQUEEN = 10
RUNNING = 11
CHECKMATE = 12
STALEMATE = 13
EXIT = 14

titleFont = 'Impact'
titleSize = 100
endTitleSize = 50
titlePosition = 300, 100
title = pygame.font.SysFont(titleFont, titleSize, True)
titleDisplay = title.render(titleText, 1, GREEN)

itemFont = 'Impact'
itemSize = 40
option1Position = (300, 250)
option = pygame.font.SysFont(itemFont, itemSize)
option1Display = option.render(option1Text, 1, WHITE)

option2Position = (300, 350)
option2Display = option.render(option2Text, 1, WHITE)

option3Position = (300, 450)
option3Display = option.render(option3Text, 1, WHITE)

endTitle = pygame.font.SysFont(titleFont, endTitleSize, True)

option4Position = (300, 250)
option4Display = option.render(option4Text, 1, WHITE)

option5Position = (300, 350)
option5Display = option.render(option5Text, 1, WHITE)

option6Position = (300, 450)
option6Display = option.render(option6Text, 1, WHITE)

startMusic = os.path.join('gameSounds', 'Main_Theme01.mp3')
endMusic = os.path.join('gameSounds', 'Lost_Game01.mp3')
CaptureSound1 = os.path.join('gameSounds', 'Male_Death01.wav')
CaptureSound2 = os.path.join('gameSounds', 'Male_Death02.wav')
CaptureSound3 = os.path.join('gameSounds', 'Male_Death03.wav')
CaptureSound4 = os.path.join('gameSounds', 'Male_Death04.wav')
CaptureSound5 = os.path.join('gameSounds', 'Male_Death05.wav')
CaptureSound6 = os.path.join('gameSounds', 'Male_Death06.wav')
captureSounds = [CaptureSound1, CaptureSound2, CaptureSound3, CaptureSound4, CaptureSound5, CaptureSound6]
checkSound = os.path.join('gameSounds', 'Check.mp3')