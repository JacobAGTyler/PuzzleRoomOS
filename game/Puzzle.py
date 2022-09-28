from typing import Optional


class Puzzle:
    def __init__(self, puzzle_id: str):
        self._puzzle_id: str = puzzle_id

        self.prerequisites: Optional[set] = None
