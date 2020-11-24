# Projects with the TTGO T-Display

Installation and power measurements are found at the bottom of this document.

## MicroPython

Some example programs:

- Mandelbrot
- green terminal
- prime numbers

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

You need 2 programs and 1 file to get started with MicroPython on the T-Display. I downloaded the most recent in November 2020 and have them here:

- [esptool 2.6.1](esptool.exe) to install the firmware

Connect your T-Display to a USB port of your computer and determine the port. You can do this by right-click on the Windows symbol > Device Manager > ports (COM & LPT) and there you'll find ```Silicon Labs CP210x USB to UART Bridge (COM6)```. Here COM6 would be your serial port. Open ```cmd``` or ```powershell``` and navigate to the folder with the esptool.exe and firmware.bin.

- Check your board with ```esptool.exe --port COM6 flash_id```
- Erase the flash ```esptool --port COM6 erase_flash```
- Flash the new firmware with ```esptool --chip esp32 --port COM6 --baud 460800 write_flash -z 0x1000 firmware.bin```

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

The __esptool.py__ is the software provided by esp to upload the firmware to their SoCs. I got mine from the Arduino installation at the path ```C:\Users\You\AppData\Local\Arduino15\packages\esp32\tools\esptool_py\2.6.1\```. You can download the latest version from github:

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

The pins are

![Pinmap T-Display](pinmap_t-display.jpg)
