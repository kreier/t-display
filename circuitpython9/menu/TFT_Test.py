# ST7789 on T-Display RP2040 @kreier 2022-05-23

import board, displayio

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x2345FF

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)


# standardized final loop part for T-Display programs to return to the menu
import time, board, digitalio, config
BUTTON_EXIT = digitalio.DigitalInOut(config.pin_button_ok)
BUTTON_EXIT.direction = digitalio.Direction.INPUT
if config.pullup:
    BUTTON_EXIT.pull = digitalio.Pull.UP
LED = digitalio.DigitalInOut(config.pin_led)
LED.direction = digitalio.Direction.OUTPUT
timer = time.monotonic()
LED.value = True
while True:
    if not BUTTON_EXIT.value:
        LED.deinit()
        BUTTON_EXIT.deinit()
        exec(open("code.py").read())
    if timer + 2 < time.monotonic():
        LED.value = not LED.value
        timer = time.monotonic()
