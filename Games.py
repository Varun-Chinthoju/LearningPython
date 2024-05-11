import Number_guesser
import rock_paper_scissiors
from pygame_Learning import game
from pygame_Learning import platformer
from pygame_Learning import yay_I_got_into_VEX



def games():
    player_game = input(
        "what game do you want to play, number guesser, or rock paper scissors? Type 'number guesser' or 'rps' or 'rocket' or 'yay' or 'platformer':  "
    )
    if player_game.lower() == "number_guesser":
        Number_guesser.number_guesser()
    elif player_game.lower() == "rps":
        rock_paper_scissiors.run()
    elif player_game.lower() == "rocket":
        game.main()
    elif player_game.lower() == "yay":
        platformer.main()
    elif player_game.lower() == "platformer":
        yay_I_got_into_VEX.main()
    else:
        print("Please select a game!")
        games()


games()
