n = input()
s = set(map(int, raw_input().split()))
N = input()

for i in range (N):
    command_list = raw_input().split()
    if len(command_list) > 1:
        command_str = 's'+'.'+command_list[0]+'('+command_list[1]+')'
    else:
        command_str = 's'+'.'+command_list[0]+'()'
    eval(command_str)
  
print(sum(s))