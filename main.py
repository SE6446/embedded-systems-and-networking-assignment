import _thread
from random import uniform

import urequests as requests
from machine import Pin
from utime import sleep

from game_engine import AI, Game  # pyright: ignore[reportPrivateLocalImportUsage]
from game_engine.infoSaving import InfoSaving
from hardware_interface import (  # pyright: ignore[reportPrivateLocalImportUsage]
    clear_matrix,
    get_key_input,
    update_matrix,
)
from server.server import connect

led = Pin("LED", Pin.OUT)
game_matrix: list[list[int]] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # pyright: ignore[reportRedeclaration]


def set_matrix(input_matrix: list[list[int]]) -> None:
    global game_matrix
    game_matrix: list[list[int]] = input_matrix
    print(game_matrix)


def __render_matrix():
    global game_matrix
    while True:
        update_matrix(game_matrix)


def __get_index_from_input() -> int:
    key: str = get_key_input()
    while key not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        key = get_key_input()
    else:
        return int(key) - 1


def game_thread():
    global ip
    print("game")
    while True:
        opponent: str = get_key_input()
        if opponent == "*":
            print("Input difficulty: 1-3")
            difficulty = int(get_key_input())
            while difficulty not in range(1, 4):
                print("WRONG!\nInput difficulty: 1-3")
                difficulty = int(get_key_input())
            __ai_game(difficulty)
            # At the end of each game we take the file, convert it to JSON and send it to the server.
            infoManager = InfoSaving("./scores.txt")
            jsonreturn: str = infoManager.readFileToJSON()
            r = requests.post(ip, data={"body": jsonreturn})
            if r.status != 200:
                print(
                    "Uh oh! Looks like we couldn't communicate your changes, don't worry, it'll update on the next upload"
                )
        elif opponent == "#":
            __human_game()
            # At the end of each game we take the file, convert it to JSON and send it to the server.
            infoManager = InfoSaving("./scores.txt")
            jsonreturn: str = infoManager.readFileToJSON()
            r = requests.post(ip, data={"body": jsonreturn})
            if r.status != 200:
                print(
                    "Uh oh! Looks like we couldn't communicate your changes, don't worry, it'll update on the next upload"
                )

        else:
            print("Invalid input, repeating...")

        sleep(0.2)


def __ai_game(difficulty: int):
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

        ai.game.perform_move(index, "x")

        print("##################")
        ai.game.display()
        set_matrix(led_matrix_converter())

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
        weights = __difficulty_weights(legal_moves, best_legal_move_index, difficulty)

        # Pick weighted move
        index = random_choice(legal_moves, weights)  # pyright: ignore[reportArgumentType]
        ai.game.perform_move(index, "o")
        print("##################")
        ai.game.display()
        if index != best_index:
            print("Blunder!")
        print(ai.game.to_led_matrix())
        set_matrix(led_matrix_converter())
        print(
            f"Best move {best_index}, chosen move {index}\nLegal moves: {legal_moves}, weights {weights}"
        )
        led.off()

    ai.game.display()
    infoManager: InfoSaving = InfoSaving("./scores.txt")
    # get player names
    playerXName = "DefaultX"
    playerXName = input("Please Enter A Name for Player 1 (X)")
    playerOName = "CPU"

    if ai.game.is_won("x"):
        print("Human win")
        # update score file
        infoManager.addScore(playerXName, True)
        infoManager.addScore(playerOName, False)
    elif ai.game.is_won("o"):
        print("AI win")
        infoManager.addScore(playerXName, False)
        infoManager.addScore(playerOName, True)
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


def __difficulty_weights(legal_moves, best_legal_index, difficulty):
    total = 100
    lock_in_chance = 50
    if difficulty == 3:
        lock_in_chance = 75
    elif difficulty == 2:
        lock_in_chance = 60

    total -= lock_in_chance
    blunder_chance = int(total / (len(legal_moves) - 1))

    weights = [blunder_chance for _ in range(len(legal_moves))]

    weights[best_legal_index] = lock_in_chance

    return weights


def __human_game():
    game = Game()
    led_matrix_converter = game.to_led_matrix
    game.display()
    while not game.is_won("x") or not game.is_won("o") and len(game.empty_space()) >= 0:
        print("Player X turn: ")

        index = -1
        while index not in game.empty_space():
            index = __get_index_from_input()
        game.perform_move(index, "x")
        print("##################")
        game.display()
        set_matrix(led_matrix_converter())

        if game.is_won("x") or game.is_won("o") or len(game.empty_space()) == 0:
            # print("break")
            break

        print("Player O turn: ")

        index = -1
        while index not in game.empty_space():
            index = __get_index_from_input()
        game.perform_move(index, "o")
        game.display()
        set_matrix(led_matrix_converter())

    infoManager: InfoSaving = InfoSaving("./scores.txt")

    playerXName = "DefaultX"
    playerXName = input("Please Enter A Name for Player 1 (X)")
    playerOName = "DefaultO"
    playerOName = input("Please Enter A Name for Player 2 (O)")
    if game.is_won("x"):
        print(f"{playerXName} wins!")
        infoManager.addScore(playerXName, True)
        infoManager.addScore(playerOName, False)

    elif game.is_won("o"):
        print(f"{playerOName} win")
        infoManager.addScore(playerXName, False)
        infoManager.addScore(playerOName, True)

    else:
        print("Draw!")


wlan = connect(ssid="RHO6298", password="Jet2Holiday")
ifconfig = wlan.ifconfig()
ip: str = ifconfig[2] + ":80"

_thread.start_new_thread(__render_matrix, ())


print("Commencing health check")
clear_matrix()
try:
    # Define one or more frames
    frame1 = [[2, 2, 2], [2, 2, 2], [2, 2, 2]]
    frame2 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    frame3 = [[3, 3, 3], [3, 3, 3], [3, 3, 3]]
    frame4 = [[1, 0, 1], [0, 2, 0], [1, 0, 1]]
    frame5 = [[2, 0, 2], [0, 1, 0], [2, 0, 2]]

    set_matrix(frame1)
    sleep(1)
    set_matrix(frame2)
    sleep(1)
    set_matrix(frame3)
    sleep(1)
    set_matrix(frame4)
    sleep(1)
    set_matrix(frame5)
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
        f.write("CPU,0,0")  # Add CPU as a default


game_thread()
