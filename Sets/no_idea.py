def inp():
    return map(int, raw_input().split())

if __name__ == '__main__':
    n, m = inp()
    arr = inp()
    A = set(inp())
    B = set(inp())

    happiness = 0
    for i in arr:
        if i in A:
            happiness +=1
        if i in B:
            happiness -=1

    print(happiness)

