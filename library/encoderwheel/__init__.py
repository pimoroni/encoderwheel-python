import time
from ioexpander import IOE, IN, IN_PU
from encoderwheel import is31fl3731

__version__ = '0.0.1'

I2C_ADDR = 0x13
DEFAULT_LED_I2C_ADDR = 0x77
ALTERNATE_LED_I2C_ADDR = 0x74

class EncoderWheel():
    NUM_LEDS = 24
    ENC_CHANNEL = 1
    ENC_TERM_A = 3
    ENC_TERM_B = 12
    
    SW_UP = 13
    SW_DOWN = 4
    SW_LEFT = 11
    SW_RIGHT = 2
    SW_CENTRE = 1

    def __init__(self, enc_i2c_addr=I2C_ADDR, led_i2c_addr=DEFAULT_LED_I2C_ADDR, interrupt_timeout=1.0, interrupt_pin=None, gpio=None, skip_chip_id_check=False):
        self.ioe = IOE(i2c_addr=enc_i2c_addr,
                       interrupt_timeout=interrupt_timeout,
                       interrupt_pin=interrupt_pin,
                       gpio=gpio,
                       skip_chip_id_check=skip_chip_id_check
                       )

        self.ioe.setup_rotary_encoder(self.ENC_CHANNEL, self.ENC_TERM_A, self.ENC_TERM_B, count_microsteps=True)
        self.ioe.set_mode(self.SW_UP, IN_PU)
        self.ioe.set_mode(self.SW_DOWN, IN_PU)
        self.ioe.set_mode(self.SW_LEFT, IN_PU)
        self.ioe.set_mode(self.SW_RIGHT, IN_PU)
        self.ioe.set_mode(self.SW_CENTRE, IN_PU)

        self.is31fl3731 = is31fl3731.RGBRing(None, address=led_i2c_addr, gamma_table=is31fl3731.LED_GAMMA)
        self.is31fl3731.clear()
        self.is31fl3731.show()

    def set_pixel(self, index, r, g, b):
        if index < 0 or index >= self.NUM_LEDS:
            raise ValueError("index out of range. Expected 0 to 23")

        self.is31fl3731.set_pixel(index, r, g, b)
        
    def show(self):
        self.is31fl3731.show()
        
    def count(self):
        return self.ioe.read_rotary_encoder(self.ENC_CHANNEL) // 2


if __name__ == "__main__":
    wheel = EncoderWheel()#led_i2c_addr=ALTERNATE_LED_I2C_ADDR)

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
   
