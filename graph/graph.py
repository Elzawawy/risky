class BaseGraph:
    def __init__(self, graph_dict):
        self.adjacency_list = graph_dict

    def add_node(self, node):
        if node in self.adjacency_list:
            raise Exception("node already exists")
        self.adjacency_list[node] = set()

    def add_edge(self, node_1, node_2):
        self.adjacency_list[node_1].add(node_2)
        self.adjacency_list[node_2].add(node_2)

    def get_adjacent_nodes(self, node):
        return self.adjacency_list[node]

class RiskGameGraph(BaseGraph):
    def __init__(self, graph_dict):
        super(graph_dict)
        
    def reinforce_territory(self, territory, additional_armies):
        keys = self.adjacency_list.keys()
        for key in keys:
            if key.territory_name == territory.name:
                key.armies_number += additional_armies

    def get_owned_territories(self, player_name):
        return [x for x in self.adjacency_list.keys() if x.player_name == player_name]

    def get_attacking_strategy(self, player_name):
        """
        returns: dictionary of territories eligibe to attack mapped to the adjacent territories that 
        it can attack
        """   
        eligible_to_attack_territories = [x for x in self.get_owned_territories(player_name) if x.number_of_armies > 1 ]
        attacking_strategy_map = {}

        for territory in eligible_to_attack_territories:
            adjacent_territories =[x for x in self.get_adjacent_nodes(territory) if x.player_name != player_name and territory.number_of_armies > x.number_of_armies]
            if len(adjacent_territories) > 0:
                attacking_strategy_map[territory] = adjacent_territories
        return attacking_strategy_map
