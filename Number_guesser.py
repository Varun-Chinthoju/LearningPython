import random


def number_guesser():
    print(
        "Welcome to Number Guesser, where a bot generates a random number, and you have to guess the numnber."
    )
    mode = input(
        "Do you want to play on 'Easy mode', or 'medium mode', or 'hard mode', or the hardest, meet 'INSANE MODE' Type 'easy' for easy mode, 'med' for medium mode, 'hard' for hard mode, or 'insane' for insane mode!:  "
    )
    player_guess = 0
    guesses = 0
    trys = 0
    winning_emoji = "\N{smiling face with sunglasses}"
    if mode.lower() == "easy":
        number = random.randint(1, 10)
        guesses = 5
        print("Pick a number from 1 to 10")
        while player_guess != number and guesses != 0:
            player_guess = int(input("Your guess: "))
            if player_guess > number:
                print("Less")
            elif player_guess < number:
                print("Higher")
            else:
                print(winning_emoji)
                print("Congrats!, you got it!!!")
                print(winning_emoji)
            guesses -= 1
            trys += 1

    elif mode.lower() == "med":
        number = random.randint(1, 100)
        guesses = 20
        print("Pick a number from 1 to 100")
        while player_guess != number and guesses != 0:
            player_guess = int(input("Your guess: "))
            if player_guess > number:
                print("Less")
            elif player_guess < number:
                print("Higher")
            else:
                print(winning_emoji)
                print("Congrats!, you got it!!!")
                print(winning_emoji)
            guesses -= 1
            trys += 1

    elif mode.lower() == "hard":
        number = random.randint(1, 1000)
        guesses = 100
        print("Pick a number from 1 to 1000")
        while player_guess != number and guesses != 0:
            player_guess = int(input("Your guess: "))
            if player_guess > number:
                print("Less")
            elif player_guess < number:
                print("Higher")
            else:
                print(winning_emoji)
                print("Congrats!, you got it!!!")
                print(winning_emoji)
            guesses -= 1
            trys += 1

    elif mode.lower() == "insane":
        number = random.randint(1, 10000)
        guesses = 1000
        print("Pick a number from 1 to 10000")
        while player_guess != number and guesses != 0:
            player_guess = int(input("Your guess: "))
            if player_guess > number:
                print("Less")
            elif player_guess < number:
                print("Higher")
            else:
                print(winning_emoji)
                print("Congrats!, you got it!!!")
                print(winning_emoji)
            guesses -= 1
            trys += 1
    print("thanks for playing!")
    print(winning_emoji)


number_guesser()
