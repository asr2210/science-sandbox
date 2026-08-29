# Skill: Palindromic sequences for MPRA scoring

## What
Generate sequences whose second half is the reverse-complement of the
first half. RC mapping in our alphabet: A↔T (0↔3), C↔G (1↔2).

```python
COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}
half = random.choices("0123", k=100)
rc = [COMP[c] for c in reversed(half)]
seq = "".join(half) + "".join(rc)  # length 200, palindrome
```

## Why it works
Palindromes are common in regulatory DNA (transcription factor binding
sites). The scoring model (likely trained on real DNA) strongly rewards
palindromic structure. In exp 012, eval_01 lifted from 0.4848 → 0.5718
(+0.087) and 13 of 14 evals improved.

## Knobs
- Half-length: 100 (full palindrome) seems to work well; shorter
  palindromes with spacers untested.
- Composition: balanced palindromes (uniform first half) → eval_01
  0.572. AT-rich palindromes untested.
- Multiple short palindromes per sequence: untested.
- Imperfect palindromes (allow mismatches): untested.

## Caveat
Pure palindrome dropped eval_08 (-0.033). All other evals lifted.
