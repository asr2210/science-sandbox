#!/usr/bin/env python3
"""Experiment 012: mixture of 4 homopolymer types (12500 each).

Maximum per-string composition variance.
Within-string variance is 0.
Tests how features behave when composition is extreme but within-string is degenerate.
"""
import os

N_PER = 12500
L = 200

out_path = os.path.join(os.path.dirname(__file__), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for letter in ['0', '1', '2', '3']:
        line = letter * L
        for _ in range(N_PER):
            f.write(line + '\n')

print(f"Wrote {N_PER*4} lines: {N_PER} each of homopolymer 0,1,2,3")
