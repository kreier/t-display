# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
# SPDX-License-Identifier: MIT
# https://github.com/kreier/clue 2022-10-28

"""CircuitPython I2C Device Address Scan"""
# If you run this and it seems to hang, try manually unlocking
# your I2C bus from the REPL with
#  >>> import board
#  >>> board.I2C().unlock()

import time
import board
import busio

# To use default I2C bus (most boards)
#i2c = board.I2C()

# To create I2C bus on specific pins
# import busio
# i2c = busio.I2C(board.SCL1, board.SDA1)  # QT Py RP2040 STEMMA connector
# i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040
#i2c = busio.I2C(board.GP17, board.GP16)    # Pi Pico RP2040
i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040


print("i2c detection range 0x00-0x7F")
print("      0 1 2 3 4 5 6 7 8 9 A B C D E F")

while not i2c.try_lock():
    pass

try:
    devices = i2c.scan()

finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()

devices.append(0)
device = 0
for row in range(0, 127, 16):
    print(f"0x{row:02x}", end=":")
    for col in range(16):
        if devices[device] == (row + col):
            print(hex(row+col)[2:], end="")
            device += 1
        else:
            print(" -", end="")
    print(" ")
