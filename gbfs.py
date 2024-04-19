# Pacman agent implementation using greedy best-first search (GBFS)
# Import necessary modules
from pacman_module.game import Agent, Directions
from pacman_module.util import PriorityQueue
import random

# Function to extract a key that uniquely identifies a Pacman game state
def key(state):
    """Returns a key that uniquely identifies a Pacman game state.

    Arguments:
        state: a game state. See API or class `pacman.GameState`.

    Returns:
        A hashable key tuple.
    """
    return state.getPacmanPosition()

# PacmanAgent class definition
class PacmanAgent(Agent):
    """Pacman agent based on greedy best-first search (GBFS)."""

    # Constructor method
    def __init__(self):
        super().__init__()
        self.moves = None

    # Method to get the next legal move for Pacman
    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Return:
            A legal move as defined in `game.Directions`.
        """
        if self.moves is None or len(self.moves) == 0:
            self.moves = self.gbfs(state, set())

        if self.moves:
            return self.moves.pop(0)
        else:
            return Directions.STOP

    # Method to perform greedy best-first search
    def gbfs(self, state, visited):
        """Given a Pacman game state and a set of visited states, returns a list of legal moves
        to solve the search layout while avoiding revisiting visited states.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.
            visited: a set of visited states.

        Returns:
            A list of legal moves.
        """
        path = []
        fringe = PriorityQueue()
        fringe.push((state, path), 0)  # Initialize priority with 0
        walls = state.getWalls()  # Take Walls

        #  Loop until the fringe is empty
        while not fringe.isEmpty():
            current, path = fringe.pop()

            current_key = key(current)

            if current_key in visited:
                continue

            visited.add(current_key)

            if current.isWin():
                return path

            successors = list(current.generatePacmanSuccessors())
            random.shuffle(successors)

            for successor, action in successors:
                successor_key = key(successor)
                successor_position = successor.getPacmanPosition()

                if not walls[successor_position[0]][successor_position[1]]:
                    priority = self.heuristic(successor)  # Calculate priority based on heuristic
                    fringe.push((successor, path + [action]), priority)

        return path

    # Heuristic function to estimate distance to the goal
    def heuristic(self, state):
        """A heuristic function to estimate the distance to the goal.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A numeric value representing the estimated distance to the goal.
        """
        # Example: Manhattan distance to the nearest food pellet
        pacman_position = state.getPacmanPosition()
        food_positions = state.getFood().asList()
        if food_positions:
            distances = [abs(pacman_position[0] - food[0]) + abs(pacman_position[1] - food[1]) for food in food_positions]
            return min(distances)
        else:
            return 0  # If there's no food, return 0 heuristic value
