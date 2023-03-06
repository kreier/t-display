# Lilygo TTGO T-Display esp32s3 ST7789 1.9 inch 320x170 8Bit TFT

You can flash the regular [esp32s3 n8r8](https://circuitpython.org/board/espressif_esp32s3_devkitc_1_n8r8/) circuitpython firmware, but the display is obviously not running. And you don't have support for the 16 MB flash. 

Challenge: the display is not connected via SPI but parallelbus.

## Documentation

- Pull request circuitpython: [Pull by Tyeth](https://github.com/adafruit/circuitpython/tree/9db79efac734a5e5003144f36389e2e33edf8b30/ports/espressif/boards/lilygo_ttgo_t-display-s3) on February 27th, 2023
- Description LilyGO: [on github](https://github.com/Xinyuan-LilyGO/T-Display-S3)
- [Tyeth on github](https://github.com/tyeth)
- [Paralleldisplay on MicroPython](https://docs.circuitpython.org/en/latest/shared-bindings/paralleldisplay/index.html)


## T-Display rp2040

- [Pull request](https://github.com/adafruit/circuitpython/pull/6037)
