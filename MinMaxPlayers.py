########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2022, Swarthmore College
########################################

from StaticEvaluators import mancalaBasicEval, breakthroughBasicEval, \
                       breakthroughBetterEval

class MinMaxPlayer:
    """Gets moves by depth-limited minimax search."""
    def __init__(self, boardEval, depthBound):
        self.name = "MinMax"
        self.boardEval = boardEval   # static evaluation function
        self.depthBound = depthBound # limit of search
        self.bestMove = None         # best move from root

    def getMove(self, game_state):
        """Create a recursive helper function to implement Minimax, and
        call that helper from here. Initialize bestMove to None before
        the call to helper and then return bestMove found."""
        #raise NotImplementedError("TODO")
        self.bestMove = None
        bestValue = self.bounded_min_max(game_state, 0)
        return self.bestMove

    def bounded_min_max(self, game_state, depth):
        # print("depth",depth)
        if depth == self.depthBound or game_state.isTerminal:
            return self.boardEval(game_state)

        bestValue = game_state.turn * float('-inf')
        for move in game_state.availableMoves:
            nextState = game_state.makeMove(move)
            value = self.bounded_min_max(nextState, depth+1)
            if game_state.turn == 1:
                if value > bestValue:
                    bestValue = value
                    if depth == 0:
                        self.bestMove = move
            else:
                if value < bestValue:
                    bestValue = value
                    if depth == 0:
                        self.bestMove = move
        return bestValue

class PruningPlayer:
    """Gets moves by depth-limited minimax search with alpha-beta pruning."""
    def __init__(self, boardEval, depthBound):
        self.name = "Pruning"
        self.boardEval = boardEval   # static evaluation function
        self.depthBound = depthBound # limit of search
        self.bestMove = None         # best move from root

    def getMove(self, game_state):
        """Create a recursive helper function to implement AlphaBeta pruning
        and call that helper from here. Initialize bestMove to None before
        the call to helper and then return bestMove found."""
        self.bestMove = None
        bestValue = self.min_max_pruning(game_state, 0, -float('inf'),float('inf'))
        return self.bestMove
    
    def min_max_pruning(self, game_state, depth,alpha,beta):
        if depth == self.depthBound or game_state.isTerminal:
            return self.boardEval(game_state)

        bestValue = game_state.turn * float('-inf')
        for move in game_state.availableMoves:
            nextState = game_state.makeMove(move)
            value = self.min_max_pruning(nextState, depth+1,alpha,beta)
            if game_state.turn == 1:
                if value > bestValue:
                    bestValue = value
                    if depth == 0:
                        self.bestMove = move
                alpha=max(alpha,value)
            else:
                if value < bestValue:
                    bestValue = value
                    if depth == 0:
                        self.bestMove = move
                beta=min(beta,value)
            if alpha>=beta:
                break
        return bestValue
