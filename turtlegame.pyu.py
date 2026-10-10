import random
import time
import turtle

# Screen setup
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
START_LINE = -280
FINISH_LINE = 280

screen = turtle.Screen()
screen.title("Turtle Crossing Game")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor("#dfefff")
screen.tracer(0)

# Player turtle
class Player(turtle.Turtle):
    def __init__(self):
        super().__init__(shape="turtle")
        self.color("darkgreen")
        self.penup()
        self.setheading(90)
        self.goto(0, START_LINE)

    def move_up(self):
        self.forward(20)

    def reset_position(self):
        self.goto(0, START_LINE)

# Car class
class Car(turtle.Turtle):
    def __init__(self, lane_y):
        super().__init__(shape="square")
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.color(random.choice(["red", "blue", "orange", "purple", "black", "gray", "yellow"]))
        self.penup()
        self.goto(320, lane_y)
        self.setheading(180)
        self.speed = random.randint(4, 9)

    def drive(self):
        self.forward(self.speed)

    def off_screen(self):
        return self.xcor() < -340

# Scoreboard
class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.goto(-220, 260)
        self.level = 1
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"Level: {self.level}", align="left", font=("Arial", 20, "normal"))

    def game_over(self):
        self.goto(-110, 0)
        self.write("Game Over", align="left", font=("Arial", 28, "normal"))

player = Player()
scoreboard = Scoreboard()

lanes = [-220, -160, -100, -40, 20, 80, 140, 200]
cars = []
level = 1


def create_car():
    lane_y = random.choice(lanes)
    new_car = Car(lane_y)
    cars.append(new_car)


def check_collisions():
    for car in cars:
        if car.distance(player) < 22:
            return True
    return False


def next_level():
    global level
    level += 1
    scoreboard.level = level
    scoreboard.update_score()
    player.reset_position()
    for car in cars:
        car.speed += 1


screen.listen()
screen.onkey(player.move_up, "Up")
screen.onkey(player.move_up, "w")

# Game loop
while True:
    screen.update()

    if random.randint(1, 100) < 5:
        create_car()

    for car in cars:
        car.drive()
        if car.off_screen():
            car.hideturtle()
            cars.remove(car)

    if player.ycor() > FINISH_LINE:
        next_level()

    if check_collisions():
        scoreboard.game_over()
        screen.update()
        break

    time.sleep(0.05)

screen.exitonclick()
