n = input()
phoneBook = {}

for i in range(n):
    record = raw_input().split()
    phoneBook[record[0]] = record[1]

name = raw_input()
while name!=False:   
    if name in phoneBook:
        print (name+'='+phoneBook[name])
    else:
        print ("Not found")
    name = raw_input()
