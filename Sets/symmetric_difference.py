def inp():
    return map(int, raw_input().split())

if __name__ == '__main__':
    m = inp()
    M = set(inp())
    n = inp()
    N = set(inp())

    for i in sorted((M^N)):
    	print i
