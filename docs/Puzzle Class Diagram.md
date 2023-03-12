# Puzzle Classes

The game & puzzle classes at the core of the game.

**Game**: The play through of the room. Initiated at a specific time, played to a GameConfig.

**GameConfig**: The configuration of the game. Contains the puzzles, the time limit, and the number of players.

**PuzzleDefinition**: The definition of a puzzle in the abstract. It should include the solution and any hints.

**PuzzleSolutionConfig**: The automated method of generating a puzzle solution. e.g. 4 digit random number, 6 random characters, random choice of prepared tokens, string in random order...

```mermaid
classDiagram

class PuzzleSolutionConfig {
    puzzle_solution_config_id: Integer [PK]
    puzzle_solution_config_guid: UUID [UQ]
    puzzle_solution_config_name: String
    solution_parameters: Dictionary
    get_solution()
}

PuzzleSolutionConfig --* PuzzleConfig

class PuzzleDefinition {
    puzzle_definition_id: Integer [PK]
    puzzle_definition_guid: UUID [UQ]
    puzzle_definition: MarkdownText
    puzzle_solution: MarkdownText
    puzzle_hints: List<String>
    puzzle_assets: List<String>
    get_definition()
    get_puzzle_hint()
}

PuzzleConfig *-- PuzzleDefinition

class PuzzleConfig {
    puzzle_config_id: Integer
    game_config_id: Integer
    version_number: Integer
}

PuzzleConfig --|> Puzzle
GameConfig <-- PuzzleConfig

class Puzzle {
    puzzle_id: Integer
    game_id: Integer
    solve_time: DateTime
    solved: Boolean
    solve()
}

Game <-- Puzzle

class Game {
    game_id: Integer
    game_ref: String
    game_config_id: Integer
    started: Boolean
    ended: Boolean
    start_time: DateTime
    end_time: DateTime
    start_game()
    get_hint()
    draw_progess_graph()
}

class GameConfig {
    game_config_id: Integer [PK]
    game_config_guid: UUID [UQ]
    version_number: Integer
    draw_setup_graph()
    import()
    export()
}

GameConfig --|> Game

```
