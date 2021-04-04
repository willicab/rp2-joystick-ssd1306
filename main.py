from machine import ADC, I2C, Pin
from ssd1306 import SSD1306_I2C # https://github.com/stlehmann/micropython-ssd1306
from gfx import GFX # https://github.com/adafruit/Adafruit-GFX-Library

# Configure Joystick
MAX= 65535 # This value depends on the input voltage of the joystick
joy_x = ADC(26)
joy_y = ADC(27)
joy_z = Pin(28, Pin.IN, Pin.PULL_UP)
old_z = 1

# Configure OLED Display
WIDTH = 128
HEIGHT = 64
i2c = I2C(1, scl=Pin(19), sda=Pin(18))
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.contrast(0)

# Configure Graphic Class
gfx = GFX(WIDTH, HEIGHT, oled.pixel)
shape = 0

while True:
    # Set the shape value
    if joy_z.value() == 0 and old_z == 1:
        shape += 1
    if shape == 4:
        shape = 0
    old_z = joy_z.value()
    # Get the joystick values
    pos_x = joy_x.read_u16()
    pos_y = joy_y.read_u16()
    # Calculate the position in screen
    point_x = int((pos_x * (WIDTH - 1)) / MAX)
    point_y = int((pos_y * (HEIGHT - 1)) / MAX)
    # Draw the info and Shape
    oled.fill(0)
    oled.text('X: {}'.format(pos_x), 0, 0)
    oled.text('Y: {}'.format(pos_y), 0, 12)
    oled.text('Point X: {}'.format(point_x), 0, 24)
    oled.text('Point Y: {}'.format(point_y), 0, 36)
    oled.text('Shape: {}'.format(shape), 0, 48)
    if shape == 0:
        gfx.circle(point_x, point_y, 10, 1)
    elif shape == 1:    
        gfx.fill_circle(point_x, point_y, 10, 1)
    elif shape == 2:
        gfx.rect(point_x - 10, point_y - 10, 20, 20, 1)
    elif shape == 3:
        gfx.fill_rect(point_x - 10, point_y - 10, 20, 20, 1)
    oled.show()
