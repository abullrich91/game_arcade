import curses
from random import randrange

curses.initscr()
curses.curs_set(0)

# Creates window and draw border
win = curses.newwin(18, 18, 0, 0)
win.keypad(1)
win.nodelay(1)

# 2) cube
f = [
    [0x315,0x4cd,0x13f,0xc47],
    [0x31d,0x4cf,0x137,0xc45],
    [0x374,0x374,0x374,0x374],
    [0x741,0x51c,0xdc3,0xf34],
    [0xfc1,0x73c,0x543,0xd14],
    [0x311,0x4cc,0x133,0xc44],
    [0xc34,0x341,0x41c,0x1c3]
]


# Collision detection
def chk_fig(crds, s):
    chk = all([win.inch(c[1], c[0]) & 255 == 32 for c in crds])
    for c in crds:
        win.addch(c[1], c[0], 'X' if s == 1 else 32) if ((chk and s == 1) or s == 0) else None
    return True if s == 0 else chk


# Decode and put figure on the screen
def put_fig(fp, s):
    c = lambda el, n: -1 if (n >> el & 3) == 3 else 1 if (n >> el & 3) == 1 else 0
    pos = [c(i, f[fp[3]][fp[2]]) for i in range(0, 15, 2)[::-1]]
    return chk_fig([map(lambda x, y: x + y, fp[0:2] * 4, pos)[i-2:i] for i in range(2, 9, 2)], s)


# Figure moving function
def move_fig(fp, key, d):
    fp[0] = fp[0] - d if key == curses.KEY_LEFT else fp[0] + d if key == curses.KEY_RIGHT else fp[0]
    fp[1] = fp[1] + d if key in [curses.KEY_DOWN, -1] else fp[1]
    if key == curses.KEY_UP:
        fp[2] = 0 if fp[2] + d > 3 else 3 if fp[2] + d < 0 else fp[2] + d


# Deletes full line and increases score
def chk_board(score):
    for i in range(17):
        if all([chr(win.inch(i, x)) == 'X' for x in range(1, 17)]):
            win.deleteln()
            win.move(1, 1)
            win.insertln()
            score = score + 1
            if score % 10 == 0:
                win.timeout(300-(score * 2))
    return score


# x, y rotate figure
fig_pos = [8, 3, 0, randrange(0, 6, 1)]
score = put_fig(fig_pos, 1) ^ 1
win.timeout(300)
# Main loop
while 1:
    win.border('|', '|', '-', '-', '+', '+', '+', '+')
    win.addstr(0, 2, 'Score: ' + str(score) + ' ')
    key = win.getch()
    if key == 27:
        break
    put_fig(fig_pos, 0)
    move_fig(fig_pos, key, 1)
    if not put_fig(fig_pos, 1):
        move_fig(fig_pos, key, -1)
        put_fig(fig_pos, 1)
        if fig_pos[1] == 3:
            break
        if key in [curses.KEY_DOWN, -1]:
            score = chk_board(score)
            fig_pos = [8, 3, 0, randrange(0, 6, 1)]
            put_fig(fig_pos, 1)


# Back to console
curses.endwin()
print('\n Thanks for playing, your score: ' + str(score) + '\n')