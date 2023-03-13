# Encoder Wheel Breakout

[![Build Status](https://shields.io/github/workflow/status/pimoroni/encoderwheel-python/Python%20Tests.svg)](https://github.com/pimoroni/encoderwheel-python/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/encoderwheel-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/encoderwheel-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/encoderwheel.svg)](https://pypi.python.org/pypi/encoderwheel)
[![Python Versions](https://img.shields.io/pypi/pyversions/encoderwheel.svg)](https://pypi.python.org/pypi/encoderwheel)

# Pre-requisites

You must enable:

* i2c: `sudo raspi-config nonint do_i2c 0`

You can optionally run `sudo raspi-config` or the graphical Raspberry Pi Configuration UI to enable interfaces.

# Installing

Stable library from PyPi:

* Just run `pip3 install pimoroni-encoderwheel`

In some cases you may need to use `sudo` or install pip with: `sudo apt install python3-pip`

Latest/development library from GitHub:

* `git clone https://github.com/pimoroni/encoderwheel-python`
* `cd encoderwheel-python`
* `sudo ./install.sh --unstable`

