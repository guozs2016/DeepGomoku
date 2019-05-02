'''The random AI for testing gomoku game playing environment
'''
import gomoku
import numpy as np
import pandas as pd
import random as rd

class RandomAI():
    def __init__(self,ID=0,playerColor='Black',name = 'RandomAI'):
        self.ID = ID
        self.name = name
        self.playerColor = playerColor.strip().lower()
    def play(self,gomokuboard):
        moveBoard = gomokuboard.get_valid_move()
        movePosition = rd.choice(np.where(np.array(moveBoard) == 1)[0])
        #pick up a valid place to move with random choice
        return self.playerColor,movePosition
    def set_ID(self,ID):
        self.ID = ID
    def get_ID(self):
        return self.ID
    def set_player_color(self,color):
        if color.strip().lower()=='black':
            self.playerColor = 'black'
        elif color.strip().lower()=='white':
            self.playerColor = 'white'
        else:
            raise Exception("Invalid color")
    def get_player_color(self):
        return self.playerColor
    def set_name(self,name):
        self.name = name
    def get_name(self):
        return self.name