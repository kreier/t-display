import board, time, busio, displayio, busdisplay
import adafruit_displayio_ssd1306

#busdisplay.release_displays()
displayio.release_displays()
i2c = busio.I2C(board.GP1, board.GP0)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
