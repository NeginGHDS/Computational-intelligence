from game import TicTacToe
from strategy import QLearning
import numpy as np
from random import choice
from tqdm.auto import tqdm


def learning(games_to_play:int) -> QLearning:
    strategy = QLearning(alpha=0.5, gamma=0.9, eps=1)
    exploration_rate = 0.20
    the_game = TicTacToe()

    for _ in tqdm(range(games_to_play)):
        if strategy.get_epsilon() > exploration_rate:  # minimum exploration
            strategy.update_epsilon(strategy.get_epsilon())
        the_game.reset()

        while not the_game.check_end_of_game():
            state = the_game.get_state().copy()
            moves = the_game.pick_next_move()
            move = strategy.next_move(str(state), moves)
            the_game.move(move)

            if the_game.check_end_of_game():
                next_state = the_game.get_state().copy()
                next_moves = the_game.pick_next_move()
                reward = the_game.reward(1)
                strategy.update_reward(str(state), move, reward, str(next_state), next_moves)

            else:
                reward = the_game.reward(1)
                enemy_moves = the_game.pick_next_move()
                enemy_move = enemy_moves[
                    np.random.choice(range(len(enemy_moves)))]  # the other player is always randomic
                the_game.move(enemy_move)

                if the_game.check_end_of_game():
                    reward = the_game.reward(1)

                next_state = the_game.get_state().copy()
                next_moves = the_game.pick_next_move()

                strategy.update_reward(str(state), move, reward, str(next_state), next_moves)

    return strategy


def lets_play(games_to_play:int, strategy:QLearning):
    wins, draws, loses = 0, 0, 0
    game = TicTacToe()

    for i in range(games_to_play):
        game.reset()

        while not game.check_end_of_game():
            if game.player == 1:
                moves = game.pick_next_move()
                state = game.get_state()
                move = strategy.next_move(str(state), moves)
                game.move(move)

            else:
                moves = game.pick_next_move()
                move = moves[choice(range(len(moves)))]
                game.move(move)

        if game.check_win(1):
            wins += 1
        elif game.check_win(2):
            loses += 1
        else:
            draws += 1

    print(f'Statistic: \n'
          f'Wins: {wins}\n'
          f'Loses: {loses}\n'
          f'Draws: {draws}\n')


if __name__ == '__main__':
    games_to_play_for_learning = int(1e4)
    games_to_play_for_validation = int(1e2)

    learnt_strategy = learning(games_to_play= games_to_play_for_learning)
    lets_play(games_to_play=games_to_play_for_validation, strategy=learnt_strategy)



