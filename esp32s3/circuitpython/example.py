# sonar example 2022-02-21
import board, busio, time, math, digitalio, adafruit_hcsr04
from ssis_rvr   import pin
from sphero_rvr import RVRDrive

rvr   = RVRDrive(uart = busio.UART(pin.TX, pin.RX, baudrate=115200))
sonar = adafruit_hcsr04.HCSR04(trigger_pin=pin.TRIGGER, echo_pin=pin.ECHO)

while True:
    try:
        sensor_distance = sonar.distance
        print(sensor_distance)
        if sensor_distance < 10 :
            rvr.set_all_leds(255,0,0)
        else:
            rvr.set_all_leds(0,255,0)
        time.sleep(0.1)
        rvr.set_all_leds(0,0,0)
        time.sleep(sensor_distance / 200)

    except RuntimeError:
        print("Retrying!")
        rvr.set_all_leds(0,0,255) #set leds to blue
        pass
    time.sleep(0.2)
