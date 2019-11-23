from utils.priority_queue import PriorityQueue
import heapq


def greedy_best_first_search(initial_state, heuristic):
    """Greedy Best First Search Algorithm

    Keyword arguments:\\
    * initial_state -- starting state of problem.\\
    * heuristic -- a heuristic estimate to goal h(n)

    Return variables:\\
    * None in case of no goal found.\\
    * state -- goal state found.\\
    * nodes_expanded -- final number of expanded nodes to reach goal.\\
    * max_search_depth -- Maximum depth reached where goal resides. 
    """
    # Build minimum heap based on heuristic as key.
    frontier = PriorityQueue('min', heuristic)
    frontier.append(initial_state)
    # Build dictionary for O(1) lookups.
    frontier_config = {}
    frontier_config[tuple(initial_state.config)] = True
    # Build set of already explored states.
    explored = set()
    # Variables for algorithm evaluation purposes.
    nodes_expanded = 0
    max_search_depth = 0

    while frontier:
        state = frontier.pop()
        explored.add(state)
        # Goal Test: stop algorithm when goal is reached.
        if state.is_goal():
            return (state, nodes_expanded, max_search_depth)

        nodes_expanded += 1
        for neighbor in state.expand():
            # Add state to explored states if doesn't already exists.
            if neighbor not in explored and tuple(neighbor.config) not in frontier_config:
                frontier.append(neighbor)
                frontier_config[tuple(neighbor.config)] = True
                if neighbor.cost > max_search_depth:
                    max_search_depth = neighbor.cost
            # If state is not explored but in frontier, update it's key if less.
            elif neighbor in frontier:
                if heuristic(neighbor) < frontier[neighbor]:
                    frontier.__delitem__(neighbor)
                    frontier.append(neighbor)
    return None


def a_star_search(initial_state, heuristic, cost):
    """A* search Algorithm is greedy best-first graph search with f(n) = g(n)+h(n).

    Keyword arguments:\\
    * initial_state -- starting state of problem.\\
    * heuristic -- a heuristic estimate to goal h(n)\\
    * cost -- a cost function for a state.

    Return variables:\\
    * None in case of no goal found.\\
    * state -- goal state found.\\
    * nodes_expanded -- final number of expanded nodes to reach goal.\\
    * max_search_depth -- Maximum depth reached where goal resides. 
    """
    return greedy_best_first_search(initial_state, cost+heuristic)


def real_time_a_star_search(initial_state, heuristic, cost):
    """ An informed search that used to reduce the execution time of A*.

        Args:
            initial_state : Starting state of problem.
            heuristic : A heuristic estimate to goal h(n).
            cost : A cost function for a state.

        Returns:
            current_state : A state that eventually will be the goal state. 
    """

    visited_states_to_heuristic = {}
    current_state = initial_state
    FIRST_BEST_STATE_INDEX = 2
    SECOND_BEST_TOTAL_COST_INDEX = 0

    while(not current_state.is_goal()):

        tota_cost_to_state = []
        counter = 0

        # Expand the current state
        for neighbour in current_state.expand():

            # If the neighbour exists in the visited_states dictionary, then stored hurestic value in the dictionary is used
            # and added to the cost from the current state to the neighbour to get the total cost 
            if neighbour in visited_states_to_heuristic:
                neighbour_total_cost = visited_states_to_heuristic[neighbour] + cost(current_state, neighbour)

            # Else, then calculate the hurestic value of the neighbour
            # and add it to the cost from the current state to the neighbour to get the total cost
            else:
                neighbour_total_cost = heuristic(neighbour) + cost(current_state, neighbour)

            # Store the neighbours & their total cost in a min heap 
            heapq.heappush(tota_cost_to_state, (neighbour_total_cost, counter, neighbour))
            counter += 1

        temp_state = heapq.heappop(tota_cost_to_state)[FIRST_BEST_STATE_INDEX]

        # Store the current state associated with it the second best total cost value
        visited_states_to_heuristic[current_state] = heapq.heappop(tota_cost_to_state)[SECOND_BEST_TOTAL_COST_INDEX]

        # Choose the state with the minimum total cost to be the new current state
        current_state = temp_state

    return current_state