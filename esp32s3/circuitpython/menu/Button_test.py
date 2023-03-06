# Input button A and B test code - with debouncer
# Button A: GP15
# Button B: GP17

# https://github.com/ssis-aa/rvr2023/blob/main/circuitpython/menu/Button_test.py

import time
import board
import digitalio
from adafruit_debouncer import Debouncer

pin_a = digitalio.DigitalInOut(board.GP15)
pin_a.direction = digitalio.Direction.INPUT
pin_a.pull = digitalio.Pull.UP
button_a = Debouncer(pin_a, interval=0.05)
pin_b = digitalio.DigitalInOut(board.GP17)
pin_b.direction = digitalio.Direction.INPUT
pin_b.pull = digitalio.Pull.UP
button_b = Debouncer(pin_b, interval=0.05)

print("Press button A or B")

while True:
    button_a.update()
    button_b.update()
    if button_a.fell:
        print("A <--- button       ")
        time.sleep(0.1)
    if button_b.rose:
        print("       button ---> B")
        time.sleep(0.1)
