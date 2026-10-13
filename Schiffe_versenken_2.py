# Schiffe versenken version 2 (Computer gegen Spieler)

import random
import math

WIDTH = 9
HEIGHT = 9
NUM_TILES_1 = 4 #Schiffslänge
NUM_TILES_2 = 3
PLAYER1 = 'Computer'
PLAYER2 = 'Player'

def drawBoard(board_i, player_i):
    print ('Board: ' + player_i)
    print ('  123456789')
    for y in range(HEIGHT):
        print ('%s|' % (y+1), end = '')
        for x in range(WIDTH):
            print(board_i[x][y], end = '')
        print ('|%s' % (y+1))
    print ('  123456789')
    print()

def getNewBoard():
    board = []
    for i in range(WIDTH):
        board.append(['~'] *9)
    return board

def getNewBoardPlayer():
    board = []
    for i in range(WIDTH):
        board.append([' '] *9)
    return board

def getShip(numberTiles): #Computer wählt seine Schiffe aus
    newShip = []
    if random.randint(0,1) == 0:   #horizontal
        a = random.randint(0, WIDTH - numberTiles)
        b = random.randint (0, HEIGHT - 1)
        for i in range(numberTiles):
            newShip.append((a + i, b))
    else:   #vertikal
        a = random.randint(0, WIDTH - 1)
        b = random.randint(0, HEIGHT - numberTiles)
        for i in range(numberTiles):
            newShip.append((a, b + i))
    return newShip

def chooseShip():   #Spieler wählt seine Schiffe aus
    newShip1 = []
    print ('''Please place one ship of 4 tiles on your board.
The ship can be placed vertically or horizontally.
Type the coordinates as x,y x,y x,y x,y (whith one space in between each pair).''')
    playerInput = input()
    coordinates = playerInput.split()
    for coordinate in coordinates:
        x,y = coordinate.split(',')
        newShip1.append((int(x)-1, int(y)-1))  
        
    newShip2 = []
    print()
    print('''Please now place one ship of 3 tiles on your board.
The ship can be placed vertically or horizontally.
Type the coordinates as x,y x,y x,y (with one space in between each pair).
Make sure that the ships do NOT collide.''')
    playerInput = input()
    print()
    coordinates = playerInput.split()
    for coordinate in coordinates:
        x,y = coordinate.split(',')
        newShip2.append((int(x)-1, int(y)-1))

    return newShip1,newShip2

def showPlayerShips(board_i, s1, s2):
    for (x,y) in s1: 
        board_i[x][y] = 'S'
    for (x,y) in s2: 
        board_i[x][y] = 'S'
  

def shipsCollide(s1, s2):
    for (x,y) in s2:
        if (x,y) in s1:
            return True
    else: False

def isOnBoard(x, y):
    return x >= 0 and x <= WIDTH-1 and y >= 0 and y <= HEIGHT-1    

def getPlayerMove(board_i):
    while True:
        print ('Throw a bomb on a field of your choice on the computer\'s board (type coordinates xy).')
        DIGITS = '1 2 3 4 5 6 7 8 9'.split()
        move = input()
        if move[0] in DIGITS and move[1] in DIGITS:
         x = int(move[0])-1
         y = int(move[1])-1
        else:
            print ('Your move is not valid. Please choose again.')
            continue            
        if board_i[x][y] != '~':
            print ('You have made this move already / Your move is out of range. Please choose again.')
            continue
        elif isOnBoard(x, y) == False or len(move) != 2:
            print ('Your move is not valid. Please choose again.')
            continue
        else: return (x,y)        

def makeMove(s1,s2):
    x,y = getPlayerMove(board)
    if (x,y) in s1 or (x,y) in s2: 
        board[x][y] = 'X'
        print()
        print ('You hit a ship!!!')
        print()
        if (x, y) in s1:
            s1.remove((x, y))
        elif (x, y) in s2:
            s2.remove((x, y))
    else:
        board[x][y] = 'O'
        print()
        print ('You have not hit anything. Can you hit a ship with your next move?')
        print()

def isShipDown(s1, s2, s1_sunken, s2_sunken):
    if s1 == [] and s2 == []:
        drawBoard(board,PLAYER1)
        print('You have won! All ships are sunken!')
        print()
        return True, s1_sunken, s2_sunken

    if s1 == [] and not s1_sunken:
        print('Great, you have sunken a ship with %s tiles!' % (NUM_TILES_1))
        print()
        s1_sunken = True  

    if s2 == [] and not s2_sunken:
        print('Great, you have sunken a ship with %s tiles!' % (NUM_TILES_2))
        print()
        s2_sunken = True  

    return False, s1_sunken, s2_sunken

def whoGoesFirst():
    if random.randint(0,1) == 0:
        return 'computer'
    else: return 'player'

def compChooseMove():   #Computer-Algorithmus
    while True:
        possibleMoves = []
        
        if (len(shipP1) == 4 and len(shipP2) == 3 or    #keine offene Attacke, zufälliges Feld wählen.
        len(shipP1) == 4 and shipP2_sunken or
        shipP1_sunken and len(shipP2) == 3):
            while True:
                x = random.randint(0, WIDTH-1)
                y = random.randint(0, HEIGHT-1)

                if boardP[x][y] == ' ' or boardP[x][y] == 'S':
                    return (x,y)
                else: continue #neues Feld wählen

        elif len(shipP1) != 4 and not shipP1_sunken:  #offene Attacke auf Schiff 1
            if len(shipP1) == 3:    #bisher wurde 1 Feld getroffen
                x,y = guessedFields1[0]
                possibleMoves = [(x,y+1),(x,y-1),(x+1,y),(x-1,y)]
                while True:
                    move = random.choice(possibleMoves)
                    if move not in emptyFields and move not in guessedFields1 and move not in guessedFields2:
                        return move
                    else: continue
                
            elif len(shipP1) == 2:  #bisher wurden 2 Felder getroffen
                x1,y1 = guessedFields1[0]
                x2,y2 = guessedFields1[1]
                if x1 == x2:    #vertikal 
                    possibleMoves.append((x1,y1-1))
                    possibleMoves.append((x2,y2+1))
                    while True:
                        move = random.choice(possibleMoves)
                        if move not in emptyFields and move not in guessedFields1 and move not in guessedFields2:
                            return move
                        else: continue
                
                elif y1 == y2:    #horizontal
                    possibleMoves.append((x1-1,y1))
                    possibleMoves.append((x2+1,y2))
                    while True:
                        move = random.choice(possibleMoves)
                        if move not in emptyFields and move not in guessedFields1 and move not in guessedFields2:
                            return move
                        else: continue

            elif len(shipP1) == 1:  #bisher wurden 3 Felder getroffen
                x1,y1 = guessedFields1[0]
                x2,y2 = guessedFields1[1]
                x3,y3 = guessedFields1[2]
                if x1 == x2:    #vertikal
                    possibleMoves.append((x1,y1-1))
                    possibleMoves.append((x3,y3+1))
                    while True:
                        move = random.choice(possibleMoves)
                        if move not in emptyFields and move not in guessedFields1 and move not in guessedFields2:
                            return move
                        else: continue
                if y1 == y2:    #horizontal
                    possibleMoves.append((x1-1,y1))
                    possibleMoves.append((x3+1,y3))
                    while True:
                        move = random.choice(possibleMoves)
                        if move not in emptyFields and move not in guessedFields1 and move not in guessedFields2:
                            return move
                        else: continue        

        elif len(shipP2) != 3 and not shipP2_sunken:    #offene Attacke auf Schiff 2
            if len(shipP2) == 2:    #bisher wurde 1 Feld getroffen
                x,y = guessedFields2[0]
                possibleMoves = [(x,y+1),(x,y-1),(x+1,y),(x-1,y)]
                while True:
                    move = random.choice(possibleMoves)
                    if move not in emptyFields and move not in guessedFields1 and move not in guessedFields2:
                        return move
                    else: continue
                
            elif len(shipP2) == 1:  #bisher wurden 2 Felder getroffen
                x1,y1 = guessedFields2[0]
                x2,y2 = guessedFields2[1]
                if x1 == x2:    #vertikal hoch
                    possibleMoves.append((x1,y1-1))
                    possibleMoves.append((x2,y2+1))
                    while True:
                        move = random.choice(possibleMoves)
                        if move not in emptyFields and move not in guessedFields1 and move not in guessedFields2:
                            return move
                        else: continue
                
                elif y1 == y2:    #horizontal rechts
                    possibleMoves.append((x1-1,y1))
                    possibleMoves.append((x2+1,y2))
                    while True:
                        move = random.choice(possibleMoves)
                        if move not in emptyFields and move not in guessedFields1 and move not in guessedFields2:
                            return move
                        else: continue
            
def makeCompMove(board,s1,s2):
    (x,y) = compChooseMove()
    if (x,y) in s1 or (x,y) in s2: 
        board[x][y] = 'X'
        print()
        print ('The computer has hit a ship!')
        print()
        if (x, y) in s1:
            s1.remove((x, y))
            guessedFields1.append((x,y))
            guessedFields1.sort()
        elif (x, y) in s2:
            s2.remove((x, y))
            guessedFields2.append((x,y))
            guessedFields2.sort()
    
    else:
        board[x][y] = 'O'
        print()
        print ('The computer has not hit anything.')
        print()
        emptyFields.append((x,y))

def isShipDownComp(s1, s2, s1_sunken, s2_sunken):
    if s1 == [] and s2 == []:
        drawBoard(boardP,PLAYER2)
        print('The Computer has won! All ships are sunken! You lose ...')
        print()
        return True, s1_sunken, s2_sunken

    if s1 == [] and not s1_sunken:
        print('The computer has sunken a ship with %s tiles!' % (NUM_TILES_1))
        print()
        s1_sunken = True  

    if s2 == [] and not s2_sunken:
        print('The computer has sunken a ship with %s tiles!' % (NUM_TILES_2))
        print()
        s2_sunken = True  

    return False, s1_sunken, s2_sunken
    


#MAIN GAME

print ('Welcome to Sinking Ships!') #Im Text Rateversuche/Schiffslänge anpassen.
print()
print ('''You and the Computer will each place two ships on your boards(one of 4 tiles and one of 3 tiles).
The ships can be placed vertically or horizontally.
Your move will be marked with 'X' when you hit a ship.
Your move will be marked with 'O' when you did not hit anything.
Who can sink the other's ships first?
Press Enter to start.''')
print()
input()

while True:
    ship1 = []
    ship2 = []
    ship1_sunken = False
    ship2_sunken = False
    board = getNewBoard()

    shipP1_sunken = False
    shipP2_sunken = False
    boardP = getNewBoardPlayer()
    emptyFields = []
    guessedFields1 = []
    guessedFields2 = []

    turn = whoGoesFirst()

    #Computer wählt seine Schiffe aus
    ship1 = getShip(NUM_TILES_1)
    while True:
        ship2 = getShip(NUM_TILES_2)
        if shipsCollide(ship1,ship2) == True:
            continue
        else: break

    #Spieler wählt seine Schiffe aus
    drawBoard(board,PLAYER1)
    drawBoard(boardP,PLAYER2)    
    shipP1,shipP2 = chooseShip()
    showPlayerShips(boardP,shipP1,shipP2)

    while True:
        if turn == 'player':
            drawBoard(board,PLAYER1)
            drawBoard(boardP,PLAYER2)
            makeMove(ship1,ship2)
            game_over, ship1_sunken, ship2_sunken = isShipDown(ship1, ship2, ship1_sunken, ship2_sunken)
            if game_over == True:
                break
            else: turn = 'computer'

        else:
            makeCompMove(boardP,shipP1,shipP2)
            game_over, shipP1_sunken, shipP2_sunken = isShipDownComp(shipP1, shipP2, shipP1_sunken, shipP2_sunken)
            if game_over == True:
                break
            else: turn = 'player'

    print ('Do you want to play again? (yes or no)')
    if not input().lower().startswith('y'):
        break
