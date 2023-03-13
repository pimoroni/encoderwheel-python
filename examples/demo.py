from encoderwheel import EncoderWheel
from colorsys import hsv_to_rgb

wheel = EncoderWheel()

last_count = 0
position = 0

mode = True
last_pressed = False
while True:
    pressed = wheel.ioe.input(wheel.SW_CENTRE) == 0
    if pressed != last_pressed:
        if pressed:
            mode = not mode
            for i in range(24):
                if mode:
                    wheel.set_pixel(i, 0, 0, 0)
                else:
                    r, g, b = [int(c * 255) for c in hsv_to_rgb(i / 24, 1.0, 1.0)]
                    wheel.set_pixel(i, r, g, b)
        last_pressed = pressed

    count = wheel.count()
    if count != last_count:
        if count - last_count > 0:
            print("Clockwise, Count =", count)
        else:
            print("Counter Clockwise, Count =", count)
        
        if mode:
            wheel.set_pixel(position, 0, 0, 0)
        else:
            r, g, b = [int(c * 255) for c in hsv_to_rgb(position / 24, 1.0, 1.0)]
            wheel.set_pixel(position, r, g, b)
            
        change = count - last_count
        position += change
        if change > 0:
            if position >= 24:
                position -= 24
        else:
            if position < 0:
                position += 24
        
        last_count = count
    
    if mode:
        r, g, b = [int(c * 255) for c in hsv_to_rgb(position / 24, 1.0, 1.0)]
        wheel.set_pixel(position, r, g, b)
    else:
        wheel.set_pixel(position, 255, 255, 255)
    wheel.show()
