from game.agents.base_agent import BaseAgent
from game.action_handlers.actions import reinforce_territory, attack
from random import randint
import operator

class AggressiveAgent(BaseAgent):

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
        # Get all owned territories
        owned_territories = initial_state.get_owned_territories(self.player_name)

        # Add one army to a random territory
        random_int = randint(0, len(owned_territories) - 1)
        print("aggressive random element to place init armies",random_int)
        owned_territories[random_int].number_of_armies += ARMIES_NUMBER

    def take_turn(self, current_state):
        """ Take Turn in game. Executed each turn on agents.

            Arguments:\\
                * current_state: The current Map State of the game.\\
            Returns:\\
                * result_state: The resulting Map State of the game.
        """
        return self.aggressive_strategy(current_state)

    def aggressive_strategy(self, current_state):
        """ Employs Aggressive Strategy: always places all its bonus armies on the territory with
            the most armies, and greedily attempts to attack territories with most armies that
            he can attack.

            Arguments:\\
                * current_state: The current Map State of the game.\\
            Returns:\\
                * result_state: The resulting Map State of the game.
        """
        first_loop = True

        while(True):

            # Retrieve the player owned territories
            player_owned_territories = current_state.get_owned_territories(self.player_name)

            # Retrieve the territory with the most number of armies
            territory_with_most_armies = self.__get_first_territory_after_sorting(
                player_owned_territories, True)

            # print(territory_with_most_armies.territory_name, territory_with_most_armies.number_of_armies)

            if(first_loop):
                # Reinforce the territory with the most number of armies with the additional armies
                reinforce_territory(current_state,
                    territory_with_most_armies,current_state.get_additional_armies(self.player_name))
                first_loop = False

            # print(territory_with_most_armies.territory_name, territory_with_most_armies.number_of_armies)

            attacking_strategy = current_state.get_attacking_strategy(self.player_name)

            if(len(attacking_strategy) == 0):
                break

            # Retrieve enemy territories that could be attacked by the territory with most armies
            enemy_territories = attacking_strategy[territory_with_most_armies]

            # Get the enemy territory with fewest armies
            enemy_territory_with_fewest_armies = self.__get_first_territory_after_sorting(enemy_territories, False)

            # Attack enemies territories with most armies that could be attacked
            current_state = attack(current_state, {(territory_with_most_armies, enemy_territory_with_fewest_armies)})

        return current_state

    def __get_first_territory_after_sorting(self, territories, reverse_sort):

        # Sort the territories (ascending or descinding based on reverse_sort) based on the number of armies
        territories.sort(key=operator.attrgetter('number_of_armies'), reverse=reverse_sort)

        # Return the first territory after sorting
        return territories[0]
