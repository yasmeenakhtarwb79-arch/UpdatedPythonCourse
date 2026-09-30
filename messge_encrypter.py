"""A command-line Higher or Lower number guessing game."""

import random


def play_game() -> None:
    print("Welcome to Higher or Lower!")
    print("I'm thinking of a number from 1 to 100.")
    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Please enter a whole number.")
            continue

        if not 1 <= guess <= 100:
            print("Your guess must be between 1 and 100.")
            continue

        attempts += 1
        if guess < secret_number:
            print("Higher!")
        elif guess > secret_number:
            print("Lower!")
        else:
            print(f"Correct! You got it in {attempts} guesses.")
            break


if __name__ == "__main__":
    play_game()