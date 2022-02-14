import math
import time

first = 3
last  = 10000

@micropython.native
def check(number):
    prime = 1
    for divider in range(2, int(math.sqrt(number))+1, 1):
        f = number/divider
        if f == int(f):
            prime = 0
    return(prime)

@micropython.native
def prime_range(a, b):
    found = 1 # because we skip 2, the only even prime number
    for number in range(a, b, 2): # only check odd numbers
        if check(number) == 1:
            #print(',', number,end='')
            found += 1
    return(found)

start = time.monotonic()
print('Prime numbers to {}'.format(last))
#print('2',end='')
print('Found {:} prime numbers'.format(prime_range(first,last)))
end = time.monotonic()

print('This took:', (end - start), 'seconds.')
