import math
import time

last = 10000
found = 1  # because we skip 2, the only even prime number

start = time.monotonic()
print('Prime numbers to {}'.format(last))

# print('2',end='')
def check(number):
    prime = 1
    f = 1.5
    g = int(math.sqrt(number))+1
    for divider in range(2, g):
        f = number/divider
        if f == int(f):
            prime = 0
    return(prime)

for number in range(3, last, 2):
    if check(number) == 1:
        # print(',', number,end='')
        found += 1

end = time.monotonic()
print('Found {:} prime numbers'.format(found))
print('This took:', (end - start), 'seconds.')
