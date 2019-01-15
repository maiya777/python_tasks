n, A, number_of_commands = input(), set(map(int, raw_input().split())), input()

for i in range(number_of_commands):
	command = raw_input().split()[0]
	B = set(map(int, raw_input().split()))
	eval('A.'+command+'(B)')

print(sum(A))