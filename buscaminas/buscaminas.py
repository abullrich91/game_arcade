import curses
import random

class Mina:
    show = False
    cant = "*"
    def __init__(self):
        return

    def clicked(self, m, x, y):
        fin()

class Numero:
    cant = 0
    show = False
    def __init__(self, m, x, y):
        self.cant = contar(m, x, y)
        pass

    def clicked(self, m, x, y):
        self.show = True
        if self.cant == '-':
            mirarMas(m, x, y)

def llenarTablero(M, f, c, m):
    for i in range(0, m):
        x = random.randint(0, f-1)
        y = random.randint(0, c-1)
        while isinstance(M[x][y], Mina):
            x = random.randint(0, f-1)
            y = random.randint(0, c-1)
        M[x][y] = Mina()
    for x in range(f):
        for y in range(c):
            if not isinstance(M[x][y], Mina):
                M[x][y] = Numero(M, x, y)

def contar(m, x, y):
    f = len(m)
    c = len(m[0])
    s = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif -1 < (x + i) < f and -1 < (y + j) < c:
                if isinstance(m[x+i][y+j], Mina):
                    s = s+1
    if s == 0:
        s = '-'
    return s

def mirarMas(m, x, y):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif -1 < (x + i) < alto and -1 < (y + j) < ancho:
                if not m[x+i][y+j].show and isinstance(m[x+i][y+j], Numero):
                    m[x+i][y+j].clicked(m, x+i, y+j)

def fin():
    for x in range(0, ancho):
        for y in range(0, alto):
            win.addch(y, 2*x, str(matrix[x][y].cant), curses.color_pair(3))
    while True:
        key = win.getch()
        if key == 27:
            quit()

def ganado():
    for x in range(0, ancho):
        for y in range(0, alto):
            win.addch(y, 2*x, str(matrix[x][y].cant), curses.color_pair(4))
    while True:
        key = win.getch()
        if key == 27:
            quit()


def contarMinas(m):
    n = 0
    for x in range(0, ancho):
        for y in range(0, alto):
            n = n + ( 1 if isinstance(m[x][y], Numero) and m[x][y].show else 0)
    return (ancho*alto - n)

curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.curs_set(0)

ancho = 20
alto = 20

minas = 30

win = curses.newwin(alto, 2*ancho, 0, 0)
win.keypad(1)
curses.mousemask(curses.ALL_MOUSE_EVENTS)

matrix = [[x for x in range(ancho)] for y in range(alto)]

llenarTablero(matrix, alto, ancho, minas)

for x in range(0, ancho):
    for y in range(0, alto):
        #win.addch(y, 2*x, str(matrix[x][y].cant))
        win.addch(y, 2*x, 'X', curses.color_pair(1))

while True:
    key = win.getch()

    if key == 27:
        quit()

    if key == curses.KEY_MOUSE:
        _, mx, my, _, b = curses.getmouse()
        x = mx/2
        y = my
        mx = mx - (mx % 2)
        if -1 < y < alto and -1 < mx < 2*ancho :
            #Derecho
            if b > 1023:
                win.addch(my, mx, 'D')
            #Izquiedo
            if b < 1024:
                matrix[x][y].clicked(matrix, x, y)
                win.addch(my, mx, 'I')

            for x in range(0, ancho):
                for y in range(0, alto):
                    if matrix[x][y].show:
                        win.addch(y, 2*x, str(matrix[x][y].cant), curses.color_pair(2))
                    else:
                        win.addch(y, 2*x, 'X', curses.color_pair(1))
    if minas == contarMinas(matrix):
        ganado()
