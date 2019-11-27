from utils.common_utils import get_subsets, partitions
from game.action_handlers.actions import reinforce_territory, attack
import random

class RiskVisitor():
    def __init__(self, player_name):
        self.player_name = player_name

    def visit(self, state):
        additional_armies = state.get_additional_armies(self.player_name)
        player_territories = state.get_owned_territories(self.player_name)
        children = self._get_children(state, additional_armies, player_territories)
        for child in children:
            child.depth = state.depth + 1
            child.cost = state.cost + 1
            child.parent = state

        random.shuffle(children)
        return children

    def _validate_subset(self, attacking_moves_sequence):
        print("in validate_subset ", attacking_moves_sequence)
        attacking_territories_to_armies_number = {}
        enemy_territories = set()
        ATTACKING_TERRITORY_INDEX = 0
        ENEMY_TERRITORY_INDEX = 1

        for attacking_move in attacking_moves_sequence:
            attacking_territory = attacking_move[ATTACKING_TERRITORY_INDEX]
            enemy_territory = attacking_move[ENEMY_TERRITORY_INDEX]

            if(enemy_territory in enemy_territories):
                return False

            enemy_territories.add(enemy_territory)

            if attacking_territory not in attacking_territories_to_armies_number.keys():
                attacking_territories_to_armies_number[attacking_territory] = attacking_territory.number_of_armies

            attacking_armies_number = attacking_territories_to_armies_number[attacking_territory]

            if attacking_armies_number > enemy_territory.number_of_armies:
                attacking_territories_to_armies_number[attacking_territory] = attacking_armies_number - 1
            else:
                return False
        return True

    def _get_reinforcement_children(self, state, additional_armies, player_territories):
        """
            Used to get all the possible children states after applying all the possible reinforcement
            combinations on the state.

            Args:
                additional_armies: Number of additional armies.
                player_territories: Territories owned by a player.
            Returns:
                List of a reinforcement children states.
        """

        print("in get reinforcement chidlren")
        # Get all the possible combinations for reinforcement.
        reinforcement_combinations = partitions(
            additional_armies, len(player_territories))

        # List contains all the possible states after reinforce a player territories
        #  by the possible reinforcement combinations
        reinforcement_combination_states = []


        # loop on combinations of reinforcements ex [0,5,0] ith element id for ith territory in player_territories list
        for combination in reinforcement_combinations:
            new_state = state.__deepcopy__()  # copy self to new state
            for i in range(len(player_territories)):
                # Reinforce a territory by a number of additional armies
                reinforce_territory(new_state,
                    player_territories[i], combination[i])


            # After perfroming each reinforcement combination, add the new state to reinforcement_combination_states.
            reinforcement_combination_states.append(new_state)

        return reinforcement_combination_states

    def _get_attacking_children(self, state, max_recursion_depth):
        """
            Used to get all the children states after applying the territories attacking step.

            Args:
                state: A state after appling reinforcement step on it on the first call only
                then it's after recursion an attack state.

            Returns:
                List of all possible children states after applying the territories attacking step.
        """

        print("rec depth",max_recursion_depth)
        if max_recursion_depth == 2:
            return []
        # Dictionary of territories eligibe to attack mapped to the enemys' territories
        attacking_strategy = state.get_attacking_strategy(self.player_name)
        print("in get attacking children who can attack ", len(attacking_strategy))

        # Return if there is no enemys' territories to attack
        if(len(attacking_strategy) == 0):
            return [state]

        # List of pairs of player territory and enemy territory that could be attacked.
        eligible_to_attack_armies_enemies_pairs = []

        # Unfold the attacking_strategy dictionary to get pairs of player territory and enemy territory that could be attacked
        for key in attacking_strategy.keys():
            eligible_to_attack_armies_enemies_pairs.extend(
                [(key, x) for x in attacking_strategy[key]])

        max_subset_length = 5
        # Get all the possible attacking sequences that could be performed on the current state
        attack_sequence_subsets_pairs = get_subsets(
            eligible_to_attack_armies_enemies_pairs, max_subset_length)
        print("input set ")
        print("list of subsets ")
        # List of states consequent from applying all possible attacking sequences
        children_states = []
        for subset in attack_sequence_subsets_pairs:

            # if the subset is an empty one, append the current state to children states
            print("subset length", len(subset))
            if len(subset) == 0:
                children_states.append(state)
                continue

            # If the attacking sequence subset is valid, perform it
            print("validate ",self._validate_subset(subset))
            if self._validate_subset(subset):
                # Add to the children states the result of performing attacking sequence on it
                children_states.extend(
                    self._get_attacking_children(attack(state, subset), max_recursion_depth + 1))
        return children_states

    def _get_children(self, state, additional_armies, player_territories):
        print("===================One expansion====================")
        reinforcement_children_states = self._get_reinforcement_children(state,
            additional_armies, player_territories)

        children_states = []
        max_number_of_children = 10
        for i,reinforcement_child_state in enumerate(reinforcement_children_states):
            max_recursion_depth = 0
            if i == max_number_of_children:
                break
            children_states.extend(self._get_attacking_children(reinforcement_child_state, max_recursion_depth))

        print("children returned ",len(children_states))
        return children_states
