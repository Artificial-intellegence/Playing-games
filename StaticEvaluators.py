########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2022, Swarthmore College
########################################

from turtle import clear
import numpy as np
from random import choice
from Mancala import Mancala
from Breakthrough import Breakthrough

def mancalaBasicEval(mancala_game):
    """Difference between the scores for each player.
    Returns +(max possible score) if player +1 has won.
    Returns -(max possible score) if player -1 has won.

    Otherwise returns (player +1's score) - (player -1's score).

    Remember that the number of houses and seeds may vary."""
    if mancala_game.isTerminal:
        if mancala_game.winner ==1:
            return 48
        else :
            return -48

    return mancala_game.scores[0]-mancala_game.scores[1]

def breakthroughBasicEval(breakthrough_game):
    """Measures how far each player's pieces have advanced
    and returns the difference.

    Returns +(max possible advancement) if player +1 has won.
    Returns -(max possible advancement) if player -1 has won.

    Otherwise finds the rank of each piece (number of rows onto the board it
    has advanced), sums these ranks for each player, and
    returns (player +1's sum of ranks) - (player -1's sum of ranks).

    An example on a 5x3 board:
    ------------
    |  0  1  1 |  <-- player +1 has two pieces on rank 1
    |  1 -1  1 |  <-- +1 has two pieces on rank 2; -1 has one piece on rank 4
    |  0  1 -1 |  <-- +1 has (1 piece * rank 3); -1 has (1 piece * rank 3)
    | -1  0  0 |  <-- -1 has (1*2)
    | -1 -1 -1 |  <-- -1 has (3*1)
    ------------
    sum of +1's piece ranks = 1 + 1 + 2 + 2 + 3 = 9
    sum of -1's piece ranks = 1 + 1 + 1 + 2 + 3 + 4 = 12
    state value = 9 - 12 = -3

    Remember that the height and width of the board may vary."""
    board=breakthrough_game.board
    if breakthrough_game.isTerminal:
        if breakthrough_game.winner ==1:
            return len(board[0])*(len(board)) + len(board[0])*(len(board)-1)
        elif breakthrough_game.winner ==-1:
            return (-1)*(len(board[0])*(len(board)) + len(board[0])*(len(board)-1))

    scores=calculateTotalScores(board)
    return scores[0]-scores[1]

def calculateTotalScores(board):
    """ Helper function to calculate the scores of each player according to the
    rules provided upove.

    we call this fucntion both in the basicEval and in the betterEval"""
    firstPlayertotalScore=0
    secondPlayerTotalScore=0
    for i in range(len(board)):
        playerOne=0
        playerTwo=0
        for j in range(len(board[i])):
            if board[i][j]==1:
                playerOne+=1
            elif board[i][j]==-1:
                playerTwo+=1
        firstPlayertotalScore+=playerOne* (i+1)
        secondPlayerTotalScore+=playerTwo*(len(board)-i)
        return [firstPlayertotalScore,secondPlayerTotalScore]

def breakthroughBetterEval(breakthrough_game):
    """A heuristic that generally wins agains breakthroughBasicEval.
    This must be a static evaluation function (no search allowed).

    In our better Eval, beside considering how far the players of one side are
    from the opponent's end of the board, we also took into account the number
    of players under threat from the opponents players."""
    board=breakthrough_game.board
    if breakthrough_game.isTerminal:
        if breakthrough_game.winner ==1:
            return len(board[0])*(len(board)) + len(board[0])*(len(board)-1)
        elif breakthrough_game.winner ==-1:
            return (-1)*(len(board[0])*(len(board)) + len(board[0])*(len(board)-1))

    scores=calculateTotalScores(board)
    numberOfPlayersUnderThreat=NumUnderThreat(board)
    if breakthrough_game.turn==1:
        scores[0]+=numberOfPlayersUnderThreat
    else:
        scores[1]+=numberOfPlayersUnderThreat
    return scores[0]-scores[1]


def NumUnderThreat(board):
    """ Helper function to calculate the number of players under threat of being eliminated.

    We define a player under threat as the player who has an opponent within
    one forward diagonal move of their position  """
    numberOfPlayersUnderThreat=0
    for i in range(len(board)):
        for j in range(len(board[0])):
                if j-1>=0 and i+1<len(board):
                    if board[i][j]!=0 and board[i+1][j-1]!=0 and board[i][j]==(-1)*board[i+1][j-1]:
                         numberOfPlayersUnderThreat+=1
                if j+1<len(board[i]) and i+1<len(board) and board[i][j]==(-1)*board[i+1][j-1]:
                    if board[i][j]!=0 and board[i+1][j-1]!=0:
                         numberOfPlayersUnderThreat+=1
    return numberOfPlayersUnderThreat




if __name__ == '__main__':
    """
    Create a game of Mancala.  Try 10 random moves and check that the
    heuristic is working properly.
    """
    print("\nTESTING MANCALA HEURISTIC")
    print("-"*50)
    game1 = Mancala()
    for i in range(10):
        move = choice(game1.availableMoves)
        print("\nmaking move", move)
        game1 = game1.makeMove(move)
        print(game1)
        score = mancalaBasicEval(game1)
        print("basicEval score", score)

    print("\nTESTING BREAKTHROUGH HEURISTIC")
    print("-"*50)
    game1 = Breakthrough()
    for i in range(10):
        move = choice(game1.availableMoves)
        print("\nmaking move", move)
        game1 = game1.makeMove(move)
        print(game1)
        score = breakthroughBasicEval(game1)
        print("basicEval score", score)

    print("\nTESTING BREAKTHROUGH BETTER HEURISTIC")
    print("-"*50)
    game1 = Breakthrough()
    for i in range(10):
        move = choice(game1.availableMoves)
        print("\nmaking move", move)
        game1 = game1.makeMove(move)
        print(game1)
        score = breakthroughBetterEval(game1)
        print("basicEval score", score)

    # Add more testing for the Breakthrough
