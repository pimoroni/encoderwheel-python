import pytest
import mock
import sys


@pytest.fixture(scope='function', autouse=False)
def GPIO():
    """Mock RPi.GPIO module."""
    RPi = mock.MagicMock()
    sys.modules['RPi'] = RPi
    sys.modules['RPi.GPIO'] = RPi.GPIO
    yield RPi.GPIO
    del sys.modules['RPi']
    del sys.modules['RPi.GPIO']


@pytest.fixture(scope='function', autouse=False)
def ioexpander():
    """Mock ioexpander module."""
    io_expander = mock.MagicMock()
    sys.modules['ioexpander'] = io_expander
    sys.modules['ioexpander.motor'] = io_expander.motor
    sys.modules['ioexpander.servo'] = io_expander.servo
    sys.modules['ioexpander.encoder'] = io_expander.encoder
    sys.modules['ioexpander.common'] = io_expander.common
    yield io_expander
    del sys.modules['ioexpander']


@pytest.fixture(scope='function', autouse=False)
def smbus2():
    """Mock smbus2 module."""
    smbus = mock.MagicMock()
    sys.modules['smbus2'] = smbus
    yield smbus
    del sys.modules['smbus2']