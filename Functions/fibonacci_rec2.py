def fib2(n, a=0, b=1, i=1):
    if n < 1:
        return None
    if i == n:
        return a
    else:
        return fib2(n, a+b, a, i+1)