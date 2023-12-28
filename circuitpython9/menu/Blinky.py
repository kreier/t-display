# LED Blink T-Display rpi2040
# https://github.com/kreier/t-display/tree/main/circuitpython_rpi2040/menu

import time, board, digitalio, config, displayio

display = config.disp
display.root_group = displayio.CIRCUITPYTHON_TERMINAL
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
    if timer + 1 < time.monotonic():
        LED.value = not LED.value
        timer = time.monotonic()
        print("LED", end=" ")
