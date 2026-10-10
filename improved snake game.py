import os
import random
import turtle

WIDTH = 600
HEIGHT = 600
GRID_SIZE = 20
MOVE_DELAY = 110
MARGIN = 10

screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("#0b1120")
screen.title("Improved Snake Game")
screen.tracer(0)
screen.listen()

score_turtle = turtle.Turtle()
score_turtle.hideturtle()
score_turtle.penup()
score_turtle.color("#e2e8f0")
score_turtle.goto(0, HEIGHT / 2 - 36)

message_turtle = turtle.Turtle()
message_turtle.hideturtle()
message_turtle.penup()
message_turtle.color("#f8fafc")
message_turtle.goto(0, 0)

border = turtle.Turtle()
border.hideturtle()
border.speed(0)
border.color("#38bdf8")
border.penup()
border.goto(-WIDTH / 2 + MARGIN, -HEIGHT / 2 + MARGIN)
border.pendown()
for _ in range(4):
    border.forward(WIDTH - 2 * MARGIN)
    border.left(90)

snake = []
for index in range(3):
    segment = turtle.Turtle("square")
    segment.penup()
    segment.speed(0)
    segment.color("#86efac" if index == 0 else "#4ade80")
    segment.goto(-index * GRID_SIZE, 0)
    snake.append(segment)

food = turtle.Turtle("circle")
food.penup()
food.speed(0)
food.shapesize(0.65, 0.65, 1)
food.color("#f87171")

direction = "right"
next_direction = "right"
state = "playing"
score = 0
best_score = 0


def load_best_score():
    path = os.path.join(os.path.dirname(__file__), "snake_best_score.txt")
    try:
        with open(path, "r", encoding="utf-8") as file:
            value = int(file.read().strip())
            return max(0, value)
    except (FileNotFoundError, ValueError):
        return 0


def save_best_score(value):
    path = os.path.join(os.path.dirname(__file__), "snake_best_score.txt")
    with open(path, "w", encoding="utf-8") as file:
        file.write(str(value))


best_score = load_best_score()


def show_message(text="", color="#f8fafc"):
    message_turtle.clear()
    if text:
        message_turtle.color(color)
        message_turtle.write(text, align="center", font=("Arial", 24, "bold"))
    screen.update()


def update_score():
    score_turtle.clear()
    score_turtle.write(f"Score: {score}  Best: {best_score}", align="center", font=("Arial", 18, "bold"))
    screen.update()


def place_food():
    max_x = (WIDTH // 2) - 25
    max_y = (HEIGHT // 2) - 25
    while True:
        x = random.randint(-max_x, max_x)
        y = random.randint(-max_y, max_y)
        x = x - (x % GRID_SIZE)
        y = y - (y % GRID_SIZE)
        if all(abs(segment.xcor() - x) > 1 or abs(segment.ycor() - y) > 1 for segment in snake):
            food.goto(x, y)
            return


place_food()
update_score()


def set_direction(new_direction):
    global next_direction
    if state != "playing":
        return

    opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
    if new_direction in opposite and opposite[new_direction] != direction:
        next_direction = new_direction


def handle_turns():
    global direction
    direction = next_direction


def schedule_next_move():
    if state == "playing":
        screen.ontimer(move, MOVE_DELAY)


def end_game():
    global best_score, state
    state = "game_over"
    if score > best_score:
        best_score = score
        save_best_score(best_score)
    update_score()
    show_message("Game Over! Press R to restart", "#fca5a5")


def toggle_pause():
    global state
    if state == "game_over":
        return
    if state == "playing":
        state = "paused"
        show_message("Paused", "#fbbf24")
    else:
        state = "playing"
        show_message("")
        schedule_next_move()


def restart_game():
    global direction, next_direction, score, state
    for segment in snake:
        segment.hideturtle()
    snake.clear()
    for index in range(3):
        segment = turtle.Turtle("square")
        segment.penup()
        segment.speed(0)
        segment.color("#86efac" if index == 0 else "#4ade80")
        segment.goto(-index * GRID_SIZE, 0)
        snake.append(segment)
    direction = "right"
    next_direction = "right"
    score = 0
    state = "playing"
    show_message("")
    place_food()
    update_score()
    schedule_next_move()


def move():
    if state != "playing":
        return

    global score, best_score
    handle_turns()
    head_x, head_y = snake[0].xcor(), snake[0].ycor()

    if direction == "up":
        head_y += GRID_SIZE
    elif direction == "down":
        head_y -= GRID_SIZE
    elif direction == "left":
        head_x -= GRID_SIZE
    elif direction == "right":
        head_x += GRID_SIZE

    if (
        head_x > WIDTH / 2 - MARGIN
        or head_x < -WIDTH / 2 + MARGIN
        or head_y > HEIGHT / 2 - MARGIN
        or head_y < -HEIGHT / 2 + MARGIN
    ):
        end_game()
        return

    for segment in snake[1:]:
        if segment.distance(head_x, head_y) < 1:
            end_game()
            return

    for index in range(len(snake) - 1, 0, -1):
        snake[index].goto(snake[index - 1].xcor(), snake[index - 1].ycor())

    snake[0].goto(head_x, head_y)

    if snake[0].distance(food) < 15:
        new_segment = turtle.Turtle("square")
        new_segment.penup()
        new_segment.speed(0)
        new_segment.color("#4ade80")
        new_segment.goto(snake[-1].xcor(), snake[-1].ycor())
        snake.append(new_segment)
        score += 1
        if score > best_score:
            best_score = score
            save_best_score(best_score)
        place_food()
        update_score()

    screen.update()
    schedule_next_move()


screen.onkey(lambda: set_direction("up"), "Up")
screen.onkey(lambda: set_direction("down"), "Down")
screen.onkey(lambda: set_direction("left"), "Left")
screen.onkey(lambda: set_direction("right"), "Right")
screen.onkey(lambda: set_direction("up"), "w")
screen.onkey(lambda: set_direction("down"), "s")
screen.onkey(lambda: set_direction("left"), "a")
screen.onkey(lambda: set_direction("right"), "d")
screen.onkey(toggle_pause, "space")
screen.onkey(restart_game, "r")

move()
screen.mainloop()
