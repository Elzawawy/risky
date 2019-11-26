import unittest
from utils.search_algorithms import minimax_alpha_beta_pruning, greedy_best_first_search, real_time_minimax_alpha_beta_pruning
from utils.search_algorithms import real_time_a_star_search
from game.components import *
from game.action_handlers.risk_visitor import RiskVisitor
from game.game import RiskGame
from game.agents.aggressive_agent import AggressiveAgent

class RiskGoalTest(unittest.TestCase):

    def test_real_time_alpha_beta_pruning(self):
        risk_game = RiskGame()

        territory1 = Territory("ALexandria", "Swidan", 5)
        territory2 = Territory("Cairo", "Swidan", 4)
        territory3 = Territory("Luxor", "Mostafa", 3)

        territory_neighbours_dict = {territory1: [territory2, territory3],
                                     territory2: [territory1],
                                     territory3: [territory1]}

        initial_state = RiskGameState(territory_neighbours_dict, "Swidan")
        # greedy_best_first_search(initial_state, lambda x: 1, RiskVisitor())
        # minimax_alpha_beta_pruning(initial_state, "Swidan", "Mostafa",
        #                            RiskVisitor(), risk_game.utility,
        #                             risk_game.is_goal)


        child = real_time_minimax_alpha_beta_pruning(initial_state, "Swidan", "Mostafa",
                                   RiskVisitor("Swidan"), risk_game.utility,
                                    risk_game.cutoff_test_using_depth(100))
        pair = (len(child.get_owned_territories("Swidan")),len(child.get_owned_territories("Mostafa")))
        self.assertEqual(pair, (3,0), "3,0")

    def test_aggressive_agent(self):
        risk_game = RiskGame()

        territory1 = Territory("ALexandria", "Swidan", 5)
        territory2 = Territory("Cairo", "Swidan", 4)
        territory3 = Territory("Luxor", "Mostafa", 3)

        territory_neighbours_dict = {territory1: [territory2, territory3],
                                     territory2: [territory1],
                                     territory3: [territory1]}

        initial_state = RiskGameState(territory_neighbours_dict, "Swidan")
        # greedy_best_first_search(initial_state, lambda x: 1, RiskVisitor())
        # minimax_alpha_beta_pruning(initial_state, "Swidan", "Mostafa",
        #                            RiskVisitor(), risk_game.utility,
        #                             risk_game.is_goal)

        
        pair = len(AggressiveAgent("Swidan").take_turn(initial_state).get_owned_territories("Swidan"))
        self.assertEqual(pair, 3, "should be 3")

if __name__ == '__main__':
    unittest.main()
