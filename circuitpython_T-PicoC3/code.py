# Menu selector v0.2 for LILYGO T-Display rp2040 - 2023/12/25
# https://github.com/kreier/t-display/tree/main/circuitpython_rpi2040

import time, board, digitalio, os, terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

font_file = "fonts/LeagueSpartan-Bold-16.pcf"
# font_file = "fonts/LeagueSpartan-Bold-16.bdf"
# font_file = "fonts/Junction-regular-24.pcf"

led = digitalio.DigitalInOut(board.LED) # GP25
led.direction = digitalio.Direction.OUTPUT
led.value = True
button_next = digitalio.DigitalInOut(board.BUTTON_L) # GP6
button_next.direction = digitalio.Direction.INPUT
button_ok = digitalio.DigitalInOut(board.GP7)        # GP7
button_ok.direction = digitalio.Direction.INPUT
display = board.DISPLAY

programs = []   # link to all programs installed in /menu (avoid clutter from all apps in /apps)
menu = []       # all menu options - can be more than fit on the display
menu_item = []  # the five items that currently fit on the display
selected_item    = 0
selected_program = 0

directory = os.listdir("menu")  # folder for menu programs - less cluttered
directory.sort()                # collection of all programs are in /apps

def fill_menu(first_program):
    for i in range(5):
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

statusbar = label.Label(terminalio.FONT, text=f" CircuitPython 8.2.9 | {number_programs}     ", color=0x99AAFF)
statusbar.x = 0
statusbar.y = 6
battery = label.Label(terminalio.FONT, text="100%", color=0x00FF00)
battery.x = 210
battery.y = 0
statusbar.append(battery)
font = bitmap_font.load_font(font_file)
color = 0xFFFFFF
menu_item = []
for i in range(5):
    menu_item.append(label.Label(font, text=" Item " + str(i) + " "*30, color=color, background_color=0x000000))
    menu_item[i].x = 1
    menu_item[i].y = 20 + 23*i
    statusbar.append(menu_item[i])
fill_menu(0)
display.root_group = statusbar
led.value = False

menu_item[selected_item].color=0x000000
menu_item[selected_item].background_color=0xFFFFFF
timer = time.monotonic()
while True:
    if not button_next.value:
        led.value = True
        menu_item[selected_item].color=0xFFFFFF
        menu_item[selected_item].background_color=0x000000
        selected_program += 1
        if selected_program > len(programs):
            selected_program = 0
            selected_item = 4
        selected_item += 1
        if selected_item > 4:
            selected_item = 0
            fill_menu(selected_program)
        menu_item[selected_item].color=0x000000
        menu_item[selected_item].background_color=0xFFFFFF
        while not button_next.value:
            pass
        led.value = False
    if not button_ok.value:
        program = "menu/" + programs[selected_program - 1]
        print("Selected: ", program)
        display.show(None)
        button_next.deinit()
        button_ok.deinit()
        led.deinit()
        exec(open(program).read())
        break
    if timer + 1 < time.monotonic():
        led.value = not led.value
        timer = time.monotonic()
