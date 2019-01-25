def my_zip(*args):
    res_list = []
    sorted(args, key =len)[0]
    for i, el in enumerate(sorted(args, key =len)[0]):
        tuple_list = []
        for lst in args:
            tuple_list.append(lst[i])
        res_list.append(tuple(tuple_list))
    
    return(res_list)

