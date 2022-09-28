import datetime

from typing import Optional



class GamePuzzle:
    def __init__(self, game: Game, puzzle: Puzzle):
        self._solved = False
        self._puzzle_id = puzzle.puzzle_id
        self._solve_time = datetime.datetime.now()
