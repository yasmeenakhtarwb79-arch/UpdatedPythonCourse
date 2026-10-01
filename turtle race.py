from turtle import Turtle, Screen
import random

screen = Screen()
screen.setup(width=800, height=600)
screen.title("TURTLE RACING GAME")

# Colors
colors = ["red", "orange", "yellow", "green", "blue", "purple"]

# Ask user for bet
user_bet = screen.textinput(
    title="Make Your Bet",
    prompt="Which turtle will win? Enter a color:"
)

# Create turtles
turtles = []

start_y = -100

for color in colors:
    turtle = Turtle(shape="turtle")
    turtle.color(color)
    turtle.penup()
    turtle.goto(x=-350, y=start_y)
    turtles.append(turtle)

    start_y += 40

# Race
race_on = True

while race_on:

    for turtle in turtles:

        # Random movement
        distance = random.randint(1, 10)
        turtle.forward(distance)

        # Check finish line
        if turtle.xcor() >= 350:

            race_on = False
            winner = turtle.pencolor()

            if winner == user_bet.lower():
                print(f"YOU WON! {winner} turtle is the winner!")
            else:
                print(f"YOU LOST! {winner} turtle won.")

            break

screen.exitonclick()