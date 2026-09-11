import pygame as pg
import argparse
from pathlib import Path

from colors import Colors, colorValues
from buttonGrid import ButtonGrid


parser = argparse.ArgumentParser(prog="Mora Jai Box",
                                description='''Simulates a Mora Jai puzzle box from the game Blue Prince.\n
                                Controls: R to restart, Z to undo, Y to redo, esc to exit.''')
parser.add_argument("FILE")
parser.add_argument("-s", default=400, type=int, help="The side length of the (square) window, in pixels.")
args = vars(parser.parse_args())


screenSize = args["s"]
grid = ButtonGrid()
buttonSize = screenSize/grid.length
winColors = []
PARENT = Path(__file__).resolve().parent


colorTranslation = {
    "X": Colors.GRAY,
    "L": Colors.BLACK,
    "Y": Colors.YELLOW,
    "V": Colors.VIOLET,
    "G": Colors.GREEN,
    "P": Colors.PINK,
    "R": Colors.RED,
    "O": Colors.ORANGE,
    "W": Colors.WHITE,
    "B": Colors.BLUE
}

if not args["FILE"].endswith(".jai"):
    raise ValueError("Incorrect file supplied, please ensure it is a properly formatted '.jai' text file.")
with open(args["FILE"]) as file:
    # initial grid
    for i in range(3):
        row = file.readline().rstrip("\n")
        for j in range(3):
            color = colorTranslation[row[j]]
            grid.set_color((j, i), color)
    # win condition
    for i in range(2):
        row = file.readline().rstrip("\n")
        for j in range(2):
            winColors.append(colorTranslation[row[j]])


gridStates = [grid.get_grid()]
stateIndex = 0

pg.init()
pg.display.init()
screen = pg.display.set_mode(pg.Vector2(screenSize, screenSize))
pg.mixer.init()
win = pg.mixer.Sound(str(PARENT / "win.wav"))

won = False
def drawScreen():
    # drawing grid buttons
    for y in range(grid.length):
        for x in range(grid.length):
            posX = int(x * buttonSize)
            posY = int(y * buttonSize)

            color = colorValues[grid.get_color((x, y)).name]

            pg.draw.rect(screen, color, pg.Rect(posX, posY, buttonSize, buttonSize))

    # drawing grid lines
    TOP = 0
    LEFT = 0
    BOTTOM = screenSize
    RIGHT = screenSize

    for i in range(1, grid.length):
        lineX = int(i * screenSize / grid.length)
        pg.draw.line(screen, pg.Color(0, 0, 0), (lineX, TOP), (lineX, BOTTOM))

    for i in range(1, grid.length):
        lineY = int(i * screenSize / grid.length)
        pg.draw.line(screen, pg.Color(0, 0, 0), (LEFT, lineY), (RIGHT, lineY))

    # drawing win indicators
    border = pg.Color((30, 30, 30))
    dark = pg.Color("black")

    positionsP = [(LEFT, TOP), (RIGHT, TOP), (LEFT, BOTTOM), (RIGHT, BOTTOM)]
    positionsG = [(0, 0), (2, 0), (0, 2), (2, 2)]
    shouldWin = True
    for i in range(4):
        button = grid.get_color(positionsG[i])
        color = pg.Color(colorValues[winColors[i].name])
        
        if button != winColors[i]:
            color = color.lerp(dark, 0.5)
            shouldWin = False

        pg.draw.circle(screen, color , positionsP[i], buttonSize*0.4)
        pg.draw.circle(screen, border, positionsP[i], buttonSize*0.4, width=int(buttonSize*0.04))

    # "nooo but tam this is bad practice you cant have audio code in the draw functio-" shut the fuck up
    # i honestly cant be fucked to separate out the code and manage the win state properly, this is a small ass
    # game that does not deserve much effort put into it, the main reason i made it was to try out enums with
    # my homemade grid class, because i love my grid class, grid class my beloved.
    global won
    if not won and shouldWin:
        won = True
        print("ggs")
        pg.mixer.Sound.play(win)


while True:
    pg.time.Clock().tick(30)
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            exit(255)
        if event.type == pg.MOUSEBUTTONDOWN:
            mousePos = pg.mouse.get_pos()
            buttonPos = (int(mousePos[0]/buttonSize), int(mousePos[1]/buttonSize))

            while stateIndex + 1 < len(gridStates):
                gridStates.pop()
            grid.press(buttonPos)

            if gridStates[-1] != grid.get_grid():
                gridStates.append(grid.get_grid())
                stateIndex += 1
        if event.type == pg.KEYDOWN and event.key == pg.K_r:
            stateIndex = 0
            won = False
            grid.set_grid(gridStates[stateIndex])
            while len(gridStates) > 1:
                gridStates.pop()
        if event.type == pg.KEYDOWN and event.key == pg.K_z and stateIndex > 0:
            stateIndex -= 1
            grid.set_grid(gridStates[stateIndex])
        if event.type == pg.KEYDOWN and event.key == pg.K_y and stateIndex+1 < len(gridStates):
            stateIndex += 1
            grid.set_grid(gridStates[stateIndex])

    drawScreen()

    pg.display.flip()
