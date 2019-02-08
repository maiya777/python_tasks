import operator

def person_lister(f):
    def inner(people):
        getage = operator.itemgetter(2)
        for person in people:
            person[2] = int(person[2]) 
        return map(f, sorted(people, key = getage))
    return inner

@person_lister
def name_format(person):
    return ("Mr. " if person[3] == "M" else "Ms. ") + person[0] + " " + person[1]

if __name__ == '__main__':
    people = [raw_input().split() for i in range(int(raw_input()))]
    print '\n'.join(name_format(people))