from .game import Game  # pyright: ignore[reportImplicitRelativeImport]


class AI:
    def __init__(self, game: Game) -> None:
        self.game: Game = game

    def minimax(
        self,
        human: str,
        ai: str,
        player_turn: int = 0,
        simulation: int = 0,
        debug: bool = False,
    ) -> tuple[int, int, list[int]]:
        """
        The Minimax algorithm for the AI

        Parameters:

        human: string: the value that represents the human (x or o)
        ai: string: the value representing the ai (o or x). Cannot be the same as human. AI is the one we are trying to maximise
        player_turn: int: 0 if it is the human's turn, 1 is the ai's

        returns the score
        """
        game: Game = self.game
        if human == ai:
            raise Exception("Human player cannot be the same as the AI!")
        if player_turn > 1 or player_turn < 0:
            raise Exception(
                f"Player_turn is invalid: {player_turn}. Expected value in range 0,1"
            )

        # Check for terminal states first
        if game.is_won(ai, simulation):
            return 1, -1, []
        elif game.is_won(human, simulation):
            return -1, -1, []

        # Check for draw
        legal_moves: tuple[int, ...] = game.empty_space(simulation)
        if len(legal_moves) == 0:
            return 0, 0, []

        scores: list[int] = []
        indexes = []
        current_token: str = human if player_turn == 0 else ai

        # Populate scores for all possible moves
        for index in legal_moves:
            if debug:
                print("###########")
                print(game.sim_boards)
            next_simulation: int = game.start_simulation(simulation)
            game.simulate_move(index, current_token, next_simulation)

            # Recursive call with opponent's turn
            score = self.minimax(
                human, ai, 1 if player_turn == 0 else 0, next_simulation
            )
            scores.append(score[0])
            indexes.append(index)

            game.reset_sim(next_simulation)

        # Return the appropriate score based on whose turn it is
        if player_turn == 1:  # AI's turn - maximize
            maximum = max(scores)
            return (maximum, indexes[scores.index(maximum)], scores)
        else:  # Human's turn - minimize and then exterminate.
            minimum = min(scores)
            return (minimum, indexes[scores.index(minimum)], scores)

    def score(self, human: str, ai: str) -> int:
        if self.game.is_won(human):
            return -1
        elif self.game.is_won(ai):
            return 1
        else:
            return 0


if __name__ == "__main__":
    test_game = Game()
    test_game.mature_game(2)
    ai = AI(test_game)
    score, index, scores = ai.minimax("o", "x", 1, debug=True)
    print("##########################")
    print(scores)
    print(score, index)
    ai.game.display()
    ai.game.perform_move(index if index != -1 else ai.game.empty_space()[0], "o")
    ai.game.display()

    test_game = Game()
    test_game.mature_game(1)
    ai = AI(test_game)
    while (
        not ai.game.is_won("x")
        or not ai.game.is_won("o")
        and len(ai.game.empty_space()) >= 0
    ):
        try:
            print("##################")
            ai.game.display()
            score, index, scores = ai.minimax("x", "o", 1)
            ai.game.perform_move(
                index if index != -1 else ai.game.empty_space()[0], "x"
            )

            print(ai.game.display())
            if (
                not ai.game.is_won("x")
                and not ai.game.is_won("o")
                and len(ai.game.empty_space()) > 1
            ):
                score, index, scores = ai.minimax("o", "x", 1)
                ai.game.perform_move(
                    index if index != -1 else ai.game.empty_space()[0], "o"
                )
            else:
                break
        except Exception as e:
            print("##########################")
            print("Break!")
            print(scores)
            print(score, index)
            print(ai.game.empty_space())
            print(not ai.game.is_won("x"))
            print(not ai.game.is_won("o"))
            print(len(ai.game.empty_space()) > 1)
            raise e
        finally:
            pass

    print("exit!")
    ai.game.display()
