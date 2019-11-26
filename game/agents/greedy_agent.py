import game.agents.BaseAgent
from utils.search_algorithms import greedy_best_first_search

class GreedyAgent(BaseAgent):
    def __init__(self,player_name):
        super().__init__(player_name)
        # TODO: Should either send Heuristic Function as input here or Import it from file.
        self.heuristic = heuristic

    def place_initial_troops(self, initial_state, num_troops):
        """ Place Initial Troops on board. Executed once at begining of game.

            Arguments:\\
                * current_state: The current Map State of the game.\\
                * num_troops: The number of troops to reinforce with.\\
            Returns:\\
                * result_state: The resulting Map State of the game.
        """
        # TODO: Should call here random_initial_reinforcement()
        raise(NotImplementedError)

    def take_turn(self, current_state, heuristic):
        """ Take Turn in game. Executed each turn on agents.

            Arguments:\\
                * current_state: The current Map State of the game.\\
            Returns:\\
                * result_state: The resulting Map State of the game.
        """
        goal_state = greedy_best_first_search(current_state, heuristic)
        # TODO: Should act upon goal_state to return action to be done in game.
        # TODO: return next_state
        raise(NotImplementedError)
