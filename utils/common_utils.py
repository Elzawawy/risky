import itertools

def get_subsets(input_set):
    subsets = []
    for i in range(input_set):
        subsets.extend(list(itertools.permutations(input_set,i)))
    return subsets