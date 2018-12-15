import os
import random
import turtle
import math
import time

# Required by MacOSX to show the turtle window
turtle.fd(0)
# Speed of animation
turtle.speed(0)
turtle.bgcolor("black")
turtle.ht()
turtle.setundobuffer(1)

if os.name == 'posix':
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

# Regulates the speed of drawing
turtle.tracer(0)
turtle.title("Space War")


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


# Create Player sprite
class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 0
        self.lives = 3

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed += 1
        if self.speed > 8:
            self.speed = 8

    def decelerate(self):
        self.speed -= 1
        if self.speed < -8:
            self.speed = -8


# Create Enemy sprite
class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 4
        self.setheading(random.randint(0, 360))


class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0, 360))

        def move(self):
            self.fd(self.speed)

            # Boundary checking
            if self.xcor() > 290:
                self.setx(290)
                self.lt(60)

            if self.xcor() < -290:
                self.setx(-290)
                self.lt(60)

            if self.ycor() > 290:
                self.sety(290)
                self.lt(60)

            if self.ycor() < -290:
                self.sety(-290)
                self.lt(60)


class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 20
        self.status = "ready"
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            # Play missile sound
            os.system("afplay space_war/sounds/laser.wav&")
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):

        if self.status == "ready":
            self.goto(-1000, 1000)
        if self.status == "firing":
            self.fd(self.speed)

        # Boundary checking
        if self.xcor() < -290 or self.xcor() > 290 or self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "ready"


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


class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" % self.score
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))

    def show_legend(self):
        self.pen.undo()
        legend = ["Q = exit", "SpaceBar = shoot", "Arrowkeys = move"]
        for index, option in enumerate(legend):
            self.pen.penup()
            self.pen.goto(250, 310 - index * 10)
            self.pen.write(option, font=("Arial", 16, "normal"))


# Create game object
game = Game()
game.draw_border()

# Show the game status
game.show_status()
game.show_legend()

# Create player Sprite
player = Player("triangle", "white", 0, 0)
# enemy = Enemy("circle", "red", -100, 0)
missile = Missile("triangle", "yellow", 0, 0)
# ally = Ally("square", "blue", 100, 0)

enemies = []
for i in range(6):
    enemies.append(Enemy("circle", "red", -100, 0))

allies = []
for i in range(6):
    allies.append(Ally("square", "blue", 100, 0))

particles = []
for i in range(20):
    particles.append(Particle("circle", "orange", 0, 0))

flag = True


def game_over():
    global flag
    flag = False


# Keyboard bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.onkey(game_over, "q")
turtle.listen()


# Main game loop
while flag:
    turtle.update()
    time.sleep(0.02)

    player.move()
    # enemy.move()
    missile.move()
    # ally.move()

    for enemy in enemies:
        enemy.move()

        if player.is_collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score -= 100
            game.show_status()
            for particle in particles:
                particle.explode(player.xcor(), player.ycor())

        # Check for missile collision
        if missile.is_collision(enemy):
            # Play explosion sound
            os.system("afplay space_war/sounds/explosion.wav&")
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            # Increase the score
            game.score += 100
            game.show_status()
            # Explosion
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())

    for ally in allies:
        ally.move()

        if player.is_collision(ally):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            for particle in particles:
                particle.explode(player.xcor(), player.ycor())

        # Check for missile collision
        if missile.is_collision(ally):
            # Play explosion sound
            os.system("afplay space_war/sounds/explosion.wav&")
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            # Decrease the score
            game.score -= 50
            game.show_status()
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())

    for particle in particles:
        particle.move()

turtle.bye()