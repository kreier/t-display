# welcome blink and post

import time
import board
import digitalio
import microcontroller

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

for x in range(3):
    led.value = False
    time.sleep(0.2)
    led.value = True
    time.sleep(0.2)

print("This is a {}, running at {:.1f} MHz".format(board.board_id, float(microcontroller.cpu.frequency)/1000000))
print("The CPU has a temperature of {:.1f} °C.".format(microcontroller.cpu.temperature))
