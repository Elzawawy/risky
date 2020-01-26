from game.map import get_map
from random import shuffle
from game.components import RiskGameState
from game.agents.aggressive_agent import AggressiveAgent
from game.agents.minimax_agent import MinimaxAgent
from game.agents.a_star_agent import AStarAgent
from game.agents.passive_agent import PassiveAgent
from game.agents.greedy_agent import GreedyAgent
from game.agents.rta_star_agent import RTAStarAgent
from game.agents.human_agent import HumanAgent
from enum import Enum
from game.components import Territory


class AgentTypes(Enum):
    MINIMAX = 0
    A_STAR = 1
    RTA_STAR = 2
    GREEDY = 3
    PACIFIST = 4
    AGRESSIVE = 5
    PASSIVE = 6
    HUMAN = 7


class RiskGame:
    def __init__(self, agent1_type, agent2_type, board, agent1_name, agent2_name):
        self.agent1_type = agent1_type
        self.agent2_type = agent2_type
        self.agent1_name = agent1_name
        self.agent2_name = agent2_name
        self.board = board
        self.map = get_map(board)
        # territory1 = Territory("Alexandria")
        # territory2 = Territory("Cairo")
        # territory3 = Territory("Luxor")
        # territory1 = Territory("Giza")
        # territory2 = Territory("Qena")
        # territory3 = Territory("Sohag")
        # territory1 = Territory("Suez")

        # territory_neighbours_dict = {territory1: [territory2, territory3],
        #                              territory2: [territory1], territory3:[territory1]}
        # self.map = territory_neighbours_dict
        self.agent1 = self.get_agent(agent1_type, agent1_name)
        self.agent2 = self.get_agent(agent2_type, agent2_name)
        self.turn = 0
        self.agent_names = {0: self.agent1.player_name,
                            1: self.agent2.player_name}
        self.initial_armies = 20

    def get_agent(self, agent_type, player_name):
        return {
            AgentTypes.MINIMAX: MinimaxAgent(self.agent1_name, self. agent2_name, self.utility, self.cutoff_test_using_depth(3)),
            AgentTypes.A_STAR: AStarAgent(player_name, self.heuristic, self.is_goal),
            AgentTypes.RTA_STAR: RTAStarAgent(player_name, self.heuristic, self.is_goal),
            AgentTypes.GREEDY: GreedyAgent(player_name, self.heuristic, self.is_goal),
            AgentTypes.PACIFIST: PassiveAgent(player_name),
            AgentTypes.AGRESSIVE: AggressiveAgent(player_name),
            AgentTypes.PASSIVE: PassiveAgent(player_name),
            AgentTypes.HUMAN: HumanAgent(player_name)
        }[agent_type]

    def start(self):
        state = RiskGameState(self.map)

        for i in range(self.initial_armies):
            self.turn = 0
            self.agent1.place_initial_armies(state)
            self.turn = 1
            self.agent2.place_initial_armies(state)
        owned_territories_1 = None
        tie_counter = 0

        initial_state = state.__deepcopy__()

        while(1):
            owned_territories_1 = state.get_owned_territories(self.agent1.player_name)
            print("==================Agent 1========================")
            self.turn = 0
            state = self.agent1.take_turn(state)
            if self.is_goal(state):
                print(self.agent1_name)
                for territory in state.map.keys():
                    print(territory.territory_name, territory.number_of_armies)
                return self.agent1_name, state
            print("==================Agent 2========================")
            state.parent = None
            self.turn = 1
            state = self.agent2.take_turn(state)
            if self.is_goal(state):
                print(self.agent2_name)
                for territory in state.map.keys():
                    print(territory.territory_name, territory.number_of_armies)
                return self.agent2_name, state

            if len(owned_territories_1) == len(state.get_owned_territories(self.agent1.player_name)):
                tie_counter += 1
                print("tie ", tie_counter)

            if tie_counter >= 5:
                tie_counter = 0
                self.break_tie(state)
                owned_territories_1 = state.get_owned_territories(self.agent1.player_name)

    def break_tie(self, state):
        print("in tie breaking")
        for territory in state.get_owned_territories(self.agent1_name):
            territory.number_of_armies = 2

        for territory in state.get_owned_territories(self.agent2_name):
            territory.number_of_armies = 2

        

    def is_goal(self, state):
        print("owned territories ", len(
            state.get_owned_territories(self.agent_names[self.turn])))
        armies = [x.number_of_armies for x in state.get_owned_territories(self.agent_names[self.turn])]
        if self.turn == 0:
            x=1
        else:
            x=0
        enemy_armies = [x.number_of_armies for x in state.get_owned_territories(self.agent_names[x])]
        print("armies owned ",armies, "enemy armies",enemy_armies)
        return len(state.get_owned_territories(self.agent_names[0])) >= 0.7 * len(self.map) or len(state.get_owned_territories(self.agent_names[1])) >= 0.7 * len(self.map)

    def heuristic(self, state):
        sum_enemy_amount_of_units = 0
        sum_border_security_ratio = 0
        for owned_territory in state.get_owned_territories(self.agent_names[self.turn]):
            for enemy_territory in state.get_attacking_enemies(owned_territory, self.agent_names[self.turn]):
                sum_enemy_amount_of_units += enemy_territory.number_of_armies
            sum_border_security_ratio += sum_enemy_amount_of_units * \
                1.0 / owned_territory.number_of_armies
            sum_enemy_amount_of_units = 0
        return 0.5*sum_border_security_ratio + 0.5 * len(state.get_owned_territories(self.agent_names[not self.turn]))

    def utility(self, state):
        return len(state.get_owned_territories(self.agent_names[self.turn]))

    def cutoff_test_using_depth(self, depth):
        def cutoff_test(state):
            return state.depth == depth or self.is_goal(state)
        return cutoff_test

    def initialize_map_with_armies(self):
        ARMIES_NUMBER = 2
        shuffled_map_keys = list(self.map.keys())
        shuffle(shuffled_map_keys)
        each_player_max_territory_number = len(self.map.keys())//2

        for i in range(each_player_max_territory_number):
            shuffled_map_keys[i].owner = self.agent_names[0]
            shuffled_map_keys[i].number_of_armies = ARMIES_NUMBER
            shuffled_map_keys[i
                              + each_player_max_territory_number].owner = self.agent_names[1]
            shuffled_map_keys[i
                              + each_player_max_territory_number].number_of_armies = ARMIES_NUMBER
        if len(self.map.keys()) % 2 != 0:
            shuffled_map_keys[len(self.map.keys())
                              - 1].owner = self.agent_names[1]
            shuffled_map_keys[len(self.map.keys())
                              - 1].number_of_armies = ARMIES_NUMBER
