import time
from encoderwheel import EncoderWheel
from colorsys import hsv_to_rgb

UPDATES = 50                           # How many times to update the LEDs per second
UPDATE_RATE = 1 / UPDATES
BRIGHTNESS_STEP = 0.02
SATURATION_STEP = 0.02

wheel = EncoderWheel()

last_count = 0
position = 0

last_centre_pressed = False

brightness = 1.0
saturation = 1.0

def clamp01(value):
    return max(min(value, 1.0), 0.0)


# Sleep until a specific time in the future. Use this instead of time.sleep() to correct for
# inconsistent timings when dealing with complex operations or external communication
def sleep_until(end_time):
    time_to_sleep = end_time - time.monotonic()
    if time_to_sleep > 0.0:
        time.sleep(time_to_sleep)

changed = True
while True:
    # Record the start time of this loop
    start_time = time.monotonic()

    if wheel.ioe.input(wheel.SW_UP) == 0:
        brightness += BRIGHTNESS_STEP
        changed = True

    if wheel.ioe.input(wheel.SW_DOWN) == 0:
        brightness -= BRIGHTNESS_STEP
        changed = True
    brightness = clamp01(brightness)

    if wheel.ioe.input(wheel.SW_RIGHT) == 0:
        saturation += SATURATION_STEP
        changed = True

    if wheel.ioe.input(wheel.SW_LEFT) == 0:
        saturation -= SATURATION_STEP
        changed = True
    saturation = clamp01(saturation)

    count = wheel.count()
    if count != last_count:
        change = count - last_count
        position += change
        if change > 0:
            if position >= 24:
                position -= 24
        else:
            if position < 0:
                position += 24

        last_count = count
        changed = True

    centre_pressed = wheel.ioe.input(wheel.SW_CENTRE) == 0
    if centre_pressed != last_centre_pressed:
        changed = True
        last_centre_pressed = centre_pressed

    if changed:
        r, g, b = [int(c * 255) for c in hsv_to_rgb(position / 24, saturation, brightness)]
        if centre_pressed:
            wheel.set_pixel(position, r, g, b)
        else:
            wheel.set_pixel(position, 255 - r, 255 - g, 255 - b)
        print("Colour Code = #", hex(r)[2:].zfill(2), hex(g)[2:].zfill(2), hex(b)[2:].zfill(2), sep="")

        for i in range(0, position):
            r, g, b = [int(c * 255) for c in hsv_to_rgb(i / 24, saturation, brightness)]
            wheel.set_pixel(i, r, g, b)

        for i in range(position + 1, 24):
            r, g, b = [int(c * 255) for c in hsv_to_rgb(i / 24, saturation, brightness)]
            wheel.set_pixel(i, r, g, b)
        wheel.show()
        changed = False

    # Sleep until the next update, accounting for how long the above operations took to perform
    sleep_until(start_time + UPDATE_RATE)
