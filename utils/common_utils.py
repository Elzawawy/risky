import itertools


def get_subsets(input_set):
    subsets = []
    for i in range(len(input_set)+1):
        subsets.extend(list(itertools.permutations(input_set, i)))
    return subsets

#n is objects and k is bins
def partitions(n, k):
    """
        Used to get all the possible combinations to reinforce one player territories.

        Args:
            n: Number of additional armies.
            k: Number of territories owned by a player.
        Returns:
            List of lists of reinforcement combination.
    """
    for c in itertools.combinations(range(n+k-1), k-1):
        yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]
