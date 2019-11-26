from game.agents.base_agent import BaseAgent
from random import seed
from random import randint


class MinimaxAgent(BaseAgent):
    def __init__(self, player_name):
        super().__init__(player_name)

    def place_initial_armies(self, initial_state):
        """ Place Initial Armies on board. Executed once at begining of game.
        
            Arguments:\\
                * current_state: The current Map State of the game.\\
            Returns:\\
                * result_state: The resulting Map State of the game.
        """
        ARMIES_NUMBER = 1
        seed(1)
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
            Returns:\\
                * result_state: The resulting Map State of the game.
        """
        raise(NotImplementedError)
