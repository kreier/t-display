# Menu selector v0.3 for LILYGO T-Display rp2040 - 2023/12/28
# https://github.com/kreier/t-display/tree/main/circuitpython9

import time, board, digitalio, os, terminalio, config, gc
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

LED = digitalio.DigitalInOut(config.pin_led)
LED.direction = digitalio.Direction.OUTPUT
LED.value = True
BUTTON_NEXT = digitalio.DigitalInOut(config.pin_button_next)
BUTTON_NEXT.direction = digitalio.Direction.INPUT
BUTTON_OK = digitalio.DigitalInOut(config.pin_button_ok)
BUTTON_OK.direction = digitalio.Direction.INPUT

font_file = "fonts/LeagueSpartan-Bold-16.pcf"
display = board.DISPLAY
gc.collect()

programs  = []  # link to all programs installed in /menu (avoid clutter from all apps in /apps)
menu      = []  # all menu options - can be more than fit on the display
menu_item = []  # the five items that currently fit on the display
selected_item    = 0
selected_program = 0
nr_menuitems = int((display.height-12)/22)

directory = os.listdir("menu")  # folder for menu programs - less cluttered
directory.sort()                # collection of all programs are in /apps

def fill_menu(first_program):
    for i in range(nr_menuitems):
        if i + first_program < len(menu):
            menu_item[i].text = menu[i + first_program]
        else:
            menu_item[i].text = " "

# create program list in /menu but skipping deleted programs
for i, x in enumerate(directory):
    if x[:2] != "._":
        programs.append(directory[i])
number_programs = len(programs)  # number of installed programs

# first menu item:
menu.append(" Settings [{}] ".format(number_programs))
for i, x in enumerate(programs):
    menu.append(" " + x[:-3].replace("_", " ") + " ")  # remove the .py from program files

statusbar = label.Label(terminalio.FONT, text=f" CP 9.0 | {number_programs}     ", color=0x99AAFF)
statusbar.x = 0
statusbar.y = 6
battery = label.Label(terminalio.FONT, text="100%", color=0x00FF00)
battery.x = 210
battery.y = 0
statusbar.append(battery)
font = bitmap_font.load_font(font_file)
color = 0xFFFFFF
menu_item = []
for i in range(nr_menuitems):
    menu_item.append(label.Label(font, text=" Item " + str(i) + " "*30, color=color, background_color=0x000000))
    menu_item[i].x = 1
    menu_item[i].y = 20 + 23*i
    statusbar.append(menu_item[i])
fill_menu(0)
display.root_group = statusbar
LED.value = False

menu_item[selected_item].color=0x000000
menu_item[selected_item].background_color=0xFFFFFF
timer = time.monotonic()
while True:
    if not BUTTON_NEXT.value:
        LED.value = True
        menu_item[selected_item].color=0xFFFFFF
        menu_item[selected_item].background_color=0x000000
        selected_program += 1
        if selected_program > len(programs):
            selected_program = 0
            selected_item = nr_menuitems
        selected_item += 1
        if selected_item >= nr_menuitems:
            selected_item = 0
            fill_menu(selected_program)
        menu_item[selected_item].color=0x000000
        menu_item[selected_item].background_color=0xFFFFFF
        while not BUTTON_NEXT.value:
            pass
        LED.value = False
    if not BUTTON_OK.value:
        program = "menu/" + programs[selected_program - 1]
        print("Selected: ", program)
        display.root_group = None
        while not BUTTON_OK.value:
            pass
        BUTTON_NEXT.deinit()
        BUTTON_OK.deinit()
        LED.deinit()
        exec(open(program).read())
        break
    if timer + 1 < time.monotonic():
        LED.value = not LED.value
        timer = time.monotonic()
