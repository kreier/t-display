# Start for T-Display S3 320x170
# 2023/12/06

import time, os, sys
import board, displayio, terminalio, digitalio, busio, paralleldisplaybus
from adafruit_st7789 import ST7789
from adafruit_debouncer    import Debouncer
from adafruit_display_text import label

DISPLAY_ROWS = 5
color_menu   = 0xFFFFFF
color_select = 0x000000   # 0x00FF55
long_press   = 0.5        # time in seconds for long press to start program

pin_select            = digitalio.DigitalInOut(board.IO14)
pin_select.direction  = digitalio.Direction.INPUT
pin_select.pull       = digitalio.Pull.UP
switchA               = Debouncer(pin_select, interval=0.05)
pin_confirm           = digitalio.DigitalInOut(board.IO0)
pin_confirm.direction = digitalio.Direction.INPUT
pin_confirm.pull      = digitalio.Pull.UP
switchB               = Debouncer(pin_confirm, interval=0.05)

directory = os.listdir("menu")  # folder for programs
directory.sort()
programs = []
# create program list but skipping deleted programs
for i, x in enumerate(directory):
    if x[:2] != "._":
        programs.append(directory[i])
number_programs = len(programs)  # number of installed programs

displayio.release_displays()
# spi = busio.SPI(clock=board.GP10, MOSI=board.GP11)
#tft_cs = board.IO06
#tft_dc = board.IO07
display_bus = paralleldisplaybus.ParallelBus(data0 = board.IO39,
                                    command = board.IO07,
                                    chip_select = board.IO06,
                                    write = board.IO08,
                                    read  = board.IO09
)
display = ST7789(display_bus, width=320, height=160, rowstart=0, rotation=90)


menu = []  # all menu options - can be more than fit on the display
# first menu item:
menu.append(" Menu/Settings [{}] ".format(number_programs))

for i, x in enumerate(programs):
    menu.append(" " + x[:-3] + " ")  # remove the .py from program files

displaymenu = displayio.Group()  # menu options actually shown on display
select   = 0                     # item select on the list shown


def menu_create():
    for item in range(DISPLAY_ROWS):
        listitem = label.Label(terminalio.FONT, text="")
        listitem.x = 0
        listitem.y = 5 + 13 * item
        displaymenu.append(listitem)


def menu_fill(s):
    if len(menu) < DISPLAY_ROWS:
        for item in range(len(menu)):
            displaymenu[item].text = menu[item]
    else:
        for item in range(DISPLAY_ROWS):
            displaymenu[item].text = menu[item + s]
        # this code fills from the bottom - its slightly faster
        #for item in range(DISPLAY_ROWS - 1, -1, -1):
        #    displaymenu[item].text = menu[item + s]


def menu_select(x):
    # highlight selected item
    displaymenu[x].color = color_select
    displaymenu[x].background_color = color_menu
    # de-select old item
    if x == 0:
        if len(menu) > DISPLAY_ROWS:
            x = DISPLAY_ROWS
        else:
            x = len(menu)
    x -= 1
    displaymenu[x].color = color_menu
    displaymenu[x].background_color = color_select


# setup
menu_create()
menu_fill(0)
menu_select(0)
display.show(displaymenu)
pressed = time.monotonic()

# input loop
while True:
    switchA.update()
    switchB.update()
    if switchA.fell:  # button pressed
        pressed = time.monotonic()
    if switchA.rose:  # button released
        time_pressed = time.monotonic() - pressed
        if time_pressed > long_press:  # alternative to press button B
            if select < 1:
                sys.exit()
            program = "menu/" + programs[select - 1]
            display.show(None)
            pin_select.deinit()
            pin_confirm.deinit()
            exec(open(program).read())
            break
        select += 1
        if select > len(menu) - 1:
            select = 0
            menu_fill(0)
        if select > DISPLAY_ROWS - 1:
            menu_fill(select - DISPLAY_ROWS + 1)
        else:
            menu_select(select)
    if switchB.rose:
        if select < 1:
            sys.exit()
        program = "menu/" + programs[select - 1]
        print("Selected: ", program)
        display.show(None)
        pin_select.deinit()
        pin_confirm.deinit()
        exec(open(program).read())
        break
