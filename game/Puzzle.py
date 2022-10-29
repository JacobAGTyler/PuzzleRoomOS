from typing import Optional


class Puzzle:
    def __init__(self, puzzle_id: str):
        self._puzzle_id: str = puzzle_id

        self._prerequisites: Optional[set[str]] = None

    def get_puzzle_id(self) -> str:
        return self._puzzle_id

    def set_prerequisites(self, prerequisites: set[str]):
        self._prerequisites = prerequisites

    def add_prerequisite(self, prerequisite: str):
        if self._prerequisites is None:
            self._prerequisites = set()

        self._prerequisites.add(prerequisite)

    def get_prerequisites(self) -> Optional[set[str]]:
        return self._prerequisites

    def has_prerequisites(self) -> bool:
        return self._prerequisites is not None and len(self._prerequisites) > 0
