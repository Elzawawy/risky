from graph import RiskGameGraph
import math
import itertools
from utils.common_utils import get_subsets


class Territory:
    def __init__(self, territory_name, owner, number_of_armies=0):
        self.territory_name = territory_name
        self.number_of_armies = number_of_armies
        self.owner = owner

    def __eq__(self, obj):
        return self.territory_name == obj.territory_name


class RiskGameState:
    def __init__(self, territory_neighbours_dict, player_name=None, parent=None, cost=0, depth=0):
        self.map = RiskGameGraph(territory_neighbours_dict)
        self.action_visitors = action_visitors
        self.children = []
        self.player_name = player_name

    def __copy__(self):
        new_instance = type(self)(territory_neighbours_dict,
                                  player_name, parent, cost, depth)
        return new_instance

    def _get_additional_armies(self, player_name):
        return max(3, math.ceil(len(self.map.get_owned_territories(player_name)) / 3))

    def reinforce_territory(self, territory, additional_armies):
        self.map.reinforce_territory(territory, additional_armies)

    def _get_reinforcment_children(self, additional_armies, player_territories):
        #n is objects and k is bins
        def partitions(n, k):
            for c in itertools.combinations(range(n+k-1), k-1):
                yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]

        reinforcement_combinations = partitions(
            additional_armies, len(player_territories))
        reinforcement_combination_states = []

        # loop on combinations of reinforcments ex [0,5,0] ith element id for ith territory in player_territories list
        for combination in reinforcement_combinations:
            new_state = self.__copy__()  # copy self to new state
            for i in range(len(player_territories)):
                new_state.reinforce_territory(
                    player_territories[i], combination[i])
            reinforcement_combination_states.append(new_state)
        return reinforcement_combination_states

    def expand(self, player_name):
        additional_armies = self._get_additional_armies(player_name)
        player_territories = self.map.get_owned_territories(player_name)

        for visitor in self.action_visitors:
            visitor.visit(self)
