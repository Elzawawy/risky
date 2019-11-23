from utils.datastructures.graph import BaseGraph
import math

class RiskGameGraph(BaseGraph):
    def __init__(self, graph_dict):
        super(graph_dict)

    def get_owned_territories(self, player_name):
        return [x for x in self.adjacency_list.keys() if x.player_name == player_name]

    def get_territories_to_attack(self, player_name):
        eligible_to_attack_territories = [x for x in self.get_owned_territories(player_name) if x.number_of_armies > 1 ]
        territories_with_enemies_to_attack = []

        for territory in eligible_to_attack_territories:
            adjacent_territories =[x for x in self.get_adjacent_nodes(territory) if x.player_name != player_name]
            if len(adjacent_territories) > 0:
                territories_with_enemies_to_attack.append(territory)
        return territories_with_enemies_to_attack

class Territory:
    def __init__(self, territory_name, owner, number_of_armies=0):
        self.territory_name = territory_name
        self.number_of_armies = number_of_armies
        self.owner = owner

class RiskGameState:
    def __init__(self, territory_neighbors_dict, action_visitors, player_name=None, parent=None, cost=0, depth=0):
        self.map = RiskGameGraph(territory_neighbors_dict)
        self.action_visitors = action_visitors
        self.children = []
        self.player_name = player_name

    def _get_additional_armies(self, player_name):
        return max(3, math.ceil(len(self.map.get_owned_territories(player_name)) / 3))
