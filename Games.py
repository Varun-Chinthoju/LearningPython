import Number_guesser
import rock_paper_scissiors


def games():
    player_game = input(
        "what game do you want to play, number guesser, or rock paper scissors? Type 'number guesser' or 'rps':  "
    )
    if player_game.lower() == "number_guesser":
        Number_guesser.number_guesser()
    elif player_game.lower() == "rps":
        rock_paper_scissiors.run()
    else:
        print("Please select a game!")
        games()


games()
