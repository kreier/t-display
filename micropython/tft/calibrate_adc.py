# /micropython/apps/calibrate_adc.py  2022-03-31

from machine import Pin, SPI, ADC
import st7789, time

import vga1_16x32 as font

pin_adc = ADC(Pin(12))
pin_adc.atten(ADC.ATTN_11DB)  # full range: 3.3V

white = st7789.color565(255,255,255)
blue  = st7789.color565(0,0,255)
green = st7789.color565(0,255,0)
red   = st7789.color565(255,0,0)
black = st7789.color565(0,0,0)

tft = st7789.ST7789(
    SPI(2, baudrate=30000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(19), miso=Pin(14)),
    135, 240,
    reset = Pin(23, Pin.OUT),
    cs    = Pin(5,  Pin.OUT),
    dc    = Pin(16, Pin.OUT),
    backlight = Pin(4, Pin.OUT),
    rotation=1)
tft.init()
tft.fill(0)

def main():
    pin_raw = supersample(100)
    text1   = "{:}   ".format(int(pin_raw))
    text2   = "{:.3f} V   ".format(pin_raw * 0.000793 + 0.108)
    tft.text(font, "12 bit raw:",    0,   0, green, black)
    tft.text(font, text1,          140,  32, white, black)
    tft.text(font, "Voltage pin:",   0,  74, blue,  black)
    tft.text(font, text2,          140, 102, red,   black)

def supersample(iterations):
    raw = 0
    for k in range(iterations):
        raw += pin_adc.read()
    raw = raw / iterations
    return raw

while True:
    main()
    time.sleep(0.5)
    
print("Done.")

