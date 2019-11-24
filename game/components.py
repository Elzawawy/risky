from utils.datastructures.graph import BaseGraph
import math
import itertools
from utils.common_utils import get_subsets
from copy import deepcopy

class RiskGameGraph(BaseGraph):
    def __init__(self, graph_dict):
        super().__init__(graph_dict)

    def reinforce_territory(self, territory, additional_armies):
        """
            Used to add reinforcement armies to a territory.

            Args:
                territory: The territory that will have the reinforcement.
                additional_armies: the armies which will be added to the territory.
        """
        keys = self.adjacency_list.keys()
       
        for key in keys:
            if key.territory_name == territory.territory_name:
                key.number_of_armies += additional_armies
                return

    def get_owned_territories(self, player_name):
        """
            Used to get the territories owned by a player.

            Args:
                player_name: the name of the player who want to get its territories.

            Returns:
                All the territories owned by a player
        """
        return [x for x in self.adjacency_list.keys() if x.owner == player_name]

    def get_attacking_strategy(self, player_name):
        """
        returns: dictionary of territories eligibe to attack mapped to the adjacent territories that 
        it can attack
        """
        # Get all the owned territories which have number of armies > 1 (eligible to attack)
        eligible_to_attack_territories = [
            x for x in self.get_owned_territories(player_name) if x.number_of_armies > 1]
        # A map where:
        # key -> territory eligible to attack
        # value -> enemys' territories list that could be attacked
        attacking_strategy_map = {}

        for territory in eligible_to_attack_territories:
            # For each eligible territories, find the enemys' territories list that it could attack
            adjacent_territories = [x for x in self.get_adjacent_nodes(
                territory) if x.owner != player_name and territory.number_of_armies > x.number_of_armies]

            # If the enemys' territories list number of armies > 0 add it to the attacking_strategy_map
            if len(adjacent_territories) > 0:
                attacking_strategy_map[territory] = adjacent_territories
        return attacking_strategy_map

    def get_territory(self, territory):
        for node in self.adjacency_list.keys():
            if node == territory:
                return node
        return None

class Territory:
    def __init__(self, territory_name, owner, number_of_armies=0):
        self.territory_name = territory_name
        self.number_of_armies = number_of_armies
        self.owner = owner

    def __eq__(self, obj):
        return self.territory_name == obj.territory_name

    def __hash__(self):
        return hash(self.territory_name)


class RiskGameState:
    def __init__(self, territory_neighbours_dict, player_name=None, parent=None, cost=0, depth=0):
        self.map = RiskGameGraph(territory_neighbours_dict)
        self.children = []
        self.player_name = player_name
        self.parent = parent
        self.cost = cost
        self.depth = depth
        self.cost_function = lambda x: 1

    def __deepcopy__(self):
        new_instance = type(self)(deepcopy(self.map.adjacency_list), self.player_name,self.parent, self.cost, self.depth)
        return new_instance

    def _get_territory(self, territory):
        return self.map.get_territory(territory)

    def is_goal(self):
        print("owned territories ",len(self.map.get_owned_territories(self.player_name)))
        return len(self.map.get_owned_territories(self.player_name)) == 3

    def validate_subset(self, attacking_moves_sequence):
        attacking_territories_to_armies_number = {}

        for attacking_move in attacking_moves_sequence:
            attacking_territory = attacking_move[0]
            enemy_territory = attacking_move[1]

            if not attacking_territory in attacking_territories_to_armies_number.keys():
                attacking_territories_to_armies_number[attacking_territory] = attacking_territory.number_of_armies

            attacking_armies_number = attacking_territories_to_armies_number[attacking_territory]

            if attacking_armies_number > enemy_territory.number_of_armies:
                attacking_territories_to_armies_number[attacking_territory] = attacking_armies_number - 1
            else:
                return False

        return True

    def attack(self, state, attacking_moves_sequence):
        new_state = state.__deepcopy__()
        for attacking_move in attacking_moves_sequence:
            attacking_territory = new_state._get_territory(attacking_move[0])
            enemy_territory = new_state._get_territory(attacking_move[1])
            attacking_territory.number_of_armies -= 1
            enemy_territory.number_of_armies = 1
            enemy_territory.owner = attacking_territory.owner
        print("owned terrirories after attacking",len(new_state.map.get_owned_territories(new_state.player_name)))
        return new_state

    def _get_additional_armies(self, player_name):
        return max(3, len(self.map.get_owned_territories(player_name)) / 3)

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
            new_state = self.__deepcopy__()  # copy self to new state
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
                state: A state after appling reinforcement step on it on the first call only
                then it's after recusrsion an attack state.

            Returns: 
                List of all possible children states after applying the territories attacking step.
        """
        print("in get attacking children")
        # Dictionary of territories eligibe to attack mapped to the enemys' territories
        attacking_strategy = state.map.get_attacking_strategy(state.player_name)

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
            print("validate ",self.validate_subset(subset))
            if self.validate_subset(subset):
                # Add to the children states the result of performing attacking sequence on it
                children_states.extend(
                    self._get_attacking_children(self.attack(state, subset)))
        return children_states

    def _get_children(self, additional_armies, player_territories):
        reinforcement_children_states = self._get_reinforcement_children(
            additional_armies, player_territories)

        childern_states = []
        for reinforcement_child_state in reinforcement_children_states:
            childern_states.extend(self._get_attacking_children(reinforcement_child_state))
            
        return childern_states
        
    def expand(self):
        print("=================================================")
        additional_armies = self._get_additional_armies(self.player_name)
        player_territories = self.map.get_owned_territories(self.player_name)
        return self._get_children(additional_armies, player_territories)

    def __lt__(self, other):
        return self.cost_function(self) < self.cost_function(other)

    def __le__(self, other):
        return self.cost_function(self) <= self.cost_function(other)

        
