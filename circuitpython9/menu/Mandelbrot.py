# mandelbrot on rp2040 with lcd 240x240
# https://github.com/kreier/rp2040/blob/main/tft_st7789_240x240/menu/Mandelbrot.py
# 2023/12/26 v0.3

import board, displayio, random, digitalio

# Create a bitmap with 256 colors
bitmap = displayio.Bitmap(display.width, display.height, 256)

def hsv_to_rgb(h, s, v):
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.)
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: ret = (65536*v + 256*t + p)
    if i == 1: ret = (65536*q + 256*v + p)
    if i == 2: ret = (65536*p + 256*v + t)
    if i == 3: ret = (65536*p + 256*q + v)
    if i == 4: ret = (65536*t + 256*p + v)
    if i == 5: ret = (65536*v + 256*p + q)
    #return f"{ret:06X}"
    return ret

# Create a 256 color palette
palette = displayio.Palette(256)
for i in range(256):
    #palette[i] = random.randrange(16777216)
    palette[i] = hsv_to_rgb(i/256, 1, 1)
palette[0] = 0

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.root_group = group

# Draw even more pixels
#for c in range(len(palette)):
#    for x in range(display.width):
#        for y in range(display.height):
#            bitmap[x, y] = (x + y) % 256

minX = -1.9
maxX = 0.6
width = display.width
height = display.height
aspectRatio = 1
ITERATION = 20
yScale = (maxX-minX)*(float(height)/width)*aspectRatio

for y in range(height):
    for x in range(width):
        c = complex(minX+x*(maxX-minX)/width, y*yScale/height-yScale/2)
        z = c
        for iter in range(ITERATION):
            if abs(z) > 2:
                break
            z = z*z+c
        if iter == ITERATION - 1:
            pixelcolor = 0
        else:
            pixelcolor = iter *5
        bitmap[x, y] = pixelcolor

# standardized final loop part for T-Display programs to return to the menu
import time, board, digitalio, config
BUTTON_EXIT = digitalio.DigitalInOut(config.pin_button_ok)
BUTTON_EXIT.direction = digitalio.Direction.INPUT
if config.pullup:
    BUTTON_EXIT.pull = digitalio.Pull.UP
LED = digitalio.DigitalInOut(config.pin_led)
LED.direction = digitalio.Direction.OUTPUT
timer = time.monotonic()
LED.value = True
while True:
    if not BUTTON_EXIT.value:
        LED.deinit()
        BUTTON_EXIT.deinit()
        exec(open("code.py").read())
    if timer + 2 < time.monotonic():
        LED.value = not LED.value
        timer = time.monotonic()
