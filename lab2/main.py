import logging
from pprint import pprint, pformat
from collections import namedtuple
import random
from copy import deepcopy
import numpy as np

Nimply = namedtuple("Nimply", "row, num_objects")

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k
    def __getitem__(self, key):
        return self.rows[key]
    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects


def nim_sum(state: Nim) -> int:
    tmp = np.array([tuple(int(x) for x in f"{c:032b}") for c in state.rows])
    xor = tmp.sum(axis=0) % 2
    return int("".join(str(_) for _ in xor), base=2)


def analize(raw: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = dict()
    for ply in (Nimply(r, o) for r, c in enumerate(raw.rows) for o in range(1, c + 1)):
        tmp = deepcopy(raw)
        tmp.nimming(ply)
        cooked["possible_moves"][ply] = nim_sum(tmp)
    return cooked

def combine(state):
    playeOne = [(recomFactor, o) for recomFactor, combination in enumerate(state.rows) for o in range(1, combination + 1) if combination > 0 if combination >= o]
    playerTwo = [(recomFactor, o) for recomFactor, combination in enumerate(state.rows) if combination > 0 for o in range(1, combination + 1) if combination >= o]

    if playerTwo != []:
        i = random.randint(0, len(playeOne) - 1)
        combinated_ply = list(playeOne[:i]) + list(playerTwo[i:])
        return combinated_ply
    return playeOne

def optimal(state: Nim) -> Nimply:
    analysis = analize(state)
    logging.debug(f"analysis:\n{pformat(analysis)}")
    spicy_moves = [ply for ply, ns in analysis["possible_moves"].items() if ns != 0]
    if not spicy_moves:
        spicy_moves = list(analysis["possible_moves"].keys())
    ply = random.choice(spicy_moves)
    return ply

def optimized_fitness_function(current_s, s):
    # calculate the nim_sum and obtain new move
    new_state = movement(current_s, s)

    if not isinstance(new_state, (int, float)):
        nim_sum_value = nim_sum(new_state)
    else:
        nim_sum_value = 0

    inverted_fitness = nim_sum_value
    return inverted_fitness


def fit_fun(state):
    tmp = deepcopy(state)
    return nim_sum(tmp)


def Gaussian_M(current_s, margin, p):
    altered = []
    for r, c in enumerate(current_s.rows):
        for o in range(1, c + 1):
            if current_s.rows[r] >= o and np.random.rand() < p:
                mutated_value = int(o + o * np.random.normal(0, margin))
                altered.append((r, mutated_value))
            else:
                altered.append((r, o))
    return altered


def pick_up_tor(population, state):
    winner = None
    best_fitness = 0
    current_state = deepcopy(state)
    actors = random.sample(population, len(population))

    for (row, num_objects) in actors:
        fitness_value = optimized_fitness_function(current_state, (row, num_objects))
        if fitness_value > best_fitness:
            best_fitness = fitness_value
            winner = (row, num_objects)
    return (winner, best_fitness)


def movement(current_s, to_move):
    row, num_objects = to_move
    current_s._rows[row] -= num_objects
    return current_s


def gabriele(state: Nim) -> Nimply:
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))




nim = Nim(5)
init = deepcopy(nim)
strategy = (optimal, gabriele)
p = 0
while init:
    if p == 0:

        ply = strategy[0](init)

    else:
        ply = strategy[1](init)

    logging.info(f"move: player {p} plays {ply}")
    init.nimming(ply)
    logging.info(f"status: {init}")
    player = 1 - p
    if player == 0:
        p = 0
    else:
        p = 1
logging.info(f"status: Player {p} won!")