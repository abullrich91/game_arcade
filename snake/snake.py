import random
import curses

# Initializes screen and sets the cursor to 0 so it doesn't show on the screen
s = curses.initscr()
curses.curs_set(0)

# Sets screen height and width
sh, sw = s.getmaxyx()

# Creates new window and initializes it on the top left of the screen
w = curses.newwin(sh, sw, 0, 0)

w.keypad(1)

# Refreshes screen every N milliseconds
w.timeout(100)

# Snake's initial position
snake_x = sw / 4
snake_y = sh / 2

# The snake initially has 3 parts, separated by one position
snake = [
    [snake_y, snake_x],
    [snake_y, snake_x - 1],
    [snake_y, snake_x - 2]
]

# Creates the food
food = [sh / 2, sw / 2]
w.addch(food[0], food[1], curses.ACS_PI)

key = curses.KEY_RIGHT

while True:
    next_key = w.getch()
    key = key if next_key == -1 else next_key

    # You lose if the snake is at the top or the bottom of the screen
    # or if the snake touches the left or right border of the screen
    # or if the snake is within itself
    if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
        curses.endwin()
        quit()

    # Determines the head of the snake
    new_head = [snake[0][0], snake[0][1]]

    # Movement instructions for the snake
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] += -1
    if key == curses.KEY_LEFT:
        new_head[1] += -1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    snake.insert(0, new_head)

    if snake[0] == food:
        food = None
        while food is None:
            # Randomizes new food position
            nf = [
                random.randint(1, sh - 1),
                random.randint(1, sw - 1)
            ]

            food = nf if nf not in snake else None

        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(tail[0], tail[1], ' ')

    w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

