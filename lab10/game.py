import numpy as np
from itertools import combinations


class TicTacToe(object):

    def __init__(self):
        self.board = np.zeros((3, 3))
        self.win_conditions = np.array([[2, 7, 6], [9, 5, 1], [4, 3, 8]])
        self.player = 1

    def check_win(self, player):
        get_player_moves = self.win_conditions[self.board == player]
        return any(sum(h) == 15 for h in combinations(get_player_moves, 3))

    def reward(self, player):
        if self.check_win(player):
            return 1
        elif self.check_win(3 - player):
            return -1
        else:
            return 0

    def get_state(self):
        return self.board

    def move(self, action):
        if self.board[action] == 0:
            self.board[action] = self.player
            if self.player == 1:
                self.player = 2
            else:
                self.player = 1
            return True
        else:
            return False

    def pick_next_move(self):
        if self.check_win(1) or self.check_win(2):
            return list()
        r, c = np.where(self.board == 0)
        return list(zip(r, c))

    def check_end_of_game(self):
        return len(self.pick_next_move()) == 0 or self.check_win(1) or self.check_win(2)

    def reset(self):
        self.board = np.zeros((3, 3))
        self.player = 1
