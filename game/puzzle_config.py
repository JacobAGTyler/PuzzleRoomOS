class PuzzleConfig:
    def __init__(
            self,
            puzzle_reference: str,
            definition: dict,
            setup: dict,
            puzzle_code: str = 'DEFAULT'
    ):
        if definition is None or setup is None:
            raise ValueError('Puzzle definition and setup are required attributes')

        self._puzzle_code = puzzle_code

        self.definition = definition
        self.setup = setup
        self._puzzle_reference = puzzle_reference

    def get_reference(self) -> str:
        return self._puzzle_reference

    def to_dict(self) -> dict:
        return {
            'puzzleReference': self._puzzle_reference,
            'puzzleCode': self._puzzle_code,
            'definition': self.definition,
            'setup': self.setup
        }
