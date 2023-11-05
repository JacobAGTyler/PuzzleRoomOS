from datetime import datetime
from typing import Optional

from game.PuzzleConfig import PuzzleConfig


class Puzzle:
    def __init__(
            self,
            puzzle_config: PuzzleConfig,
            puzzle_reference: str,
            game_id: Optional[int] = None,
            puzzle_id: Optional[int] = None,
            solved: bool = False,
            solve_time: Optional[datetime] = None,
            data: Optional[dict] = None,
            prerequisites: Optional[list[str]] = None,
            solutions: Optional[list[str]] = None,
            triggers: Optional[list[str]] = None,
    ):
        self.puzzle_id: Optional[int] = puzzle_id
        self.game_id: Optional[int] = game_id

        if type(puzzle_config) is not PuzzleConfig:
            raise ValueError("Puzzle config must be a PuzzleConfig")

        if type(puzzle_reference) is not str:
            raise ValueError("Puzzle reference must be a string")

        self.puzzle_reference = puzzle_reference
        self.puzzle_config: PuzzleConfig = puzzle_config

        self.data: Optional[dict] = data
        self.solve_time: Optional[datetime] = solve_time
        self.solved: bool = solved

        self.prerequisites: Optional[list[str]] = prerequisites
        self.solutions: Optional[list[str]] = solutions
        self.triggers: Optional[list[str]] = triggers

    def get_puzzle_id(self) -> int:
        return self.puzzle_id

    def get_puzzle_reference(self) -> str:
        return self.puzzle_reference

    def set_solutions(self, solutions: Optional[list[str]]):
        if solutions is None:
            return

        if type(solutions) is not list:
            raise ValueError("Solutions must be a list")

        self.solutions = solutions

    def get_solutions(self) -> Optional[list[str]]:
        return self.solutions

    def add_solution(self, solution: str):
        if type(solution) is not str:
            raise ValueError("Solution must be a string")

        if type(self.solutions) is not list:
            self.solutions = list()

        self.solutions.append(solution)
        self.solutions = list(set(self.solutions))

    def evaluate_solution(self, solution: str) -> bool:
        return solution in self.solutions

    def set_triggers(self, triggers: Optional[list[str]]):
        if triggers is None:
            return

        if type(triggers) is not list:
            raise ValueError("Triggers must be a list")

        self.triggers = triggers

    def get_triggers(self) -> Optional[list[str]]:
        return self.triggers

    def add_trigger(self, trigger: str):
        if type(trigger) is not str:
            raise ValueError("Trigger must be a string")

        if type(self.triggers) is not list:
            self.triggers = list()

        self.triggers.append(trigger)
        self.triggers = list(set(self.triggers))

    def set_prerequisites(self, prerequisites: Optional[list[str]]):
        if prerequisites is None:
            return

        if type(prerequisites) is not list:
            raise ValueError("Prerequisites must be a list")

        self.prerequisites = prerequisites

    def add_prerequisite(self, prerequisite: str):
        if type(prerequisite) is not str:
            raise ValueError("Prerequisite must be a string")

        if type(self.prerequisites) is not list:
            self.prerequisites = list()

        self.prerequisites.append(prerequisite)
        self.prerequisites = list(set(self.prerequisites))

    def get_prerequisites(self) -> list[str]:
        return self.prerequisites

    def has_prerequisites(self) -> bool:
        return self.prerequisites is not None and len(self.prerequisites) > 0

    def to_dict(self) -> dict:
        return {
            'puzzle_id': self.puzzle_id,
            'game_id': self.game_id,
            'puzzle_reference': self.puzzle_reference,
            'puzzle_config': self.puzzle_config.to_dict(),

            'data': self.data,
            'solve_time': self.solve_time,
            'solved': self.solved,

            'prerequisites': self.prerequisites,
            'solutions': self.solutions,
            'triggers': self.triggers,
        }
