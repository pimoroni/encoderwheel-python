import time
from encoderwheel import EncoderWheel
from colorsys import hsv_to_rgb

"""
Displays a rotating rainbow pattern on Encoder Wheel's LED ring.
"""

# Constants
SPEED = 5           # The speed that the LEDs will cycle at
BRIGHTNESS = 1.0    # The brightness of the LEDs
UPDATES = 50        # How many times the LEDs will be updated per second
UPDATE_RATE = 1 / UPDATES

# Create a new EncoderWheel
wheel = EncoderWheel()

# Variables
offset = 0.0


# Sleep until a specific time in the future. Use this instead of time.sleep() to correct for
# inconsistent timings when dealing with complex operations or external communication
def sleep_until(end_time):
    time_to_sleep = end_time - time.monotonic()
    if time_to_sleep > 0.0:
        time.sleep(time_to_sleep)


# Make rainbows
while True:

    # Record the start time of this loop
    start_time = time.monotonic()

    offset += SPEED / 1000.0

    # Update all the LEDs
    for i in range(24):
        hue = float(i) / 24
        r, g, b = [int(c * 255) for c in hsv_to_rgb(hue + offset, 1.0, BRIGHTNESS)]
        wheel.set_pixel(i, r, g, b)
    wheel.show()

    # Sleep until the next update, accounting for how long the above operations took to perform
    sleep_until(start_time + UPDATE_RATE)
