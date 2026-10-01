from ursina import *
import random
import json
import os

app = Ursina()

# ==========================================
# GAME SETTINGS
# ==========================================

GRID_SIZE = 20
MOVE_TIME = 0.15

# ==========================================
# GAME VARIABLES
# ==========================================

snake = []
food = None

direction = Vec2(1, 0)
next_direction = Vec2(1, 0)

score = 0
high_score = 0
game_over = False

# ==========================================
# HIGH SCORE FILE
# ==========================================

SCORE_FILE = "highscore.json"

if os.path.exists(SCORE_FILE):

    try:
        with open(SCORE_FILE, "r") as file:
            data = json.load(file)
            high_score = data.get("high_score", 0)

    except:
        high_score = 0


# ==========================================
# SCORE TEXT
# ==========================================

score_text = Text(
    text="Score: 0",
    position=(-0.85, 0.45),
    scale=1.5
)

high_score_text = Text(
    text=f"High Score: {high_score}",
    position=(-0.85, 0.40),
    scale=1.2
)


# ==========================================
# GAME OVER TEXT
# ==========================================

game_over_text = Text(
    text="",
    origin=(0, 0),
    scale=2
)


# ==========================================
# CREATE SNAKE
# ==========================================

def create_snake():

    global snake

    snake = []

    for i in range(3):

        block = Entity(
            model="cube",
            color=color.green,
            scale=(1, 1, 1),
            position=(-i, 0, 0)
        )

        snake.append(block)


# ==========================================
# CREATE RANDOM FOOD
# ==========================================

def create_food():

    global food

    if food:
        destroy(food)

    while True:

        x = random.randint(
            -GRID_SIZE // 2 + 1,
            GRID_SIZE // 2 - 1
        )

        z = random.randint(
            -GRID_SIZE // 2 + 1,
            GRID_SIZE // 2 - 1
        )

        # Check food is not inside snake
        occupied = False

        for block in snake:

            if round(block.x) == x and round(block.z) == z:
                occupied = True
                break

        if not occupied:
            break

    food = Entity(
        model="cube",
        color=color.red,
        scale=(0.7, 0.7, 0.7),
        position=(x, 0.5, z)
    )


# ==========================================
# SAVE HIGH SCORE
# ==========================================

def save_high_score():

    with open(SCORE_FILE, "w") as file:

        json.dump(
            {
                "high_score": high_score
            },
            file
        )


# ==========================================
# UPDATE SCORE
# ==========================================

def update_score():

    score_text.text = f"Score: {score}"
    high_score_text.text = f"High Score: {high_score}"


# ==========================================
# CONTROLS
# ==========================================

def input(key):

    global next_direction

    # UP
    if key in ("w", "up arrow"):

        if direction != Vec2(0, -1):
            next_direction = Vec2(0, 1)

    # DOWN
    elif key in ("s", "down arrow"):

        if direction != Vec2(0, 1):
            next_direction = Vec2(0, -1)

    # LEFT
    elif key in ("a", "left arrow"):

        if direction != Vec2(1, 0):
            next_direction = Vec2(-1, 0)

    # RIGHT
    elif key in ("d", "right arrow"):

        if direction != Vec2(-1, 0):
            next_direction = Vec2(1, 0)

    # RESTART
    elif key == "r" and game_over:

        restart_game()


# ==========================================
# MOVE SNAKE
# ==========================================

def move_snake():

    global direction
    global next_direction
    global score
    global high_score
    global game_over

    # Stop moving after Game Over
    if game_over:
        return

    direction = next_direction

    # Current head
    head = snake[0]

    # New position
    new_x = round(head.x + direction.x)
    new_z = round(head.z + direction.y)

    # ======================================
    # WALL COLLISION
    # ======================================

    if (
        new_x <= -GRID_SIZE // 2
        or new_x >= GRID_SIZE // 2
        or new_z <= -GRID_SIZE // 2
        or new_z >= GRID_SIZE // 2
    ):

        end_game()
        return

    # ======================================
    # BODY COLLISION
    # ======================================

    for block in snake:

        if (
            round(block.x) == new_x
            and round(block.z) == new_z
        ):

            end_game()
            return

    # ======================================
    # CREATE NEW HEAD
    # ======================================

    new_head = Entity(
        model="cube",
        color=color.green,
        scale=(1, 1, 1),
        position=(new_x, 0, new_z)
    )

    snake.insert(0, new_head)

    # ======================================
    # FOOD COLLISION
    # ======================================

    if (
        round(new_head.x) == round(food.x)
        and round(new_head.z) == round(food.z)
    ):

        # Increase score
        score += 1

        # High score
        if score > high_score:

            high_score = score
            save_high_score()

        update_score()

        # New food
        create_food()

    else:

        # Remove tail
        tail = snake.pop()

        destroy(tail)

    # ======================================
    # NEXT MOVE
    # ======================================

    invoke(
        move_snake,
        delay=MOVE_TIME
    )


# ==========================================
# GAME OVER
# ==========================================

def end_game():

    global game_over

    game_over = True

    game_over_text.text = (
        "GAME OVER\n\n"
        f"Score: {score}\n"
        f"High Score: {high_score}\n\n"
        "Press R to Restart"
    )


# ==========================================
# RESTART GAME
# ==========================================

def restart_game():

    global snake
    global score
    global direction
    global next_direction
    global game_over

    # Destroy old snake
    for block in snake:
        destroy(block)

    snake = []

    # Reset variables
    score = 0

    direction = Vec2(1, 0)
    next_direction = Vec2(1, 0)

    game_over = False

    # Reset UI
    score_text.text = "Score: 0"
    game_over_text.text = ""

    # Create new snake
    create_snake()

    # Create new food
    create_food()

    # Start movement again
    invoke(
        move_snake,
        delay=MOVE_TIME
    )


# ==========================================
# 3D GROUND
# ==========================================

ground = Entity(
    model="cube",
    scale=(GRID_SIZE, 0.1, GRID_SIZE),
    color=color.dark_gray,
    position=(0, -0.55, 0)
)


# ==========================================
# 3D BORDER
# ==========================================

border1 = Entity(
    model="cube",
    scale=(GRID_SIZE, 1, 0.3),
    color=color.white,
    position=(0, 0, GRID_SIZE / 2)
)

border2 = Entity(
    model="cube",
    scale=(GRID_SIZE, 1, 0.3),
    color=color.white,
    position=(0, 0, -GRID_SIZE / 2)
)

border3 = Entity(
    model="cube",
    scale=(0.3, 1, GRID_SIZE),
    color=color.white,
    position=(GRID_SIZE / 2, 0, 0)
)

border4 = Entity(
    model="cube",
    scale=(0.3, 1, GRID_SIZE),
    color=color.white,
    position=(-GRID_SIZE / 2, 0, 0)
)


# ==========================================
# CAMERA
# ==========================================

camera.position = (0, 18, -18)
camera.rotation_x = 45


# ==========================================
# START GAME
# ==========================================

create_snake()

create_food()

invoke(
    move_snake,
    delay=MOVE_TIME
)


# ==========================================
# RUN GAME
# ==========================================

app.run()