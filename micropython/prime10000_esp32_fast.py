import math
import time
import machine

machine.freq(240000000)    # standard frequency is 160000000 for ESP32

last = 10000

start = time.ticks_ms()
print("Prime numbers to 10000")

print('2, 3, 5, 7',end='')
for number in range(11, last, 2):
    prime = 1
    for divider in range(2, int(math.sqrt(number))+1, 1):
        if number/divider == int(number/divider):
            prime = 0

    if prime == 1:
        print(',', number,end='')
        
end = time.ticks_ms()
print('\nThis took:', (end - start), 'ms.')
