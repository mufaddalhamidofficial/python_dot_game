from turtle import Turtle, Screen, colormode, done, Vec2D
from time import sleep
import math
# from dot import Dot


class Dot:
    def __init__(self, x, y, size, index):
        self.x = x
        self.y = y
        self.size = size
        self.index = index


dot_width = 15
line_width = 7.5
dot_spacing = 50
col = 10  # total in a single horiz line
row = 10

current_highlighted = None

gameOver = False
gameActive = False


line_made: list[tuple[int]] = []
box_claimed: list[list[int]] = []

numberOfPlayers = 2
colormode(255)
playerColors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
                (255, 255, 0), (255, 0, 255), (0, 255, 255)]
playerInitial = ["R", "G", "B", "Y", "P", "C"]
currentPlayer = 0
playerPoints = [0] * numberOfPlayers

th = dot_spacing * row
tw = dot_spacing * col


tim = Turtle()
tim.speed(500)
tim.penup()
tim.hideturtle()
all_dots: list[Dot] = []
screen = Screen()
screenTk = screen.getcanvas().winfo_toplevel()
# screenTk.attributes("-fullscreen", True)
screenTk.state('zoomed')


def clearScreen():
    tim.color("white")
    tim.begin_fill()
    tim.setpos(-500, -500)
    tim.setheading(0)
    tim.forward(1000)
    tim.setheading(90)
    tim.forward(1000)
    tim.setheading(180)
    tim.forward(1000)
    tim.setheading(270)
    tim.forward(1000)
    tim.end_fill()


def writeScores():
    global tim, tw, th, scorePos, playerColors, playerInitial, playerPoints, currentPlayer
    tim.penup()
    tim.setpos((-tw-100)/2, scorePos + (dot_spacing * 2 / 3))
    tim.color('white')
    tim.width(1)
    tim.pendown()
    tim.begin_fill()
    tim.setheading(0)
    tim.forward(tw+100)
    tim.setheading(270)
    tim.forward(((dot_spacing / 3)) * 2)
    tim.setheading(180)
    tim.forward(tw+100)
    tim.setheading(270)
    tim.forward(((dot_spacing / 3)) * 2)
    tim.end_fill()
    tim.penup()
    tim.color('black')
    tim.setpos(0, scorePos)
    scoreStr = ""
    for i in range(len(playerPoints)):
        scoreStr += f"{playerInitial[i]}: {playerPoints[i]}{' ' if gameOver or currentPlayer != i else '*'}    "
    tim.write(scoreStr[:-4], align="center", font=["Arial", 20, "bold"])


def playGame():
    global tim, th, tw, dot_spacing, col, row, dot_width, number_of_dots, scorePos, titlePos, all_dots, screen
    tim.penup()
    tim.color('black')
    tim.setpos(0, 0)

    tim.setheading(270)
    tim.forward(dot_spacing/2)

    th = dot_spacing * row
    tw = dot_spacing * col
    print(th)
    print(tw)
    tim.setheading(math.degrees(math.radians(180)+math.atan(th / tw)))

    tim.forward(math.sqrt(((th) ** 2) + ((tw) ** 2)) / 2)
    tim.setheading(0)
    number_of_dots = col * row

    ctr = 0

    for dot_count in range(1, number_of_dots + 1):
        tim.forward(dot_spacing / 2)
        dot = Dot(x=tim.pos()[0], y=tim.pos()[1], size=dot_width, index=ctr)
        ctr += 1
        all_dots.append(dot)
        tim.dot(dot_width, 'black')
        tim.forward(dot_spacing / 2)

        if dot_count % (col) == 0:

            tim.setheading(90)
            tim.forward(dot_spacing)
            tim.setheading(180)
            tim.forward(tw)
            tim.setheading(0)

    tim.setheading(270)
    tim.forward(dot_spacing / 3)

    tim.setx(0)
    scorePos = tim.pos()[1]

    writeScores()

    tim.setheading(90)
    tim.forward(dot_spacing)
    titlePos = tim.pos()
    tim.write("Dots and Boxes", align="center", font=["Arial", 50, "bold"])

    print(len(all_dots))


def changePlayer():
    global currentPlayer
    currentPlayer += 1
    if currentPlayer >= numberOfPlayers:
        currentPlayer = 0


def addToLineMade(a, b):
    global line_made
    if a > b:
        line_made.append((b, a))
    else:
        line_made.append((a, b))


def isLineMade(a, b):
    global line_made
    if a > b:
        return line_made.count((b, a)) > 0
    else:
        return line_made.count((a, b)) > 0


def checkLineContains(a, b):
    global line_made
    if a > b:
        return (b, a) in line_made
    else:
        return (a, b) in line_made


def colorBox(x, y):
    tim.penup()
    tim.setpos(x, y)
    tim.setheading(90)
    tim.forward((dot_width / 2) + 0.5)
    tim.setheading(0)
    tim.forward((dot_width / 2) + 0.5)
    # tim.speed(1)
    tim.width(0)
    # tim.color(144, 238, 144)
    pc = playerColors[currentPlayer]
    r = pc[0]
    g = pc[1]
    b = pc[2]
    tim.color(255 if r == 255 else 150, 255 if g ==
              255 else 150, 255 if b == 255 else 150)
    tim.begin_fill()
    tim.pendown()
    tim.forward(dot_spacing - dot_width - 1)
    tim.setheading(90)
    tim.forward(dot_spacing - dot_width - 1)
    tim.setheading(180)
    tim.forward(dot_spacing - dot_width - 1)
    tim.setheading(270)
    tim.forward(dot_spacing - dot_width - 1)

    tim.penup()
    tim.end_fill()

    tim.setpos(x, y)
    tim.setheading(90)
    tim.forward((dot_spacing / 2) - ((16 * 1.5) / 2))
    # tim.dot(2, 'black')
    tim.setheading(0)
    tim.forward(dot_spacing / 2 + 1)
    # tim.dot(2, 'black')

    tim.color(200 if r == 255 else r, 200 if g ==
              255 else g, 200 if b == 255 else b)
    tim.write(playerInitial[currentPlayer],
              align="center", font=["Arial", 16, "bold"])


def checkWinner():
    global gameOver,   playerInitial, gameActive, buttonPos
    print(playerPoints)
    totalBoxes = (row - 1) * (col - 1)
    if sum(playerPoints) >= 2:
        clearScreen()
        gameOver = True
        gameActive = False
        mp = max(playerPoints)
        winnerName = ""
        # winner = playerPoints.index(mp)
        for i in range(len(playerPoints)):
            if playerPoints[i] == mp:
                winnerName += ", " + playerInitial[i]

        tim.setpos(titlePos)
        tim.color('black')
        tim.write("Dots and Boxes", align="center", font=["Arial", 50, "bold"])
        # writeScores()

        tim.setpos(0, 0)
        tim.setheading(270)
        tim.forward((60 * 1.4) / 2)
        tim.write(f"Congrats {winnerName[2:]} 🎉", align="center", font=[
                  "Arial", 60, "bold"])
        tim.color("black")
        tim.setpos(-200 / 2, -150)
        tim.width(5)
        tim.pendown()
        tim.begin_fill()
        tim.setheading(0)
        tim.forward(200)
        tim.setheading(270)
        tim.forward(50)
        tim.setheading(180)
        tim.forward(200)
        buttonPos = tim.pos()
        tim.setheading(90)
        tim.forward(50)
        tim.end_fill()
        tim.penup()
        tim.setheading(0)
        tim.forward(200 / 2)
        tim.setheading(270)
        tim.forward(25 + (20 * 1.65)/2)
        tim.color("white")
        tim.write("Restart Game", align='center', font=["Arial", 20, "bold"])


def checkBoxMade():
    global line_made
    current = line_made[-1]
    horiz = current[1] - current[0] > 1
    # print(horiz)
    print("")
    print("")
    print("")
    c1 = current[0]
    c2 = current[1]
    p_c3 = [c2 + 1, c2 - 1, c2 + col,
            c2 - col]
    n_p_c3: list[int] = []
    if (c2 % col) == 0:
        p_c3.remove(c2 - 1)
    if ((c2 + 1) % col) == 0:
        p_c3.remove(c2 + 1)
    for p in p_c3:
        if p == c1:
            continue
        if p < 0 or p > number_of_dots - 1:
            continue
        if not checkLineContains(p, c2):
            continue
        n_p_c3.append(p)
    p_c3 = n_p_c3
    del n_p_c3
    if len(p_c3) <= 0:
        changePlayer()

    for c3 in p_c3:
        p_c4 = [c3 + 1, c3 - 1, c3 + col,
                c3 - col]
        n_p_c4: list[int] = []
        if (c3 % col) == 0:
            p_c4.remove(c3 - 1)
        if ((c3 + 1) % col) == 0:
            p_c4.remove(c3 + 1)
        for p in p_c4:
            if p == c2:
                continue
            if p < 0 or p > number_of_dots - 1:
                continue
            if abs(p - c1) != col and abs(p - c1) != 1:
                continue
            if not checkLineContains(p, c3):
                continue
            if not checkLineContains(p, c1):
                continue
            n_p_c4.append(p)
        p_c4 = n_p_c4
        del n_p_c4
        # print(f'c1: {c1}')
        # print(f'c2: {c2}')
        # print(f'c3: {c3}')
        print(f'p_c4: {p_c4}')
        if len(p_c4) <= 0:
            changePlayer()

        for c4 in p_c4:
            box = [c1, c2, c3, c4]
            box.sort()
            t = box[2]
            box[2] = box[3]
            box[3] = t
            if box in box_claimed:
                continue
            box_claimed.append(box)
            d1 = all_dots[box[0]]
            # tim.setpos((d1.x + d2.x) / 2, (d2.y + d3.y) / 2)
            # tim.dot(dot_width, playerColors[currentPlayer])
            colorBox(d1.x, d1.y)
            playerPoints[currentPlayer] += 1
            # writeScores()
            checkWinner()


iswriting = False

# def isInside(x, y, x1, x2, y1, y2):


i = 0


def onGamePress(x, y):
    global current_highlighted, line_made, currentPlayer, playerColors, iswriting, i
    print(f"I am hereee {i}")
    i += 1
    if iswriting or gameOver:
        return
    for dot in all_dots:
        if (dot.x - (dot.size / 2)) < x and (dot.x + (dot.size / 2)) > x and (dot.y - (dot.size / 2)) < y and (dot.y + (dot.size / 2)) > y:
            # if current_highlighted.index -

            if current_highlighted is not None:
                iswriting = True
                if (current_highlighted.x - dot_spacing - (current_highlighted.size * 3 / 2)) < x \
                        and (current_highlighted.x + dot_spacing + (current_highlighted.size * 3 / 2)) > x \
                        and (current_highlighted.y - dot_spacing - (current_highlighted.size * 3 / 2)) < y \
                        and (current_highlighted.y + dot_spacing + (current_highlighted.size * 3 / 2)) > y \
                        and (round(current_highlighted.x) == round(dot.x) or round(current_highlighted.y) == round(dot.y)) \
                        and not isLineMade(current_highlighted.index, dot.index):
                    # tim.setheading()
                    # 90, 180, 270, 360
                    angle = None
                    if round(current_highlighted.x) < round(dot.x):
                        angle = 0
                    elif round(current_highlighted.y) < round(dot.y):
                        angle = 90
                    elif round(current_highlighted.x) > round(dot.x):
                        angle = 180
                    elif round(current_highlighted.y) > round(dot.y):
                        angle = 270
                    if angle is not None:
                        tim.color(playerColors[currentPlayer])
                        tim.setheading(angle)
                        tim.width(line_width)
                        tim.pendown()
                        tim.forward(dot_spacing)
                        tim.penup()
                        tim.dot(dot_width, 'black')
                        addToLineMade(dot.index, current_highlighted.index)
                        checkBoxMade()
                        writeScores()
                if not gameOver:
                    tim.setpos(current_highlighted.x, current_highlighted.y)
                    tim.dot(dot_width, 'black')

                iswriting = False
                current_highlighted = None
            else:
                iswriting = True
                current_highlighted = dot
                tim.setpos(current_highlighted.x, current_highlighted.y)
                tim.dot(dot_width, 'red')
                iswriting = False


def onHomePress(x, y, force=False):
    global buttonPos,  numberOfPlayers, playerPoints, gameOver, gameActive, current_highlighted, line_made, box_claimed, currentPlayer, all_dots
    print(f"hello {x} {y}")
    if buttonPos[0] < x and buttonPos[1] < y and buttonPos[0] + 200 > x and buttonPos[1] + 50 > y:
        d = screen.textinput(
            "Enter", "Number of players must be not be more than 6" if force else "Please enter number of players (Max 6)")
        # try:
        numberOfPlayers = int(d)
        if numberOfPlayers > 6:
            if not force:
                onHomePress(x, y, True)
            return

        playerPoints = [0] * numberOfPlayers
        # except e:
        colormode(255)
        clearScreen()
        current_highlighted = None
        line_made = []
        box_claimed = []
        currentPlayer = 0
        all_dots = []

        playGame()

        gameOver = False
        gameActive = True

    # screen.bye()
    # canvas = screen.getcanvas()
    # root = canvas.winfo_toplevel()
    # root./
    # playGame()


def displayHomePage():
    global buttonPos
    # screen.setup(500, 500)
    # screen.screensize()
    # screen.setup(width=1.0, height=1.0, startx=None, starty=None)
    tim.setpos(0, 100)
    tim.color('black')
    tim.write("Dots and Boxes", align="center", font=["Arial", 50, "bold"])
    tim.setpos(0, 0)
    # tim.write("Enter Player Count: ", move=True, align="center",
    #           font=["Arial", 20, "bold"])
    # tim.showturtle()

    tim.setpos(-200 / 2, -50)
    tim.width(5)
    tim.pendown()
    tim.begin_fill()
    tim.setheading(0)
    tim.forward(200)
    tim.setheading(270)
    tim.forward(50)
    tim.setheading(180)
    tim.forward(200)
    buttonPos = tim.pos()
    tim.setheading(90)
    tim.forward(50)
    tim.end_fill()
    tim.penup()
    tim.setheading(0)
    tim.forward(200 / 2)
    tim.setheading(270)
    tim.forward(25 + (20 * 1.65)/2)
    tim.color("white")
    tim.write("Start Game", align='center', font=["Arial", 20, "bold"])


def onPress(x, y):
    global gameOver, gameActive
    if not gameOver and gameActive:
        print("here1")
        onGamePress(x, y)
    elif not gameActive:
        print("here2")
        onHomePress(x, y)
    else:
        print("here3")


displayHomePage()
# playGame()

screen.onclick(onPress)
# screen.onclick(onGamePress)

done()
