from game_engine.game import Game

class AI:
    def __init__(self, game:Game) -> None:
        self.game: Game = game

    def minimax(self,human:str,ai:str,player_turn:int = 0) -> int:
        """The Minimax algorithm for the AI
        
        Parameters:
        human: string: the value that represents the human (x or o)
        ai: string: the value representing the ai (o or x). Cannot be the same as human. AI is the one we are trying to maximise
        player_turn: int: 0 if it is the human's turn, 1 is the ai's
        """
        if human == ai:
            raise Exception("Human player cannot be the same as the AI!")
        if player_turn > 1 or player_turn < 0:
            raise Exception(f"Player_turn is invalid: {player_turn}. Expected value in range 0,1")
        
        #setup
        game: Game = self.game
        if len(game.empty_space()) == 0:
            return self.score(human,ai)
        scores: list[int] = []
        moves: list[int] = []

        legal_moves: tuple[int, ...] = game.empty_space()

        # Populating arrays
        for index in legal_moves:
            game.simulate_move(index, human if player_turn == 0 else ai)
            scores.append(self.minimax(human,ai,0 if player_turn==1 else 1))
            moves.append(index)

        if player_turn == 1:
            # max calculation
            max_score_index: int = scores.index(max(scores)) 
            max_move: int = moves[max_score_index]
            game.perform_move(max_move,ai)
            return scores[max_score_index]
        else:
            # This is the min calculation
            min_score_index: int = scores.index(min(scores))
            return scores[min_score_index]
        

        




    def score(self, human:str, ai:str)-> int:
        if self.game.is_won(human):
            return -1
        elif self.game.is_won(ai):
            return 1
        else:
            return 0
        
