import math


def minimax_alpha_beta_pruning(initial_state):
    def minimize(state, alpha, beta):
        if state.is_terminal():
            return None, state.calculate_utility()

        minChild, minUtility = None, math.inf

        for child in state.expand():
            child, utility = maximize(child, alpha, beta)

            if utility < minUtility:
                minChild, minUtility = child, utility
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility

        return minChild, minUtility

    def maximize(state, alpha, beta):
        if state.is_terminal():
            return None, state.calculate_utility()

        maxChild, maxUtility = None, -math.inf

        for child in state.expand():
            child, utility = minimize(child, alpha, beta)

            if utility > maxUtility:
                maxChild, maxUtility = child, utility
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility

        return maxChild, maxUtility

    child, utility = maximize(initial_state, -math.inf, math.inf)

    return child
