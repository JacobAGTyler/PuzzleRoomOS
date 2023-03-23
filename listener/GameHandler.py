from sqlalchemy.orm import Session

from game.Game import Game
from data.database import save_entity, retrieve_entity
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

    def start_game(self):
        evt = self.make_and_send(EventType.GAME_START)
        self.game.start_game()

        if evt.is_published() and self.game.started:
            self.do_save(evt)

    def end_game(self):
        evt = self.make_and_send(EventType.GAME_END)
        self.game.end_game()

        if evt.is_published() and self.game.ended:
            self.do_save(evt)
