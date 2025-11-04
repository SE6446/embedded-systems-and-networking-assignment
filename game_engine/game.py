class Game:
    def __init__(self) -> None:
        self.board: list[str] = self.__init_board()
        self.sim_board: list[str] = []

    def __init_board(self) -> list[str]:
        board: list[str] = []
        for _ in range(8):
            board.append("")
        return board

    def empty_space(self) -> tuple[int, ...]:
        """Returns the indexes of empty spaces on the board."""
        indexes: list[int] = []
        for i in range(len(self.board) - 1):
            if self.board[i] == "":
                indexes.append(i)

        return tuple(indexes)

    def simulate_move(self, index: int, player: str):
        self.sim_board = self.board
        legal_moves = self.empty_space()
        if index not in legal_moves:
            raise Exception(
                "Illegal move: " + index + "! Legal moves are " + legal_moves  # pyright: ignore[reportUnknownArgumentType, reportOperatorIssue]
            )  # My parser flags an error here even though it should be vaild.
        self.sim_board[index] = player

    def display_board(self):
        for i in range(8):
            string = self.board[i]
            if i == 2 or i == 5 or i == 8:
                string = string + "\n"

    def perform_move(self, index: int, player: str):
        legal_moves = self.empty_space()
        if index not in legal_moves:
            raise Exception(
                "Illegal move: " + index + "! Legal moves are " + legal_moves  # pyright: ignore[reportUnknownArgumentType, reportOperatorIssue]
            )
        self.board[index] = player

    def is_won(
        self, player: str, use_sim: bool = False
    ) -> bool:  # You will not stop me from making my hard typed python
        """Used to determine if the player has won, player is defined as x or o.

        Parameters:

        player: string - x or o, the player we're checking if winning

        use_sim: bool - Whether to check the simulated board or the real one.

        returns:
        boolean: true if won, false if not.
        """
        board = self.board if not use_sim else self.sim_board
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
