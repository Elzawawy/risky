class RiskGame:
    def __init__(self, agent1, agent2, board):
        self.agent1 = agent1
        self.agent2 = agent2
        self.board = board
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
