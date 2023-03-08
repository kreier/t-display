# Circuitpython on T-Display rp2040 and T-PicoC3

Both boards are similar to the T-Display from 2019, but have a rp2040 MCU and in case of the C3 and additional esp32c3 for wifi connectivity.

To support them we need a VID and PID combination, see https://github.com/adafruit/circuitpython/pull/6037

Since the MCU is a rp2040 the VID could be `USB_VID = 0x2E8A` (that's the Raspberry Pi foundation) and we need to request a PID according to 

https://github.com/raspberrypi/usb-pid

It was requested already according to [https://github.com/adafruit/circuitpython/pull/6037](https://github.com/Xinyuan-LilyGO/LILYGO-T-display-RP2040/issues/5) from May 25, 2022:

Some history:

- https://github.com/adafruit/circuitpython/issues/6024 Feb 2022 - still open
- https://github.com/adafruit/circuitpython/pull/6037 Feb 2022 - still open
- https://github.com/Xinyuan-LilyGO/LILYGO-T-display-RP2040/issues/5 March 2022
- https://github.com/Xinyuan-LilyGO/LILYGO-T-display-RP2040/issues/13 Dec 2022

## Post on the forum

- https://community.lilygo.cc/topic/50/help-with-usb-vid-pid-for-circuitpython February 2022
- https://community.lilygo.cc/topic/145/t-display-rp2040-needs-usb-vid-pid?_=1678274382618 December 2022

## Write to info@raspberrypi.com

What is the current state? Fill out the form from https://github.com/raspberrypi/usb-pid 

