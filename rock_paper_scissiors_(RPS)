import random


def rock_paper_scissiors():
    winning_emoji = "\N{smiling face with sunglasses}"
    player = input(
        "Choose your champion! Rock, the one that beats scissors, Paper, which defeats rock, and Scissors, the one to beat paper!:  "
    )
    rock_paper_scissiors = int(random.randint(1, 3))
    if rock_paper_scissiors == 1:
        print("your opponent played 'rock'!")
        if player.lower() == "rock":
            return "Tie"
        elif player.lower() == "paper":
            print(winning_emoji)
            return "you win!!"
        elif player.lower() == "scissiors" or player.lower == "scissior":
            return "you lose :( try again next time!"
    if rock_paper_scissiors == 2:
        print("your opponent played 'paper'!")
        if player.lower() == "rock":
            print(winning_emoji)
            return "you win"
        elif player.lower() == "paper":
            return "Tie"
        elif player.lower() == "scissiors" or player.lower == "scissior":
            return "you lose :( try again next time!"
    if rock_paper_scissiors == 3:
        print("your opponent played 'scissors'!")
        if player.lower() == "rock":
            return "you lose :( try again next time!"
        elif player.lower() == "paper":
            print(winning_emoji)
            return "you win!!"
        elif player.lower() == "scissiors" or player.lower == "scissior":
            return "Tie"


Times_want_to_play = input("How many times do you want to play?:  ") or 3
if type(Times_want_to_play) == str:
    if Times_want_to_play.isdigit() == False:
        print("You need to input a number, not a string or bool")
        exit()
    Times_want_to_play = int(Times_want_to_play)
for i in range(Times_want_to_play):
    print(rock_paper_scissiors())
