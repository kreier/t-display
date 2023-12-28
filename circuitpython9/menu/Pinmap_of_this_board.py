"""CircuitPython Essentials Pin Map Script"""
# adapted for T-Display with line 5-8 led and button_next and the finishing loop
# https://github.com/kreier/t-display/tree/main/circuitpython_rpi2040/menu

import microcontroller, board, displayio

display.root_group = displayio.CIRCUITPYTHON_TERMINAL

board_pins = []
for pin in dir(microcontroller.pin):
    if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
        pins = []
        for alias in dir(board):
            if getattr(board, alias) is getattr(microcontroller.pin, pin):
                pins.append("board.{}".format(alias))
        if len(pins) > 0:
            board_pins.append(" ".join(pins))
for pins in sorted(board_pins):
    print(pins)

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
