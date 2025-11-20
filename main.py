import _thread
from utime import sleep
from random import uniform
import asyncio

from game_engine import AI, Game  # pyright: ignore[reportPrivateLocalImportUsage]
from hardware_interface import get_key_input, update_matrix, clear_matrix # pyright: ignore[reportPrivateLocalImportUsage]
from server.server import connect, open_socket, serve
from machine import Pin

led = Pin("LED", Pin.OUT)

def __get_index_from_input() -> int:
    key: str = get_key_input()
    while key not in ["1","2","3","4","5","6","7","8","9"]:
        key = get_key_input()
    else:
        return int(key) - 1


def game_thread():
    print("game")
    while True:
        opponent: str = get_key_input()
        if opponent == "*":
            difficulty = int(input("Input difficulty: 1-3"))
            while difficulty not in range(1, 4):
                difficulty = int(input("WRONG!\nInput difficulty: 1-3"))
            __ai_game(difficulty)
        elif opponent == "#":
            __human_game()
        else:
            print("Invalid input, repeating...")
        
        sleep(0.2)


def __ai_game(difficulty:int):
    # Instantiate the game
    game: Game = Game()
    ai: AI = AI(game)
    led_matrix_converter = ai.game.to_led_matrix

    ai.game.display()
    while (
        not ai.game.is_won("x")
        or not ai.game.is_won("o")
        and len(ai.game.empty_space()) >= 0
    ):
        # Player move
        index = -1
        while index not in ai.game.empty_space():
            index: int = __get_index_from_input()
        
        ai.game.perform_move(index,"x")
            
        print("##################")
        ai.game.display()
        update_matrix(led_matrix_converter())

        # print(ai.game.is_won("x"))
        # print(ai.game.is_won("o"))
        # print(len(ai.game.empty_space()) == 0)

        if (
            ai.game.is_won("x")
            or ai.game.is_won("o")
            or len(ai.game.empty_space()) == 0
        ):
            # print("break")
            break

        # AI move
        print("AI making move, this may take a while...")
        led.on()
        _, best_index, _ = ai.minimax("x", "o", 1)
        # Chance to blunder
        # We make a weighted choice, defined by difficulty
        legal_moves = ai.game.empty_space()
        best_legal_move_index = legal_moves.index(best_index)
        weights = [1 for _ in range(len(legal_moves))]
        handicap = 1
        if difficulty == 3:
            handicap = 3
        elif difficulty == 2:
            handicap = 2
        weights[best_legal_move_index] = handicap

        # Pick weighted move
        index = random_choice(legal_moves, weights)  # pyright: ignore[reportArgumentType]
        ai.game.perform_move(index, "o")
        print("##################")
        ai.game.display()
        if index != best_index:
            print("Blunder!")
        print(ai.game.to_led_matrix())
        update_matrix(led_matrix_converter())
        print(
            f"Best move {best_index}, chosen move {index}\nLegal moves: {legal_moves}, weights {weights}"
        )
        led.off()

    ai.game.display()
    if ai.game.is_won("x"):
        print("Human win")
    elif ai.game.is_won("o"):
        print("AI win")
    else:
        print("Draw!")


def random_choice(items: list[int] | tuple[int], weights: list[int]) -> int:
    if len(items) != len(weights):
        raise Exception(
            f"Input Mistmatch: expected size {len(items)} but got {len(weights)}"
        )

    summed_weights = sum(weights)

    r = uniform(0, summed_weights)

    culmmative_weights = 0
    for i, item in enumerate(items):
        culmmative_weights += weights[i]
        if r < culmmative_weights:
            return item

    return items[-1]  # Fallback.


def __human_game():
    game = Game()
    led_matrix_converter = game.to_led_matrix
    game.display()
    while not game.is_won("x") or not game.is_won("o") and len(game.empty_space()) >= 0:    
        print("Player X turn: ")
        
        
        index = -1
        while index not in game.empty_space():
            index: int = __get_index_from_input()
        game.perform_move(index, "x")
        print("##################")
        game.display()
        update_matrix(led_matrix_converter())


        if game.is_won("x") or game.is_won("o") or len(game.empty_space()) == 0:
            # print("break")
            break

        print("Player O turn: ")
        
        
        index = -1
        while index not in game.empty_space():
            index: int = __get_index_from_input()
        game.perform_move(index, "o")
        game.display()
        update_matrix(led_matrix_converter())


    if game.is_won("x"):
        print("Human win")
    elif game.is_won("o"):
        print("AI win")
    else:
        print("Draw!")


def server_thread():
    print("Server started")
    wlan = connect(ssid="GalAM4a47", password="pitb3872")
    socket = open_socket(wlan)
    serve(socket, "scores.txt")

print("Commencing health check")
clear_matrix()
try:
    # Define one or more frames
    frame1 = [
        [2, 2, 2],                      
        [2, 2, 2],
        [2, 2, 2]
    ]
    frame2 = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    frame3 = [
        [3, 3, 3],
        [3, 3, 3],
        [3, 3, 3]
    ]
    frame4 = [
        [1,0,1],
        [0,2,0],
        [1,0,1]
    ]
    frame5 = [
        [2,0,2],
        [0,1,0],
        [2,0,2]
    ]


    update_matrix(frame1)
    sleep(1)
    update_matrix(frame2)
    sleep(1)
    update_matrix(frame3)
    sleep(1)
    update_matrix(frame4)
    sleep(1)
    update_matrix(frame5)
    sleep(1)

except KeyboardInterrupt:
    clear_matrix()
finally:
    clear_matrix()
    print("Health check complete")
# Ensure the scores file exists.
try:
    with open("scores.txt", "r") as f:
        pass
except:
    with open("scores.txt", "w") as f:
        f.write("CPU,0,0") #Add CPU as a default

    
_ = _thread.start_new_thread(game_thread, ())

server_thread()
   
