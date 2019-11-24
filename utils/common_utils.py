import itertools


def get_subsets(input_set):
    subsets = []
    for i in range(len(input_set)+1):
        subsets.extend(list(itertools.permutations(input_set, i)))
    return subsets