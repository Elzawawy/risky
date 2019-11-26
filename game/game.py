class RiskGame:

    def is_goal(self, state):
        print("owned territories ", len(state.get_owned_territories(state.player_name)))
        return len(state.get_owned_territories(state.player_name)) == 3

    def heuristic(self, state):
        return 1

    def utility(self, state):
        return len(state.get_owned_territories(state.player_name))

    def cutoffTest(self, state):
        return state.depth == 3 or self.is_goal(state)
    
