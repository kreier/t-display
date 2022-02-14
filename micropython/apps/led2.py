import time, machine

led = machine.Pin(4, machine.Pin.OUT)
N = 200_000

# Within a function
def blink_simple(n):
    for i in range(n):
        led.on()
        led.off()

def time_it(f, n):
    t0 = time.ticks_us() 
    f(n)
    t1 = time.ticks_us()
    dt = time.ticks_diff(t1, t0)
    fmt = '{:5.3f} sec,  {:6.3f} µsec/blink : {:8.2f} kblinks/sec'
    print(fmt.format(dt * 1e-6, dt/N, N/dt*1e3))

time_it(blink_simple, N)
