def my_zip3(*args):
    res_list = []
    for i, el in enumerate(args[0]):
        tuple_list = []
        for lst in args:
            tuple_list.append(lst[i])
        res_list.append(tuple(tuple_list))
    
    return(res_list)
