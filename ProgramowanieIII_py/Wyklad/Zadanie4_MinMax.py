import random

def randomize(nr_elements: int, max_value=999999) -> []:
    return [random.randrange(max_value) for __ in range(nr_elements)]


def min_max_iteration(tab: []) -> (int, int):
    min_val, max_val = None, None
    if not tab:
        return min_val, max_val
    elif len(tab) == 1:
        min_val, max_val = tab[0], tab[0]
    for it in range(1, len(tab), 2):
        if tab[it-1] > tab[it]:
            tab[it-1], tab[it] = tab[it], tab[it-1]
    for even in range(0, len(tab), 2):
        if min_val is None or min_val > tab[even]:
            min_val = tab[even]
    for odd in range(1, len(tab), 2):
        if max_val is None or max_val < tab[odd]:
            max_val = tab[odd]
    return min_val, max_val



def min_max_make_recursion(the_tab: []) -> (int, int):
    the_len = len(the_tab)
    if the_len > 2:
        min1, max1 = min_max_make_recursion(the_tab[0:(the_len//2)])
        min2, max2 = min_max_make_recursion(the_tab[(the_len//2):the_len])
        if min1 > min2:
            min1 = min2
        if max1 < max2:
            max1 = max2
        return min1, max1
    elif the_len == 2:
        if the_tab[0] > the_tab[1]:
            return the_tab[1], the_tab[0]
        return the_tab[0], the_tab[1]
    return the_tab[0], the_tab[0]

# Recursion can be made using iterations only mode. The implemented version is naive recursive
if __name__ == "__main__":
    n = 200
    tab = randomize(n)
    my_min1, my_max1 = min_max_iteration(tab[::1])
    my_min2, my_max2 = min_max_make_recursion(tab[::1])

    print("The n=" + str(n) + " element random list:")
    print(str(tab) + "\n\n")
    print("Iteration min: " + str(my_min1) + " max: " + str(my_max1))
    print("Recursion min: " + str(my_min2) + " max: " + str(my_max2))
    exit(0)