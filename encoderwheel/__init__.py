import time
from colorsys import hsv_to_rgb

from ioexpander import IN_PU, IOE
from ioexpander.encoder import Encoder

from encoderwheel import is31fl3731

__version__ = '0.0.1'

I2C_ADDR = 0x13
DEFAULT_LED_I2C_ADDR = 0x77
ALTERNATE_LED_I2C_ADDR = 0x74
NUM_LEDS = 24
NUM_BUTTONS = 5

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
CENTRE = 4

GP7 = 7
GP8 = 8
GP9 = 9


class EncoderWheel():
    ENC_CHANNEL = 1
    ENC_TERMS = (3, 12)

    SW_UP = 13
    SW_DOWN = 4
    SW_LEFT = 11
    SW_RIGHT = 2
    SW_CENTRE = 1

    def __init__(self, enc_i2c_addr=I2C_ADDR, led_i2c_addr=DEFAULT_LED_I2C_ADDR, interrupt_timeout=1.0, interrupt_pin=None, skip_chip_id_check=False):
        self.ioe = IOE(i2c_addr=enc_i2c_addr,
                       interrupt_timeout=interrupt_timeout,
                       interrupt_pin=interrupt_pin,
                       gpio=None,
                       skip_chip_id_check=skip_chip_id_check
                       )

        self.encoder = Encoder(self.ioe, self.ENC_CHANNEL, self.ENC_TERMS, count_microsteps=True, count_divider=2)
        self.ioe.set_mode(self.SW_UP, IN_PU)
        self.ioe.set_mode(self.SW_DOWN, IN_PU)
        self.ioe.set_mode(self.SW_LEFT, IN_PU)
        self.ioe.set_mode(self.SW_RIGHT, IN_PU)
        self.ioe.set_mode(self.SW_CENTRE, IN_PU)
        self.button_map = {
            UP: self.SW_UP,
            RIGHT: self.SW_RIGHT,
            DOWN: self.SW_DOWN,
            LEFT: self.SW_LEFT,
            CENTRE: self.SW_CENTRE
        }

        self.is31fl3731 = is31fl3731.RGBRing(None, address=led_i2c_addr, gamma_table=is31fl3731.LED_GAMMA)
        self.is31fl3731.clear()
        self.is31fl3731.show()

    def pressed(self, button):
        if button < 0 or button >= NUM_BUTTONS:
            raise ValueError(f"button out of range. Expected 0 to {NUM_BUTTONS - 1}")

        return self.ioe.input(self.button_map[button]) == 0

    def count(self):
        return self.encoder.count()

    def delta(self):
        return self.encoder.delta()

    def step(self):
        return self.encoder.step()

    def turn(self):
        return self.encoder.turn()

    def zero(self):
        return self.encoder.zero()

    def revolutions(self):
        return self.encoder.revolutions()

    def degrees(self):
        return self.encoder.degrees()

    def radians(self):
        return self.encoder.radians()

    def direction(self, direction=None):
        return self.encoder.direction(direction)

    def set_rgb(self, index, r, g, b):
        if index < 0 or index >= NUM_LEDS:
            raise ValueError(f"index out of range. Expected 0 to {NUM_LEDS - 1}")

        self.is31fl3731.set_pixel(index, r, g, b)

    def set_hsv(self, index, h, s=1.0, v=1.0):
        if index < 0 or index >= NUM_LEDS:
            raise ValueError(f"index out of range. Expected 0 to {NUM_LEDS - 1}")

        r, g, b = [int(c * 255) for c in hsv_to_rgb(h, s, v)]
        self.is31fl3731.set_pixel(index, r, g, b)

    def clear(self):
        self.is31fl3731.clear()

    def show(self):
        self.is31fl3731.show()


if __name__ == "__main__":
    wheel = EncoderWheel()

    last_update_time = time.monotonic()
    led_index = 0
    led_sequence = 0
    last_count = 0

    last_pressed = {
        wheel.SW_UP: False,
        wheel.SW_DOWN: False,
        wheel.SW_LEFT: False,
        wheel.SW_RIGHT: False,
        wheel.SW_CENTRE: False,
    }

    while True:

        current_time = time.monotonic()
        if current_time >= last_update_time + 0.1:
            if led_sequence == 0:
                wheel.set_pixel(led_index, 255, 0, 0)

            if led_sequence == 1:
                wheel.set_pixel(led_index, 0, 255, 0)

            if led_sequence == 2:
                wheel.set_pixel(led_index, 0, 0, 255)

            if led_sequence == 3:
                wheel.set_pixel(led_index, 255, 255, 255)

            if led_sequence == 4:
                wheel.set_pixel(led_index, 0, 0, 0)

            led_index += 1
            if led_index >= 24:
                led_index = 0
                led_sequence += 1
                if led_sequence >= 5:
                    led_sequence = 0

            last_update_time = current_time
            wheel.show()

        count = wheel.count()
        if count != last_count:
            if count - last_count > 0:
                print("Clockwise, Count =", count)
            else:
                print("Counter Clockwise, Count =", count)
            last_count = count

        pressed = wheel.ioe.input(wheel.SW_UP) == 0
        if pressed != last_pressed[wheel.SW_UP]:
            if pressed:
                print("Up Pressed")
            else:
                print("Up Released")
            last_pressed[wheel.SW_UP] = pressed

        pressed = wheel.ioe.input(wheel.SW_DOWN) == 0
        if pressed != last_pressed[wheel.SW_DOWN]:
            if pressed:
                print("Down Pressed")
            else:
                print("Down Released")
            last_pressed[wheel.SW_DOWN] = pressed

        pressed = wheel.ioe.input(wheel.SW_LEFT) == 0
        if pressed != last_pressed[wheel.SW_LEFT]:
            if pressed:
                print("Left Pressed")
            else:
                print("Left Released")
            last_pressed[wheel.SW_LEFT] = pressed

        pressed = wheel.ioe.input(wheel.SW_RIGHT) == 0
        if pressed != last_pressed[wheel.SW_RIGHT]:
            if pressed:
                print("Right Pressed")
            else:
                print("Right Released")
            last_pressed[wheel.SW_RIGHT] = pressed

        pressed = wheel.ioe.input(wheel.SW_CENTRE) == 0
        if pressed != last_pressed[wheel.SW_CENTRE]:
            if pressed:
                print("Centre Pressed")
            else:
                print("Centre Released")
            last_pressed[wheel.SW_CENTRE] = pressed
