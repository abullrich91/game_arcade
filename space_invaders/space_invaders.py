import turtle
import os
import math
import random
import time

assets_path = "space_invaders/assets/"
sounds_path = "space_invaders/sounds/"

turtle.tracer(0)
turtle.speed(0)
turtle.title("Space Invaders")

# Set up the screen
wn = turtle.Screen()

if os.name == 'posix':
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("%sspace_invaders_background.gif" % assets_path)

# Register shapes
turtle.register_shape("%sinvader.gif" % assets_path)
turtle.register_shape("%splayer.gif" % assets_path)
# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)

for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)

border_pen.hideturtle()

# Set score to 0
score = 0

# Draw score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" % score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("%splayer.gif" % assets_path)
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

# Enemy movement
enemyspeed = 2

# Choose number of enemies
number_of_enemies = 5

# Create an empty list of enemies
enemies = []

# Add enemies to the list
for i in range(number_of_enemies):
    # Create enemy
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.color("red")
    enemy.shape("%sinvader.gif" % assets_path)
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-20 * 10, 20 * 10)
    y = random.randint(10 * 10, 25 * 10)
    enemy.setposition(x, y)

# Enemy movement
enemyspeed = 2


# Player movement
playerspeed = 15

# Create the bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

# Bullet movement
bulletspeed = 20

# Define bullet state
# ready - ready to fire
# fire - bullet is firing
bulletstate = "ready"


# Move player left
def move_left():
    x = player.xcor()
    x -= playerspeed

    # Boundary checking
    if x < -280:
        x = -280

    player.setx(x)


# Move player right
def move_right():
    x = player.xcor()
    x += playerspeed

    # Boundary checking
    if x > 280:
        x = 280

    player.setx(x)


# Changes bullet state to fire
def fire_bullet():
    # Declare bullet state as global if it needs changed
    global bulletstate

    if bulletstate == "ready":
        if os.name == 'posix':
            os.system("afplay space_invaders/sounds/laser.wav&")
        bulletstate = "fire"
        # Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor()
        bullet.setposition(x, y + 10)
        bullet.showturtle()


# Child of Turtle
class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        # Boundary checking
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self, other):
        distance = math.sqrt(math.pow(self.xcor() - other.xcor(), 2) + math.pow(self.ycor() - other.ycor(), 2))
        return distance < 20


# Create Particle sprite
class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.frame += 1
            self.fd(10)

        if self.frame > 10:
            self.frame = 0
            self.goto(-1000, -1000)


# Detect turtle collision
def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))

    if distance < 15:
        return True
    else:
        return False


flag = True


def game_over():
    global flag
    flag = False


# Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")
turtle.onkey(game_over, "q")

particles = []
for i in range(20):
    particles.append(Particle("circle", "orange", 0, 0))

# Main game loop
while flag:
    turtle.update()
    if os.name != 'posix':
        time.sleep(0.02)

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # Move enemy back and down
        if enemy.xcor() > 280:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1

        if enemy.xcor() < -280:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1

        # Check for collision between bullet and enemy
        if isCollision(bullet, enemy):
            if os.name == 'posix':
                os.system("afplay space_invaders/sounds/explosion.wav&")
            for particle in particles:
                particle.explode(bullet.xcor(), bullet.ycor())
            # Reset bullet
            bullet.hideturtle()
            bulletstate = "ready"
            # We set it to -400 to avoid further collisions
            bullet.setposition(0, -400)

            # Reset enemy
            x = random.randint(-20 * 10, 20 * 10)
            y = random.randint(10 * 10, 25 * 10)
            enemy.setposition(x, y)

            # Update score
            score += 10
            scorestring = "Score: %s" % score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

        if isCollision(enemy, player):
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            break

    # Move bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Boundary checking for bullet
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

    for particle in particles:
        particle.move()


turtle.bye()
