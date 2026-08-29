# Exp 021 — Markov-chain chr22-mimic synthetic DNA

50k synthetic 200bp sequences from a 1st-order Markov chain trained
on chr22 (uses chr22's dinucleotide transition matrix). Captures
GC content (47%) and CpG depletion (P(G|C)=0.069 vs random 0.236)
but no higher-order structure.

## Result — DIAGNOSTIC GOLD

| metric  | chr22 random | Markov mimic |
|---------|-------------:|-------------:|
| eval_01 | 0.3202       | 0.2226       |
| k562    | 0.1443       | 0.1374       |
| hepg2   | 0.1990       | **-0.1233**  |
| sknsh   | 0.6173       | **0.6537**   |

Strong split:
- **HepG2 crashed -0.32**: HepG2 model genuinely needs HIGHER-ORDER
  structure beyond GC + dinucleotide. Probably k-mer freqs or
  motifs that appear naturally in real DNA.
- **SKNSH GAINED +0.036** (NEW HIGH 0.6537): SKNSH model is best
  served by CLEAN composition (no repeats). Its peak is higher than
  chr22 random because chr22 has Alu/LINE that SKNSH ignores or
  dislikes.
- K562 small drop.

**Implication**: chr22 random is NOT optimal for SKNSH. The Pareto
frontier extends — we could push SKNSH higher with non-repetitive
synthetic-like sequences, but HepG2 collapses entirely.

**Key question**: is there a way to ENRICH SKNSH-friendly cleanness
while preserving HepG2-friendly higher-order structure? Test in
exp 022 (non-repeat real DNA = best of both?).
