from random import randint


class Game:
    def __init__(self) -> None:
        self.board: list[str] = self.__init_board()
        self.sim_boards: dict[int, list[str]] = {}
        self._next_simulation_id: int = 1

    def __init_board(self) -> list[str]:
        board: list[str] = []
        for _ in range(9):
            board.append("")
        return board

    def _get_board_state(self, simulation: int = 0) -> list[str]:
        if simulation == 0:
            return self.board
        board = self.sim_boards.get(simulation)
        if board is None:
            raise ValueError(f"Simulation index out of range: {simulation}")
        return board

    def empty_space(self, simulation: int = 0) -> tuple[int, ...]:
        """Returns the indexes of empty spaces on the specified board."""
        board = self._get_board_state(simulation)
        indexes: list[int] = []
        for i, value in enumerate(board):
            if value == "":
                indexes.append(i)

        return tuple(indexes)

    def simulate_move(self, index: int, player: str, simulation: int) -> None:
        if simulation == 0:
            raise ValueError(
                "Simulation id 0 refers to the live board; call start_simulation first."
            )
        legal_moves = self.empty_space(simulation)
        if index not in legal_moves:
            raise Exception(
                "Illegal move: " + str(index) + "! Legal moves are " + str(legal_moves)
            )
        board = self._get_board_state(simulation)
        board[index] = player

    def reset_sim(self, simulation: int) -> None:
        if simulation == 0:
            raise ValueError("Cannot reset the main game board.")
        if simulation not in self.sim_boards:
            raise ValueError(f"Simulation index out of range: {simulation}")
        self.sim_boards.pop(simulation)

    def start_simulation(self, base_simulation: int = 0) -> int:
        """Starts a new simulation and returns its index."""
        base_board = self._get_board_state(base_simulation)
        simulation_id = self._next_simulation_id
        self._next_simulation_id += 1
        self.sim_boards[simulation_id] = base_board.copy()
        return simulation_id

    def perform_move(self, index: int, player: str):
        legal_moves = self.empty_space()
        if index not in legal_moves:
            raise Exception(
                "Illegal move: " + str(index) + "! Legal moves are " + str(legal_moves)
            )
        self.board[index] = player

    def is_won(
        self, player: str, simulation: int = 0
    ) -> bool:  # You will not stop me from making my hard typed python
        """Determine if the player has won on the main or a simulated board.

        Parameters:

        player: string - x or o, the player we're checking if winning

        simulation: int - Simulation id to evaluate. 0 targets the live board.

        returns:
        boolean: true if won, false if not.
        """
        board = self._get_board_state(simulation)
        status = False

        if player != "x" and player != "o":
            raise Exception("Player is not valid. Expected x or o. Got: " + player)

        # Horizontal wins
        if board[0] == player and board[1] == player and board[2] == player:
            status = True
        elif board[3] == player and board[4] == player and board[5] == player:
            status = True
        elif board[6] == player and board[7] == player and board[8] == player:
            status = True

        # Vertical wins
        elif board[2] == player and board[5] == player and board[8] == player:
            status = True
        elif board[1] == player and board[4] == player and board[7] == player:
            status = True
        elif board[0] == player and board[3] == player and board[6] == player:
            status = True

        # Diagonal wins
        elif board[0] == player and board[4] == player and board[8] == player:
            status = True
        elif board[2] == player and board[4] == player and board[6] == player:
            status = True

        return status

    # Deepseek made this cause I was lazy, for clarification I did make edits and review it.
    # I don't just slap ChatGPT into it and call it a day. Professionals have standards!
    # As those edits it was mostly trimming some fluff and adjusting the ranges because it wen out of bounds.
    def display(self):
        for i in range(3):
            row = ""
            for j in range(3):
                index = i * 3 + j
                cell = self.board[index]
                if cell == "":
                    row += " "
                else:
                    row += cell
                if j < 2:
                    row += " | "
            print(row)
            if i < 2:
                print("-" * 9)

    def mature_game(self, turns: int = 2) -> None:
        for _ in range(turns):
            randx = randint(0, 8)
            while self.board[randx] != "":
                randx = randint(0, 8)
            self.board[randx] = "x"
            rando = randint(0, 8)
            while self.board[rando] != "":
                rando = randint(0, 8)
            self.board[rando] = "o"

    def to_led_matrix(self) -> list[list[int]]:
        led_code_board: list[int] = []
        for space in self.board:
            if space == "":
                led_code_board.append(0)
            elif space == "x":
                led_code_board.append(1)
            elif space == "o":
                led_code_board.append(2)
            else:
                led_code_board.append(3)
                print("WARN: Unexpected variable in board!")
        row1, row2, row3 = (
            led_code_board[0:3],
            led_code_board[3:6],
            led_code_board[6:9],
        )
        print(row1)
        print(row2)
        print(row3)
        return [row1, row2, row3]


class Cursor:
    def __init__(self) -> None:
        self.position: int = 0  # Index on the board from 0-8

    def move_to(self, i: int, j: int) -> None:
        if i < 0:
            i = 0
        elif i > 2:
            i = 2
        if j < 0:
            j = 0
        elif j > 2:
            j = 2
        self.position = i + 3 * j

    def to_vector(self) -> tuple[int, int]:
        x = self.position % 3
        y = self.position // 3
        return (x, y)

    def get_position(self) -> int:
        return self.position


# Adding a test game into __main__ for testing purposes, this won't run when imported
if __name__ == "__main__":
    game: Game = Game()

    game.display()
    if input("Use Cursor? (y/n): ") == "n":
        while (
            not game.is_won("x")
            and not game.is_won("o")
            and len(game.empty_space()) != 0
        ):
            print("Player X turn.")
            x = int(input("Input x: ")) - 1
            if x >= 3:
                x = 2
            elif x <= -1:
                x = 0
            y = int(input("Input y: ")) - 1
            if y >= 3:
                y = 2
            elif y <= -1:
                y = 0
            index = x + 3 * y
            game.perform_move(index, "x")
            game.display()
            if game.is_won("x") or len(game.empty_space()) == 0:
                break
            print("Player O turn.")
            x = int(input("Input x: ")) - 1
            if x >= 3:
                x = 2
            elif x <= -1:
                x = 0
            y = int(input("Input y: ")) - 1
            if y >= 3:
                y = 2
            elif y <= -1:
                y = 0
            index = x + 3 * y
            game.perform_move(index, "o")
            game.display()
            if game.is_won("x") or len(game.empty_space()) == 0:
                break
    else:
        while (
            not game.is_won("x")
            and not game.is_won("o")
            and len(game.empty_space()) != 0
        ):
            cursor: Cursor = Cursor()
            print("Player X turn.")
            print("Cursor at positions: " + str(cursor.to_vector()))
            indexes: list[int] = [
                int(input("Input i (0-3): ")) - 1,
                int(input("Input j (0-3): ")) - 1,
            ]
            cursor.move_to(indexes[0], indexes[1])
            index: int = cursor.get_position()
            if index < 0:
                index = 0
            elif index > 8:
                index = 8
            game.perform_move(index, "x")
            game.display()
            if game.is_won("x") or len(game.empty_space()) == 0:
                break
            print("Player O turn.")
            print("Cursor at positions: " + str(cursor.to_vector()))
            indexes = [
                int(input("Input i (0-3): ")) - 1,
                int(input("Input j (0-3): ")) - 1,
            ]
            cursor.move_to(indexes[0], indexes[1])
            index = cursor.get_position()
            if index < 0:
                index = 0
            elif index > 8:
                index = 8
            game.perform_move(index, "o")
            game.display()
            if game.is_won("x") or len(game.empty_space()) == 0:
                break
    print("Game over!")
    if game.is_won("x"):
        print("X wins!")
    elif game.is_won("o"):
        print("O wins!")
    else:
        print("Draw!")
