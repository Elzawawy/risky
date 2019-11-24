from utils.search_algorithms import minimax_alpha_beta_pruning
from game.components import *

if __name__ == "__main__":
    territory1 = Territory("ALexandria", "Swidan", 5)
    territory2 = Territory("Cairo", "Swidan", 4)
    territory3 = Territory("Luxor", "Mostafa", 3)

    territory_neighbours_dict = {territory1:[territory2, territory3],
                                 territory2:[territory1],
                                 territory3:[territory1]}

    initial_state = RiskGameState(territory_neighbours_dict, "Swidan")
    minimax_alpha_beta_pruning(initial_state, "Swidan", "Mostafa")