from utils.datastructures.graph import BaseGraph
import itertools
from utils.common_utils import get_subsets, partitions
from copy import deepcopy

class Territory:
    def __init__(self, territory_name, owner, number_of_armies=0):
        self.territory_name = territory_name
        self.number_of_armies = number_of_armies
        self.owner = owner

    def __eq__(self, obj):
        return self.territory_name == obj.territory_name

    def __hash__(self):
        return hash(self.territory_name)


class RiskGameState(BaseGraph):
    def __init__(self, territory_neighbours_dict, player_name=None, parent=None, cost=0, depth=0):
        super().__init__(territory_neighbours_dict)
        self.map = self.adjacency_list
        self.children = []
        self.player_name = player_name
        self.parent = parent
        self.cost = cost
        self.depth = depth
        self.cost_function = lambda x: 1


    def __deepcopy__(self):
        new_instance = type(self)(deepcopy(self.map), self.player_name,self.parent, self.cost, self.depth)
        return new_instance

    def __eq__(self, other):
        other_map_keys = {x.territory_name: x for x in other.map.keys()}
        for key in self.map.keys():
            other_key = other_map_keys[key.territory_name]
            if key.number_of_armies != other_key.number_of_armies or key.owner != other_key.owner:
                return False
        return True

    def __hash__(self):
        hash_value = 0
        for key in self.map.keys():
            hash_value = hash_value ^ hash((key, key.owner, key.number_of_armies))
        return hash_value

    def get_owned_territories(self, player_name):
        """
            Used to get the territories owned by a player.

            Args:
                player_name: the name of the player who want to get its territories.

            Returns:
                All the territories owned by a player
        """
        return [x for x in self.adjacency_list.keys() if x.owner == player_name]

    def get_attacking_strategy(self, player_name):
        """
        returns: dictionary of territories eligibe to attack mapped to the adjacent territories that
        it can attack
        """
        # Get all the owned territories which have number of armies > 1 (eligible to attack)
        eligible_to_attack_territories = [
            x for x in self.get_owned_territories(player_name) if x.number_of_armies > 1]
        # A map where:
        # key -> territory eligible to attack
        # value -> enemys' territories list that could be attacked
        attacking_strategy_map = {}

        for territory in eligible_to_attack_territories:
            # For each eligible territories, find the enemys' territories list that it could attack
            adjacent_territories = [x for x in self.get_adjacent_nodes(
                territory) if x.owner != player_name and territory.number_of_armies > x.number_of_armies]

            # If the enemys' territories list number of armies > 0 add it to the attacking_strategy_map
            if len(adjacent_territories) > 0:
                attacking_strategy_map[territory] = adjacent_territories
        return attacking_strategy_map

    def get_territory(self, territory):
        for node in self.adjacency_list.keys():
            if node == territory:
                return node
        return None

    def get_additional_armies(self, player_name):
        return max(3, len(self.get_owned_territories(player_name)) / 3)

    def cost_to(self, state):
        # TODO: change it to calculate a cost from the self state to the other state
        return 1

    def get_attacking_enemies(self, territory, player_name):
        return [x for x in self.get_adjacent_nodes(territory) 
        if x.owner != player_name and territory.number_of_armies < x.number_of_armies]

    def __lt__(self, other):
        return self.cost_function(self) < self.cost_function(other)

    def __le__(self, other):
        return self.cost_function(self) <= self.cost_function(other)
