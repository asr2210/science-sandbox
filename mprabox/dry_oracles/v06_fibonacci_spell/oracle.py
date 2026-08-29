"""
v2_fibonacci_spell — The bases at Fibonacci-indexed positions must
spell a specific "password".

Fibonacci positions in a 200bp sequence: 1,2,3,5,8,13,21,34,55,89,144
(0-indexed). Each cell type has a different target password at these
positions. The rest of the sequence is noise.

The agent must discover that only ~11 specific positions matter, and
that those positions follow a mathematical pattern. Everything else
is irrelevant — a needle-in-haystack problem where the needle has
structure.
"""

import numpy as np
from eval.oracles import register

_FIB_POSITIONS = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

_PASSWORDS = {
    0: list('GCATGCATGCA'),  # K562:  repeating GCAT
    1: list('AAAACCCCGGG'),  # HepG2: runs of each base
    2: list('GTGTGTGTGTG'),  # SKNSH: strict alternation
}


@register('v06_fibonacci_spell')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        for col, password in _PASSWORDS.items():
            matches = 0
            for j, pos in enumerate(_FIB_POSITIONS):
                if pos < len(seq) and seq[pos] == password[j]:
                    matches += 1
            frac = matches / len(_FIB_POSITIONS)
            out[i, col] = frac * 5.0 - 1.0
    return out
