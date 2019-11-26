class RiskGame:

    def is_goal(self, state):
        print("owned territories ", len(state.get_owned_territories(state.player_name)))
        return len(state.get_owned_territories(state.player_name)) == 3

    def heuristic(self, state):
        return 1

    def utility(self, state):
        return len(state.get_owned_territories(state.player_name))

    def cutoff_test_using_depth(self, depth):
        def cutoff_test(state):
            return state.depth == depth or self.is_goal(state)
        return cutoff_test
