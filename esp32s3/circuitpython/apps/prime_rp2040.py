import math, time, board, busio, terminalio, displayio
from adafruit_st7789 import ST7789
displayio.release_displays()
spi = busio.SPI(clock=board.GP10, MOSI=board.GP11)
tft_cs = board.GP9
tft_dc = board.GP8
display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=board.GP12
)
display = ST7789(display_bus, width=240, height=240, rowstart=80)

last = 500
disp = True
found = 4             # we start from 11, know 2, 3, 5, 7
print(f"Prime numbers to {last}")
print("2, 3, 5, 7", end="")

start = time.monotonic()
for number in range(11, last, 2):
    prime = True
    for divider in range(3, int(math.sqrt(number))+1, 2):
        if number % divider == 0:
            prime = False
            break
    if prime:
        found += 1
        if disp:
            print(number, sep=', ', end=' ')
end = time.monotonic()
print(f"\nThis took: {(end - start)} seconds.")
print(f"I found {found} prime numbers.")
