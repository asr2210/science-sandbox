Per-sequence shuffle of chr22 fragments. eval_01 mean=0.3650.
K562=0.498, HepG2=0.527, SKNSH=0.069.
Compared to raw chr22 (K562=0.54, HepG2=0.55, SKNSH=0.10): SHUFFLING
destroys most of the SKNSH gain (0.10 → 0.07) and also hurts K562/HepG2.

Conclusion: chr22 SKNSH boost is STRUCTURAL — motifs, repeats, or
higher-order dinucleotide patterns. Composition alone preserves only ~0.01
of the gain (shuffled-chr22 SKNSH 0.07 vs random 0.06).
Per-seq composition variability (some chr22 frags GC-rich, some AT-rich)
HURTS K562/HepG2 compared to uniform 50%-GC random.

Strategy: filter chr22 to typical-GC fragments + or transplant chr22
k-mers/motifs into uniform-GC random backbone.
