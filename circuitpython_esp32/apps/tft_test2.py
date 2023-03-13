# ST7789 on T-Display RP2040 @kreier 2023-03-04
# TFT_SCLK  2
# TFT_CS    5
# TFT_DC    1
# TFT_RST   0
# TFT_BL    4
# TFT_MOSI  3
# TFT_MISO  N/A

import board, time
import displayio
import digitalio
import busio
import terminalio
import adafruit_st7789
from adafruit_display_text import label

# First set some parameters used for shapes and text
BORDER = 20
FONTSCALE = 2
BACKGROUND_COLOR = 0x00FF00  # Bright Green
FOREGROUND_COLOR = 0xAA0088  # Purple
TEXT_COLOR = 0xFFFF00

print("Start SPI bus")
time.sleep(5)
print("Let's go")
displayio.release_displays()
spi = busio.SPI(board.D18, MOSI=board.D19, MISO=None)
while not spi.try_lock():
    pass
spi.configure(baudrate=24000000) # Configure SPI for 24MHz
spi.unlock()
tft_cs = board.D5
tft_dc = board.RX

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D23)
display = adafruit_st7789.ST7789(display_bus, width=240, height=135, rowstart=40, colstart=53, rotation=270)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(
    display.width - BORDER * 2, display.height - BORDER * 2, 1
)
inner_palette = displayio.Palette(1)
inner_palette[0] = FOREGROUND_COLOR
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# Draw a label
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
text_width = text_area.bounding_box[2] * FONTSCALE
text_group = displayio.Group(
    scale=FONTSCALE,
    x=display.width // 2 - text_width // 2,
    y=display.height // 2,
)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

bl = digitalio.DigitalInOut(board.D2)
bl.direction = digitalio.Direction.OUTPUT
while True:
    print("Backlight on.")
    bl.value = True
    time.sleep(1)
    print("Backlight off.")
    bl.value = False
    time.sleep(1)
    pass