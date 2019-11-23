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

    def get_owned_territories(self, player_name):
        return [x for x in self.adjacency_list.keys() if x.player_name == player_name]

    def get_territroies_to_attack(self, player_name):
        eligible_to_attack_territories = [x for x in self.get_owned_territories(player_name) if x.number_of_armies > 1 ]
        territories_with_enemies_to_attack = []

        for territory in eligible_to_attack_territories:
            adjacent_territories =[x for x in self.get_adjacent_nodes(territory) if x.player_name != player_name]
            if len(adjacent_territories) > 0:
                territories_with_enemies_to_attack.append(territory)
        return territories_with_enemies_to_attack
