import math
import time

last = 10000
found = 1  # because we skip 2, the only even prime number

start = time.monotonic()
print('Prime numbers to {}'.format(last))

# print('2',end='')
for number in range(3, last, 2):
    prime = 1
    for divider in range(2, int(math.sqrt(number))+1, 1):
        if number/divider == int(number/divider):
            prime = 0

    if prime == 1:
        # print(',', number,end='')
        found += 1

end = time.monotonic()
print('Found {:} prime numbers'.format(found))
print('This took:', (end - start), 'seconds.')
