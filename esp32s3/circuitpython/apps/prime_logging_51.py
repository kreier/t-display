# prime v5.0
# cycles through limits and writes to the filesystem

import math, time, digitalio, board, os

scope = [100, 1000, 10000, 100000, 1000000, 10000000, 25000000, 100000000, 1000000000]
reference = [25, 168, 1229, 9592, 78498, 664579, 1565927, 5761455, 123456789]

def is_prime(number):
    global found
    flag_prime = 1
    for divider in range(3, int(math.sqrt(number)) + 1, 2):
        if number % divider == 0:
            flag_prime = 0
            break
    return flag_prime

def find_primes(largest):
    global primes
    global found
    for number in range(11, largest + 1, 2):
        if is_prime(number) > 0:
            found += 1
            primes.append(number)

def is_prime_fast(number):
    global found
    flag_prime = 1
    largest_divider = int(math.sqrt(number)) + 1
    for divider in primes:
        if number % divider == 0:
            flag_prime = 0
            break
        if divider > largest_divider:
            break
    return flag_prime

if __name__ == "__main__":
    for i in range(len(scope)):
        last = scope[i]
        found = 4              # we start from 11, know 2, 3, 5, 7
        primes = [3, 5, 7]     # exclude 2 since we only test odd numbers
        print(f"\nPrime numbers to {last}")
        start = time.monotonic()
        largest_divider = int(math.sqrt(last))
        if largest_divider % 2 == 0:
            largest_divider += 1
        print(f'First find prime dividers up to {largest_divider}.')
        find_primes(largest_divider)
        print(f'Found {found} primes, now use them als dividers.')
        for number in range(largest_divider + 2, last, 2):
            found += is_prime_fast(number)
        end = time.monotonic()
        print(f'This took: {(end - start)} seconds.')
        print(f'Found {found} primes.')
        filename = "/" + str(last) + ".txt"
        with open(filename, "w") as fp:
            fp.write(board.board_id)
            fp.write(f'\nPrimes to {last} took {(end - start)} seconds.')
            fp.write(f'\nFound {found} primes. Should be {reference[i]}.')
        print('Exported to filesystem ')
        #print(board.board_id)
        #print(f'Primes to {last} took {(end - start)} seconds.')
        #print(f'Found {found} primes. Should be {reference[i]}.')