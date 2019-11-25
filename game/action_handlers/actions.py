
def attack(state, attacking_moves_sequence):
    new_state = state.__deepcopy__()
    for attacking_move in attacking_moves_sequence:
        attacking_territory = new_state.get_territory(attacking_move[0])
        enemy_territory = new_state.get_territory(attacking_move[1])
        attacking_territory.number_of_armies -= 1
        enemy_territory.number_of_armies = 1
        if attacking_territory.number_of_armies <= 0 or enemy_territory.number_of_armies <= 0 :
            raise(ValueError("Not valid attack move sequence"))
        enemy_territory.owner = attacking_territory.owner
    print("owned terrirories after attacking",len(new_state.get_owned_territories(new_state.player_name)))
    return new_state

def reinforce_territory(state, territory, additional_armies):
    """
        Used to add reinforcement armies to a territory.

        Args:
            territory: The territory that will have the reinforcement.
            additional_armies: the armies which will be added to the territory.
    """
    keys = state.adjacency_list.keys()

    for key in keys:
        if key.territory_name == territory.territory_name:
            key.number_of_armies += additional_armies
            return
