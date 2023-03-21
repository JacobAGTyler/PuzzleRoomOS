import uuid

import pytest

from listener.Event import Event, EventType
from tests.fixtures.game_fixtures import mock_game


class TestEvent:
    @pytest.mark.usefixtures('mock_game')
    def test_event_init(self, mock_game):
        evt = Event(EventType.GAME_START, mock_game)

        assert isinstance(evt, Event)
        assert evt._event_id is not None
        assert isinstance(evt._event_id, uuid.UUID)
        assert evt._game == mock_game
        assert evt._event_time is not None
        assert evt._event_type == EventType.GAME_START
        assert evt._event_data == {}

    @pytest.mark.usefixtures('mock_game')
    def test_event_init_fail(self, mock_game):
        with pytest.raises(ValueError):
            Event(None, None)

        with pytest.raises(ValueError) as evt_type_err:
            Event(None, mock_game)

            assert str(evt_type_err.value.args[0]) == "Event type cannot be empty & must be of type EventType"


