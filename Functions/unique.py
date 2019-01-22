def unique(L):
    res = []
    i = 0
    for el in L:
        if not el in L[:i]+L[i+1:]:
            res.append(el)
        i+=1
    return res


def unique1(L):
    return [el for el in L if L.count(el) == 1]

