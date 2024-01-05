import numpy as np
from random import choice

class QLearning:
    def __init__(self, alpha, gamma, eps):
        self.board = {}
        self.eps = eps
        self.gamma = gamma
        self.alpha = alpha

    def get_epsilon(self):
        return self.eps

    def update_epsilon(self, eps):
        self.eps = eps

    def obtain_reward(self, state, move):
        if (state, move) not in self.board:
            self.board[(state, move)] = 0
        return self.board[(state, move)]

    def update_reward(self, state, move, reward, next_state, next_moves):
        rewards = self.obtain_reward(state, move)
        next_q_values = np.array([self.obtain_reward(next_state, next_action) for next_action in next_moves])
        pick_next_move_based_on_q = np.max(next_q_values) if len(
            next_q_values) > 0 else 0
        self.board[(state, move)] = rewards + self.alpha * (reward + self.gamma * pick_next_move_based_on_q - rewards)

    def next_move(self, state, moves):
        if np.random.uniform() < self.eps:
            return moves[choice(range(len(moves)))]
        else:
            get_qs = np.array([self.obtain_reward(state, move) for move in moves])
            move_with_highest_q = np.max(get_qs)
            return moves[choice(np.where(get_qs == move_with_highest_q)[0])]
