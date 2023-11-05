# Code Structure

The code is broken down into separations of concern.

1. Game - the game logic for solving and setup of puzzles. Including the overall dependency cascade.
2. Listener - the devices and listeners that effect state changes in the game boxes.
3. Data - the data structures and data access objects for the game. Persists a consistent state of the game and records transactions in a log of game play.
4. Server - the server that hosts a game interface and can view and control the state of the game.
5. Utilities - shared utility functions which no specific purpose.

## Game
The game code is composed of a [number of classes](Puzzle%20Class%20Diagram.md), which is the core of the game logic.

Each class has a Definition and an Instance. The instance is an instantiated version of the definition. Definitions are designed to be imported via JSON or YAML, from external sources or a centrally hosted server.

An instance of a game is a puzzle room session. Each session will have specific answers and m


## Listener



## Data



## Server




## Utilities

