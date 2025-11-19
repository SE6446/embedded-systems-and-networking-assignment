import _thread
import time
from random import uniform

from game_engine import AI, Game  # pyright: ignore[reportPrivateLocalImportUsage]


def game_thread():
    while True:
        opponent: str = input("CPU (*) or Human (#): ")
        if opponent == "*":
            difficulty = int(input("Input difficulty: 1-3"))
            while difficulty not in range(1, 4):
                difficulty = int(input("WRONG!\nInput difficulty: 1-3"))
            __ai_game(difficulty)
        elif opponent == "#":
            __human_game()
        else:
            print("Invalid input, repeating...")


def __ai_game(difficulty:int):
    # Instantiate the game
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
        index: int = 3 * move_y + move_x
        ai.game.perform_move(index, "x")
        print("##################")
        ai.game.display()
        print(ai.game.to_led_matrix())

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
        print(
            f"Best move {best_index}, chosen move {index}\nLegal moves: {legal_moves}, weights {weights}"
        )

    ai.game.display()
    if ai.game.is_won("x"):
        print("Human win")
    elif ai.game.is_won("o"):
        print("AI win")
    else:
        print("Draw!")


def random_choice(items: list[int] | tuple[int], weights: list[int]) -> int:  # pyright: ignore[reportMissingTypeArgument]
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

    game.display()
    while not game.is_won("x") or not game.is_won("o") and len(game.empty_space()) >= 0:
        print("Player X turn: ")
        move_x: int = int(input("Input x: ")) - 1
        move_y: int = int(input("Input y: ")) - 1
        index: int = 3 * move_y + move_x
        game.perform_move(index, "x")
        print("##################")
        game.display()

        if game.is_won("x") or game.is_won("o") or len(game.empty_space()) == 0:
            # print("break")
            break

        print("Player O turn: ")
        move_x = int(input("Input x: ")) - 1
        move_y = int(input("Input y: ")) - 1
        index = 3 * move_y + move_x
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
