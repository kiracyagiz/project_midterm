from pacman_module.game import Agent, Directions

def key(state):
    """Returns a key that uniquely identifies a Pacman game state.

    Arguments:
        state: a game state. See API or class pacman.GameState.

    Returns:
        A hashable key tuple.
    """
    return (
        state.getPacmanPosition(),
        state.getFood(),
        state.getNumFood()
    )

class PacmanAgent(Agent):
    """Pacman agent based on Iterative Deepening Search (IDS)."""

    def __init__(self):
        super().__init__()
        self.moves = None

    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        Arguments:
            state: a game state. See API or class pacman.GameState.

        Returns:
            A legal move as defined in game.Directions.
        """

        if self.moves is None:
            self.moves = self.ids(state)

        if self.moves:
            return self.moves.pop(0)
        else:
            return Directions.STOP

    def ids(self, state):
        """Iterative Deepening Search algorithm to find the optimal path.

        Arguments:
            state: a game state. See API or class pacman.GameState.

        Returns:
            A list of legal moves.
        """

        for depth in range(1, float('inf')):
            result = self.dls(state, depth)
            if result is not None:
                return result

    def dls(self, state, depth):
        """Depth-limited Search to explore paths up to a given depth.

        Arguments:
            state: a game state. See API or class pacman.GameState.
            depth: the maximum depth to explore.

        Returns:
            A list of legal moves if a solution is found within the depth limit,
            otherwise None.
        """

        def recursive_dls(current_state, current_depth, path):
            if current_depth == 0:
                return path

            if current_state.isWin():
                return path

            for successor, action, _ in current_state.generatePacmanSuccessors():
                result = recursive_dls(successor, current_depth - 1, path + [action])
                if result is not None:
                    return result

            return None

        return recursive_dls(state, depth, [])
