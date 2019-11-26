class RiskGame:
    def __init__(self, agent1, agent2, board):
        self.agent1 = agent1
        self.agent2 = agent2
        self.board = board
        self.turn = 0
        self.agents = {0: agent1, 1: agent2}

    def is_goal(self, state):
        # print("owned territories ", len(state.get_owned_territories(state.player_name)))
        return len(state.get_owned_territories(agent1.player_name)) == 3

    def heuristic(self, state):
        sum_enemy_amount_of_units = 0
        sum_border_security_ratio = 0
        for owned_territory in state.get_owned_territories(agents[turn]):
            for enemy_territory in state.get_attacking_enemies(owned_territory, agents[turn]):
                sum_enemy_amount_of_units += enemy_territory.number_of_armies
            sum_border_security_ratio += sum_enemy_amount_of_units * 1.0 / owned_territory.number_of_armies
            sum_enemy_amount_of_units = 0
        return sum_border_security_ratio

    def utility(self, state):
        return len(state.get_owned_territories(state.player_name))

    def cutoffTest(self, state):
        return state.depth == 3 or self.is_goal(state)
    
