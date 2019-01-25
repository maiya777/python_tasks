def fib3(n):
    if n < 1:
        return None
    a, b = 0, 1
    for i in range(1, n):
        a, b = b, a+b
    return a



