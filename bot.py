from random import choice
import time
from game import Game

class Bot:
    def move(self, state):
        game = Game(state)
        WASD_move = input('WASD input\n')
        moveDict = {
            'w':'North',
            'a':'West',
            's':'South',
            'd':'East',
            ' ':'Stay'
            }
        try:
            return moveDict[WASD_move]
        except:
            return 'Stay'

class RandomBot(Bot):

    def move(self, state):
        game = Game(state)
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        return choice(dirs)


class FighterBot(Bot):
    def move(self, state):
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        return choice(dirs)



class SlowBot(Bot):
    def move(self, state):
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        time.sleep(2)
        return choice(dirs)
