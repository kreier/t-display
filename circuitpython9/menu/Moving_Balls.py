# lilygo_t_display_rp2040_demo.py - show how to use LILYGO T display RP2040 board
# 23 Jun 2022 - @todbot / Tod Kurt

import time, random, board, busio, digitalio, displayio
import vectorio, rainbowio

BUTTON_EXIT = digitalio.DigitalInOut(config.pin_button_ok)
BUTTON_EXIT.direction = digitalio.Direction.INPUT
LED = digitalio.DigitalInOut(config.pin_led)
LED.direction = digitalio.Direction.OUTPUT

maingroup = displayio.Group()
display.root_group = maingroup

# demo with a bunch of vectorio circles
for i in range(20):
    palette = displayio.Palette(1)
    palette[0] = rainbowio.colorwheel(random.randint(0,255))
    x,y = random.randint(0,display.width), random.randint(0,display.height)
    ball = vectorio.Circle(pixel_shader=palette, radius=20, x=x, y=y)
    maingroup.append(ball)

timer = time.monotonic()
LED.value = True
while True:
    if not BUTTON_EXIT.value:
        LED.deinit()
        BUTTON_EXIT.deinit()
        exec(open("code.py").read())
    for ball in maingroup:
        ball.x = (ball.x + 1) % display.width
    time.sleep(0.1)
    if timer + 0.2 < time.monotonic():
        LED.value = not LED.value
        timer = time.monotonic()
