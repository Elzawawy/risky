from game.agents.base_agent import BaseAgent
from utils.search_algorithms import greedy_best_first_search
from utils.common_utils import back_track_path

class GreedyAgent(BaseAgent):
    def __init__(self,player_name):
        super().__init__(player_name)

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
                * heuristic: The Game heuristic employed in our RISK.\\
            Returns:\\
                * result_state: The resulting Map State of the game that should be played.
        """
        current_state.parent = None
        goal_state = greedy_best_first_search(current_state, heuristic)
        return back_track_path(goal_state)[0]