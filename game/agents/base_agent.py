from abc import ABC, abstractmethod

# What is ABC ?
# Python on its own doesn't provide abstract classes.
# Yet, `abc` is a module which provides the infrastructure for defining Abstract Base Classes (ABCs).
# They are useful, if you want to make base classes that cannot be instantiated, but provide a specific interface or part of an implementation.
# An abstract method can have an implementation in the abstract class.
# Even if they are implemented, designers of subclasses will be forced to override the implementation.
class BaseAgent(ABC):
    def __init__(self, player_name):
        self.player_name = player_name
        super().__init__()

    @abstractmethod
    def place_initial_troops(self, initial_state, num_troops):
        """ Place Initial Troops on board. Executed once at begining of game.

            Arguments:\\
                * current_state: The current Map State of the game.\\
                * num_troops: The number of troops to reinforce with.\\
            Returns:\\
                * result_state: The resulting Map State of the game.
        """
        pass

    @abstractmethod
    def take_turn(self, current_state):
        """ Take Turn in game. Executed each turn on agents.

            Arguments:\\
                * current_state: The current Map State of the game.\\
            Returns:\\
                * result_state: The resulting Map State of the game.
        """
        pass
