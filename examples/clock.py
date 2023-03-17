import time
import math
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

PULSE_CYCLE_TIME = 2
UPDATES_PER_PULSE = PULSE_CYCLE_TIME * UPDATES

COUNTING_TIME = 60
UPDATES_PER_COUNT = COUNTING_TIME * UPDATES

# Create a new EncoderWheel
wheel = EncoderWheel()


# Sleep until a specific time in the future. Use this instead of time.sleep() to correct for
# inconsistent timings when dealing with complex operations or external communication
def sleep_until(end_time):
    time_to_sleep = end_time - time.monotonic()
    if time_to_sleep > 0.0:
        time.sleep(time_to_sleep)
        
        
def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))    

from datetime import datetime

# Make rainbows
while True:

    # Record the start time of this loop
    start_time = time.monotonic()
    
    t = time.localtime(time.time())
    now = datetime.now()
    r_update = (now.second * 1000) + (now.microsecond // 1000)
    g_update = (now.minute * 60 * 1000) + r_update
    b_update = ((now.hour % 12) * 60 * 60 * 1000) + g_update
            
    #leds_to_light = min(update / UPDATES_PER_COUNT, 1.0) * 24
    r_to_light = min(r_update / (1000 * 60), 1.0) * 24
    g_to_light = min(g_update / (1000 * 60 * 60), 1.0) * 24
    b_to_light = min(b_update / (1000 * 60 * 60 * 12), 1.0) * 24
    for i in range(24):  #Has an issue with effect wrapping around the top
        if i > r_to_light:
            r = clamp((r_to_light - i) + 1, 0.0, 1.0) * BRIGHTNESS * 255
        else:
            r = clamp((i - r_to_light) + 1, 0.0, 1.0) * BRIGHTNESS * 255

        if i > g_to_light:
            g = clamp((g_to_light - i) + 1, 0.0, 1.0) * BRIGHTNESS * 255
        else:
            g = clamp((i - g_to_light) + 1, 0.0, 1.0) * BRIGHTNESS * 255
            
        if i > b_to_light:
            b = clamp((b_to_light - i) + 1, 0.0, 1.0) * BRIGHTNESS * 255
        else:
            b = clamp((i - b_to_light) + 1, 0.0, 1.0) * BRIGHTNESS * 255
        wheel.set_pixel(i, r, g, b)
    wheel.show()

    # Sleep until the next update, accounting for how long the above operations took to perform
    sleep_until(start_time + UPDATE_RATE)
