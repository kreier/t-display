# Projects with the TTGO T-Display

[![GitHub release](https://img.shields.io/github/release/kreier/t-display.svg)](https://GitHub.com/kreier/t-display/releases/)
[![MIT license](https://img.shields.io/github/license/kreier/t-display)](https://kreier.mit-license.org/)

Installation and power measurements are found at the bottom of this document.

## MicroPython

Some example programs:

- Mandelbrot
- green terminal
- [prime numbers](https://github.com/kreier/t-display/blob/main/micropython/prime10000_esp32_fast.py)

### With the TFT display in /tft folder

- Mandelbrot
- Scrolling
- Matrix

## Arduino C

Examples here are:

- [Starfield simulation](https://github.com/kreier/t-display/tree/main/arduino/TFT_Starfield)
- [Mandelbrot calculation](https://github.com/kreier/t-display/tree/main/arduino/TFT_Mandlebrot)
- [Matrix simulation](https://github.com/kreier/t-display/tree/main/arduino/TFT_Matrix)
- [Analog readings](https://github.com/kreier/t-display/tree/main/arduino/TFT_Voltage)

![Starfield simulation](starfield.gif)

## Installation of Arduino

You need the following 5 steps to be able to program your T-Display with your Laptop/PC.

## Installation of MicroPython

### Simplified Installation

You need 2 programs and 1 file to get started with MicroPython on the T-Display. I downloaded the most recent in November 2020 and put them in the [first v0.1 release](https://github.com/kreier/t-display/releases/tag/v0.1). They include:

- [esptool 2.6.1](https://github.com/kreier/t-display/releases/download/v0.1/esptool.exe) to install the firmware
- [firmware.bin](https://github.com/kreier/t-display/releases/download/v0.1/firmware.bin) micropython v1.12 with ST7789V driver library
- [Thonny 3.3.0](https://github.com/thonny/thonny/releases/download/v3.3.0/thonny-3.3.0.exe) for Windos, [other operation systems](https://github.com/thonny/thonny/releases/tag/v3.3.0)

Connect your T-Display to a USB port of your computer and determine the port. You can do this by right-click on the Windows symbol > Device Manager > ports (COM & LPT) and there you'll find ```Silicon Labs CP210x USB to UART Bridge (COM6)```. Here COM6 would be your serial port. Open ```cmd``` or ```powershell``` and navigate to the folder with the esptool.exe and firmware.bin.

- Check your board with `esptool.exe --port COM6 flash_id`
- Erase the flash `esptool --port COM6 erase_flash`
- Flash the new firmware with `esptool --chip esp32 --port COM6 --baud 460800 write_flash -z 0x1000 firmware.bin`

MicroPython should now be running on your T-Display. To see this we need to upload a program. Install Thonny. After opening Thonny change the settings to *Tools > Options... > Interpreter*. Here you select *MicroPython (ESP32)* and the correct Port or WebREPL *Silicon Labs CP210x USB to UART Bridge (COM6)*. You might have to press *STOP* once and then will be greeted with


``` py
  MicroPython v1.12-464-gcae77daf0-dirty on 2020-06-28; ESP32 module with ESP32
  Type "help()" for more information.
>>> 
```

Here you can directly try your first *hello_world*.

``` py
>>> print("Hello world!")
Hello world.
```


### Original sources with updates

First he have to obtain the two programs and the firmware.

#### esptool.py

The __esptool.py__ is the software provided by esp to upload the firmware to their SoCs. I got mine from the Arduino installation at the path `C:\Users\You\AppData\Local\Arduino15\packages\esp32\tools\esptool_py\2.6.1\`. You can download the latest version from github:

  [https://github.com/espressif/esptool](https://github.com/espressif/esptool)

#### firmware

The latest MicroPython firmware for the ESP32 can be found on [micropython.org](https://micropython.org/download/esp32/). This firmware does not include a driver for the ST7789 display. You have several options to include the display library.

#### IDE - integrated development environment

To edit, upload and download your python programs to your ESP32 you need a program on your laptop. Some options include:

- [Thonny]() 17 MByte
- [Mu Editor](https://codewith.mu/en/download) 65 MByte

If you have already Arduino IDE you can directly connect to the REPL interface:

``` py
>>> print("Hello world!")
Hello world.
```

## Power consumption

As [measured in April 2020](https://github.com/kreier/solarmeter/blob/master/README.md#power-consumption-t-display) the board needs 68 mA for running. With a battery of 1000 mAh you can use it for 9 hours.

Further measurement has been conducted in November 2020. The results.

You can directly measure the voltage of the LiPo battery on Pin 34. This can be seen in the [provided schematics from TTGO for the T-Display](TTGO_T-Display_schematics.pdf):

<img src="bat_esp32.png" width="65%" align="right">
<img src="bat_divider.png" width="25%">

The pins on the T-Display are

![Pinmap T-Display](pinmap_t-display.jpg)

## I2C connector

`2020/07/09`

Following the inspiration of SparkFun with their [QWIIC](https://www.sparkfun.com/qwiic#products) connector I tried to replicate the pin order. But instead of SMD 1.0 mm connector I just use the regular 2.54mm raster with XH connector on the board and respective 4 pin connector wire.

![QWIIC system](qwiic.png)

Following the same order the pins are assigned:
1. black - GND
2. red - 3.3 V
3. blue - SDA
4. yellow - SCL

![XH 2.54 connector](xh254.jpg)

The order does not match several OLED displays, but the ZS-042 rtc clock, the 1602 display adapter and many more.

`2020/11/27`

With the new [T-Display](https://kreier.github.io/t-display/) project I included the I2C connector as well. The pins look like this:

![I2C on T-Display](x254-i2c.jpg)

At the ESP32 __SCL__ (SCK) is on `GPIO 22` and __SDA__ (SDI) is on `GPIO 21`. 
