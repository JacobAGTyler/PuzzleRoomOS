import pytest

from unittest.mock import Mock

from listener.Interface import Interface
from listener.device import Device
from listener.event import Event


@pytest.fixture
def mock_interface() -> Interface:
    m_inf = Mock(spec=Interface)
    m_inf.get_trigger_references.return_value = ['trigger_1', 'trigger_2']
    return m_inf


m_inf_cfg = {
    'name': 'Key 1',
    'relay': 1,
    'pin_number': 18,
    'relay_on_activate': False
}


@pytest.fixture
def mock_interface_config() -> dict:
    return m_inf_cfg


m_dev_cfg = {
    'topic': 'game',
    'isDatabase': False,
    'interfaces': [
        m_inf_cfg
    ]
}


@pytest.fixture
def mock_device_config() -> dict:
    return m_dev_cfg


@pytest.fixture
def built_device() -> Device:
    return Device(m_dev_cfg, 'test_device')


@pytest.fixture
def mock_event() -> Event:
    return Mock(spec=Event)
