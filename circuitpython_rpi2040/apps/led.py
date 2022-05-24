import time
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True
time.sleep(1)
led.value = False
time.sleep(1)

print("Done!")
led.deinit()
