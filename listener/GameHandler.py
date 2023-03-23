from typing import Union

from sqlalchemy.orm import Session

from game.Game import Game, make_new_game
from data.database import save_entity, retrieve_entity, get_engine, get_connection
from listener.Event import Event, EventType


class GameHandler:
    def __init__(self, game: Game, session: Session):
        self.game = game
        self.session = session

    def do_save(self, event: Event):
        save_entity(self.game, self.session)
        save_entity(event, self.session)
        self.session.commit()

    def make_and_send(self, event_type: EventType, event_data: dict = None):
        evt = Event(event_type=event_type, game=self.game, event_data=event_data)
        evt.publish()
        return evt

    def initialise_game(self, game_config_code: Union[str, int]):
        pass

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
