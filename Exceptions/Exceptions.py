
T, ab_list= int(input()), []

for i in range(T):
    ab_list.append(raw_input().split())

for values in ab_list:
    try:
        print int(values[0])/int(values[1])
    except ValueError as e:
        print"Error Code:", e
        
    except ZeroDivisionError as e:
        print"Error Code:", e

