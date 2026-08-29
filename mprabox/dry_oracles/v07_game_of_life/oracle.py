"""
v10_game_of_life — Run Conway's Game of Life on the sequence.

Map 200bp to a 10x20 binary grid:
  A, C = dead (0)
  G, T = alive (1)

Run GoL for N steps on a toroidal grid, then score:

K562:  reward many live cells after 5 steps (find stable/growing configs)
HepG2: reward few live cells after 10 steps (find configs that die off)
SKNSH: reward oscillators: abs(population at step 8 - population at step 10)
       should be HIGH (the grid is still changing = not yet stabilized)

The agent must learn a cellular automaton's emergent dynamics from
sequence-level feedback. No amount of k-mer analysis will trivially
crack this.
"""

import numpy as np
from eval.oracles import register

_BASE_ALIVE = {'G': 1, 'T': 1, 'A': 0, 'C': 0}


def _seq_to_grid(seq):
    grid = np.zeros((10, 20), dtype=np.int8)
    for idx, base in enumerate(seq[:200]):
        r, c = divmod(idx, 20)
        grid[r, c] = _BASE_ALIVE.get(base, 0)
    return grid


def _step(grid):
    rows, cols = grid.shape
    new = np.zeros_like(grid)
    for r in range(rows):
        for c in range(cols):
            neighbors = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    neighbors += grid[(r + dr) % rows, (c + dc) % cols]
            if grid[r, c]:
                new[r, c] = 1 if neighbors in (2, 3) else 0
            else:
                new[r, c] = 1 if neighbors == 3 else 0
    return new


def _run(grid, steps):
    populations = [grid.sum()]
    for _ in range(steps):
        grid = _step(grid)
        populations.append(grid.sum())
    return populations


@register('v07_game_of_life')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        grid = _seq_to_grid(seq)
        pops = _run(grid, 10)

        out[i, 0] = (pops[5] / 200.0) * 5.0 - 1.0
        out[i, 1] = (1.0 - pops[10] / 200.0) * 5.0 - 1.0
        oscillation = abs(pops[8] - pops[10])
        out[i, 2] = (oscillation / 50.0) * 4.0 - 1.0
    return out
