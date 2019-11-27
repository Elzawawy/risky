from game.agents.base_agent import BaseAgent
from utils.search_algorithms import real_time_a_star_search
from game.action_handlers.risk_visitor import RiskVisitor
from utils.common_utils import back_track_path
from random import seed
from random import randint

class RTAStarAgent(BaseAgent):

    def __init__(self,player_name, heuristic, goal_test):
        super().__init__(player_name)
        self.visitor = RiskVisitor(player_name)
        self.heuristic = heuristic
        self.goal_test = goal_test

    def place_initial_armies(self, initial_state):
        """ Place Initial Armies on board. Executed once at begining of game.

            Arguments:\\
                * current_state: The current Map State of the game.\\
            Returns:\\
                * result_state: The resulting Map State of the game.
        """
        ARMIES_NUMBER = 1
        # Get all owned territories
        owned_territories = initial_state.get_owned_territories(
            self.player_name)

        # Add one army to a random territory
        owned_territories[randint(
            0, len(owned_territories) - 1)].number_of_armies += ARMIES_NUMBER

    def take_turn(self, current_state):
        """ Take Turn in game. Executed each turn on agents.

            Arguments:\\
                * current_state: The current Map State of the game.\\
                * heuristic: The Game heuristic employed in our RISK.\\
                * goal_test: The goal test to terminate employed in our RISK.\\
            Returns:\\
                * result_state: The resulting Map State of the game that should be played.
        """
        current_state.parent = None
        goal_state = real_time_a_star_search(current_state, self.goal_test, self.heuristic, self.visitor)
        return back_track_path(goal_state)[0]
