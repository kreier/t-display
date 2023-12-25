# toggle the write switch to the local file system 2023/12/23

import board
import busio
import displayio
from adafruit_st7789 import ST7789

# Release any resources currently in use for the displays
displayio.release_displays()

tft_dc    = board.LCD_DC
tft_cs    = board.LCD_CS
spi_clk   = board.LCD_CLK
spi_mosi  = board.LCD_MOSI
tft_rst   = board.LCD_RESET
backlight = board.LCD_BACKLIGHT
spi = busio.SPI(spi_clk, spi_mosi)

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)

display = ST7789(
    display_bus,
    rotation=270,
    width=240,
    height=135,
    rowstart=40,
    colstart=53,
    backlight_pin=backlight,
)


import time
import board
import digitalio
import storage

button_pin = board.BUTTON_L
# T-Display rp2040     board.BUTTON_L    False if pressed
# rp2040 with NeoPixel board.BUTTON
# T-Display ESP32-S2   board.IO0

button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
# button.pull = digitalio.Pull.UP

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

time.sleep(1)
timer = 5
can_write = False
print(f"Press the button in the next {timer} seconds to activate saving")
end = time.monotonic() + timer
print(timer)
while end - time.monotonic() > 0:
    if not button.value:
        print("write access activated")
        storage.remount("/", False)
        can_write = True
    if end - timer + 1 < time.monotonic():
        timer -= 1
        led.value = False
        time.sleep(0.1)
        led.value = True
        print(timer)
    if can_write:
        led.value = False
    else:
        led.value = True
if not can_write:
    print("Not activated")
time.sleep(1)
