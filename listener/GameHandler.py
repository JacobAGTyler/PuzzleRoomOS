from typing import Union

from sqlalchemy.orm import Session

from game.Game import Game
from game.game_factory import make_new_game
from data.database import save_entity, get_engine, get_connection
from listener.Event import EventType
from listener.GameEvent import GameEvent


class GameHandler:
    def __init__(self, game: Game, session: Session):
        self.game = game
        self.session = session

    def do_save(self, event: GameEvent):
        save_entity(self.game, self.session)
        save_entity(event, self.session)
        self.session.commit()

    def make_and_send(self, event_type: EventType, event_data: dict = None):
        evt = GameEvent(event_type=event_type, game=self.game, event_data=event_data)
        evt.publish()
        return evt

    def initialise_game(self, game_config_code: Union[str, int]):
        pass

    def evaluate_trigger(self, trigger: str):
        triggers = self.game.evaluate_trigger(trigger)

        if not triggers or type(triggers) is not set:
            return

        trigger_string: str
        for trigger_string in triggers:
            trigger_evt = self.make_and_send(EventType.PUZZLE_SOLVE, event_data={'trigger': trigger_string})
            if trigger_evt.is_published():
                self.do_save(trigger_evt)

    def new_game(self):
        evt = self.make_and_send(EventType.GAME_CREATION)

        if evt.is_published():
            self.do_save(evt)

    def start_game(self):
        evt = self.make_and_send(EventType.GAME_START)
        started = self.game.start_game()

        if evt.is_published() and started:
            self.do_save(evt)

    def end_game(self):
        evt = self.make_and_send(EventType.GAME_END)
        ended = self.game.end_game()

        if evt.is_published() and ended:
            self.do_save(evt)


def make_new_game_handler(game_config_code: Union[str, int], session: Session = get_connection(get_engine())):
    game = make_new_game(game_config_code=game_config_code, session=session)
    return GameHandler(game=game, session=session)
