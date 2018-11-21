import pygame
import random

class Mina:
    show = False
    cant = "*"
    def __init__(self):
        return

    def clicked(m, x, y):
        fin()

class Numero:
    cant = 0
    show = False
    def __init__(self, m, x, y):
        self.cant = contar(m, x, y)
        pass

    def clicked(self, m, x, y):
        if self.cant == 0:
            mirarMas(m, x, y)
        self.show = True

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
    return s

def mostrar(m, f, c):
    for i in range(f):
        S = ""
        for j in range(c):
            S = S + str(m[i][j].cant) + "  "
        print(S)

f = 4
c = 4
w = 30

minas = 3

matrix = [[x for x in range(c)] for y in range(f)]

llenarTablero(matrix, f, c, minas)

mostrar(matrix, f, c)
