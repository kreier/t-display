# /micropython/tft/temperature_tft_mqtt.py  2022-04-15

import network
import secrets
import time
import gc
import machine
from mqtt import MQTTClient 
from machine import Pin, SPI
import st7789
import vga1_bold_16x32 as font

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

start     = 0
last_msg  = 0
client_id = b'10521c66507c'
white = st7789.color565(255,255,255)
black = st7789.color565(0,0,0)
green = st7789.color565(0,255,0)

aio_topic1 = secrets["aio_username"] + "/feeds/temperature"
aio_topic2 = secrets["aio_username"] + "/feeds/lipo"
aio_topic3 = secrets["aio_username"] + "/feeds/freemem"
aio_connected = False
wlan = network.WLAN(network.STA_IF)

pin_temp = machine.ADC(machine.Pin(36))
pin_temp.atten(machine.ADC.ATTN_11DB)  # full range: 3.3V
pin_lipo = machine.ADC(machine.Pin(34))
pin_lipo.atten(machine.ADC.ATTN_11DB)

def sub_cb(topic, msg):
    last_msg = float(msg.decode('UTF-8'))
    print("Returned:", last_msg, "pure bytecode:", msg, "as string", msg.decode('UTF-8'))

def wifi_start():
    wlan.active(True)
    x = 0
    while not wlan.isconnected():
        tft.text(font, ".",    x*16,   32, white, black)
        try:
            wlan.connect(secrets["ssid"], secrets["password"])
        except:
            print("connection error, retrying")
        print('.', end='')
        x += 1
        if x > 15:
            x = 0
            tft.text(font, "                .",    0,   32, white, black)
            wlan.active(False)
            time.sleep(1)
            wlan.active(True)
            exec (open("main.py").read())
        time.sleep(1)

def wifi_stop():
    wlan.active(False)

def supersample(pin, iterations):
    raw = 0
    for k in range(iterations):
        raw += pin.read()
    raw = raw / iterations
    return raw

def aio_connect():
    try:
        client.connect()
        client.subscribe(topic=aio_topic1)
        client.subscribe(topic=aio_topic2)
        client.subscribe(topic=aio_topic3)
        print("Sucessfully connected to Adafruit IO")
        return True
    except:
        print(".", end='')
        time.sleep(5)
        return False

def aio_send(message1, message2, message3):
    #wifi_start()
    #client.ping()
    failure = True
    while failure:
        try:
            client.publish(topic=aio_topic1, msg=message1)
            print(" msg1 ", end='')
            time.sleep(1)
            client.publish(topic=aio_topic2, msg=message2)
            print(" msg2 ", end='')
            time.sleep(1)
            client.publish(topic=aio_topic3, msg=message3)
            print(" msg3 ", end='')
            failure = False
        except:
            print("Lost connection. Reconnecting ...", end='')
            aio_connected = False
            while not aio_connect():
                pass
            
        time.sleep(1) # take a second between each attempt
#        if failure == False:
#            try:
#                failure = True
#                client.check_msg()
#               failure = False
#            except:
#                print("Some error.")
#            time.sleep(1)
#        print('.', end='')

def print_temp_lipo():
    temp_raw = supersample(pin_temp, 100)
    lipo_raw = supersample(pin_lipo, 100)
    freemem = gc.mem_free()
    text_temp = "{:.1f}".format(temp_raw * 0.0793 + 10.8)
    text_lipo = "{:.3f}".format((lipo_raw * 0.000793 + 0.108) * 2)
    tft.text(font, text_temp + " C  " + text_lipo + " V",    0,  64, green, black)
    tft.text(font, "Memory: " + str(freemem),    0,  96, green, black)    

##### Here is where the real program starts

tft = st7789.ST7789(
    SPI(1, baudrate=30000000, sck=Pin(18), mosi=Pin(19)),
    135,
    240,
    reset=Pin(23, Pin.OUT),
    cs=Pin(5, Pin.OUT),
    dc=Pin(16, Pin.OUT),
    backlight=Pin(4, Pin.OUT),
    rotation=1)

tft.init()
tft.text(font, "Connect WIFI",    0,   0, white, black)
print_temp_lipo()

print("Connecting to %s " % secrets["ssid"], end='')
wifi_start()
print("\nConnection to Wifi successful.") 
 
client = MQTTClient(client_id, "io.adafruit.com", user=secrets["aio_username"], password=secrets["aio_password"], port=1883) 
client.set_callback(sub_cb)
tft.text(font, "Connect AIO",    0,  32, white, black)
print("Connecting to AIO ...")
while not aio_connect():
    pass
    
while True:
    temp_raw = supersample(pin_temp, 100)
    lipo_raw = supersample(pin_lipo, 100)
    freemem = gc.mem_free()
    text_temp = "{:.1f}".format(temp_raw * 0.0793 + 10.8)
    text_lipo = "{:.3f}".format((lipo_raw * 0.000793 + 0.108) * 2)
    tft.text(font, text_temp + " C  " + text_lipo + " V",    0,  64, white, black)
    #json = '{ "value": {"temp": ' + text_temp + ', "liion": ' + text_lipo + ', "mem-free": ' + str(freemem) + '}, '
    #json += '"lat": 38.1123, "lon": -91.2325, "ele": 112 }'
    #print(json)
    print("Sending:", text_temp, "and", text_lipo, end=' ')
    start = time.ticks_ms()
    aio_send(text_temp, text_lipo, str(freemem))
    print("The roundtrip for this message took {:.0f} milliseconds. Bytes free:".format(time.ticks_ms() - start - 1000), freemem)
    if freemem < 50000:
        gc.collect()
    tft.text(font, "Memory: " + str(freemem),    0,  96, white, black)
    time.sleep(3)
    machine.lightsleep(54000)
    tft.text(font, "...................................",    0,  64, white, black)
    time.sleep(3)

