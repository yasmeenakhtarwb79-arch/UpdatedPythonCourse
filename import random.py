import random

def start_guessing_game():
    # The computer selects a secret number between 1 and 50
    secret_number = random.randint(1, 50)
    attempts = 0  # This local variable tracks the number of guesses
    
    print("=== Welcome to the Number Guessing Game! ===")
    print("I have thought of a number between 1 and 50. Can you guess it?")
    
    # This loop runs until the user guesses the correct number
    while True:
        # Taking input from the user
        user_guess = int(input("\nEnter your guess: "))
        attempts += 1  # Increment the attempt count
        
        # Checking if the guess is correct, too low, or too high
        if user_guess == secret_number:
            print("🎉 Congratulations! You guessed the correct number.")
            print(f"🏆 You found it in {attempts} attempts.")
            break  # Exit the loop and end the game
        elif user_guess < secret_number:
            print("📉 Too low! Try a larger number.")
        else:
            print("📈 Too high! Try a smaller number.")

# Call the function to start the game
start_guessing_game()
