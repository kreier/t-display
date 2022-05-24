import time
import board
import digitalio
import re

# What pins can be switched on and off?
pins = []

for item in dir(board):
    if item[0] == "G":
        pins.append(item)

for pin in pins:
    print("We investigate Pin {}".format(pin))
    led_pin = "board." + pin
    print(led_pin)
    led = digitalio.DigitalInOut(led_pin)



'''
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True
time.sleep(1)
led.value = False
time.sleep(1)

print("Done!")
led.deinit()

"""CircuitPython Essentials Pin Map Script"""
import microcontroller
import board

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
'''
print("Hello world!")
