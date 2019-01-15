def is_A_superset_of_all_B_sets():
    for i in range(N):
        B = set(map(int, raw_input().split()))
        if A>B:
               continue
        else:
               return False
    return True

A, N = set(map(int, raw_input().split())), input()

print(is_A_superset_of_all_B_sets())