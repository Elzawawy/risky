from utils.common_utils import get_subsets, partitions
from game.action_handlers.actions import reinforce_territory, attack

class RiskVisitor():
    def visit(self, state):
        additional_armies = state.get_additional_armies(state.player_name)
        player_territories = state.get_owned_territories(state.player_name)
        return self._get_children(state, additional_armies, player_territories)

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

            if not attacking_territory in attacking_territories_to_armies_number.keys():
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

    def _get_attacking_children(self, state):
        """
            Used to get all the children states after applying the territories attacking step.

            Args:
                state: A state after appling reinforcement step on it on the first call only
                then it's after recursion an attack state.

            Returns:
                List of all possible children states after applying the territories attacking step.
        """
        print("in get attacking children")
        # Dictionary of territories eligibe to attack mapped to the enemys' territories
        attacking_strategy = state.get_attacking_strategy(state.player_name)

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
        print("input set ",eligible_to_attack_armies_enemies_pairs)
        print("list of subsets ",attack_sequence_subsets_pairs)
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
                    self._get_attacking_children(attack(state, subset)))
        return children_states

    def _get_children(self, state, additional_armies, player_territories):
        reinforcement_children_states = self._get_reinforcement_children(state,
            additional_armies, player_territories)

        children_states = []
        for reinforcement_child_state in reinforcement_children_states:
            children_states.extend(self._get_attacking_children(reinforcement_child_state))

        return children_states
