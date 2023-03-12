import pytest

from listener.Event import Event, EventType
from tests.fixtures.game_fixtures import mock_game


class TestEvent:
    @pytest.mark.usefixtures('mock_game')
    def test_event_init(self, mock_game):
        evt = Event(mock_game, EventType.GAME_START)

        assert isinstance(evt, Event)
        assert evt._event_id is not None

    def test_event_init_fail(self):
        with pytest.raises(ValueError):
            Event(None, None)
