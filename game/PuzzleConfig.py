class PuzzleConfig:
    def __init__(self, puzzle_data: dict):
        if 'definition' not in puzzle_data.keys() or 'setup' not in puzzle_data.keys():
            raise ValueError('Puzzle definition and setup are required attributes')

        definition = puzzle_data['definition']
        setup = puzzle_data['setup']
