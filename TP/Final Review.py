
def solveDoomBox(L):
    N = list(range(1, len(L)**2+1))
    for row in range(len(L)):
        for col in range(len(L[0])):
            if L[row][col] in N:
                N.remove(L[row][col])
    return solveDoomBoxHelper(L, N)

def solveDoomBoxHelper(L, N):
    if len(N) == 0:
        return L
    else:
        for row in range(len(L)):
            for col in range(len(L)):
                for value in N:
                    if legalMove(L, value, col, row):
                        L[row][col] = value
                        N.remove(value)
                        solution = solveDoomBoxHelper(L, N)
                        if solution != None:
                            return solution
                        else:
                            N.append(value)
                            L[row][col] = -1
        return None

def legalMove(L, value, col, row):
    if L[row][col] != -1:
        return False
    (drow, dcol) = ([0], [0])
    if col + 1 < len(L[0]): dcol += [1]
    if col - 1 > 0: dcol += [-1]
    if row + 1 < len(L): drow += [1]
    if row - 1 > 0: drow += [-1]
    for r in drow:
        for c in dcol:
            if L[row+r][col+c] == value + 1 or L[row+r][col+c] == value -1:
                return False
    return True


L = [[ 1, 8, -1, 14],
[-1, 11, 16, -1],
[-1, 9, -1, 10],
[-1, -1, -1, -1]]

#print(solveDoomBox(L))


def bishopDict(L,c):
    d = dict()
    for row in range(len(L)):
        for col in range(len(L[0])):
            if L[row][col] == c:
                d[(row,col)] = set()
                findLegalMoves(d, L, row, col)
    return d

def findLegalMoves(d, L, row, col):
    drows = [1, -1]
    dcols = [1, -1]
    for drow in drows:
        for dcol in dcols:
            t = 1
            while ((row+drow*t) < len(L) and (row+drow*t)>=0 and 
                    (col+dcol*t) < len(L[0]) and (col+dcol*t)>=0):
                    if L[row+drow*t][col+dcol*t] == "w":
                        d[(row, col)].add((row+drow*t, col+dcol*t))
                        break
                    elif L[row+drow*t][col+dcol*t] == "-":
                        t+=1
                    else:
                        break

L = [["b", "-", "w", "-", "-"],
["-", "b", "-", "-", "-"],
["-", "-", "w", "-", "w"],
["-", "-", "-", "b", "-"],
["-", "-", "-", "-", "-"],
["-", "w", "-", "w", "-"]]

#print(bishopDict(L,'b'))

def nthMaxwellNumber(n):
    count = 0
    value = 3
    while count < n:
        value += 1
        if isMaxwellNumber(value):
            count += 1
    return value

def isMaxwellNumber(value):
    factorSum = 0
    for i in range(2, value):
        if value%i == 0:
            factorSum += i
    if factorSum > value:
        return True
    return False

n=3

#print(nthMaxwellNumber(n))

from cmu_112_graphics import *


def appStarted(app):
    app.r = 5
    app.circles = []

def redrawAll(app, canvas):
    for circle in app.circles:
        (r, cx, cy) = circle
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r)

def timerFired(app):
    for circle in app.circles:
        circle[0] += 10
        if (circle[1] + circle[0] > app.width or
            circle[1] - circle[0] < 0 or
            circle[2] + circle[0] > app.height or
            circle[2] - circle[0] < 0):
            app.circles.remove(circle)

def mousePressed(app, event):
    (cx, cy) = (event.x, event.y)
    app.circles.append([app.r, cx, cy])

runApp(width = 500, height = 500)