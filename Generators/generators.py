def fib():
    next_fib_number, fib_number, fib_1 = 1, 1, 0
    while 1:
        yield fib_number
        next_fib_number = fib_number + fib_1
        fib_number, fib_1 = next_fib_number, fib_number

# testing code

counter = 0
for n in fib():
    print(n)
    counter += 1
    if counter == 100:
        break