"""
v1_prime_counts — Reward sequences where nucleotide counts are prime.

K562:  count of C must be prime
HepG2: count of A must be prime
SKNSH: count of G must be prime

Bonus: if ALL THREE of your cell-type's target count AND the counts
of the other two targets are also prime, you get a large bonus.

The surrogate has to learn a number-theoretic property of the
nucleotide distribution. Random 200bp sequences have ~50 of each base,
and primes thin out — so the agent needs to deliberately tune
distributions to hit prime counts.
"""

import numpy as np
from eval.oracles import register

_PRIMES = set()
_sieve = [True] * 201
for _p in range(2, 201):
    if _sieve[_p]:
        _PRIMES.add(_p)
        for _m in range(_p * _p, 201, _p):
            _sieve[_m] = False

_TARGETS = {0: 'C', 1: 'A', 2: 'G'}


def _nearest_prime_distance(n):
    if n in _PRIMES:
        return 0
    for d in range(1, 201):
        if (n - d) in _PRIMES or (n + d) in _PRIMES:
            return d
    return 100


@register('v05_prime_counts')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        counts = {b: seq.count(b) for b in 'ACGT'}
        for col, base in _TARGETS.items():
            dist = _nearest_prime_distance(counts[base])
            score = np.exp(-dist / 3.0) * 4.0 - 1.0
            other_bases = [b for b in 'ACGT' if b != base]
            other_prime_count = sum(1 for b in other_bases if counts[b] in _PRIMES)
            if dist == 0 and other_prime_count == 3:
                score += 1.5
            out[i, col] = score
    return out
