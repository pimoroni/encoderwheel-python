import time
from encoderwheel import EncoderWheel
from colorsys import hsv_to_rgb

"""
Create a colour wheel on the Encoder Wheel's LED ring, and use all functions of the wheel to interact with it.

Rotate the wheel to select a Hue
Press the up direction to increase Brightness
Press the down direction to decrease Brightness
Press the left direction to decrease Saturation
Press the right direction to increase Saturation
Press the centre to hide the selection marker
"""

# Constants
BRIGHTNESS_STEP = 0.02      # How much to increase or decrease the brightness each update
SATURATION_STEP = 0.02      # How much to increase or decrease the saturation each update
UPDATES = 50                # How many times to update the LEDs per second
UPDATE_RATE = 1 / UPDATES

# Create a new EncoderWheel
wheel = EncoderWheel()

# Variables
brightness = 1.0
saturation = 1.0
last_count = 0
position = 0
changed = True
last_centre_pressed = False


# Simple function to clamp a value between 0.0 and 1.0
def clamp01(value):
    return max(min(value, 1.0), 0.0)


# Sleep until a specific time in the future. Use this instead of time.sleep() to correct for
# inconsistent timings when dealing with complex operations or external communication
def sleep_until(end_time):
    time_to_sleep = end_time - time.monotonic()
    if time_to_sleep > 0.0:
        time.sleep(time_to_sleep)


while True:
    # Record the start time of this loop
    start_time = time.monotonic()

    # If up is pressed, increase the brightness
    if wheel.ioe.input(wheel.SW_UP) == 0:
        brightness += BRIGHTNESS_STEP
        changed = True  # Trigger a change

    # If down is pressed, decrease the brightness
    if wheel.ioe.input(wheel.SW_DOWN) == 0:
        brightness -= BRIGHTNESS_STEP
        changed = True  # Trigger a change

    # If right is pressed, increase the saturation
    if wheel.ioe.input(wheel.SW_RIGHT) == 0:
        saturation += SATURATION_STEP
        changed = True  # Trigger a change

    # If left is pressed, decrease the saturation
    if wheel.ioe.input(wheel.SW_LEFT) == 0:
        saturation -= SATURATION_STEP
        changed = True  # Trigger a change

    # Limit the brightness and saturation between 0.0 and 1.0
    brightness = clamp01(brightness)
    saturation = clamp01(saturation)

    # Check if the encoder has been turned
    count = wheel.count()
    if count != last_count:
        change = count - last_count
        last_count = count

        # Update the position based on the count change
        position += change
        if change > 0:
            if position >= 24:
                position -= 24
        else:
            if position < 0:
                position += 24
        changed = True  # Trigger a change

    # If centre is pressed, trigger a change
    centre_pressed = wheel.ioe.input(wheel.SW_CENTRE) == 0
    if centre_pressed != last_centre_pressed:
        changed = True
    last_centre_pressed = centre_pressed

    # Was a change triggered?
    if changed:
        # Print the colour at the current hue, saturation, and brightness
        r, g, b = [int(c * 255) for c in hsv_to_rgb(position / 24, saturation, brightness)]
        print("Colour Code = #", hex(r)[2:].zfill(2), hex(g)[2:].zfill(2), hex(b)[2:].zfill(2), sep="")

        # Set the LED at the current position to either the actual colour,
        # or an inverted version to show a "selection marker"
        if centre_pressed:
            wheel.set_pixel(position, r, g, b)
        else:
            wheel.set_pixel(position, 255 - r, 255 - g, 255 - b)

        # Set the LEDs below the current position
        for i in range(0, position):
            r, g, b = [int(c * 255) for c in hsv_to_rgb(i / 24, saturation, brightness)]
            wheel.set_pixel(i, r, g, b)

        # Set the LEDs after the current position
        for i in range(position + 1, 24):
            r, g, b = [int(c * 255) for c in hsv_to_rgb(i / 24, saturation, brightness)]
            wheel.set_pixel(i, r, g, b)
        wheel.show()
        changed = False

    # Sleep until the next update, accounting for how long the above operations took to perform
    sleep_until(start_time + UPDATE_RATE)
