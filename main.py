from utils.search_algorithms import minimax_alpha_beta_pruning, greedy_best_first_search, real_time_minimax_alpha_beta_pruning
from utils.search_algorithms import real_time_a_star_search
from game.components import *
from game.action_handlers.risk_visitor import RiskVisitor
from game.game import RiskGame
from game.agents.pacifist_agent import PacifistAgent
from game.game import AgentTypes
from game.map import get_map
from random import seed
from time import time

if __name__ == "__main__":

    # print(get_map("Egypt"))
    risk_game = RiskGame(AgentTypes.AGRESSIVE,
                         AgentTypes.PASSIVE, "test", "Swidan", "Mostafa")
    risk_game.initialize_map_with_armies()

    print(risk_game.start())

    # risk_game = RiskGame()
    # territory1 = Territory("ALexandria", "Swidan", 5)
    # territory2 = Territory("Cairo", "Swidan", 4)
    # territory3 = Territory("Luxor", "Mostafa", 3)
    #
    # territory_neighbours_dict = {territory1: [territory2, territory3],
    #                              territory2: [territory1],
    #                              territory3: [territory1]}
    #
    # initial_state = RiskGameState(territory_neighbours_dict, "Swidan")
    # greedy_best_first_search(initial_state, lambda x: 1, RiskVisitor())
    # minimax_alpha_beta_pruning(initial_state, "Swidan", "Mostafa",
    #                            RiskVisitor(), risk_game.utility,
    #                             risk_game.is_goal)
    # real_time_minimax_alpha_beta_pruning(initial_state, "Swidan", "Mostafa",
    #                             RiskVisitor(), risk_game.utility,
    #                             risk_game.cutoff_test_using_depth(100))

    # PacifistAgent("Swidan").take_turn(initial_state)
