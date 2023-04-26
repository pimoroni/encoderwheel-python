# Encoder Wheel - Library Reference <!-- omit in toc -->

This is the library reference for the [Pimoroni Encoder Wheel Breakout](https://shop.pimoroni.com/products/encoder-wheel-breakout).


## Table of Content <!-- omit in toc -->
- [Getting Started](#getting-started)
- [Reading the Buttons](#reading-the-buttons)
- [Reading the Encoder](#reading-the-encoder)
  - [Count and Angle](#count-and-angle)
  - [Count Delta](#count-delta)
  - [Step and Turn](#step-and-turn)
  - [Changing the Direction](#changing-the-direction)
  - [Resetting to Zero](#resetting-to-zero)
- [LEDs](#leds)
  - [Setting an LED](#setting-an-led)
    - [RGB](#rgb)
    - [HSV](#hsv)
  - [Clear all LEDs](#clear-all-leds)
  - [Showing](#showing)
- [Function Reference](#function-reference)
- [Constants Reference](#constants-reference)
  - [Address Constants](#address-constants)
  - [Button Constants](#button-constants)
  - [GPIO Constants](#gpio-constants)
  - [Count Constants](#count-constants)


<!-- pypa starts reference here -->

## Getting Started

To start coding for your Encoder Wheel breakout, you will need to add the following lines to the start of your code file.

```python
from encoderwheel import EncoderWheel
wheel = EncoderWheel()
```

This will create an `EncoderWheel` class called `wheel` that will be used in the rest of the examples going forward.


## Reading the Buttons

EncoderWheel has five buttons, covering up, down, left, right, and centre. These can be read using the `.pressed(button)` function, which accepts a button number between `0` and `4`. For convenience, each button can be referred to using these constants:

* `UP` = `0`
* `DOWN` = `1`
* `LEFT` = `2`
* `RIGHT` = `3`
* `CENTRE` = `4`

For example, to read the centre button you would write:

```python
centre_state = wheel.pressed(CENTRE)
```

You can also get the number of buttons using the `NUM_BUTTONS` constant.


## Reading the Encoder

Within the directional buttons of the Encoder Wheel breakout is a rotary encoder with 24 counts per revolution.

### Count and Angle

The current count can be read by calling `.count()`. It can also be read back as either the number of `.revolutions()` of the encoder, or the angle in `.degrees()` or `.radians()`.

Be aware that the count is stored as an integer, if it is continually increased or decreased it will eventually wrap at `+2147483647` and `-2147483648`. This will cause a jump in the returned by `.revolutions()`, `degrees()` and `.radians()`, that will need handling by your code.

In practice this will take an extremely long time to reach.


### Count Delta

Often you are not interested in the exact count that the encoder is at, but rather if the count has changed since the last time you checked. This change can be read by calling `.delta()` at regular intervals. The returned value can then be used with a check in code, for the value being non-zero.


### Step and Turn

Sometimes it can be useful to know the encoder's position in the form of which step it is at and how many turns have occurred. The current step can be read by calling `.step()`, which returns a value from `0` to `23`, and the number of turns can be read by calling `.turn()`.

These functions differ from reading the `.count()` or `.revolutions()` by using separate counters, and so avoid the wrapping issue that these functions experience.


### Changing the Direction

The counting direction of an encoder can be changed by calling `.direction(REVERSED_DIR)` at any time in code. The `REVERSED_DIR` constant comes from the `ioexpander.common` module. There is also a `NORMAL_DIR` constant, though this is the default.


### Resetting to Zero

There are times where an encoder's count (and related values) need to be reset back to zero. This can be done by calling `.zero()`.


## LEDs

The Encoder Wheel breakout features 24 RGB LEDs arranged in a ring around the wheel. This is the same number as there are steps on the wheel, letting you use the LEDs to show the current step of the wheel.


### Setting an LED

You can set the colour of a LED on the ring in either the RGB colourspace, or HSV (Hue, Saturation, Value). HSV is useful for creating rainbow patterns.

#### RGB

Set the first LED - `0` - to Purple `255, 0, 255`:

```python
wheel.set_rgb(0, 255, 0, 255)
```

#### HSV

Set the first LED - `0` - to Red `0.0`:

```python
wheel.set_hsv(0, 0.0, 1.0, 1.0)
```


### Clear all LEDs

To turn off all the LEDs, the function `.clear()` can be called. This simply goes through each LED and sets its RGB colour to black, making them emit no light.

This function is useful to have at the end of your code to turn the lights off, otherwise they will continue to show the last colours they were given.


### Showing

Changes to the LEDs do not get applied immediately, due to the amount of I2C communication involved. As such, to have the LEDs show what they have been set to after calling the `.set_rgb()`, `.set_hsv()`, and `.clear()` functions, a specific call to `.show()` needs to be made.


## Function Reference

Here is the complete list of functions available on the `EncoderWheel` class:
```python
EncoderWheel(enc_i2c_addr=0x13, led_i2c_addr=0x77, interrupt_timeout=1.0, interrupt_pin=None, skip_chip_id_check=False)
pressed(button)
count()
delta()
step()
turn()
zero()
revolutions()
degrees()
radians()
direction()
direction(direction)
set_rgb(index, r, g, b)
set_hsv(index, h, s=1.0, v=1.0)
clear()
show()
```

## Constants Reference

Here is the complete list of constants on the `encoderwheel` module:

### Address Constants

* `I2C_ADDR` = `0x13`
* `DEFAULT_LED_I2C_ADDR` = `0x77`
* `ALTERNATE_LED_I2C_ADDR` = `0x74`


### Button Constants

* `UP` = `0`
* `DOWN` = `1`
* `LEFT` = `2`
* `RIGHT` = `3`
* `CENTRE` = `4`


### GPIO Constants

* `GP7` = `7`
* `GP8` = `8`
* `GP9` = `9`


### Count Constants

* `NUM_LEDS` = `24`
* `NUM_BUTTONS` = `5`
