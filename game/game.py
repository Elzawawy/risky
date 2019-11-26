from game.map import get_map
from random import shuffle

class RiskGame:
    def __init__(self, agent1, agent2, board):
        self.agent1 = agent1
        self.agent2 = agent2
        self.board = board
        self.map = get_map(board)
        self.turn = 0
        self.agent_names = {0: agent1.player_name, 1: agent2.player_name}

    def is_goal(self, state):
        # print("owned territories ", len(state.get_owned_territories(state.player_name)))
        return len(state.get_owned_territories(self.agent_names[self.turn])) == 3

    def heuristic(self, state):
        sum_enemy_amount_of_units = 0
        sum_border_security_ratio = 0
        for owned_territory in state.get_owned_territories(self.agent_names[self.turn]):
            for enemy_territory in state.get_attacking_enemies(owned_territory, self.agent_names[self.turn]):
                sum_enemy_amount_of_units += enemy_territory.number_of_armies
            sum_border_security_ratio += sum_enemy_amount_of_units * 1.0 / owned_territory.number_of_armies
            sum_enemy_amount_of_units = 0
        return sum_border_security_ratio

    def utility(self, state):
        return len(state.get_owned_territories(state.player_name))

    def cutoff_test_using_depth(self, depth):
        def cutoff_test(state):
            return state.depth == depth or self.is_goal(state)
        return cutoff_test

    def initialize_map_with_armies(self):
        shuffled_map_keys = shuffle(self.map.keys())
        each_player_max_territory_number = len(self.map.key())/2

        for i in range(each_player_max_territory_number):
            shuffled_map_keys[i].owner = self.agent_names[0]
            shuffled_map_keys[i+each_player_max_territory_number].owner = self.agent_names[1]
        if len(self.map.key()) % 2 != 0:
            shuffled_map_keys[len(self.map.key())].owner = self.agent_names[1]
