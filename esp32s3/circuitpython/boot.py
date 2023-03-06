# Start rp2040 and initiate the display
# https://github.com/kreier/rp2040/blob/main/tft_st7789_240x240/boot.py
# 2023/02/23 v0.2

import board, busio, displayio
from adafruit_st7789 import ST7789
displayio.release_displays()
spi = busio.SPI(clock=board.GP10, MOSI=board.GP11)
tft_cs = board.GP9
tft_dc = board.GP8
display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=board.GP12
)
display = ST7789(display_bus, width=240, height=240, rowstart=80, rotation=90)

print("Display activated.")
# exec(open("apps/menu.py").read())
# does not work
