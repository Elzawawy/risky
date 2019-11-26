from utils.search_algorithms import minimax_alpha_beta_pruning, greedy_best_first_search, real_time_minimax_alpha_beta_pruning
from utils.search_algorithms import real_time_a_star_search
from game.components import *
from game.action_handlers.risk_visitor import RiskVisitor
from game.game import RiskGame
from game.map import get_map

if __name__ == "__main__":
    print(get_map("Egypt"))
    # for distro in distros_dict:
        # print(distro['Delaware'])
