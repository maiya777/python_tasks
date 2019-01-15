K, rooms_arr = input(), map(int, raw_input().split())

print(((sum(set(rooms_arr))*K) - sum(rooms_arr))/(K-1))