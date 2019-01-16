def inp():
    input_list = map(int,raw_input().split())
    if  len(input_list) > 1:
        return input_list
    else:
        return input_list[0]

n, set1, m, set2 = inp(), set(inp()), inp(), set(inp())

print(len(set1.symmetric_difference(set2)))