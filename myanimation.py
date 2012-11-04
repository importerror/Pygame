import pygame,random,sys
from pygame.locals import *

#dimensions of board and window
w_width=640
w_height=480
boxsize=40
boxspeed=8
boxgap=10
b_width=10
b_height=7
b_size=b_width*b_height
assert(b_width*b_height)%2==0,'Error! For having pair matches:The board size must be even!'
XMARGIN = int((w_width - (b_width * (boxsize + boxgap))) / 2)
YMARGIN = int((w_height - (b_height * (boxsize + boxgap))) / 2)

#colors used in the game
BLACK=(0,0,0)
GRAY=(100,100,100)
NAVYBLUE=(60,60,100)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
ORANGE=(255,128,0)
PURPLE=(255,0,255)
CYAN=(0,255,255)

#designing of board color
bgcolor=NAVYBLUE
lightbgcolor=GRAY
highlightcolor=BLUE
boxcolor=BLACK

#shapes used in the game
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

#To check whether board is available for all combinations of shapes/colors
colors=(RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
shapes=(DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert(len(colors)*len(shapes*2))>=(b_width*b_height),'Board is too big considering all the combination of shapes/colors.'

def main():
    global clock,screen
    pygame.init()
    clock=pygame.time.Clock()
    screen=pygame.display.set_mode((w_width,w_height))
    pygame.display.set_caption("Memory game")
    mouse_x=0
    mouse_y=0

    mainBoard=getRandomizedBoard()
    revealedBoxes=generateRevealedBoxesData(False)
    firstclick=None
    screen.fill(bgcolor)
    startgame(mainBoard)

    while True:
        click=False
        screen.fill(bgcolor)
        drawBoard(mainBoard,revealedBoxes)
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        box_x,box_y=getBox(mouse_x,mouse_y)
        if box_x!=None and box_y!=None:
            if not revealedBoxes[box_x][box_y]:#if not clicked, but mouse is over the box
                HighlightBox(box_x,box_y)
            if not revealedBoxes[box_x][box_y] and click:#if the box is clicked
                revealBoxesAnimation(mainBoard,[(box_x,box_y)])
                revealedBoxes[box_x][box_y]=True
                if firstClick==None:#if first box pair is clicked
                    firstClick=[box_x][box_y]
                else:
                    iconshape1,iconcolor1=getdata(mainBoard,firstClick[0],firstClick[1])#if second box is clicked
                    iconshape2,iconcolor2=getdata(mainBoard,box_x,box_y)
                    if iconshape1!=iconshape2 or iconcolor1!=iconcolor2:#if the pairs don't match
                        pygame.time.wait(1000)
                        coverBoxes(mainBoard,[(firstClick[0],firstClick[1]),(box_x,box_y)])#cover the boxes back
                        revealedBoxes[firstClick[0]][firsClick[1]]=False
                        revealedBoxes[box_x][box_y]=False
                    elif Won(revealedBoxes):#if all pairs are found
                        gameWon(mainBoard)
                        pygame.time.wait(3000)
                        #reset the board
                        mainBoard=getRandomizedBoard()
                        revealedBoxes=generateRevealedBoxesData(False)
                        #show the board fully revealed for some seconds
                        drawBoard(mainBoard,revealBoxes)
                        pygame.display.update()#update the screen object with the data
                        pygame.time.wait(2000)
                        #restart Game
                        startGame(mainBoard)
                        firstClick=None
            pygame.display.update()
            clock.tick(30)

#definition of revealing the box
def generateRevealedBoxesData(val):
    revealedBoxes=[]
    for i in range(b_width):
        revealedBoxes.append([val]*b_width)
    return revealedBoxes
#definition of function to get all combinations of shape and color
def getRandomizedBoard():
    icons=[]
    for color in colors:
        for shape in shapes:
            icons.append((shape,color))
    random.shuffle(icons)#To randomize the order of icons list
    numIcons=int(b_width*b_height/2)#total number of icons needed
    icons=icons[:numIcons]*2#replicate
    random.shuffle(icons)#shuffle again
    board=[]
    for x in range(b_width):
        column=[]
        for y in range(b_height):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (boxsize + boxgap) + XMARGIN
    top = boxy * (boxsize + boxgap) + YMARGIN
    return (left, top)


def getBox(x, y):
    for boxx in range(b_width):
        for boxy in range(b_height):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, boxsize, boxsize)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(boxsize * 0.25) 
    half =int(boxsize * 0.5)

    left, top = leftTopCoordsOfBox(boxx, boxy)
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(screen, color, (left + half, top + half), half - 5)
        pygame.draw.circle(screen, bgcolor, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(screen, color, (left + quarter, top + quarter, boxsize - half, boxsize - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(screen, color, ((left + half, top), (left + boxsize - 1, top + half), (left + half, top + boxsize - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, boxsize, 4):
            pygame.draw.line(screen, color, (left, top + i), (left + i, top))
            pygame.draw.line(screen, color, (left + i, top + boxsize - 1), (left + boxsize - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(screen, color, (left, top + quarter, boxsize, half))


def getData(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(screen, bgcolor, (left, top, boxsize, boxsize))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(screen, boxcolor, (left, top, coverage, boxsize))
    pygame.display.update()
    clock.tick(30)
    
def revealBoxes(board, boxesToReveal):
    for coverage in range(boxsize, (-boxspeed) - 1, -boxspeed):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxes(board, boxesToCover):
    for coverage in range(0,boxsize + boxspeed, boxspeed):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    for boxx in range(b_width):
        for boxy in range(b_height):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(screen, boxcolor,(left,top,boxsize,boxsize))
            else:
                shape, color = getData(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(screen,hightlightcolor, (left - 5, top - 5, boxsize + 10, boxsize + 10), 4)


def startgame(board):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(b_width):
        for y in range(b_height):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxes(board, boxGroup)
        coverBoxes(board, boxGroup)


def gameWon(board):
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = lightbgcolor
    color2 = bgcolor

    for i in range(13):
        color1, color2 = color2, color1
        screen.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def Won(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False 
    return True


if __name__ == '__main__':
    main()
