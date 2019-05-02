import randomAI
import numpy as np
import pandas as pd
from scipy.signal import convolve2d

class GomokuBoard(object):
    """Set up gomuku game with a (225,1) vector
    """
    def __init__(self):
        self.__board = np.zeros((15*15,1))
    def initialize_board(self):
        self.__board = np.zeros((15*15,1))
    def set_board(self,newboard):
        self.__board = newboard
    def get_board(self):
        return self.__board
    """Get a valid move from the gameboard. Once a stone has been put, it can't
       be removed or replaced by another stone.
       return a (15*15,1) array with 1 means valid and 0 means invalid
    """
    def get_valid_move(self):
        move = np.zeros((15*15,1))
        for i in range(15*15):
            if self.__board[i] == 0:
                move[i] = 1
        return move
    """Move of player, set 1 for black and -1 for white in a gameboard position

    raise error put stone in placed position
    """
    def move_black(self,place):
        if self.__board[place] != 0:
            raise Exception("A stone has been put in this place!")
        else:
            self.__board[place] = 1
    def move_white(self,place):
        if self.__board[place] != 0:
            raise Exception("A stone has been put in this place!")
        else:
            self.__board[place] = -1
    """Use convolution calculation to find game condition,
    Condition is a (4,1) vector represent:
     (if black player wins,
      if white player wins,
      if draw,
      if game is not finished)
    """
    def get_game_condition(self):
        m = self.get_board().reshape((15,15))
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
            return np.array([0.,1.,0.,0.]).reshape(1,4)
        elif 0 not in m:
            return np.array([0.,0.,1.,0.]).reshape(1,4)
        else:
            return np.array([0.,0.,0.,1.]).reshape(1,4)
class GomokuAIPlay(object):
    def __init__(self,player1=randomAI.RandomAI(1,"black","randomAIOne"),player2=randomAI.RandomAI(1,"white","randomAITwo")):
        self.player1 = player1
        self.player2 = player2
        self.__gameBoard = GomokuBoard()
        self.isRecord = False
        self.resultHistory = np.zeros((1,1,4))
        self.gameHistory = None
    """set up a new game, to be updated with pygame imported
    """
    def set_new_game(self):
        self.__gameBoard.initialize_board()
    def play_one_round(self):
        step = 0
        if self.isRecord == False:
        #when isRecord is set off
            while True:
                pos = self.player1.play(self.__gameBoard)[1]
                #print("black:",array_to_board(pos))
                self.__gameBoard.move_black(pos)
                step += 1
                result = self.__gameBoard.get_game_condition()
                if sum(result[0,:3]) == 1:
                    if np.array_equal(self.resultHistory[0],np.array([[0., 0., 0., 0.]])):
                        self.resultHistory[0]=result
                    else:
                        n = np.append(n,result)
                        n.reshape((int(len(n)/4),4))
                    break
                else:
                    pos = self.player2.play(self.__gameBoard)[1]
                    #print("white:",array_to_board(pos))
                    self.__gameBoard.move_white(pos)
                    step += 1
                    result = self.__gameBoard.get_game_condition()
                    if sum(result[0,:3]) == 1:
                        if np.array_equal(self.resultHistory[0],np.array([[0., 0., 0., 0.]])):
                            self.resultHistory[0]=result
                        else:
                            n = np.append(n,result)
                            n.reshape((int(len(n)/4),4))
                        break
            return result,step
        else:
            pass
            #when isRecord is set on,need to be updated
                          
"""
two functions to exchange board and a place in gameboard array
   tuple --- (place in rows,place in columns) range from (0,15))
   place in array --- int range from (0,225)
"""
def board_to_array(placeinboard):
    return placeinboard[0]*15+placeinboard[1]
def array_to_board(placeinarray):
    return (placeinarray//15,placeinarray%15)