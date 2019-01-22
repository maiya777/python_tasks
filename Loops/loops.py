if __name__ == '__main__':
    
    n = int(input())
    
    if  n > 0:
        for i in range(n):
            print (i**2)
    elif n == 0:
        print(n)
    else:
        print ('n must be >= 0!')



    # n = raw_input()
    # if n.isdigit():
    #     i = 0
    #     while i <= int(n):
    #         print(i**2)
    #         i +=1
    # else:
    #     print ('Input an integer >= 0!')

