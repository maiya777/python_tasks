if __name__ == '__main__':
    n = raw_input()
    
    if n.isdigit() and n >= 0:
        for i in range(0, n):
            print (i**2)
    else:
        print ('Input an integer >= 0!')



    # if n.isdigit() and n >= 0:
    #     i = 0
    #     while i < int(n):
    #         print(i**2)
    #         i +=1
    # else:
    #     print ('Input an integer >= 0!')

