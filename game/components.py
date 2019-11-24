from graph import RiskGameGraph
import math
import itertools
from utils.common_utils import get_subsets


class Territory:
    def __init__(self, territory_name, owner, number_of_armies=0):
        self.territory_name = territory_name
        self.number_of_armies = number_of_armies
        self.owner = owner

    def __eq__(self, obj):
        return self.territory_name == obj.territory_name


class RiskGameState:
    def __init__(self, territory_neighbours_dict, player_name=None, parent=None, cost=0, depth=0):
        self.map = RiskGameGraph(territory_neighbours_dict)
        self.action_visitors = action_visitors
        self.children = []
        self.player_name = player_name

    def __copy__(self):
        new_instance = type(self)(territory_neighbours_dict,
                                  player_name, parent, cost, depth)
        return new_instance

    def _get_additional_armies(self, player_name):
        return max(3, math.ceil(len(self.map.get_owned_territories(player_name)) / 3))

    def reinforce_territory(self, territory, additional_armies):
        self.map.reinforce_territory(territory, additional_armies)

    def _get_reinforcement_children(self, additional_armies, player_territories):
        """
            Used to get all the possible children states after applying all the possible reinforcement
            combinations on the state.

            Args:
                additional_armies: Number of additional armies.
                player_territories: Territories owned by a player.
            Returns: 
                List of a reinforcement children states.
        """
        #n is objects and k is bins
        def partitions(n, k):
            """
                Used to get all the possible combinations to reinforce one player territories.

                Args:
                    n: Number of additional armies.
                    k: Number of territories owned by a player.
                Returns: 
                    List of lists of reinforcement combination.
            """
            for c in itertools.combinations(range(n+k-1), k-1):
                yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]

        # Get all the possible combinations for reinforcement.
        reinforcement_combinations = partitions(
            additional_armies, len(player_territories))

        # List contains all the possible states after reinforce a player territories
        #  by the possible reinforcement combinations
        reinforcement_combination_states = []

        # loop on combinations of reinforcements ex [0,5,0] ith element id for ith territory in player_territories list
        for combination in reinforcement_combinations:
            new_state = self.__copy__()  # copy self to new state
            for i in range(len(player_territories)):
                # Reinforce a territory by a number of additional armies
                new_state.reinforce_territory(
                    player_territories[i], combination[i])

            # After perfroming each reinforcement combination, add the new state to reinforcement_combination_states.
            reinforcement_combination_states.append(new_state)
        return reinforcement_combination_states

    def _get_attacking_children(self, state):
        """
            Used to get all the children states after applying the territories attacking step.

            Args:
                state: A state after appling reinforcement step on it.

            Returns: 
                List of all possible children states after applying the territories attacking step.
        """
        # Dictionary of territories eligibe to attack mapped to the enemys' territories
        attacking_strategy = state.map.get_attacking_strategy()

        # Return if there is no enemys' territories to attack
        if(len(attacking_strategy) == 0):
            return [state]

        # List of pairs of player territory and enemy territory that could be attacked.
        eligible_to_attack_armies_enemies_pairs = []

        # Unfold the attacking_strategy dictionary to get pairs of player territory and enemy territory that could be attacked
        for key in attacking_strategy.keys():
            eligible_to_attack_armies_enemies_pairs.extend(
                [(key, x) for x in attacking_strategy[key]])

        # Get all the possible attacking sequences that could be performed on the current state
        attack_sequence_subsets_pairs = get_subsets(
            eligible_to_attack_armies_enemies_pairs)

        # List of states consequent from applying all possible attacking sequences
        children_states = []
        for subset in attack_sequence_subsets_pairs:

            # if the subset is an empty one, append the current state to children states
            if len(subset) == 0:
                children_states.append(state)
                continue
            # TODO validate subset
            # If the attacking sequence subset is valid, perform it
            if validate_subset(subset):
                # TODO attack
                # Add to the children states the result of performing attacking sequence on it
                children_states.extend(
                    self._get_attacking_children(attack(state, subset)))
        return children_states

    def _get_children(self, additional_armies, player_territories):
        reinforcement_children_states = self._get_reinforcement_children(
            additional_armies, player_territories)

    def expand(self, player_name):
        additional_armies = self._get_additional_armies(player_name)
        player_territories = self.map.get_owned_territories(player_name)

        for visitor in self.action_visitors:
            visitor.visit(self)
