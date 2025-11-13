import _thread
import time
from game_engine import AI, Game  # pyright: ignore[reportPrivateLocalImportUsage]

def game_thread():
    while True:
        opponent: str = input("CPU (*) or Human (#): ")
        if opponent == "*":
            __ai_game()
        elif opponent == "#":
            __human_game()
        else:
            print("Invalid input, repeating...")
        

    
def __ai_game():
    #Instantiate the game
    game: Game = Game()
    ai: AI = AI(game)

    ai.game.display()
    while (
        not ai.game.is_won("x")
        or not ai.game.is_won("o")
        and len(ai.game.empty_space()) >= 0
    ):
        # Player move
        move_x: int = int(input("Input x: ")) - 1
        move_y: int = int(input("Input y: ")) - 1
        index: int = 3*move_y +move_x
        ai.game.perform_move(index, "x")
        print("##################")
        ai.game.display()

        #print(ai.game.is_won("x"))
        #print(ai.game.is_won("o"))
        #print(len(ai.game.empty_space()) == 0)


        if (ai.game.is_won("x")
            or ai.game.is_won("o")
            or len(ai.game.empty_space()) == 0
        ):
            #print("break")
            break

        # AI move
        _, index, _ = ai.minimax("x","o",1)
        ai.game.perform_move(index, "o")
        print("##################")
        ai.game.display()

    ai.game.display()
    if ai.game.is_won("x"):
        print("Human win")
    elif ai.game.is_won("o"):
        print("AI win")
    else:
        print("Draw!")




def __human_game():
    game = Game()

    game.display()
    while (
        not game.is_won("x")
        or not game.is_won("o")
        and len(game.empty_space()) >= 0
    ):
        print("Player X turn: ")
        move_x: int = int(input("Input x: ")) - 1
        move_y: int = int(input("Input y: ")) - 1
        index: int = 3*move_y +move_x
        game.perform_move(index, "x")
        print("##################")
        game.display()

        if (game.is_won("x")
            or game.is_won("o")
            or len(game.empty_space()) == 0
        ):
            #print("break")
            break

        print("Player O turn: ")
        move_x= int(input("Input x: ")) - 1
        move_y= int(input("Input y: ")) - 1
        index= 3*move_y +move_x
        game.perform_move(index, "o")
    game.display()
    if game.is_won("x"):
        print("Human win")
    elif game.is_won("o"):
        print("AI win")
    else:
        print("Draw!")

        

def server_thread():
    pass


def __server():
    pass


_ = _thread.start_new_thread(game_thread, ())  # pyright: ignore[reportUnknownMemberType, reportAny]
_ = _thread.start_new_thread(server_thread, ())  # pyright: ignore[reportUnknownMemberType, reportAny]

while True:
    time.sleep(1)  # pyright: ignore[reportUnknownMemberType]
