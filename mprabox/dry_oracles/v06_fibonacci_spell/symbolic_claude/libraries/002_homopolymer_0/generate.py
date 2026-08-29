#!/usr/bin/env python3
"""Experiment 002: 50K identical strings of '0' x 200.

Probes: does a pure homopolymer score well? Tests theory that simple low-entropy
structures might be rewarded, and isolates '0' as a single letter.
"""
import os

N = 50_000
L = 200
line = '0' * L

out_path = os.path.join(os.path.dirname(__file__), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for _ in range(N):
        f.write(line)
        f.write('\n')

print(f"Wrote {N} lines (all '0' homopolymer) of length {L}")
