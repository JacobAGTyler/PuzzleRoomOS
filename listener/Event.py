import datetime

from game.Game import Game


class Event:
    def __init__(self, game: Game):
        self._game = game
        self._event_time = datetime.datetime.now()
