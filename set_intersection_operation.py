n = input()
eng_subscribe_set = set(map(int, raw_input().split()))
m = input()
french_subscribe_set = set(map(int, raw_input().split()))


print (len(eng_subscribe_set&french_subscribe_set))