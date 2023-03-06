import math, time
last = 10000
found = 4             # we start from 11, know 2, 3, 5, 7
print(f"Prime numbers to {last}")
#print("2, 3, 5, 7")
start = time.monotonic()
for number in range(11, last, 2):
    prime = True
    for divider in range(3, int(math.sqrt(number))+1, 2):
        if number % divider == 0:
            prime = False
            break
    if prime:
        found += 1
#        print(number, sep=', ', end=' ')
end = time.monotonic()
print(f"This took: {(end - start)} seconds.")
print(f"I found {found} prime numbers.")
