'''
Name: Ryan Brooks, Charlie Chen
ID: 1530605
Course: CKPUT 274 fall 2018
assignment: Final Project: Minesweeper with a solver
'''
'''
Credits
https://www.youtube.com/watch?v=AI2zs3nKHgg
helped with some of the game code below
none of the solver code was taken from here

https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
helped with timer

TA Joseph Melseshko assisted with figuring out and debugging the autoflagging function.
TA's Patrisha De Boon and Veronica Salm helped with figuring out how to use the coordinates of the tile objects as dictionary keys.
TA Arseniy Kouzmenkov helped with figuring out the algorithm for calculating conditional probability.
Assistance from TA Daniel Mitchell with debugging the next move indicator.
'''

# imported libraries
from random import randint
import pygame
import time
import string
import sys


pygame.init()

# Initializes probdict as a global dictionary.
probdict = {}

# function that clears the highscores of the bookkeeping file
def clearFile():
    try:
        f = open('bookkeeping', 'w')
        for i in range(6):
            f.write('1' + '\n')
        f.close()
    except IOError:
        print('File open failed: %s' % ('bookkeeping'))
        sys.exit(-1)

# the following 2 functions are for opening and reading a file
def fileOpen():
    try:
        x = open('bookkeeping', 'r')
        return(x)
    except IOError:
        print('File open failed: %s' % ('bookkeeping'))
        sys.exit(-1)


def fileRead(file):
    try:
        numbers = file.readlines()
        stripList = [s.strip() for s in numbers]
        return(stripList)
        f.close()
    except:
        print('File read failed')
        sys.exit(-1)

# creates the global variables by reading the lines of the opened file
# and storing them in appropriate variables
f = fileOpen()
recordList = fileRead(f)
if recordList == [] or recordList == ['1', '1', '1', '1', '1', '1']:
    wins = 0
    losses = 0
    totalGames = 0
    winPercent = 0
    explorationPercent = 0
    timePerMine = 0
else:
    wins = float(recordList[0])
    losses = float(recordList[1])
    totalGames = float(recordList[2])
    winPercent = float(recordList[3])
    explorationPercent = float(recordList[4])
    timePerMine = float(recordList[5])

# score printing function
def printScores(wins, losses, totalGames, winPercent, explorationPercent, timePerMine, size, screen):
    black = (0, 0, 0)
    size = size * 40
    print1 = 'Your scores are:'
    w = 'Wins: ' + str(wins)
    l = 'Losses: ' + str(losses)
    tg = 'total Games played: ' + str(totalGames)
    wp = 'Win Percentage: ' + str(winPercent)
    ep = 'Exploration Percentage: ' + str(explorationPercent)
    tpm = 'Best time per mine: ' + str(timePerMine)
    screen.fill(black)
    pygame.font.init()
    text = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(text, 12)
    print11 = font_renderer.render(print1, 1, (255, 255, 255))
    screen.blit(print11, (size / 3, (size / 2) - 60))
    text = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(text, 12)
    w1 = font_renderer.render(w, 1, (255, 255, 255))
    screen.blit(w1, (size / 3, (size / 2) - 40))
    text = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(text, 12)
    l1 = font_renderer.render(l, 1, (255, 255, 255))
    screen.blit(l1, (size / 3, (size / 2) - 20))
    text = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(text, 12)
    tg1 = font_renderer.render(tg, 1, (255, 255, 255))
    screen.blit(tg1, (size / 3, size / 2))
    text = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(text, 12)
    wp1 = font_renderer.render(wp, 1, (255, 255, 255))
    screen.blit(wp1, (size / 3, (size / 2) + 20))
    text = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(text, 12)
    ep1 = font_renderer.render(ep, 1, (255, 255, 255))
    screen.blit(ep1, (size / 3, (size / 2) + 40))
    text = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(text, 12)
    tpm1 = font_renderer.render(tpm, 1, (255, 255, 255))
    screen.blit(tpm1, (size / 3, (size / 2) + 60))
    pygame.display.flip()



# creates the mine table for later use
# taken from the youtube video above
def createMineTable(n, mines):
    table = [[0] * n for i in range(n)]
    table = mineAdd(table, mines)
    table = checkTable(table)
    return table


# adds mines at random intervals of the table
# taken from the youtube video above
def mineAdd(table, mines):
    for i in range(mines):
        mine = False
        while not mine:
            x = randint(0, len(table) - 1)
            y = randint(0, len(table) - 1)
            if table[x][y] != 9:
                table[x][y] = 9
                mine = True
    return table


# function that creates the count values for the mine table
# taken from the youtube video above
def checkTable(table):
    for x in range(len(table)):
        for y in range(len(table[x])):
            if table[x][y] == 9:
                table = checkDownLeft(table, x, y)
                table = checkDownRight(table, x, y)
                table = checkBelow(table, x, y)
                table = checkUpLeft(table, x, y)
                table = checkUpRight(table, x, y)
                table = checkAbove(table, x, y)
                table = checkLeft(table, x, y)
                table = checkRight(table, x, y)
    return table


# the following 8 functions work to create the tile values
# of greater than 0 for determination of the mines for the user
# or solver
# taken from the youtube video above
def checkAbove(table, x, y):
    if (x - 1) >= 0:
        if table[x - 1][y] != 9:
            table[x - 1][y] += 1
    return table


def checkBelow(table, x, y):
    if (x + 1) < len(table[0]):
        if table[x + 1][y] != 9:
            table[x + 1][y] += 1
    return table


def checkLeft(table, x, y):
    if (y - 1) >= 0:
        if table[x][y - 1] != 9:
            table[x][y - 1] += 1
    return table


def checkRight(table, x, y):
    if (y + 1) < len(table):
        if table[x][y + 1] != 9:
            table[x][y + 1] += 1
    return table


def checkUpLeft(table, x, y):
    if (x - 1) >= 0 and (y - 1) >= 0:
        if table[x - 1][y - 1] != 9:
            table[x - 1][y - 1] += 1
    return table


def checkUpRight(table, x, y):
    if (x - 1) >= 0 and (y + 1) < len(table):
        if table[x - 1][y + 1] != 9:
            table[x - 1][y + 1] += 1
    return table


def checkDownLeft(table, x, y):
    if (x + 1) < len(table[x]) and (y - 1) >= 0:
        if table[x + 1][y - 1] != 9:
            table[x + 1][y - 1] += 1
    return table


def checkDownRight(table, x, y):
    if (x + 1) < (len(table[0])) and (y + 1) < len(table):
        if table[x + 1][y + 1] != 9:
            table[x + 1][y + 1] += 1
    return table


# function only needed to check the mine table
# taken from the youtube video above
def pr(table):
    for i in table:
        print(i)


# class creation
# taken from the youtube video above
class field:
    def __init__(self, field):
        self.field = field

    def __repr__(self):
        pr(self.field)
        return ('is your table')


class tile:
    def __init__(self, x, y, width, height, field, ij):
        self.rect = pygame.rect.Rect(x, y, width, height)
        i, j = ij
        self.val = field[i][j]
        self.x = x
        self.y = y
        self.visible = False
        self.flag = False
        self.move = False


# taken from the youtube video above
def restart(size, mines, isSolver):
# restarts the game if the r button is pressed    
    if isSolver == True:
        solver(size, mines)
    elif isSolver == False:
        game(size, mines)


def zeroOpen(listn, tile):
    # this function checks all tiles around the clicked tile and if they are of
    #  value 0 then it opens the tile and reruns the function until all the
    #  boundaries are numbers
    # taken from the youtube video above
    tile.visible = True
    i, j = tile.x // 40, tile.y // 40
    if (i + 1) < len(listn):
        if listn[i + 1][j].visible == False and listn[i + 1][j].flag == False:
            listn[i + 1][j].visible = True
            if listn[i + 1][j].val == 0:
                zeroOpen(listn, listn[i + 1][j])
        if (j + 1) < len(listn):
            if listn[i + 1][j + 1].visible == False and listn[i + 1][j + 1].flag == False:
                listn[i + 1][j + 1].visible = True
                if listn[i + 1][j + 1].val == 0:
                    zeroOpen(listn, listn[i + 1][j + 1])
        if (j - 1) >= 0:
            if listn[i + 1][j - 1].visible == False and listn[i + 1][j - 1].flag == False:
                listn[i + 1][j - 1].visible = True
                if listn[i + 1][j - 1].val == 0:
                    zeroOpen(listn, listn[i + 1][j - 1])
    if (i - 1) >= 0:
        if listn[i - 1][j].visible == False and listn[i - 1][j].flag == False:
            listn[i - 1][j].visible = True
            if listn[i - 1][j].val == 0:
                zeroOpen(listn, listn[i - 1][j])
        if (j + 1) < len(listn):
            if listn[i - 1][j + 1].visible == False and listn[i - 1][j + 1].flag == False:
                listn[i - 1][j + 1].visible = True
                if listn[i - 1][j + 1].val == 0:
                    zeroOpen(listn, listn[i - 1][j + 1])
        if (j - 1) >= 0:
            if listn[i - 1][j - 1].visible == False and listn[i - 1][j - 1].flag == False:
                listn[i - 1][j - 1].visible = True
                if listn[i - 1][j - 1].val == 0:
                    zeroOpen(listn, listn[i - 1][j - 1])
    if (j - 1) >= 0:
        if listn[i][j - 1].visible == False and listn[i][j - 1].flag == False:
            listn[i][j - 1].visible = True
            if listn[i][j - 1].val == 0:
                zeroOpen(listn, listn[i][j - 1])
    if (j + 1) < len(listn):
            if listn[i][j + 1].visible == False and listn[i][j + 1].flag == False:
                listn[i][j + 1].visible = True
                if listn[i][j + 1].val == 0:
                    zeroOpen(listn, listn[i][j + 1])


def game(size, mines):
    # global variable setup and file open setup for
    # highscores to be sent later
    global wins, losses, totalGames, winPercent, explorationPercent, timePerMine
    try:
        f = open('bookkeeping', 'w')
    except IOError:
        print('File open failed: %s' % ('bookkeeping'))
        sys.exit(-1)
    # arbitrary value for the restart function
    isSolver = False
    # basic setup of images
    # taken from the youtube video above
    darkGray = pygame.image.load('darkGray.jpg')
    darkGray = pygame.transform.scale(darkGray, (40, 40))
    lightGray = pygame.image.load('lightGray.jpg')
    lightGray = pygame.transform.scale(lightGray, (40, 40))
    blank = pygame.image.load('white.png')
    blank = pygame.transform.scale(blank, (40, 40))
    one = pygame.image.load('1.png')
    one = pygame.transform.scale(one, (20, 20))
    two = pygame.image.load('2.png')
    two = pygame.transform.scale(two, (20, 20))
    three = pygame.image.load('3.png')
    three = pygame.transform.scale(three, (20, 20))
    four = pygame.image.load('4.png')
    four = pygame.transform.scale(four, (20, 20))
    five = pygame.image.load('5.png')
    five = pygame.transform.scale(five, (20, 20))
    six = pygame.image.load('6.png')
    six = pygame.transform.scale(six, (20, 20))
    seven = pygame.image.load('7.png')
    seven = pygame.transform.scale(seven, (20, 20))
    eight = pygame.image.load('8.png')
    eight = pygame.transform.scale(eight, (20, 20))
    mineImg = pygame.image.load('mine.png')
    mineImg = pygame.transform.scale(mineImg, (20, 20))
    Flag = pygame.image.load('Flag.jpg')
    Flag = pygame.transform.scale(Flag, (20, 20))
    # number list setup for later
    # taken from the youtube video above
    listNums = (blank, one, two, three, four, five, six, seven, eight, mineImg)
    # create a blank field so that mines aren't initialized
    # before the first click
    blankField = field([[0] * size for i in range(size)])
    width = height = len(blankField.field) * 40
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Minesweeper          Minecount: ' + str(mines))
    # create the graphics window
    # taken from the youtube video above
    listn = [[] for i in range(size)]
    for i in range(0, size * 40, 40):
        for j in range(0, size * 40, 40):
            listn[i//40] += [tile(i, j, 40, 40, blankField.field, (i//40, j//40))]
            screen.blit(darkGray, (i, j))

    mineInit = False
    running = True
    minecount = mines
    while running:
        # section modified from youtube vide oabove to include
        # the initial click check
        # score keeping was added seperately from the video above
        for event in pygame.event.get():  # if the window is closed end the program
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:  # if r is pressed reset the game
                # checks for reset or highscore clear button press
                if event.key == pygame.K_r:
                    run = False
                    restart(size, mines, isSolver)
                elif event.key == pygame.K_c:
                    choose = input('Would you like to clear your data? yes or no: ')
                    choose = choose.lower()
                    if choose == 'yes':
                        clearFile()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mineInit == False:
                # initial click for loop that creates the mines after the initial click and then
                # checks if the clicked value is equal to 9 and if it is it reruns the loop until
                # the value of the tile clicked is 0 at which points it runs the whitespace open
                # function and sets the mineInit arbitrary value to true thereby stopping this check
                # from being run and sets the initial time for the timer
                while True:
                    O = field(createMineTable(size, mines))
                    width = height = len(O.field) * 40
                    listn = [[] for i in range(size)]
                    for i in range(0, size * 40, 40):
                        for j in range(0, size * 40, 40):
                            listn[i//40] += [tile(i, j, 40, 40, O.field, (i//40, j//40))]
                            screen.blit(darkGray, (i, j))
                    for i in listn:
                        for j in i:
                            rectangle = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                            if j.rect.colliderect(rectangle):
                                if j.flag == False:
                                    if j.val == 9:
                                        O = field(createMineTable(size, mines))
                                        width = height = len(O.field) * 40
                                        listn = [[] for i in range(size)]
                                        for x in range(0, size * 40, 40):
                                            for y in range(0, size * 40, 40):
                                                listn[x//40] += [tile(x, y, 40, 40, O.field, (x//40, y//40))]
                                                screen.blit(darkGray, (x, y))
                                    if j.val == 0:
                                        j.visible = zeroOpen(listn, j)
                                        j.visible = True
                                        mineInit = True
                                        initTime = int(time.time())
                    if mineInit == True:
                        break

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # left mouse click for loop.  If the value of the tile clicked is 9
                # then print game over else open the tile and if the tile has value 0
                # then run the function that opens all whitespace around the clicked tile
                # taken from the youtube video above
                for i in listn:
                    for j in i:
                        rectangle = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                        if j.rect.colliderect(rectangle):
                            if j.flag == False:
                                if j.val == 9:
                                    # calculates all highscores and prints them for a gameover
                                    # not taken from youtube video above
                                    endTime = int(time.time())
                                    totalTime = endTime - initTime
                                    pygame.display.set_caption('Game Over          Time: ' + str(totalTime))
                                    losses += 1
                                    totalGames += 1
                                    winPercent = (wins / totalGames) * 100
                                    timePerMine1 = totalTime / mines
                                    if timePerMine == 0:
                                        timePerMine = timePerMine1
                                    elif timePerMine1 < timePerMine:
                                        timePerMine = timePerMine1
                                    explorationPercent1 = (exploreCount / (size * size)) * 100
                                    if explorationPercent == 0:
                                        explorationPercent = explorationPercent1
                                    else:
                                        explorationPercent = (explorationPercent + explorationPercent1) / 2
                                    printScores(wins, losses, totalGames, winPercent, explorationPercent, timePerMine, size, screen)
                                    time.sleep(10)
                                    running = False
                                j.visible = True
                                # opens all whitespace tiles if a whitespace tile is clicked.
                                if j.val == 0:
                                    j.visible = zeroOpen(listn, j)
                                    j.visible = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                # if right mouse button is clicked determine if the flag value of the
                # tile is true or false and flip it then take away or add a flag
                # also increase or decrease the minecount
                for i in listn:
                    for j in i:
                        rectangle = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                        if j.rect.colliderect(rectangle):
                            if j.visible == False:
                                # adds or removes a flag as well as changes the
                                # minecount based on number of flags and number of mines
                                # modified from youtube video above to include a minecount for the
                                # user
                                if j.flag == False:
                                    j.flag = True
                                    minecount -= 1
                                    if minecount <= 0:
                                        pygame.display.set_caption('Minesweeper          Minecount: 0')
                                    else:
                                        pygame.display.set_caption('Minesweeper          Minecount: ' + str(minecount))

                                elif j.flag == True:
                                    j.flag = False
                                    minecount += 1
                                    if minecount > 0:
                                        pygame.display.set_caption('Minesweeper          Minecount: ' + str(minecount))
                                    else:
                                        pygame.display.set_caption('Minesweeper          Minecount: 0')
        # determine what to paste onto the screen based on conditions
        # taken from the youtube video above
        for i in listn:
            for j in i:
                if j.visible == True:
                    # pastes numbers or white space if the tile has been
                    # made visible
                    screen.blit(lightGray, (j.x, j.y))
                    screen.blit(listNums[j.val], (j.x + 10, j.y + 10))
                if j.flag == True and j.visible == False:
                    # pastes a flag if the flag value is true
                    screen.blit(Flag, (j.x + 10, j.y + 10))
                if j.flag == False and j.visible == False:
                    # pastes a flag if flag value is false
                    screen.blit(darkGray, (j.x, j.y))
        # runs through the game until all tiles that do not hide mines
        # are open based on the squarecount value
        # taken from the youtube video above with some modifications
        squareCount = 0
        exploreCount = 0
        # increments squareCount and explorationCount
        # until squareCount is equal to the size squared
        # or a mine is clicked.
        # essentially the win condition for the game
        for i in listn:
            for j in i:
                if j.visible == True and j.val != 9:
                    squareCount += 1
                    exploreCount += 1
            if squareCount == size * size - mines:
                running = False
                # takes end time and calculates all highscores
                # as well as prints them all
                endTime = int(time.time())
                totalTime = endTime - initTime
                pygame.display.set_caption('You Win          Time: ' + str(totalTime))
                wins += 1
                totalGames += 1
                winPercent = (wins / totalGames) * 100
                timePerMine1 = totalTime / mines
                if timePerMine == 0:
                    timePerMine = timePerMine1
                elif timePerMine1 < timePerMine:
                    timePerMine = timePerMine1
                explorationPercent1 = (exploreCount / (size * size)) * 100
                if explorationPercent == 0:
                    explorationPercent = explorationPercent1
                else:
                    explorationPercent = (explorationPercent + explorationPercent1) / 2
                printScores(wins, losses, totalGames, winPercent, explorationPercent, timePerMine, size, screen)
                time.sleep(10)
        pygame.display.update()
        # if game win display all mines
    for i in listn:
        for j in i:
            if j.val == 9:
                screen.blit(mineImg, (j.x + 10, j.y + 10))
    pygame.display.update()
    # waits for either quit or reset upon loss or win
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # if the game window is closed the highscores
                # get sent to the bookkeeping file for safekeeping
                # not taken from video above
                intList = [1, 1, 1, 1, 1, 1]
                intList[0] = wins
                intList[1] = losses
                intList[2] = totalGames
                intList[3] = winPercent
                intList[4] = explorationPercent
                intList[5] = timePerMine
                for i in range(len(intList)):
                    f.write(str(intList[i]) + '\n')
                f.close()
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                # checks for r button press and restarts the game
                if event.key == pygame.K_r:
                    run = False
                    restart(size, mines, isSolver)
                # checks for a c button press and prompts for information
                elif event.key == pygame.K_c:
                    choose = input('Would you like to clear your data? yes or no: ')
                    choose = choose.lower()
                    if choose == 'yes':
                        clearFile()

# The following functions (excluding main)
# are dedicated to the solver program


def solverOpen(listn, tile):
    # this function checks all tiles around the clicked tile and if they are of value
    # 0 then it opens the tile and reruns the function until all the boundaries
    # are numbers
    # Then it runs the  tilecheck function on every visible tile.
    # Inputs: listn: A 2 dimensional list that indexes all the tiles on the board.
    # tile: The tile object used to represent the tiles on the board.
    tile.visible = True
    i, j = tile.x // 40, tile.y // 40
    # Checks all adjacent tiles and ensures the program never goes out of range
    # of the listn index.
    if (i + 1) < len(listn):
        if listn[i + 1][j].visible == False and listn[i + 1][j].flag == False:
            listn[i + 1][j].visible = True
            # runs the tilecheck function for every visible tile.
            tilecheck(listn, tile)
            if listn[i + 1][j].val == 0:
                # recurses if the function opens a blank tile.
                solverOpen(listn, listn[i + 1][j])
        if (j + 1) < len(listn):
            if listn[i + 1][j + 1].visible == False and listn[i + 1][j + 1].flag == False:
                listn[i + 1][j + 1].visible = True
                tilecheck(listn, tile)
                if listn[i + 1][j + 1].val == 0:
                    solverOpen(listn, listn[i + 1][j + 1])
        if (j - 1) >= 0:
            if listn[i + 1][j - 1].visible == False and listn[i + 1][j - 1].flag == False:
                listn[i + 1][j - 1].visible = True
                tilecheck(listn, tile)
                if listn[i + 1][j - 1].val == 0:
                    solverOpen(listn, listn[i + 1][j - 1])
    if (i - 1) >= 0:
        if listn[i - 1][j].visible == False and listn[i - 1][j].flag == False:
            listn[i - 1][j].visible = True
            tilecheck(listn, tile)
            if listn[i - 1][j].val == 0:
                solverOpen(listn, listn[i - 1][j])
        if (j + 1) < len(listn):
            if listn[i - 1][j + 1].visible == False and listn[i - 1][j + 1].flag == False:
                listn[i - 1][j + 1].visible = True
                tilecheck(listn, tile)
                if listn[i - 1][j + 1].val == 0:
                    solverOpen(listn, listn[i - 1][j + 1])
        if (j - 1) >= 0:
            if listn[i - 1][j - 1].visible == False and listn[i - 1][j - 1].flag == False:
                listn[i - 1][j - 1].visible = True
                tilecheck(listn, tile)
                if listn[i - 1][j - 1].val == 0:
                    solverOpen(listn, listn[i - 1][j - 1])
    if (j - 1) >= 0:
        if listn[i][j - 1].visible == False and listn[i][j - 1].flag == False:
            listn[i][j - 1].visible = True
            tilecheck(listn, tile)
            if listn[i][j - 1].val == 0:
                solverOpen(listn, listn[i][j - 1])
    if (j + 1) < len(listn):
        if listn[i][j + 1].visible == False and listn[i][j + 1].flag == False:
            listn[i][j + 1].visible = True
            tilecheck(listn, tile)
            if listn[i][j + 1].val == 0:
                solverOpen(listn, listn[i][j + 1])


def createprobdict(listn):
    # Creates a global dictionary that indexes all the tiles and
    # the probability (float) that there is going to be a mine on each tile.
    # all probabilities initially start at 1.0.
    # Inputs: listn: A 2 dimensional list that indexes all the tiles on the board.
    for i in listn:
        for j in i:
            # Sets the coordinates of each tile as the keys for the dictionary.
            d1 = {(j.x, j.y): 1.0}
            probdict.update(d1)


def autoflag(listn, i, j):
    # Automatically flags covered tiles that are guaranteed to be mines
    # by checking around every visible numbered tile and flagging covered tiles
    # if the number of adjacent covered tiles matches the number on the tile.
    # Inputs: listn: A 2 dimensional list that indexes all the tiles on the board.
    # i: the row of the current tile.
    # j: the current tile.
    k = listn[i][j].val
    count = 0
    toflag = []
    # Checks all adjacent tiles and ensures the program never goes out of range
    # of the listn index.
    if (i + 1) < len(listn):
        if listn[i + 1][j].visible == False:
            # increments the local variable count for every visible tile
            # and adds the corrdinates to a local list.
            count += 1
            toflag.append([i + 1, j])
        if (j + 1) < len(listn):
            if listn[i + 1][j + 1].visible == False:
                count += 1
                toflag.append([i + 1, j + 1])
        if (j - 1) >= 0:
            if listn[i + 1][j - 1].visible == False:
                count += 1
                toflag.append([i + 1, j - 1])
    if (i - 1) >= 0:
        if listn[i - 1][j].visible == False:
            count += 1
            toflag.append([i - 1, j])
        if (j + 1) < len(listn):
            if listn[i - 1][j + 1].visible == False:
                count += 1
                toflag.append([i - 1, j + 1])
        if (j - 1) >= 0:
            if listn[i - 1][j - 1].visible == False:
                count += 1
                toflag.append([i - 1, j - 1])
    if (j - 1) >= 0:
        if listn[i][j - 1].visible == False:
            count += 1
            toflag.append([i, j - 1])
    if (j + 1) < len(listn):
        if listn[i][j + 1].visible == False:
            count += 1
            toflag.append([i, j + 1])

    if count == k:
        # flags every tile in the toflag list if the value of the
        # tile matches the number of covered adjacent tiles.
        for m in toflag:
            listn[m[0]][m[1]].flag = True

    
def tilecheck(listn, tile):
    # The function that does the majority of the calculations for the solver.
    # Checks if any of the adjacent tiles are revealed and if they are, first runs
    # the autoflag function, then performs probability calculations for each adjacent
    # uncovered tile and updates the main probability dictionary.
    # Inputs: listn: A 2 dimensional list that indexes all the tiles on the board.
    # tile: The tile object used to represent the tiles on the board
    i, j = tile.x // 40, tile.y // 40
    # Checks all adjacent tiles and ensures the program never goes out of range
    # of the listn index.
    if (i + 1) < len(listn):
        if listn[i + 1][j].visible == True and listn[i + 1][j].val >  0:
            autoflag(listn, i + 1, j)
            # sets the number of mines around the tile to the value of the tile
            minenum = listn[i + 1][j].val
            # recalculates the minenum and calculates the number of uncovered tiles and
            # returns them in a list
            paramlist = minecalc(minenum, listn, i + 1, j)
            minenum = paramlist[0]
            # The number of adjacent covered tiles
            count = paramlist[1]
            # The coordinates of all the adjacent covered tiles in a list
            tlist = listcalc(listn, i + 1, j)
            # A temporary probability dictionary is created and used to update the main
            # probability dictionary.
            interdict = createinterdict(tlist, minenum, count)
            updatedict(interdict)

        if (j + 1) < len(listn):
            if listn[i + 1][j + 1].visible == True and listn[i + 1][j + 1].val > 0:
                autoflag(listn, i + 1, j + 1)
                minenum = listn[i + 1][j + 1].val
                paramlist = minecalc(minenum, listn, i + 1, j + 1)
                minenum = paramlist[0]
                count = paramlist[1]
                tlist = listcalc(listn, i + 1, j + 1)
                interdict = createinterdict(tlist, minenum, count)
                updatedict(interdict)
        if (j - 1) >= 0:
            if listn[i + 1][j - 1].visible == True and listn[i + 1][j - 1].val > 0:
                autoflag(listn, i + 1, j - 1)
                minenum = listn[i + 1][j - 1].val
                paramlist = minecalc(minenum, listn, i + 1, j - 1)
                minenum = paramlist[0]
                count = paramlist[1]
                tlist = listcalc(listn, i + 1, j - 1)
                interdict = createinterdict(tlist, minenum, count)
                updatedict(interdict)
    if (i - 1) >= 0:
        if listn[i - 1][j].visible == True and listn[i - 1][j].val > 0:
            autoflag(listn, i - 1, j)
            minenum = listn[i - 1][j].val
            paramlist = minecalc(minenum, listn, i - 1, j)
            minenum = paramlist[0]
            count = paramlist[1]
            tlist = listcalc(listn, i - 1, j)
            interdict = createinterdict(tlist, minenum, count)
            updatedict(interdict)
        if (j + 1) < len(listn):    
            if listn[i - 1][j + 1].visible == True and listn[i - 1][j + 1].val > 0:
                autoflag(listn, i - 1, j + 1)
                minenum = listn[i - 1][j + 1].val
                paramlist = minecalc(minenum, listn, i - 1, j + 1)
                minenum = paramlist[0]
                count = paramlist[1]
                tlist = listcalc(listn, i - 1, j + 1)
                interdict = createinterdict(tlist, minenum, count)
                updatedict(interdict)
        if (j - 1) >= 0:
            if listn[i - 1][j - 1].visible == True and listn[i - 1][j - 1].val > 0:
                autoflag(listn, i - 1, j - 1)
                minenum = listn[i - 1][j - 1].val
                paramlist = minecalc(minenum, listn, i - 1, j - 1)
                minenum = paramlist[0]
                count = paramlist[1]
                tlist = listcalc(listn, i - 1, j - 1)
                interdict = createinterdict(tlist, minenum, count)
                updatedict(interdict)
    if (j - 1) >= 0:
        if listn[i][j - 1].visible == True and listn[i][j - 1].val > 0:
            autoflag(listn, i, j - 1)
            minenum = listn[i][j - 1].val
            paramlist = minecalc(minenum, listn, i, j - 1)
            minenum = paramlist[0]
            count = paramlist[1]
            tlist = listcalc(listn, i, j - 1)
            interdict = createinterdict(tlist, minenum, count)
            updatedict(interdict)
    if (j + 1) < len(listn):
        if listn[i][j + 1].visible == True and listn[i][j + 1].val > 0:
            autoflag(listn, i, j + 1)
            minenum = listn[i][j + 1].val
            paramlist = minecalc(minenum, listn, i, j + 1)
            minenum = paramlist[0]
            count = paramlist[1]
            tlist = listcalc(listn, i, j + 1)
            interdict = createinterdict(tlist, minenum, count)
            updatedict(interdict)


def minecalc(minenum, listn, i, j):
    # The function subtracts the number of mines around the current tile by the
    # number of adjacent flags and also records the number of uncovered tiles.
    # Inputs: minenum: an initial calculation of the number of adjacent mines, based
    # on the value of the current tile.
    # listn: A 2 dimensional list that indexes all the tiles on the board.
    # i: the row of the current tile.
    # j: the current tile.
    # Returns: paramlist: A list that contains the recalculated minenum and the
    # number of covered tiles.
    tlist = []
    count = 0
    # Checks all adjacent tiles and ensures the program never goes out of range
    # of the listn index.
    if (i + 1) < len(listn):
        # Increments the count if a covered tile is detected.
        # Changed after the demo to exclude flagged tiles, debugging done here.
        if listn[i + 1][j].visible == False and listn[i + 1][j].flag == False:
            count += 1
            # decrements the minenum if a flag is detected.
            if listn[i + 1][j].flag == True:
                minenum -= 1
            
        if (j + 1) < len(listn):
            if listn[i + 1][j + 1].visible == False and listn[i + 1][j + 1].flag == False:
                count += 1
                if listn[i + 1][j + 1].flag == True:
                    minenum -= 1
                               
        if (j - 1) >= 0:
            if listn[i + 1][j - 1].visible == False and listn[i + 1][j - 1].flag == False:
                count += 1
                if listn[i + 1][j - 1].flag == True:
                    minenum -= 1
               
    if (i - 1) >= 0:
        if listn[i - 1][j].visible == False and listn[i - 1][j].flag == False:
            count += 1
            if listn[i - 1][j].flag == True:
                minenum -= 1

        if (j + 1) < len(listn):
            if listn[i - 1][j + 1].visible == False and listn[i - 1][j + 1].flag == False:
                count += 1
                if listn[i - 1][j + 1].flag == True:
                    minenum -= 1
                
        if (j - 1) >= 0:
            if listn[i - 1][j - 1].visible == False and listn[i - 1][j - 1].flag == False:
                count += 1
                if listn[i - 1][j - 1].flag == True:
                    minenum -= 1
                
    if (j - 1) >= 0:
        if listn[i][j - 1].visible == False and listn[i][j - 1].flag == False:
            count += 1
            if listn[i][j - 1].flag == True:
                minenum -= 1
            
    if (j + 1) < len(listn):
        if listn[i][j + 1].visible == False and listn[i][j + 1].flag == False:
            count += 1
            if listn[i][j + 1].flag == True:
                minenum -= 1
    paramlist = [minenum, count]
    return paramlist


def listcalc(listn, i, j):
    # This function creates a list of coordinates of all the covered tiles.
    # Inputs: listn: A 2 dimensional list that indexes all the tiles on the board.
    # i: the row of the current tile.
    # j: the current tile.
    # Returns: tlist: a list of the coordinates of all adjacent covered tiles.
    tlist = []
    # Checks all adjacent tiles and ensures the program never goes out of range
    # of the listn index.
    if (i + 1) < len(listn):
        # Only covered and unflagged tiles are added to the tlist.
        if listn[i + 1][j].visible == False:
            if listn[i + 1][j].flag == False:
                tlist.append((i + 1, j))
            
        if (j + 1) < len(listn):
            if listn[i + 1][j + 1].visible == False:
                if listn[i + 1][j + 1].flag == False:
                    tlist.append((i + 1, j + 1))
                               
        if (j - 1) >= 0:
            if listn[i + 1][j - 1].visible == False:
                if listn[i + 1][j - 1].flag == False:
                    tlist.append((i + 1, j - 1))
               
    if (i - 1) >= 0:
        if listn[i - 1][j].visible == False:
            if listn[i - 1][j].flag == False:
                tlist.append((i - 1, j))

        if (j + 1) < len(listn):
            if listn[i - 1][j + 1].visible == False:
                if listn[i - 1][j + 1].flag == False:
                    tlist.append((i - 1, j + 1))
                
        if (j - 1) >= 0:
            if listn[i - 1][j - 1].visible == False:
                if listn[i - 1][j - 1].flag == False:
                    tlist.append((i - 1, j - 1))
                
    if (j - 1) >= 0:
        if listn[i][j - 1].visible == False:
            if listn[i][j - 1].flag == False:
                tlist.append((i, j - 1))
            
    if (j + 1) < len(listn):
        if listn[i][j + 1].visible == False:
            if listn[i][j + 1].flag == False:
                tlist.append((i, j + 1))
    return tlist


def createinterdict(tlist, minenum, count):
    # creates a temporary probability dictionary for all adjacent
    # tiles to the current tile. Uses conditional probability to calculate 
    # the chance of there being a mine on an adjacent uncovered tile based 
    # on the updated minecount and the number of covered tiles.
    # Inputs: tlist: a list of the coordinates of all adjacent covered tiles.
    # minenum: the updated calculation of the number of adjacent mines, based
    # on the number of flags around the current tile.
    # count: The number of adjacent covered tiles.
    # Returns: interdict: A temporary dictionary containing the updated
    # probabilities.
    interdict = {}
    # only runs if the count is greater than 0.
    if count > 0:
        prob = minenum / count
        # Uses the coordinates in the tlist as the keys in the temporary
        # dictionary.
        for i in tlist:
            d2 = {i: prob}
            interdict.update(d2)
    return interdict


def updatedict(interdict):
    # This function updates the global probability dictionary using
    # value from the temporary dictionary interdict.
    # Inputs: interdict: A temporary dictionary containing probabilities
    # for the adjacent covered tiles.
    for k in interdict.items():
        for d in probdict.items():
            # if the keys match, the corresponding global probdict value
            # is recalculated.
            if k[0] == d[0]:
                # If this is the first update for the key, value pair, the
                # value is replaced.
                if d[1] == 1.0:
                    probdict[d[0]] = k[1]
                    # otherwise the probabilities are combined.
                else:
                    f = k[1] + d[1]
                    probdict[d[0]] = f
def nextMove():
    # This function calculates the best move based on the lowest probability
    # for a mine on the board and returns the coordinates of the tile.
    # Returns: key: a tuple containing the coordinates of the tile.
    small = 2.0
    key = None
    # Finds the smallest value in the probdict and returns the corresponding key.
    for k, v in probdict.items():
        if v < small:
            small = v
            key = k
    return key


def isVisible(listn, locate):
    # This function checks the tile chosen for the next move. If the tile
    # is already visible or has a flag then the probability for that tile is
    # set to a high probability to remove it from the possible moves and the function
    # returns False. The function returns true if it finds a valid next move, that is,
    # a tile that is covered and unflagged.
    # Inputs: listn: A 2 dimensional list that indexes all the tiles on the board.
    # locate: a tuple containing the coordinates of the tile.
    # Return: True or False
    # Checks if the tile is covered and unflagged.
    if listn[locate[0]//40][locate[1]//40].visible == False and \
    listn[locate[0]//40][locate[1]//40].flag == False:
        return True
    else:
        # If the tile is visible or flagged, the probability value of the tile is reset to
        # to remove it from the possible next moves and the program returns false
        probdict[locate] = 2.0
        return False


def solver(size, mines):
    # runs a few solver only conditions in the code.
    isSolver = True
    darkGray = pygame.image.load('darkGray.jpg')
    darkGray = pygame.transform.scale(darkGray, (40, 40))
    lightGray = pygame.image.load('lightGray.jpg')
    lightGray = pygame.transform.scale(lightGray, (40, 40))
    green = pygame.image.load('green.jpg')
    green = pygame.transform.scale(green, (40, 40))
    blank = pygame.image.load('white.png')
    blank = pygame.transform.scale(blank, (40, 40))
    one = pygame.image.load('1.png')
    one = pygame.transform.scale(one, (20, 20))
    two = pygame.image.load('2.png')
    two = pygame.transform.scale(two, (20, 20))
    three = pygame.image.load('3.png')
    three = pygame.transform.scale(three, (20, 20))
    four = pygame.image.load('4.png')
    four = pygame.transform.scale(four, (20, 20))
    five = pygame.image.load('5.png')
    five = pygame.transform.scale(five, (20, 20))
    six = pygame.image.load('6.png')
    six = pygame.transform.scale(six, (20, 20))
    seven = pygame.image.load('7.png')
    seven = pygame.transform.scale(seven, (20, 20))
    eight = pygame.image.load('8.png')
    eight = pygame.transform.scale(eight, (20, 20))
    mineImg = pygame.image.load('mine.png')
    mineImg = pygame.transform.scale(mineImg, (20, 20))
    Flag = pygame.image.load('Flag.jpg')
    Flag = pygame.transform.scale(Flag, (20, 20))
    # number list setup for later
    listNums = (blank, one, two, three, four, five, six, seven, eight, mineImg)
    # create a blank field so that mines aren't initialized
    # before the first click
    blankField = field([[0] * size for i in range(size)])
    width = height = len(blankField.field) * 40
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Minesweeper          Minecount: ' + str(mines))
    # create the graphics window
    listn = [[] for i in range(size)]
    for i in range(0, size * 40, 40):
        for j in range(0, size * 40, 40):
            listn[i//40] += [tile(i, j, 40, 40, blankField.field, (i//40, j//40))]
            screen.blit(darkGray, (i, j))

    mineInit = False
    running = True
    minecount = mines
    createprobdict(listn)
    while running:
        for event in pygame.event.get(): # if the window is closed end the program
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN: # if r is pressed reset the game
                if event.key == pygame.K_r:
                    run = False
                    restart(size, mines, isSolver)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mineInit == False:
                # initial click for loop that creates the mines after the initial click and then
                # checks if the clicked value is equal to 9 and if it is it reruns the loop until
                # the value of the tile clicked is 0 at which points it runs the whitespace open
                # function and sets the mineInit arbitrary value to true thereby stopping this check
                # from being run and sets the initial time for the timer
                while True:
                    O = field(createMineTable(size, mines))
                    width = height = len(O.field) * 40
                    listn = [[] for i in range(size)]
                    for i in range(0, size * 40, 40):
                        for j in range(0, size * 40, 40):
                            listn[i//40] += [tile(i, j, 40, 40, O.field, (i//40, j//40))]
                            screen.blit(darkGray, (i, j))
                    for i in listn:
                        for j in i:
                            rectangle = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                            if j.rect.colliderect(rectangle):
                                if j.flag == False:
                                    if j.val == 9:
                                        # reruns the loop until the value of the clicked tile is 0
                                        O = field(createMineTable(size, mines))
                                        width = height = len(O.field) * 40
                                        listn = [[] for i in range(size)]
                                        for x in range(0, size * 40, 40):
                                            for y in range(0, size * 40, 40):
                                                listn[x//40] += [tile(x, y, 40, 40, O.field, (x//40, y//40))]
                                                screen.blit(darkGray, (x, y))
                                    if j.val == 0:
                                        # Runs the solverOpen function for every visible tile
                                        j.visible = solverOpen(listn, j)
                                        j.visible = True
                                        # Runs the tilecheck calculations on every visible tile
                                        tilecheck(listn, j)
                                        mineInit = True
                                        initTime = int(time.time())
                                        nexttile = False
                                        while nexttile == False:
                                            locate = nextMove()
                                            nexttile = isVisible(listn, locate)
                                        listn[locate[0]//40][locate[1]//40].move = True
                    if mineInit == True:
                        break 
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # left mouse click for loop.  If the value of the tile clicked is 9
                # then print game over else open the tile and if the tile has value 0
                # then run the function that opens all whitespace around the clicked tile
                for i in listn:
                    for j in i:
                        rectangle = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                        if j.rect.colliderect(rectangle):
                            if j.flag == False:
                                if j.val == 9:
                                    # ends the timer
                                    endTime = int(time.time())
                                    totalTime = endTime - initTime
                                    pygame.display.set_caption('Game Over          Time: ' + str(totalTime))
                                    running = False
                                if j.val == 0:
                                    # Runs the solverOpen function for every visible tile
                                    j.visible = solverOpen(listn, j)
                                    j.visible = True
                                    # Runs the tilecheck calculations on every visible tile
                                    tilecheck(listn, j)
                                    nexttile = False
                                    try:
                                        # Runs looks for a valid next move until an unflagged covered
                                        # tile is found.
                                        while nexttile == False:
                                            locate = nextMove()
                                            nexttile = isVisible(listn, locate)
                                        # Sets the tile.move property of the chosen tile to true to allow
                                        # the green indicator to be pasted
                                        listn[locate[0]//40][locate[1]//40].move = True
                                    except Exception:
                                        pass
                                else:
                                    j.visible = True
                                    tilecheck(listn, j)
                                    # arbitrary value set to False, the while lop will continue until a
                                    # valid next move is found and the arbitrary value set to True.
                                    nexttile = False
                                    # Catches errors that occur when the game ends and there are no more
                                    # valid covered tiles.
                                    try:
                                        # Runs looks for a valid next move until an unflagged covered
                                        # tile is found.
                                        while nexttile == False:
                                            locate = nextMove()
                                            nexttile = isVisible(listn, locate)
                                        # Sets the tile.move property of the chosen tile to true to allow
                                        # the green indicator to be pasted
                                        listn[locate[0]//40][locate[1]//40].move = True
                                    except Exception:
                                       pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                # if right mouse button is clicked determine if the flag value of the
                # tile is true or false and flip it then take away or add a flag
                # also increase or decrease the minecount
                for i in listn:
                    for j in i:
                        rectangle = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                        if j.rect.colliderect(rectangle):
                            if j.visible == False:
                                if j.flag == False:
                                    j.flag = True
                                    minecount -= 1
                                    if minecount <= 0:
                                        pygame.display.set_caption('Minesweeper          Minecount: 0')
                                    else:
                                        pygame.display.set_caption('Minesweeper          Minecount: ' + str(minecount))
                                    
                                elif j.flag == True:
                                    j.flag = False
                                    minecount += 1
                                    if minecount > 0:    
                                        pygame.display.set_caption('Minesweeper          Minecount: ' + str(minecount))
                                    else:
                                       pygame.display.set_caption('Minesweeper          Minecount: 0')
        # determine what to paste onto the screen based on conditions
        for i in listn:
            for j in i:
                if j.visible == True and j.move == True:
                    # pastes numbers or white space if the tile has been
                    # made visible.
                    # removes the green next move marker.
                    screen.blit(lightGray, (j.x, j.y))
                    screen.blit(listNums[j.val], (j.x + 10, j.y + 10))
                    probdict[(j.x, j.y)] = 2.0
                    j.move == False
                if j.move == False and j.visible == True:
                    screen.blit(lightGray, (j.x, j.y))
                    screen.blit(listNums[j.val], (j.x + 10, j.y + 10))
                    # Sets the probabilties of visible tiles to an arbitrarily high
                    # number to remove them from the possible next moves.
                    probdict[(j.x, j.y)] = 2.0                  
                if j.move == False and j.flag == True and j.visible == False:
                    # pastes a flag if the flag value is true.
                    screen.blit(Flag, (j.x + 10, j.y + 10))
                    probdict[(j.x, j.y)] = 2.0
                if j.flag == False and j.visible == False:
                    # pastes a flag if flag value is false.
                    screen.blit(darkGray, (j.x, j.y))
                if j.move == True and j.visible == False:
                    # If the tile is chosen as the next move, pastes the green indicator
                    # onto the tile.
                    screen.blit(green, (j.x, j.y))
                    probdict[(j.x, j.y)] = 2.0
        # runs through the game until all tiles that do not hide mines
        # are open based on the squarecount value.
        squareCount = 0
        for i in listn:
            for j in i:
                if j.visible == True and j.val != 9:
                    squareCount += 1
                    
            if squareCount == size * size - mines:
                running = False
                endTime = int(time.time())
                totalTime = endTime - initTime
                pygame.display.set_caption('You Win          Time: ' + str(totalTime))
        pygame.display.update()
        # if game win display all mines
    for i in listn:
        for j in i:
            if j.val == 9:
                screen.blit(mineImg, (j.x + 10, j.y + 10))
    pygame.display.update()
    # waits for either quit or reset upon loss or win
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run = False
                    restart(size, mines, isSolver)  



def main():
    print('Instructions:')
    print('Press r to restart the game')
    print('right click a tile to flag it')
    print('left click a tile to reveal what is beneath')
    print('After the game is closed your highscores (these are printed after the You Win or Game Over')
    print('lines are printed) will be saved to a seperate file.')
    print('if you wish to reset the file containing your highscorces, press c on the keyboard and type')
    print('yes into the terminal')
    size = int(input('Enter the height and width of the table (one number between 4 and 21): '))
    mines = int(input('Enter a mine count for the board (between 1 and size * size - 1: '))
    choice = input('Who will be solving the field? The user or the solver: ')
    choice = choice.lower()
    if choice == 'user':
        game(size, mines)
    elif choice == 'solver':
        solver(size, mines)


if __name__ == '__main__':
    main()
