from graph import RiskGameGraph
import math


class Territory:
    def __init__(self, territory_name, owner, number_of_armies=0):
        self.territory_name = territory_name
        self.number_of_armies = number_of_armies
        self.owner = owner


class RiskGameState:
    def __init__(self, territory_neighbours_dict, action_visitors, player_name=None, parent=None, cost=0, depth=0):
        self.map = RiskGameGraph(territory_neighbours_dict)
        self.action_visitors = action_visitors
        self.children = []
        self.player_name = player_name

    def _get_additional_armies(self, player_name):
        return max(3, math.ceil(len(self.map.get_owned_territories(player_name)) / 3))
