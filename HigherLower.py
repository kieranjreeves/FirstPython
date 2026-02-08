#Algorithm HigherLowerGame

import random

def main():
    print("=== Higher / Lower Game ===\n")

    # Get Bounds
    while True:
        try:
            low = int(input("Lower bound: "))
            high = int(input("Upper bound: "))
            if low > high:
                print("Lower bound must be less than upper bound. Try again.\n")
                continue
            break
        except ValueError:
            print("Please enter whole numbers only.\n")
    secret = random.randint(low, high)
    attempts = 0

    print (f"\nI'm thinking of a number between {low} and {high}...")

    while True:
        try:
            guess = int(input("\nGuess: "))
            attempts += 1

            if guess < low or guess > high:
                print(f"Guess must be between {low} and {high}.")
                continue

            if guess == secret:
                print(f"\nYou Guessed it!!!")
                print ("You Won!!!")
                print (f"It took {attempts} attempts!")
                break
            elif guess < secret:
                print(f"Too low. Try again.")
            else:
                print(f"Too high. Try again.")

        except ValueError:
            print("Please enter whole numbers only.\n")

    print("\nGame over. Play again sometime!")
if __name__ == "__main__":
    main()