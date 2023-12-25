# LED Blink T-Display rpi2040
# https://github.com/kreier/t-display/tree/main/circuitpython_rpi2040/menu

import time, board, digitalio

button_next = digitalio.DigitalInOut(board.BUTTON_L)
button_next.direction = digitalio.Direction.INPUT
led = digitalio.DigitalInOut(board.LED) # GP25
led.direction = digitalio.Direction.OUTPUT

timer = time.monotonic()
led.value = True
while True:
    if not button_next.value:
        led.deinit()
        button_next.deinit()
        exec(open("code.py").read())
    if timer + 1 < time.monotonic():
        led.value = not led.value
        timer = time.monotonic()
        print("LED", end=" ")
