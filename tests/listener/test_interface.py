import pytest

from gpiozero import OutputDevice

from listener.Interface import Interface

from tests.fixtures.listener_fixtures import mock_interface_config


class TestInterface:
    @pytest.mark.usefixtures('mock_interface_config')
    def test_interface_init(self, monkeypatch, mock_interface_config):
        monkeypatch.setenv('GPIOZERO_PIN_FACTORY', 'mock')
        inf = Interface([], mock_interface_config)

        assert isinstance(inf, Interface)
        assert inf.name == mock_interface_config['name']
        assert isinstance(inf._device, OutputDevice)

    def test_interface_init_no_config(self):
        with pytest.raises(TypeError):
            _ = Interface()

    def test_activate_deactivate(self, monkeypatch, mock_interface_config):
        monkeypatch.setenv('GPIOZERO_PIN_FACTORY', 'mock')
        mock_interface_config['pin_number'] = 21
        inf = Interface([], mock_interface_config)
        assert not inf._device.is_active

        inf.activate()
        assert inf._device.is_active

        inf.deactivate()
        assert not inf._device.is_active

    def test_get_relay_number(self, monkeypatch, mock_interface_config):
        monkeypatch.setenv('GPIOZERO_PIN_FACTORY', 'mock')
        mock_interface_config['pin_number'] = 20
        inf = Interface([], mock_interface_config)

        assert inf.get_relay_number() == 1
