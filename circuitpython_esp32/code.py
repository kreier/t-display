import math, time
last = 10000
found = 4     # we start from 11, know already 2, 3, 5, 7
print(f"Prime numbers to {last}")
start = time.monotonic()
for number in range(11, last, 2):
    prime = True
    for divider in range(3, int(math.sqrt(number))+1, 2):
        if number % divider == 0:
            prime = False
            break
    if prime:
        found += 1
end = time.monotonic()
print(f"This took: {(end - start)} seconds.")
print(f"I found {found} prime numbers.")

import board, analogio, digitalio

bat = analogio.AnalogIn(board.BAT_ADC)
button_l = digitalio.DigitalInOut(board.BUTTON_L)
button_l.direction = digitalio.Direction.INPUT
button_r = digitalio.DigitalInOut(board.BUTTON_R)
button_r.direction = digitalio.Direction.INPUT

def batteryvoltage(): # max analog is 65536 but input is 2:1 voltage divider
    battery = 0
    for i in range(100):
        battery += bat.value
    return (battery/100 * 3.3) / 32768 # only half of max because of voltage divider

while True:
    print('(',batteryvoltage(), ')')
    time.sleep(1)
