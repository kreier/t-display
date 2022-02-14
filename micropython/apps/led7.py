import time, machine, esp32

led = machine.Pin(4, machine.Pin.OUT)
N = 200_000

# Viper mode, directly writing GPIO registers
#@micropython.viper
@micropython.native
def blink_unrolled8_viper(n):
    n //= 8
    #on = led.on
    #off = led.off
    #on  = machine.mem32[0x3FF44008] = 0x10
    #off = machine.mem32[0x3FF4400C] = 0x10   
    r = range(n)
    for i in r:
        machine.mem32[0x3FF44008] = 0x10
        machine.mem32[0x3FF4400C] = 0x10
        machine.mem32[0x3FF44008] = 0x10
        machine.mem32[0x3FF4400C] = 0x10
        machine.mem32[0x3FF44008] = 0x10
        machine.mem32[0x3FF4400C] = 0x10
        machine.mem32[0x3FF44008] = 0x10
        machine.mem32[0x3FF4400C] = 0x10
        machine.mem32[0x3FF44008] = 0x10
        machine.mem32[0x3FF4400C] = 0x10
        machine.mem32[0x3FF44008] = 0x10
        machine.mem32[0x3FF4400C] = 0x10
        machine.mem32[0x3FF44008] = 0x10
        machine.mem32[0x3FF4400C] = 0x10
        machine.mem32[0x3FF44008] = 0x10
        machine.mem32[0x3FF4400C] = 0x10
        #on()
        #off()    
        
def time_it(f, n):
    t0 = time.ticks_us() 
    f(n)
    t1 = time.ticks_us()
    dt = time.ticks_diff(t1, t0)
    fmt = '{:5.3f} sec,  {:6.3f} µsec/blink : {:8.2f} kblinks/sec'
    print(fmt.format(dt * 1e-6, dt/N, N/dt*1e3))

time_it(blink_unrolled8_viper, N)
