from game.agents.base_agent import BaseAgent
from game.action_handlers.actions import reinforce_territory, attack
from random import randint
import operator

class PacifistAgent(BaseAgent):

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
        return self.pacifist_strategy(current_state)

    def pacifist_strategy(self, current_state):
        """ Employs Pacifist Strategy: places all of its bonus armies to the territory with the fewest armies,
            then conquers only the one territory with fewest armies (if it can).

            Arguments:\\
                * current_state: The current Map State of the game.\\
            Returns:\\
                * result_state: The resulting Map State of the game.
        """
        # Retrieve the player owned territories
        player_owned_territories = current_state.get_owned_territories(self.player_name)

        # Get the territory with the fewest number of armies
        territory_with_fewest_armies = self.__sort_territories_ascending(player_owned_territories)

        # Reinforce the territory with the fewest number of armies with the additional armies
        reinforce_territory(current_state,
                            territory_with_fewest_armies, current_state.get_additional_armies(self.player_name))
        
        attacking_strategy = current_state.get_attacking_strategy(self.player_name)

        # Get enemy territories as a list
        enemy_territories = [territory for enemy_territories_list in list(
            attacking_strategy.values()) for territory in enemy_territories_list]

        # Get the enemy territory with fewest armies
        enemy_territory_with_fewest_armies = self.__sort_territories_ascending(enemy_territories)

        # Attack the enemy territory with fewest armies by
        #  the player owned territory that can attack it
        for key in attacking_strategy.keys():
            if(enemy_territory_with_fewest_armies in attacking_strategy[key]):
                print(key.territory_name, key.number_of_armies)
                current_state = attack(current_state,
                 {(key, enemy_territory_with_fewest_armies)})
                break

        return current_state

    def __sort_territories_ascending(self, territories):
        # Sort the territories based on the number of armies ascending
        territories.sort(key=operator.attrgetter('number_of_armies'))

        # Get the territory with the fewest number of armies
        return territories[0]

