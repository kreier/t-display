# Start rp2040 and initiate the display
# https://github.com/kreier/rp2040/blob/main/tft_st7789_240x240/boot.py
# 2023/02/23 v0.2
# 2023/12/29 v0.3 adjusted for CircuitPython 9.0 with fourwire

import board, busio, fourwire
from adafruit_st7789 import ST7789

display.release_displays()

if board.board_id == 'vcc_gnd_yd_rp2040' or board.board_id == 'raspberry_pi_pico_w':
    spi = busio.SPI(clock=board.GP10, MOSI=board.GP11)
    tft_cs = board.GP9
    tft_dc = board.GP8
    display_bus = fourwire.FourWire(
        spi, command=tft_dc, chip_select=tft_cs, reset=board.GP12
    )
    display = ST7789(display_bus, width=240, height=240, rowstart=80, rotation=0)
if board.board_id == 'lilygo_ttgo_tdisplay_esp32_4m':
    tft_dc    = board.LCD_DC
    tft_cs    = board.LCD_CS
    spi_clk   = board.LCD_CLK
    spi_mosi  = board.LCD_MOSI
    tft_rst   = board.LCD_RESET
    backlight = board.LCD_BACKLIGHT
    spi = busio.SPI(spi_clk, spi_mosi)    
    display = ST7789(
        display_bus,
        rotation=270,
        width=240,
        height=135,
        rowstart=40,
        colstart=53,
        backlight_pin=backlight,
    )
