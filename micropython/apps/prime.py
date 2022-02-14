import math, time

last = 1000

start = time.ticks_us()
print('Prime numbers to {}'.format(last))

#print('2, 3, 5, 7',end='')
for number in range(11, last, 2):
    prime = 1
    for divider in range(2, int(math.sqrt(number))+1, 1):
        if number/divider == int(number/divider):
            prime = 0

    if prime == 1:
        #print(',', number, end='')
        prime = 1

end = time.ticks_us()
print('\nThis took:', (end - start)/1000000, 'seconds.')
