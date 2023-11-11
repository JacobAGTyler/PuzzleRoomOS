import datetime
import uuid
from typing import Optional

from listener.event import Event, EventType
from game.game import Game


class GameEvent(Event):
    def __init__(
            self,
            event_type: EventType,
            game: Game = None,
            published: bool = False,
            event_data: Optional[dict] = None,
            event_id: uuid.UUID = uuid.uuid4(),
            event_time: datetime.datetime = datetime.datetime.now(),
    ):
        super().__init__(
            event_type,
            published,
            event_data,
            event_id,
            event_time
        )
        self.game = game

        if not event_type or not isinstance(event_type, EventType):
            raise ValueError("Event type cannot be empty & must be of type EventType")

        self._event_type = event_type

        if event_data is None or not isinstance(event_data, dict):
            event_data = {}

        self._event_data = event_data

    def to_dict(self) -> dict:
        data = super().to_dict()

        if isinstance(self.game, Game):
            data['game'] = self.game.to_dict()

        return data

    def get_trigger_value(self) -> Optional[str]:
        triggered_event_types = [EventType.PUZZLE_SOLVE, EventType.ATTEMPT]

        if 'trigger' in self._event_data.keys() and self._event_type in triggered_event_types:
            return self._event_data['trigger']

        return None
