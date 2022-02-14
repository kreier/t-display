import time, machine

led = machine.Pin(4, machine.Pin.OUT)
N = 200_000

t0 = time.ticks_us() 

# Simple loop
for i in range(N):
    led.on()
    led.off()
    
t1 = time.ticks_us()
dt = time.ticks_diff(t1, t0)
fmt = '{:5.3f} sec,  {:6.3f} µsec/blink : {:8.2f} kblinks/sec'
print(fmt.format(dt * 1e-6, dt/N, N/dt*1e3))
