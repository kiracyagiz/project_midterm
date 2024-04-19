from pacman_module.game import Agent, Directions
from pacman_module.util import Queue
import random
import time
import matplotlib.pyplot as plt

def key(state):
    """Returns a key that uniquely identifies a Pacman game state.

    Arguments:
        state: a game state. See API or class `pacman.GameState`.

    Returns:
        A hashable key tuple.
    """
    return state.getPacmanPosition()

class PacmanAgent(Agent):
    """Pacman agent based on breadth-first search (BFS)."""

    def __init__(self):
        super().__init__()
        self.moves = None
        self.expanded_nodes = 0
        self.execution_time = 0
        self.path_cost = 0
        self.optimal = True

    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Return:
            A legal move as defined in `game.Directions`.
        """
        start_time = time.time()
        if self.moves is None or len(self.moves) == 0:
            self.moves = self.bfs(state, set())

        end_time = time.time()
        self.execution_time = end_time - start_time

        if self.moves:
            return self.moves.pop(0)
        else:
            return Directions.STOP

    def bfs(self, state, visited):
        """Given a Pacman game state and a set of visited states, returns a list of legal moves
        to solve the search layout while avoiding revisiting visited states.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.
            visited: a set of visited states.

        Returns:
            A list of legal moves.
        """
        path = []
        fringe = Queue()
        fringe.push((state, path))
        walls = state.getWalls()  # Take Walls

        while not fringe.isEmpty():
            current, path = fringe.pop()
            self.expanded_nodes += 1
            
            current_key = key(current)

            if current_key in visited:
                continue

            # Add for visited
            visited.add(current_key)

            # Check for win condition
            if current.isWin():
                self.path_cost = len(path)
                self.visualize_metrics()
                return path

            # Generate successors
            successors = list(current.generatePacmanSuccessors())
            random.shuffle(successors)

            # current state valid moves
            has_valid_moves = False

            for successor, action in successors:
                successor_key = key(successor)
                successor_position = successor.getPacmanPosition()

                # Check if the successor position is valid (not a wall)
                if not walls[successor_position[0]][successor_position[1]]:
                    has_valid_moves = True
                    fringe.push((successor, path + [action]))

            # No valid moves from current state, backtrack
            if not has_valid_moves:
                path.pop()

        self.optimal = False  # If no solution found
        return path

    def visualize_metrics(self):
        # Bar chart for execution time
        plt.figure(figsize=(8, 6))
        plt.bar(['Execution Time'], [self.execution_time], color='blue')
        plt.ylabel('Time (seconds)')
        plt.title('Execution Time')
        plt.show()

        # Bar chart for nodes expanded
        plt.figure(figsize=(8, 6))
        plt.bar(['Nodes Expanded'], [self.expanded_nodes], color='green')
        plt.ylabel('Number of Nodes')
        plt.title('Nodes Expanded')
        plt.show()

        # Bar chart for path cost
        plt.figure(figsize=(8, 6))
        plt.bar(['Path Cost'], [self.path_cost], color='orange')
        plt.ylabel('Cost')
        plt.title('Path Cost')
        plt.show()

        # Print out optimality
        print('Optimal Solution:', self.optimal)
