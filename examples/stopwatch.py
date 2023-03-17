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

# Variables
offset = 0.0

PULSE_MAX_BRIGHTNESS = 0.5
PULSE_MIN_BRIGHTNESS = 0.2

IDLE, COUNTING, PAUSED = range(3)

state = IDLE


# Sleep until a specific time in the future. Use this instead of time.sleep() to correct for
# inconsistent timings when dealing with complex operations or external communication
def sleep_until(end_time):
    time_to_sleep = end_time - time.monotonic()
    if time_to_sleep > 0.0:
        time.sleep(time_to_sleep)
        
        
def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))    

update = 0
r_update = 0
g_update = 0
b_update = 0

last_centre_pressed = False

# Make rainbows
while True:

    # Record the start time of this loop
    start_time = time.monotonic()
    
    centre_pressed = wheel.ioe.input(wheel.SW_CENTRE) == 0
    if centre_pressed != last_centre_pressed:
        if centre_pressed:
            if state == IDLE:
                r_update = 0
                g_update = 0
                b_update = 0
                state = COUNTING
            elif state == COUNTING:
                update = 0
                state = PAUSED
            elif state == PAUSED:
                state = COUNTING
        last_centre_pressed = centre_pressed
    
    if state == IDLE:    
        percent_along = min(update / UPDATES_PER_PULSE, 1.0)
        brightness = ((math.cos(percent_along * math.pi * 2) + 1.0) / 2.0) * ((PULSE_MAX_BRIGHTNESS - PULSE_MIN_BRIGHTNESS)) + PULSE_MIN_BRIGHTNESS
        # Update all the LEDs
        for i in range(24):
            r, g, b = [int(c * 255) for c in hsv_to_rgb(0.0, 0.0, brightness)]
            wheel.set_pixel(i, r, g, b)
        wheel.show()
        
        update += 1
        
        if update >= UPDATES_PER_PULSE:
            update = 0

    elif state == COUNTING:
        #leds_to_light = min(update / UPDATES_PER_COUNT, 1.0) * 24
        r_to_light = min(r_update / UPDATES, 1.0) * 24
        g_to_light = min(g_update / (UPDATES * 60), 1.0) * 24
        b_to_light = min(b_update / (UPDATES * 60 * 60), 1.0) * 24
        for i in range(24):
            #percent_of_led = clamp(leds_to_light - i, 0.0, 1.0) * BRIGHTNESS
            r = clamp(r_to_light - i, 0.0, 1.0) * BRIGHTNESS * 255
            g = clamp(g_to_light - i, 0.0, 1.0) * BRIGHTNESS * 255
            b = clamp(b_to_light - i, 0.0, 1.0) * BRIGHTNESS * 255
            #r, g, b = [int(c * 255) for c in hsv_to_rgb(0.0, 0.0, percent_of_led)]
            wheel.set_pixel(i, r, g, b)
        wheel.show()
        print()
        
        r_update += 1
        g_update += 1
        b_update += 1
        
        if r_update >= UPDATES:
            r_update = 0
        if g_update >= (UPDATES * 60):
            g_update = 0
        if b_update >= (UPDATES * 60 * 60):
            b_update = 0
    
    # Sleep until the next update, accounting for how long the above operations took to perform
    sleep_until(start_time + UPDATE_RATE)
