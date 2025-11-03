from game import Game

class AI:
    def __init__(self, game:Game) -> None:
        self.game = game

    def minimax(self,human,ai):
        if self.game.game_ended:
            return self.score(human,ai)
        scores = []
        moves = []


    def score(self, human:str, ai:str):
        if self.game.is_won(human):
            return -1
        elif self.game.is_won(ai):
            return 1
        else:
            return 0