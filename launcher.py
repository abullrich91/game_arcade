import subprocess
import curses
import os

s = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

curses.curs_set(0)

alto, ancho = s.getmaxyx()

snake          = "snake/snake.py"
buscaminas     = "buscaminas/buscaminas.py"
tetris         = "tetris/tetris.py"
space_invaders = "space_invaders/space_invaders.py"
space_war = "space_war/space_war.py"

listaJuegos = [snake, buscaminas, tetris, space_invaders, space_war]

win = curses.newwin(alto, ancho, 0, 0)
curses.mousemask(curses.ALL_MOUSE_EVENTS)
win.keypad(1)
win.border('|', '|', '+', '+', '.', '.')

win.addstr(2, ancho/2 - 10, "GAME ARCADE", curses.color_pair(1))

win.addstr(8, 2, "Snake"          , curses.color_pair(2))
legend = ["Q = exit", "Arrowkeys = move"]
for index, option in enumerate(legend):
    win.addstr(9 + index, 8, option, curses.color_pair(1))

win.addstr(12, 2, "Buscaminas"    , curses.color_pair(2))
legend = ["Q = exit", "Click = check for mine"]
for index, option in enumerate(legend):
    win.addstr(13 + index, 8, option, curses.color_pair(1))

win.addstr(16, 2, "Tetris"        , curses.color_pair(2))
legend = ["Q = exit", "Up = rote", "Arrowkeys = move"]
for index, option in enumerate(legend):
    win.addstr(17 + index, 8, option, curses.color_pair(1))

win.addstr(20, 2, "Space Invaders", curses.color_pair(2))
legend = ["Q = exit", "SpaceBar = shoot", "Arrowkeys = move"]
for index, option in enumerate(legend):
    win.addstr(21 + index, 8, option, curses.color_pair(1))

win.addstr(24, 2, "Space War     ", curses.color_pair(2))
for index, option in enumerate(legend):
    win.addstr(25 + index, 8, option, curses.color_pair(1))


while True:
    key = win.getch()

    if key == ord('q'):
        quit()

    if key == curses.KEY_MOUSE:
        _, mx, my, _, b = curses.getmouse()
        if -1 < my < alto and -1 < mx < ancho :
            #Derecho
            #if b > 1023:
            #Izquiedo
            if b < 1024:
                for i in range(0, len(listaJuegos)):
                    if 6+4*i < my < 10+4*i:
                        if os.name == 'posix':
                            cwd = os.getcwd()
                            subprocess.call(['python2.7', listaJuegos[i]])
                        else:
                            subprocess.Popen("python " + listaJuegos[i])
