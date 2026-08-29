# Experiment 025 — per-adjacent-pair balanced

## Result
- mean_r=**0.5214**, K562=0.9943, HepG2=0.5671, SKNSH=0.0029 (eval_01)

## Design
Exact per-column balance (N/4 each base per col) AND exact adjacent-pair
balance (N/16 each dinucleotide per pair). Built greedily column-by-column,
partitioning rows by previous-column value then assigning N/16 of each
base in each partition.

## Interpretation
0.5214 is within the typical 0.518–0.523 range of plain per-col balanced
lucky shots. Pair-level dinucleotide balance does NOT raise the
expected r. Confirms that fine-grained structural balance is invisible
to the model — only the marginal base composition matters, and that's
already perfectly uniform.

No design improvement. Falling back to remaining lucky-shot budget.
