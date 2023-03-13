# red LED on and off - 2022/05/23 @kreier
# LILYGO T-Display rpi2040

import time
import board
import digitalio

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
print("Turn LED on")
led.value = True
time.sleep(2)
print("Turn LED off")
led.value = False
time.sleep(2)

print("Done!")
led.deinit()
