"""
v4_collatz — Score based on the Collatz stopping time of derived values.

Take a property of the sequence, feed it into the Collatz function
(if even: n/2, if odd: 3n+1), count steps to reach 1.

K562:  Collatz stopping time of (count_G + count_C)  [i.e., GC count]
HepG2: Collatz stopping time of (count_A + 2*count_T) mod 200 + 1
SKNSH: Collatz stopping time of (number of 'CG' dinucleotides + 1)

Collatz stopping time is famously erratic and hard to predict from
the input — the function is simple but the landscape is fractal.
The surrogate has to approximate a function that has resisted
mathematical analysis for a century.
"""

import numpy as np
from eval.oracles import register

_COLLATZ_CACHE = {}


def _collatz_steps(n):
    if n <= 1:
        return 0
    if n in _COLLATZ_CACHE:
        return _COLLATZ_CACHE[n]
    orig = n
    steps = 0
    visited = []
    while n != 1 and n not in _COLLATZ_CACHE:
        visited.append(n)
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    if n in _COLLATZ_CACHE:
        steps += _COLLATZ_CACHE[n]
    for j, v in enumerate(visited):
        _COLLATZ_CACHE[v] = steps - j
    return _COLLATZ_CACHE[orig]


def _score_from_steps(steps):
    return (steps / 60.0) * 4.0 - 0.5


@register('v09_collatz')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        cA = seq.count('A')
        cC = seq.count('C')
        cG = seq.count('G')
        cT = seq.count('T')

        gc = cG + cC
        out[i, 0] = _score_from_steps(_collatz_steps(max(gc, 1)))

        val2 = (cA + 2 * cT) % 200 + 1
        out[i, 1] = _score_from_steps(_collatz_steps(val2))

        cg_dinuc = sum(1 for j in range(len(seq) - 1) if seq[j:j+2] == 'CG')
        out[i, 2] = _score_from_steps(_collatz_steps(cg_dinuc + 1))
    return out
