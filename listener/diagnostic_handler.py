import logging
import uuid
from typing import Optional

from listener.event import Event, EventType


class DiagnosticHandler:
    @staticmethod
    def make_diagnostic(diagnostic_text: str, game_key: Optional[int] = None) -> bool:
        """
        Attempt can be made from any device, not necessarily the one that the game is running on.

        :param diagnostic_text: The code of the text to be checked against listeners.
        :param game_key: The key of the game that the attempt is being made for.
        :return: Successfully published attempt event.
        """
        uid = uuid.uuid4()
        logging.info(f'[EVENT CREATE] {uid}')
        evt = Event(
            event_id=uid,
            event_type=EventType.DIAGNOSTIC,
            event_data={
                'diagnostic_text': diagnostic_text,
                'game_key': game_key
            }
        )
        evt.publish()
        return evt.is_published()
