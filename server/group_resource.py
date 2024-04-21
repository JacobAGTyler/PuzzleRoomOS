import yaml
from flask_restful import Resource


class GroupResource(Resource):
    def __init__(self):
        with open('puzzles.yml') as file:
            self.data: dict = yaml.safe_load(file)
            print(self.data)

    def get(self, group_letter: str):
        puzzles = []

        puzzle: str
        groups: dict
        for puzzle, body in self.data.items():
            codewords: dict = body['codewords']

            if 'ALL' in codewords.keys():
                puzzle_dict: dict = {
                    'name': puzzle,
                    'codeword': codewords['ALL']
                }
                puzzles.append(puzzle_dict)
                continue

            for group, codeword in codewords.items():
                if group == group_letter:
                    puzzle_dict: dict = {
                        'name': puzzle,
                        'codeword': codeword
                    }
                    puzzles.append(puzzle_dict)

        return {
            'group_letter': group_letter,
            'puzzles': puzzles
        }
