import unittest.mock

import pytest

from listener.device import Device
from listener.device_factory import instantiate_device
from listener.Interface import Interface

from tests.fixtures.listener_fixtures import mock_device_config, mock_interface, built_device, mock_event


class TestDevice:
    @pytest.mark.usefixtures('mock_device_config')
    def test_device_init(self, mock_device_config: dict):
        device = Device(mock_device_config, 'test_device')

        assert isinstance(device, Device)
        assert device.device_code == 'test_device'
        assert device.device_config == mock_device_config

    def test_device_init_no_config(self):
        with pytest.raises(TypeError):
            _ = Device()

    @pytest.mark.usefixtures('mock_device_config')
    def test_device_init_no_code(self, mock_device_config):
        with pytest.raises(TypeError):
            _ = Device(mock_device_config)

    @pytest.mark.usefixtures('built_device', 'mock_interface')
    def test_add_interface(self, built_device, mock_interface):
        built_device.add_interface(mock_interface)

        assert mock_interface in built_device._interfaces

    @pytest.mark.usefixtures('built_device', 'mock_interface', 'mock_event')
    def test_device_initialisation(self, monkeypatch, built_device, mock_interface, mock_event: unittest.mock.Mock):
        monkeypatch.setattr('listener.device.Event', lambda *args, **kwargs: mock_event)
        built_device.initialise()

        assert mock_event.publish.called


class TestInstantiateDevice:
    @pytest.mark.usefixtures('mock_device_config', 'mock_interface')
    def test_instantiate_device(self, monkeypatch, mock_device_config, mock_interface):
        monkeypatch.setattr('socket.gethostname', lambda *args, **kwargs: 'puzzle-test')
        monkeypatch.setattr('listener.device_factory.import_config', lambda *args, **kwargs: mock_device_config)
        monkeypatch.setattr('listener.device_factory.Interface', lambda *args, **kwargs: mock_interface)
        device = instantiate_device()

        assert isinstance(device, Device)
        assert device.device_code == 'test'
        assert device.device_config == mock_device_config

        assert isinstance(device._interfaces[0], Interface)
        assert device._trigger_references == ['trigger_1', 'trigger_2']

    @pytest.mark.usefixtures('mock_device_config', 'mock_interface')
    def test_instantiate_device_no_hn(self, monkeypatch, mock_device_config, mock_interface):
        monkeypatch.setattr('listener.device_factory.import_config', lambda *args, **kwargs: mock_device_config)
        monkeypatch.setattr('listener.device_factory.Interface', lambda *args, **kwargs: mock_interface)
        device = instantiate_device(device_code='goat')

        assert isinstance(device, Device)
        assert device.device_code == 'goat'
        assert device.device_config == mock_device_config
