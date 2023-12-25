"""CircuitPython Essentials Pin Map Script"""
# adapted for T-Display with line 5-8 led and button_next and the finishing loop
# https://github.com/kreier/t-display/tree/main/circuitpython_rpi2040/menu

import microcontroller, board, digitalio

button_next = digitalio.DigitalInOut(board.BUTTON_L)
button_next.direction = digitalio.Direction.INPUT
led = digitalio.DigitalInOut(board.LED) # GP25
led.direction = digitalio.Direction.OUTPUT

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

timer = time.monotonic()
led.value = True
while True:
    if not button_next.value:
        led.deinit()
        button_next.deinit()
        exec(open("code.py").read())
    if timer + 0.4 < time.monotonic():
        led.value = not led.value
        timer = time.monotonic()
