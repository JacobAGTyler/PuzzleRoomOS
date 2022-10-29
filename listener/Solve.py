import datetime

from game.GamePuzzle import GamePuzzle
from listener.Event import Event


class Solve(Event):
    def __init__(self, game_puzzle: GamePuzzle):
        super().__init__(game=game_puzzle.get_game())

        self._game_puzzle = game_puzzle
        self._game_puzzle.solved = True

        self._solve_time = datetime.datetime.now()
