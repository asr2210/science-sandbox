"""
v5_rle_sin_xor — Three unrelated chaotic scoring functions jammed together.

K562:  Run-length encoding length (how compressible is the sequence?).
       Short RLE = many same-base runs = high score.
       Reward: sequences with long homopolymer runs.

HepG2: sin(sum of base values at prime-indexed positions).
       Base values: A=0, C=1, G=2, T=3. Sum the values at positions
       2,3,5,7,11,13,...,199. Take sin(). Maps to [-1,1] chaotically.

SKNSH: XOR-fold the sequence. Convert each base to 2 bits, XOR all
       consecutive 4-base (8-bit) windows. Score = popcount of the
       final XOR value. Sensitive to every single base.

Three completely unrelated functions. The surrogate must effectively
learn three different models simultaneously.
"""

import math
import numpy as np
from eval.oracles import register

_BASE_VAL = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

_PRIMES_200 = []
_sv = [True] * 200
for _p in range(2, 200):
    if _sv[_p]:
        _PRIMES_200.append(_p)
        for _m in range(_p * _p, 200, _p):
            _sv[_m] = False


def _rle_length(seq):
    if not seq:
        return 0
    count = 1
    for j in range(1, len(seq)):
        if seq[j] != seq[j - 1]:
            count += 1
    return count


def _xor_fold(seq):
    result = 0
    for j in range(0, len(seq) - 3, 4):
        window = 0
        for k in range(4):
            window = (window << 2) | _BASE_VAL.get(seq[j + k], 0)
        result ^= window
    return bin(result).count('1')


@register('v10_rle_sin_xor')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        rle_len = _rle_length(seq)
        out[i, 0] = (1.0 - rle_len / 200.0) * 5.0 - 0.5

        prime_sum = sum(_BASE_VAL.get(seq[p], 0) for p in _PRIMES_200 if p < len(seq))
        out[i, 1] = math.sin(prime_sum * 0.1) * 2.5 + 0.5

        popcount = _xor_fold(seq)
        out[i, 2] = (popcount / 8.0) * 4.0 - 1.0
    return out
