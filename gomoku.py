import numpy as np
import pandas as pd
from scipy.signal import convolve2d

class gomoku():
    """Set up gomuku game with a (225,1) vector
    """
    def __init__(self):
        self.gameBoard = np.zeros((15*15,1))
    def getGameBoard(self):
        return self.gameBoard

    """Move of player, set 1 for black and -1 for white in a gameboard position

    raise error put stone in placed position
    """
    def blackMove(self,place):
        if self.gameBoard[place] != 0:
            raise Exception("A stone has been put in this place!")
        else:
            self.gameBoard[place] = 1
    def whiteMove(self,place):
        if self.gameBoard[place] != 0:
            raise Exception("A stone has been put in this place!")
        else:
            self.gameBoard[place] = -1
    """set up a new game, to be updated with pygame imported
    """
    def newgame(self):
        self.gameBoard = np.zeros((15*15,1))

    """Use convolution calculation to find game condition,
    Condition is a (4,1) vector represent:
     (if black player wins,
      if white player wins,
      if draw,
      if game is not finished)
    """
    def gameCondition(self):
        m = self.getGameBoard().reshape((15,15))
        horizontal = np.array([1,1,1,1,1]).reshape(1,5)
        vertical = np.array([1,1,1,1,1]).reshape(5,1)
        identity = np.eye(5)
        exchange = np.fliplr(identity)
        b = convolve2d(m,horizontal,mode="valid")#5 stones in one row
        c = convolve2d(m,vertical,mode='valid')#5 stones in one column
        d = convolve2d(m,identity,mode='valid')
        #5 stones from upper left to bottom right
        e = convolve2d(m,exchange,mode='valid')
        #5 stones from supper right to bottom left
        if (5 in b or 5 in c or 5 in d or 5 in e):
            return np.array([1,0,0,0]).reshape(1,4)
        elif (-5 in b or -5 in c or -5 in d or -5 in e):
            return np.array([0,1,0,0]).reshape(1,4)
        elif 0 not in m:
            return np.array([0,0,1,0]).reshape(1,4)
        else:
            return np.array([0,0,0,1]).reshape(1,4)
"""two functions to exchange board and a place in gameboard array
   tuple --- (place in rows,place in columns) range from (0,15))
   place in array --- int range from (0,225)
"""
def boardToArray(placeInBoard):
    return placeInBoard[0]*15+placeInBoard[1]
def arrayToBoard(placeInArray):
    return (placeInArray//15,placeInArray%15)
