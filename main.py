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
    real_time_a_star_search(initial_state, risk_game.is_goal, risk_game.heuristic, RiskVisitor())
