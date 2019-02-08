def wrapper(f):
    def fun(l):
        return f (['+91 '+phone_number[-10:-5]+' '+ 
                  phone_number[-5:] for phone_number in l])
    return fun

@wrapper
def sort_phone(l):
    print '\n'.join(sorted(l))

if __name__ == '__main__':
    l = [raw_input() for _ in range(int(input()))]
    sort_phone(l) 