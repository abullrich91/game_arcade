import subprocess
import curses

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

listaJuegos = [snake, buscaminas, tetris, space_invaders]

win = curses.newwin(alto, ancho, 0, 0)
curses.mousemask(curses.ALL_MOUSE_EVENTS)
win.keypad(1)
win.border('|', '|', '+', '+', '.', '.')

win.addstr(2 , ancho/2 - 10, "GAME ARCADE", curses.color_pair(1))

win.addstr(8, 2, "Snake"          , curses.color_pair(2))
win.addstr(12, 2, "Buscaminas"    , curses.color_pair(2))
win.addstr(16, 2, "Tetris"        , curses.color_pair(2))
win.addstr(20, 2, "Space Invaders", curses.color_pair(2))


while True:
    key = win.getch()

    if key == 27:
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
                        subprocess.Popen("python " + listaJuegos[i], creationflags=subprocess.CREATE_NEW_CONSOLE)
