# TTGO T-Display ESP32 board

This board is chosen as the default board for students to learn programming because it has a display for output, a USB-C connector for data transfer and charging, build-in WiFi and Bluetooth and it is inexpensive. These are major advantages to Arduino Uno, ESP8266 or other ESP32 boards.

We are going to program these both in MicroPython and Arduino C

## Micropython

### Setup

Description ...

- https://docs.micropython.org/en/latest/esp32/tutorial/intro.html
- https://micropython.org/download/esp32/
- https://www.instructables.com/TTGO-color-Display-With-Micropython-TTGO-T-display/

### Examples

- Hello World
- Mandelbrot

## Arduino C

### Setup

- Install Arduino IDE https://www.arduino.cc/en/software
- Update Preferences > Boards Manager URLs: https://dl.espressif.com/dl/package_esp32_index.json

### Examples

- Will follow


## Hardware

Many pins of the ESP32 that are related to the ADC converter are exposed on the T-Display. This makes this board suitable for a variety of measurement applications. The pins are:

| PIN | ADC      | T-Display        | L/R | 
|-----|----------|------------------|-----| 
| 36  | ADC1_CH0 |                  | R   | 
| 37  | ADC1_CH1 |                  | R   | 
| 38  | ADC1_CH2 |                  | R   | 
| 39  | ADC1_CH3 |                  | R   | 
| 32  | ADC1_CH4 |                  | R   | 
| 33  | ADC1_CH5 |                  | R   | 
| 34  | ADC1_CH6 | battery/2        |     | 
| 35  | ADC1_CH7 | button           |     | 
| 4   | ADC2_CH0 | backlight on/off |     | 
| 0   | ADC2_CH1 | button           |     | 
| 2   | ADC2_CH2 |                  | L   | 
| 15  | ADC2_CH3 |                  | L   | 
| 13  | ADC2_CH4 |                  | L   | 
| 12  | ADC2_CH5 |                  | L   | 
| 14  | ADC2_CH6 |                  |     | 
| 27  | ADC2_CH7 |                  | R   | 
| 25  | ADC2_CH8 |                  | R   | 
| 26  | ADC2_CH9 |                  | R   | 
| 21  |          | SDA              |     | 
| 22  |          | SCL              |     | 
