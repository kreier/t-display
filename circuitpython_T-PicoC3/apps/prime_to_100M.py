# prime v5.4 2023-12-23
# cycles through limits and writes to the filesystem

import math, time, digitalio, board, os, terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# try uncommenting different font files if you like
font_file = "fonts/LeagueSpartan-Bold-16.pcf"
# font_file = "fonts/LeagueSpartan-Bold-16.bdf"
# font_file = "fonts/Junction-regular-24.pcf"

scope = [100, 1000, 10000, 100000, 1000000, 10000000, 25000000, 100000000, 1000000000, 2147483647, 4294967295]
reference = [25, 168, 1229, 9592, 78498, 664579, 1565927, 5761455, 50847534, 105097564, 203280221]
time_calc = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True
display = board.DISPLAY

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
    hours = int(seconds/3600)
    minutes = int(seconds/60 - hours*60)
    sec = int(seconds - minutes*60 - hours*3600)
    return(f"{hours}h {minutes}min {sec}s")

if __name__ == "__main__":
    # title, current_scope and progress
#    font = terminalio.FONT
    font = bitmap_font.load_font(font_file)
    color = 0xFFFFFF

    text_area = label.Label(font, text="Prime 5.4 CircuitPython", color=color)
    text_area.x = 0
    text_area.y = 20
    title = label.Label(font, text="Calculating primes to", color=color)
    title.x = 10
    title.y = 24
    text_area.append(title)
    current_scope = label.Label(font, text="100", color=color, background_color=0x000000)
    current_scope.x = 130
    current_scope.y = 50
    text_area.append(current_scope)
    percent = label.Label(font, text=" 0.00 Percent  ", color=color, background_color=0x000000)
    percent.x = 60
    percent.y = 75
    text_area.append(percent)
    runtime = label.Label(font, text=" 0h 0min 0s ", color=color, background_color=0x000000)
    runtime.x = 70
    runtime.y = 100
    text_area.append(runtime)
    display.root_group = text_area

    for i in range(8): # 8 needs less than a day - len(scope)
        last = scope[i]
        found = 4              # we start from 11, know 2, 3, 5, 7
        primes = [3, 5, 7]     # exclude 2 since we only test odd numbers

        current_scope.text = str(last)
        current_scope.x = 140 - int(math.log(last, 10))*10

        print(f"\nPrime numbers to {last} in v5.4")
        start = time.monotonic()
        dot = start
        column = 1
        largest_divider = int(math.sqrt(last))
        if largest_divider % 2 == 0:
            largest_divider += 1
        print(f'First find prime dividers up to {largest_divider}.')
        find_primes(largest_divider)
        print(f'Found {found} primes, now use them als dividers.')
        for number in range(largest_divider + 2, last, 2):
            found += is_prime_fast(number)
            if (time.monotonic() - dot) > 2:
                print(f".", end="")
                dot = time.monotonic()
                led.value = not led.value
                column += 1
                percent.text = str(int(number*10000/last)/100.0) + " Percent  "
                runtime.text = elapsed_time(time.monotonic() - start)
                if column > 40:
                    t = elapsed_time(time.monotonic() - start)
                    print(f" {t} - {number} {int(number*100/last)}% ")
                    column = 1
        duration = time.monotonic() - start
        print(f'This took: {duration} seconds.')
        print(f'Found {found} primes.')
        filename = "/" + str(last) + ".txt"
        try:
            with open(filename, "w") as fp:
                fp.write(board.board_id)
                fp.write(f'\nPrimes to {last} took {duration} seconds.')
                fp.write(f'\nFound {found} primes. Should be {reference[i]}.')
                print('Exported to filesystem ')
        except:
            print("Can't write to the filesystem. Press reset and after that the boot button in the first 5 seconds")
        #print(f'Primes to {last} took {(end - start)} seconds.')
        #print(f'Found {found} primes. Should be {reference[i]}.')
        time_calc[i] = duration
    print('\nWrite summary')
    try:
        with open("summary.txt", "w") as fp:
            fp.write(f'Primes calculation in Circuitpython v5.4 2023/12/22\n')
            fp.write(board.board_id)
            fp.write('\n last       time in seconds\n')
            for i in range(len(time_calc)):
                fp.write(f' {scope[i]}   {time_calc[i]}\n')
            print('Exported to filesystem ')
    except:
        print("Can't write to the filesystem. Press reset and after that the boot button in the first 5 seconds")

while True:
    led.value = True
    print(f'LED on - to {last} needs {duration} s')
    time.sleep(10)
    led.value = False
    print('LED off')
    time.sleep(1)
    pass
