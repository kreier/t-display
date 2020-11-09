# Micropython on esp8266 and esp32

Instructions are well found at [micropython.org](https://micropython.org/download). First I want to know how big my flash size is. The code is 

```
esptool.exe --port COM5 --chip auto flash_id
```

For ESP32 you have to push the 'BOOT' button or connect IO0 to GND, otherwise the esptool is not connecting.

## Using uPyCraft

Download (no need to install) the [latest version](https://raw.githubusercontent.com/DFRobot/uPyCraft/master/uPyCraft.exe) of [uPyCraft](http://docs.dfrobot.com/upycraft/) (developed by [DFRobot](https://www.dfrobot.com/) from Shanghai). Place a file of [SourceCodePro.ttf](SourceCodePro.ttf) into the same folder. Install this font for all users of your machine (right click > 'Install for all users'). The message at the start regarding the missing font should then dissapear. You can start uPyCraft.exe directly.

Select the correct port on 'Tools > Serial >' and hit the connect button in the right column. In the lower part the REPL should appear and you can start to communicate with your micropython device. Ask for `help()` !

## Prime numbers to 10000

This took 11375 ms on an esp32 with 160 MHz:

``` py
import math
import time

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
```

In uPyCraft V1.0 the output is lagging behind the streaming of numbers from the esp32. After changing the frequency of the esp by

``` py
import machine
machine.freq(240000000)
```
it took only 7782 ms to finish the calculation.

### Timings

| Frequency |  ESP8266 |   ESP32  | Raspberry Pi 1 | Raspberry Pi 4 |
|:---------:|:--------:|:--------:|:--------------:|:--------------:|
|    40 MHz |     -    | 44427 ms |                |                |
|    80 MHz | 32807 ms | 23323 ms |                |                |
|   160 MHz | 16113 ms | 11375 ms |                |                |
|   240 MHz |     -    |  7783 ms |                |                |
