from utils.search_algorithms import minimax_alpha_beta_pruning, greedy_best_first_search
from utils.search_algorithms import real_time_a_star_search
from game.components import *
from game.action_handlers.risk_visitor import RiskVisitor
from game.game import RiskGame

if __name__ == "__main__":

    risk_game = RiskGame()

    territory1 = Territory("ALexandria", "Swidan", 5)
    territory2 = Territory("Cairo", "Swidan", 4)
    territory3 = Territory("Luxor", "Mostafa", 3)

    territory_neighbours_dict = {territory1:[territory2, territory3],
                                 territory2:[territory1],
                                 territory3:[territory1]}

    initial_state = RiskGameState(territory_neighbours_dict, "Swidan")
    # greedy_best_first_search(initial_state, lambda x: 1, RiskVisitor())
    minimax_alpha_beta_pruning(initial_state, "Swidan", "Mostafa", RiskVisitor())
