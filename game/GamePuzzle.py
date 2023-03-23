import datetime

from game.Game import Game
from game.Puzzle import Puzzle


class GamePuzzle:
    def __init__(self, game: Game, puzzle: Puzzle):
        self._game = game
        self._puzzle = puzzle

        self.solutions = []

        self._solved = False
        self._solve_time = datetime.datetime.now()

    def get_game(self) -> Game:
        return self._game

    def get_puzzle(self) -> Puzzle:
        return self._puzzle
