# hello_world.py

from machine import Pin, SPI
import st7789

# Choose a font

# import vga1_8x8 as font
# import vga2_8x8 as font

# import vga1_8x16 as font
# import vga2_8x16 as font

# import vga1_16x16 as font
# import vga1_bold_16x16 as font
# import vga2_16x16 as font
# import vga2_bold_16x16 as font

# import vga1_16x32 as font
# import vga1_bold_16x32 as font
# import vga2_16x32 as font
import vga2_bold_16x32 as font

def main():
    tft = st7789.ST7789(
        SPI(2, baudrate=30000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(19)),
        135, 240, reset=Pin(23, Pin.OUT), cs=Pin(5, Pin.OUT), dc=Pin(16, Pin.OUT),
        backlight=Pin(4, Pin.OUT), rotation=3)

    tft.init()
    tft.fill(0)
    tft.text(font,"Hello world!",
        0,
        0,
        st7789.color565(8,8,8),
        st7789.color565(0,0,0)
    )

main()