# prime v5.4 2023-12-23
# cycles through limits and writes to the filesystem
# https://github.com/kreier/t-display/tree/main/circuitpython_rpi2040/menu

import math, time, digitalio, board, os, terminalio, config
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# try uncommenting different font files if you like
font_file = "fonts/LeagueSpartan-Bold-16.pcf"
# font_file = "fonts/LeagueSpartan-Bold-16.bdf"
# font_file = "fonts/Junction-regular-24.pcf"

scope = [
    100,
    1000,
    10000,
    100000,
    1000000,
    10000000,
    25000000,
    100000000,
    1000000000,
    2147483647,
    4294967295,
]
reference = [
    25,
    168,
    1229,
    9592,
    78498,
    664579,
    1565927,
    5761455,
    50847534,
    105097564,
    203280221,
]
scope_text = [
    "100",
    "1000",
    "10,000",
    "100,000",
    "1,000,000",
    "10,000,000",
    "25,000,000",
    "100,000,000",
    "1,000,000,000",
    "2,147,483,647",
    "4,294,967,295",
]

import time, board, digitalio, config
LED = digitalio.DigitalInOut(config.pin_led)
LED.direction = digitalio.Direction.OUTPUT
LED.value = True
BUTTON_NEXT = digitalio.DigitalInOut(config.pin_button_next)
BUTTON_NEXT.direction = digitalio.Direction.INPUT
BUTTON_OK = digitalio.DigitalInOut(config.pin_button_ok)
BUTTON_OK.direction = digitalio.Direction.INPUT
if config.pullup:
    BUTTON_NEXT.pull = digitalio.Pull.UP
    BUTTON_OK.pull   = digitalio.Pull.UP
display = config.disp


def is_prime(number):
    global found
    flag_prime = 1
    for divider in range(3, int(math.sqrt(number)) + 1, 2):
        if number % divider == 0:
            flag_prime = 0
            break
    return flag_prime


def find_primes(largest):
    global primes
    global found
    for number in range(11, largest + 1, 2):
        if is_prime(number) > 0:
            found += 1
            primes.append(number)


def is_prime_fast(number):
    global found
    flag_prime = 1
    largest_divider = int(math.sqrt(number)) + 1
    for divider in primes:
        if number % divider == 0:
            flag_prime = 0
            break
        if divider > largest_divider:
            break
    return flag_prime


def elapsed_time(seconds):
    hours = int(seconds / 3600)
    minutes = int(seconds / 60 - hours * 60)
    sec = int(seconds - minutes * 60 - hours * 3600)
    return f"{hours}h {minutes}min {sec}s"


if __name__ == "__main__":
    # title, current_scope and progress
    font = bitmap_font.load_font(font_file)
    color = 0xFFFFFF

    text_area = label.Label(font, text="   Calculating primes to   ", color=0x4488FF, background_color=0x000000)
    text_area.x = 0
    text_area.y = 20
    current_scope = label.Label(
        font, text="100", color=color, background_color=0x000000
    )
    current_scope.x = 100
    current_scope.y = 24
    text_area.append(current_scope)
    percent = label.Label(
        font, text=" 0.00 Percent  ", color=color, background_color=0x000000
    )
    percent.x = 60
    percent.y = 50
    text_area.append(percent)
    runtime_color = 0x00FF00
#    try:
#        with open("/data/summary.txt", "w") as fp:
#            fp.write(board.board_id)
#            fp.write(f"\nResults from Prime v5.4 on T-PicoC3")
#            runtime_color = 0x00FF00
#    except:
#       print(
#            "Can't write to the filesystem. Press reset and after that the boot button in the first 5 seconds"
#        )
    runtime = label.Label(
        font, text=" 0h 0min 0s ", color=runtime_color, background_color=0x000000
    )
    runtime.x = 70
    runtime.y = 75
    text_area.append(runtime)
    runtime_seconds = label.Label(
        font, text=" "*30, color=color, background_color=0x000000
    )
    runtime_seconds.x = 50
    runtime_seconds.y = 100
    text_area.append(runtime_seconds)
    display.root_group = text_area

    current_selection = 0
    current_scope.text = scope_text[current_selection]
    current_scope.x = 120 - len(scope_text[current_selection]) * 5
    timer = time.monotonic()
    LED.value = True
    while True:
        last = scope[current_selection]
        found = 4  # we start from 11, know 2, 3, 5, 7
        primes = [3, 5, 7]  # exclude 2 since we only test odd numbers

        if not BUTTON_NEXT.value:
            LED.value = True
            current_selection += 1
            if current_selection >= len(scope):
                current_selection = 0
            current_scope.text = scope_text[current_selection]
            current_scope.x = 120 - len(scope_text[current_selection]) * 5
            runtime_seconds.text = "  "
            while not BUTTON_NEXT.value:
                pass
            LED.value = False
        if not BUTTON_OK.value:
            # long press should be exit!

            print(f"\nPrime numbers to {scope_text[current_selection]} in v5.4")
            current_scope.color = 0xFF0000
            start = time.monotonic()
            dot = start
            column = 1
            largest_divider = int(math.sqrt(last))
            if largest_divider % 2 == 0:
                largest_divider += 1
            print(f"First find prime dividers up to {largest_divider}.")
            find_primes(largest_divider)
            print(f"Found {found} primes, now use them als dividers.")
            for number in range(largest_divider + 2, last, 2):
                found += is_prime_fast(number)
                if (time.monotonic() - dot) > 5:
                    print(f".", end="")
                    dot = time.monotonic()
                    LED.value = not LED.value
                    column += 1
                    percent.text = f"{(number/ (last / 100.0)):.2f} Percent  "
                    runtime.text = elapsed_time(time.monotonic() - start)
                    runtime_seconds.text = f"{(time.monotonic() - start):.6f} seconds"
                    if column > 40:
                        t = elapsed_time(time.monotonic() - start)
                        print(f" {t} - {number} {(number*100/last):.3f}% ")
                        column = 1
                    if not BUTTON_OK.value:    # make exit available
                        LED.deinit()
                        BUTTON_OK.deinit()
                        BUTTON_NEXT.deinit()
                        exec(open("code.py").read())
            duration = time.monotonic() - start
            current_scope.color = 0xFFFFFF
            percent.text = str(int(number * 10000 / last) / 100.0) + " Percent  "
            runtime.text = elapsed_time(duration)
            runtime_seconds.text = f"{duration:.6f} seconds"
            print(f"This took: {duration} seconds.")
            print(f"Found {found} primes.")
            filename = "/data/" + str(last) + ".txt"
            try:
                with open(filename, "w") as fp:
                    fp.write(board.board_id)
                    fp.write(f"\nPrimes to {scope_text[current_selection]} took {duration} seconds.")
                    fp.write(f"\nFound {found} primes. Should be {reference[current_selection]}.")
                    print("Exported to filesystem ")
            except:
                print(
                    "Can't write to the filesystem. Press reset and after that the boot button in the first 5 seconds"
                )



    for i in range(8):  # 8 needs less than a day - len(scope)
        last = scope[i]
        found = 4  # we start from 11, know 2, 3, 5, 7
        primes = [3, 5, 7]  # exclude 2 since we only test odd numbers

        current_scope.text = str(last)
        current_scope.x = 140 - int(math.log(last, 10)) * 10

        print(f"\nPrime numbers to {last} in v5.4")
        start = time.monotonic()
        dot = start
        column = 1
        largest_divider = int(math.sqrt(last))
        if largest_divider % 2 == 0:
            largest_divider += 1
        print(f"First find prime dividers up to {largest_divider}.")
        find_primes(largest_divider)
        print(f"Found {found} primes, now use them als dividers.")
        for number in range(largest_divider + 2, last, 2):
            found += is_prime_fast(number)
            if (time.monotonic() - dot) > 2:
                print(f".", end="")
                dot = time.monotonic()
                led.value = not led.value
                column += 1
                percent.text = str(int(number * 10000 / last) / 100.0) + " Percent  "
                runtime.text = elapsed_time(time.monotonic() - start)
                if column > 40:
                    t = elapsed_time(time.monotonic() - start)
                    print(f" {t} - {number} {int(number*100/last)}% ")
                    column = 1
        duration = time.monotonic() - start
        print(f"This took: {duration} seconds.")
        print(f"Found {found} primes.")
        filename = "/data/" + str(last) + ".txt"
        try:
            with open(filename, "w") as fp:
                fp.write(board.board_id)
                fp.write(f"\nPrimes to {last} took {duration} seconds.")
                fp.write(f"\nFound {found} primes. Should be {reference[i]}.")
                print("Exported to filesystem ")
        except:
            print(
                "Can't write to the filesystem. Press reset and after that the boot button in the first 5 seconds"
            )
        # print(f'Primes to {last} took {(end - start)} seconds.')
        # print(f'Found {found} primes. Should be {reference[i]}.')
        time_calc[i] = duration

timer = time.monotonic()
LED.value = True
while True:
    if not BUTTON_OK.value:
        LED.deinit()
        BUTTON_OK.deinit()
        BUTTON_NEXT.deinit()
        exec(open("code.py").read())
    if timer + 0.4 < time.monotonic():
        LED.value = not LED.value
        timer = time.monotonic()
