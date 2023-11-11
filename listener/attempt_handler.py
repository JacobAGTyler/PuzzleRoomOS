import logging
import uuid
from typing import Optional

from listener.event import Event, EventType


class AttemptHandler:
    @staticmethod
    def make_attempt(attempt_text: str, game_key: Optional[int] = None) -> bool:
        """
        Attempt can be made from any device, not necessarily the one that the game is running on.

        :param attempt_text: The code of the text to be checked against listeners.
        :param game_key: The key of the game that the attempt is being made for.
        :return: Successfully published attempt event.
        """
        uid = uuid.uuid4()
        logging.info(f'[EVENT CREATE] {uid}')
        evt = Event(
            event_id=uid,
            event_type=EventType.ATTEMPT,
            event_data={
                'trigger': attempt_text,
                'game_key': game_key
            }
        )
        evt.publish()
        return evt.is_published()
