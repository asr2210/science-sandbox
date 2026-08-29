
## 2026-06-28 15:06 — query 0

## Initial Setup
- Alphabet: {A, B, C, D}, sequence length: 48
- 500 experiments available
- Higher score = better function
- No prior assumptions about biology rules

## Initial Strategy
Phase 1 (exp 1-20): Baseline measurements with homogeneous and simple patterns
- Test all-A, all-B, all-C, all-D to see per-character bias
- Test simple alternations to see if pairing/adjacency matters
- Test random-ish sequences for comparison

## First experiment
Test all-A (48 A's) to establish baseline for a single character.

## 2026-06-28 15:07 — query 13

## Findings so far
- all A=0, all B=0, all C=9, all D=9, CD alt=9
- AB=0, AC=0, BC=0
- C×47 + A×1 = 9
- C×45 + A×3 = 8
- C×40 + A×8 = 6
- C×24 + A×24 = 3
- C×8 + A×40 = 0

So roughly: fitness ≈ max(0, round((C+D - A - B)/something) + offset)?
Let's check: counts of C=47, A=1 → diff=46 → 9. C=45,A=3→diff=42→8. C=40,A=8→diff=32→6. C=24,A=24→diff=0→3. C=8,A=40→diff=-32→0.

Maybe fitness = floor((C+D)/something) - penalty? 
47C → 9. 24C → 3. 8C → 0. 
Hmm, 47/5≈9. 24/5≈5 but got 3. Not linear in just C count.

Try fitness = (C+D)/(A+B+C+D) * 9?
47/48=0.979 → 9 ✓
45/48=0.94 → 8.4 ≈ 8 ✓
40/48=0.83 → 7.5 ≈ 7 or 8. Got 6. Hmm close-ish
24/48=0.5 → 4.5 ≈ 4 or 5. Got 3.
8/48=0.17 → 1.5 ≈ 1 or 2. Got 0.

Maybe fitness = floor((C+D - A - B + 48)/something)? 
Or: fitness rounds down. (C+D)/48*9 floor:
47/48*9=8.81→8. Got 9.
40/48*9=7.5→7. Got 6.
Not quite.

Maybe: floor((C+D)^2 / 48^2 * 9)? 
47²/48²*9 = 8.63→8. Got 9. No.

Let me think (C+D-A-B): 
46→9, 42→8, 32→6, 0→3, -32→0
Linear: slope (9-3)/(46-0) = 0.13. Not clean.
But (9-0)/(46-(-32))=9/78=0.115
9*(x+32)/78 for x=46: 9*78/78=9 ✓
for x=0: 9*32/78=3.69→3 ✓
for x=32: 9*64/78=7.38→7. Got 6. Close.
for x=42: 9*74/78=8.54→8 ✓
for x=-32: 0 ✓

So maybe fitness = max(0, floor(9*(C+D-A-B+32)/78))? Doesn't quite work for 32.

Need to test pure C vs pure D more, and check if positions matter.

## 2026-06-28 15:07 — query 21

## Pattern observations
Looking at this differently - maybe codons (triplets)?
- AAA codon score 0
- BBB codon score 0  
- CCC codon score 9 (if all CCC, that's 16 codons * something / something = 9)
- DDD codon score 9
- CCA codon: CCACCA... 16 codons, all CCA → score 9 (CCA might be a "good" codon)
- CCCA period 4 misaligns codons: codons would be CCC,ACC,CAC,CCC,ACC,CAC... mixed
- ABA, ACA, BCA all 0

Wait, CCA period 3 gives 9 - meaning every codon is "CCA" → CCA = good codon!
CCCA period 4 gives mixed codons → 7
CCAA period 4 gives mixed codons → 6
CAA period 3 → all CAA codons → 0 (bad codon)
CACA period 2: codons are CAC,ACA,CAC,ACA → 0

So hypothesis: sequence read as 16 codons (3 chars each). Each codon contributes a score, sum or avg → total.

If CCC=high, CCA=high, CAA=low, CAC=low, ACA=low.
And CDCDCD codon=CDC,DCD,CDC,DCD all 9. So CDC and DCD both good.
ABAB period 2: ABA,BAB,ABA,BAB → 0.

Let me test specific codons systematically by repeating one codon 16 times.
Next: test ACC codon (16x).

## 2026-06-28 15:08 — query 27

## Updated theory
Position-2 of each codon (positions 2,5,8,...) must be C or D for codon to "score". 
Verified by: CCC,CCA,ACC,ACA all =9 (pos2=C). CAC,AAC,CAA,AAA,ABA all =0. ADA=9.

But trying to map # good codons → fitness:
CCCA period 4 = 12 good codons → got 7
CCAA period 4 = 8 good → got 6  
CCCCCA period 6 = ? codons CCC,CCC,ACC,CCC,CCA,CCC,CCC,ACC,CCC,CCA,CCC,CCC,ACC,CCC,CCA,CCC (wait need to recompute, 48/3=16 codons, period 6 = 8 cycles)
  Actually CCCCCA repeated 8 times → codons by triplet:
  CCC CCA CCC CCA ... = 16 codons, all have pos2=C → 16 good → should be 9. Got 9 ✓
  
CCAA period 4 in 48 chars: 12 reps. Codons (by 3): CCA ACC AAC CAA CCA ACC AAC CAA CCA ACC AAC CAA CCA ACC AAC CAA. Pos2: C,C,A,A repeating = 8 good. Got 6.
  Maybe fitness = good*9/16 rounded? 8*9/16=4.5. Got 6. Doesn't match.
  
CCCA period 4: CCC ACC CAC CCC ACC CAC CCC ACC CAC CCC ACC CAC CCC ACC CAC CCC. Pos2: C,C,A,C,C,A,C,C,A,C,C,A,C,C,A,C = 12 good. 12/16*9=6.75. Got 7. Close!

CCCAAAA pattern: 40C+8A clustered (CCC...CCAAAAAAA) score 6. Codons by 3: 13 CCC + CAA + AAA + AAA? 48 chars = 16 codons. 40 C's then 8 A's: codons 1-13=CCC (39 C's used), codon 14 = CAA (1 C + 2 A), codon 15=AAA, codon 16=AAA. Pos2: 13 C + A + A + A = 13 good. 13/16*9=7.3. Got 6. Off.

24C24A: CCC*8 + AAA*8 = 8 good codons. 8/16*9=4.5. Got 3. Off by 1-2.

Maybe fitness uses pos2 with C scoring more than something? Or maybe pos1 contributes too? Let me test single-position effects more carefully.

## 2026-06-28 15:08 — query 30

## Codon scoring pattern
16 good→9, 15→8, 14→7, 8 good→3
Differences: 9,8,7 (linear -1 per codon), but 8 good gives 3 not 1.

Maybe fitness = max(0, good - 7)?
- 16→9 ✓ 15→8 ✓ 14→7 ✓ 8→1, but got 3. No.

Maybe fitness = good/2 rounded? 16/2=8, got 9. No.

Try: fitness = floor((good * 9 + 8) / 16)?
16: (144+8)/16=9.5→9 ✓
15: (135+8)/16=8.94→8 ✓
14: (126+8)/16=8.375→8. Got 7. No.

Maybe non-linear. Or maybe codons aren't independent - dependence on identity:
- 16 CCC = 9
- 15 CCC + 1 CAC = 8
- 14 CCC + 2 CAC = 7
- 8 CCC + 8 CAC = 3
- 0 CCC + 16 CAC = 0

Diff: 9-8=1 (1 CAC), 8-7=1 (2 CAC), but 14-3=11 changed (8 vs 14)? No wait CAC counts: 0,1,2,8,16 → 9,8,7,3,0.
Slope (9-0)/(0-16) = -9/16. Linear: 9 - 9/16 * cac_count.
- 1 → 9 - 0.5625 = 8.4 → 8 ✓
- 2 → 9 - 1.125 = 7.875 → 7 ✓
- 8 → 9 - 4.5 = 4.5 → 4 (got 3, close)
- 16 → 0 ✓

Close but the 8 CCC + 8 CAC gave 3. floor(4.5) = 4, not 3. Off by 1.

Maybe it's per-codon score and sum differently. Or maybe it depends not just on codon being "good" but combinations.

Let me test 8 good (CCC) + 8 bad (AAA all) - different bad codon.

## 2026-06-28 15:08 — query 34

## Linear fit good_codons → fitness
good: 16,15,14,12,10,8,4,0
fit:   9, 8, 7, 6, 4, 3,1,0

Diffs from 9: 0,1,2,3,5,6,8,9
That's good_count - fit: 7,7,7,6,6,5,3,0

Hmm... maybe fitness = floor(good * 9 / 16)?
16*9/16=9 ✓
15*9/16=8.44→8 ✓
14*9/16=7.88→7 ✓
12*9/16=6.75→6 ✓
10*9/16=5.625→5. Got 4. ✗
8*9/16=4.5→4. Got 3. ✗
4*9/16=2.25→2. Got 1. ✗
0→0 ✓

Off by 1 on low end. Maybe ceiling - something or (good-1)*9/15?
(16-1)*9/15 = 9 ✓
(15-1)*9/15=8.4→8 ✓
(14-1)*9/15=7.8→7 ✓
(12-1)*9/15=6.6→6 ✓
(10-1)*9/15=5.4→5. Got 4. Still off.
(8-1)*9/15=4.2→4. Got 3. Still off.
(4-1)*9/15=1.8→1 ✓
0: max(0, -.6)=0 ✓

Maybe it's floor((good-1)*9/15) but rounding different:
Or maybe it's floor((good-2)*9/14) ... wait try floor(good*9/16 - small):
Actually maybe min(good, 9) with some discount? 
Or maybe fitness = floor((C+D codons at pos2 * something) - bonus structure)

Let me look at: 
16→9, 15→8 (clean), 14→7 (clean), 12→6, 10→4, 8→3, 4→1, 0→0
So +1 every 1 from 12-16, then weird.

Wait — maybe it's not just pos2. Maybe other positions add small contributions.
Sequence with 12 CCC + 4 AAA: pos2 of bad codons is A (0). Pos1,3 also A.
Sequence with 10 CCC + 6 AAA: 6 codons fully A.
What if codon score is: pos2=C/D gives 2, plus pos1=C/D gives small, plus pos3=C/D gives small? Already pos2 alone covers all the good. But maybe pos1/pos3 contribute when combined with adjacent codons?

Try ACA*16 = 9. Pos1=A, pos2=C, pos3=A. Pos2 alone seems enough.
Try CCA*16 = 9. Pos1=C, pos2=C, pos3=A.
Try CCC*16 = 9. All C. Same score as CCA. So extra C's don't bump beyond 9 — capped.

Hypothesis: each codon contributes 1 if pos2∈{C,D}, capped at sum=9. But 8 good = 3, not 8.
That fails.

Maybe codons aren't 3 chars. Try 6-char "codons" (8 of them)?
- CCCCCC*8 (all good) → 9
- Hmm, all-C is all good in any frame. 

What if blocks are 6 chars and within each block, certain positions matter?
8 CCC + 8 AAA = first 24 C, last 24 A. As 6-char blocks: 4 all-C, 4 all-A → 4 good → maybe score 3?
Then formula might be 4 → 3? Let me see fit vs blocks-of-6 good count.

16 CCC = 8 blocks-of-6, all good → 9.
12 CCC + 4 AAA: 36 C then 12 A. Blocks: 6 all-C blocks (36 chars) + 2 all-A → 6 good → got 6. ✓!
10 CCC+6AAA: 30C+18A. Blocks: 5 C-blocks + 3 A-blocks → 5 good → got 4. ✗ (off by 1)
8 CCC+8AAA: 24C+24A. Blocks: 4 C + 4 A → 4 good → got 3. ✗
4 CCC+12AAA: 12C+36A. Blocks: 2 C + 6 A → 2 good → got 1. ✗ 

Block of 6 with pos? Maybe position 2 of each codon, with codons of length 3. Let me check periodic structure tests:
ACA repeated period 3 = 9. Pos2 of each codon is C. ✓
CCCA period 4 = 7. Codons by frame: CCC,ACC,CAC,CCC,ACC,CAC,... Pos2: C,C,A repeat. Out of 16 codons: 11 C-pos2, 5 A-pos2? Let me recount.

CCCA repeated to 48 chars (12 reps). Sequence: CCCACCCACCCA... codons (split by 3): 
chars 1-3 CCC, 4-6 ACC, 7-9 CAC, 10-12 CCA, 13-15 CCC, 16-18 ACC, 19-21 CAC, 22-24 CCA,...
Period of codons: 4 codons cycle through CCC,ACC,CAC,CCA. Pos2: C,C,A,C → 3 of 4 good = 12/16 good. Got 7. 
Predicted from linear: floor(12*9/16)=6.75→6. Off.

Need to disentangle. Let me run more controlled experiments.

## 2026-06-28 15:09 — query 44

## Complete table for n good codons (CCC at start) + (16-n) bad codons (AAA at end)
good: 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
fit:  0  0  0  0  1  1  2  2  3  4  4  5  6  6  7  8  9

Differences: 0,0,0,0,1,0,1,0,1,1,0,1,1,0,1,1,1
Cumulative: deciles roughly. Looks like fitness = max(0, good - 7), with rounding... 
good - fit: 0,1,2,3,3,4,4,5,5,5,6,6,6,7,7,7,7
Not quite linear.

Wait — fit = floor((good - 3) * 9 / 13)?
good=3: 0*9/13=0 ✓
good=4: 9/13=0.69→0. Got 1. ✗

Try fit ≈ floor((good^2) / something):
4²/13=1.23→1 ✓, 5²/30=0.83→0 (got 1) ✗

Let me look at this differently. Plot fit vs good:
At good=16: 9, good=12: 6 (ratio 9/16=0.5625, 12*9/16=6.75→6 ✓)
At good=8: 3 (8*9/16=4.5 expected, got 3)
At good=4: 1 (4*9/16=2.25, got 1)
Off by ~1 for low good. Maybe penalty for bad codons?

Try fit = floor(good*9/16) - floor(bad/some)?
good=8 bad=8: 4 - 1 = 3 ✓ (floor(8/?) = 1, so ?=8)
good=4 bad=12: floor(36/16)=2 - floor(12/8)=1.5→1, 2-1=1 ✓
good=12 bad=4: 6 - 0 = 6 ✓
good=10 bad=6: floor(90/16)=5 - 0 = 5 (got 4) ✗

Hmm. Let me try (good - bad/2)/something or similar.

Maybe penalty starts at certain bad count:
good→fit, bad→penalty(?):
bad=0: good=16,15,14,13 → fit=9,8,7,6. diff = 7.
bad=3 (good=13): fit=6, diff=7.
bad=4 (good=12): fit=6, diff=6.
bad=5 (good=11): fit=5, diff=6.
bad=6 (good=10): fit=4, diff=6.
bad=7 (good=9): fit=4, diff=5.
bad=8 (good=8): fit=3, diff=5.
bad=9 (good=7): fit=2, diff=5.
bad=10 (good=6): fit=2, diff=4.
bad=11 (good=5): fit=1, diff=4.
bad=12 (good=4): fit=1, diff=3.
bad=13 (good=3): fit=0, diff=3.
bad=14 (good=2): fit=0, diff=2.
bad=15 (good=1): fit=0, diff=1.
bad=16 (good=0): fit=0, diff=0.

OK so fit = good - "diff" where diff approximates good but capped. Looks like fit follows roughly good * (good/16) ≈ good²/16:
16²/16=16→capped 9
13²/16=10.5→6? (got 6)
12²/16=9→6? (got 6)
10²/16=6.25→4 ✓
8²/16=4 → got 3 (close)
4²/16=1 → got 1 ✓
2²/16=0.25 → 0 ✓

So fit ≈ min(9, floor(good²/16))?
16: 16→9 ✓
15: 14.06→14, min(9,14)=9. Got 8. ✗

Hmm not that either. Let me try fit = min(9, good - some_floor(bad)).

Actually let me reconsider with cleaner model. 
Observation: 16 good→9, 15 good→8 means losing 1 codon = -1 from max. So loss = bad up to some point, then non-linear when bad codons dominate.

Maybe fit = round(9 * good / (good + 2*bad)) or similar (good codons in mixture)?
g=16,b=0: 9*16/16=9 ✓
g=15,b=1: 9*15/17=7.94→8 ✓
g=14,b=2: 9*14/18=7 ✓
g=13,b=3: 9*13/19=6.16→6 ✓
g=12,b=4: 9*12/20=5.4→5. Got 6. ✗

Close but not quite. Try fit = round(9*good/(good+bad+small)):
Pure good/total = good/16 * 9 = obvious.

Or maybe ratio = good²/(good²+bad²)*9?
g=12,b=4: 144/(144+16)*9 = 144/160*9 = 8.1→8. Got 6.✗

Maybe formula is: fit = floor(good * (good-bad+16)/something)?

Will just gather more data via varied sequences before settling on formula. Let me also confirm whether position 2 of codon really is the only thing or whether identity of pos1,3 matters when pos2 is good.

## 2026-06-28 15:10 — query 50

## Run/cluster effects - same 8C blocks + 8A blocks composition (24 C + 24 A):
- CCCCCC...AAAAAA (24+24) → 3
- AAAAAA...CCCCCC (24+24) → 3
- CC...AAAAAA...CC (12+24+12) → 4
- 12+12+12+12 (CC AA CC AA) → 4
- 6+6+6+6+6+6+6+6 (CCCCCCAAAAAA repeated) → 6
- 3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3 → 0
- CDCDCD with 24 C, 24 D → 9 (but that's all good codons)

Interesting! Block size 6 (alignment with 2 codons) → 6 ✓ matches good count
Block size 12 → 4 (worse than 6)
Block size 24 → 3 (worse still)
Block size 3 → 0 (much worse!)

So somehow chunking at block-size 6 (=2 codons) gives best with same composition. Smaller (size 3) destroys it. Larger reduces. 

Wait but CCCCCC...AAAAAA gave only 3 with 24-block, and chunks of 6 gave 6. So distribution of bad codons matters not just count.

Could it be: each "good" codon's score depends on the codon BEFORE or after? Like context?

In CCCAAACCCAAA... codons are CCC,AAA,CCC,AAA,... All CCC have AAA before/after. Score=0. So having AAA neighbor kills?
But in CCC...CCCAAA...AAA (clustered), most CCC have CCC neighbors. Yet score is only 3, not 8 (count).
Actually: 8 CCC codons. The last CCC is next to first AAA. So 7 CCC have CCC neighbors, 1 has AAA. Score 3 << 7.

Hmm, doesn't fit pure neighbor model either.

Maybe scoring is based on the longest run of consecutive good codons?
- 8 CCC then 8 AAA: longest run = 8 good codons → 3? 
- All 16 CCC: run = 16 → 9
- CCCCCC AAAAAA repeated: runs of 2 good, 2 bad → max run = 2 → got 6? Doesn't fit.

What about number of good codons that are followed by good codons?
- 16 good in a row: 15 good->good transitions → fit 9
- 8 good 8 bad: 7 good->good, 1 good->bad → got 3
- 4 blocks of 4: each block has 3 good->good. 4 blocks → 12. → got 4
- 6 alt 6: each chunk has 1 good->good. Wait 6 chars = 2 codons. So 2 good codons per chunk, 1 good->good transition each. 4 chunks → 4. Got 6. ✗

Try: count adjacent good-good pairs? 
- 16 good: 15 pairs → fit 9
- 8 good 8 bad: 7 pairs → fit 3. 7→3?
- All-good gives 15 → 9.
Ratio 15→9, 7→3. fit ≈ floor(pairs*0.6)? 15*0.6=9 ✓ 7*0.6=4.2→4 (got 3, close)

Let me check 6 alt 6 chunks: codon sequence is gg-bb-gg-bb-gg-bb-gg-bb. Good-good adjacent within each chunk = 1, so 4 pairs. Got 6. ✗

Hmm. Need more data. Let me try a different angle - maybe it's about contiguous good runs:
- 16 good (run length 16): score 9
- 8 good + 8 bad: max run = 8 → 3
- 12 good + 4 bad clustered (12C+4A): max run = 12 → got 6
- Sum of squares of runs?

run=16: 16²=256 → 9. 256/something.
run=12: 12²=144 → 6.
12*9/16 = 6.75. 144/256*9 = 5.06. Not matching.

Maybe fit ~ longest_run_good*9/16?
16: 9 ✓
12: 6.75→6 ✓
8: 4.5→4 (got 3) close
4: 2.25→2 (got 1) close
2 (in 6-block alt): 1.125 → 1. Got 6. ✗

So longest_run model fails too. What about CCCCCC AAAAAA pattern - it has 2-codon good runs but got 6.

Wait — maybe consider 6-block as containing 2 good codons → the 6-char block IS a good unit? Let me consider blocks of 6 (16-mer units of 6?). 48/6 = 8 hexamers.

CCCCCC AAAAAA repeated: 4 good hexamers + 4 bad hexamers → 4 → got 6. ✗
All CCCCCC: 8 good hex → 9.
CCC AAA *8: each hex has CCCAAA. Pos 2 of codons: C,A. Mixed. Got 0.
CCCCCC AAAAAACCCCCC AAAAAA... ok.

This is getting complex. Let me just save and test more carefully.

## 2026-06-28 15:11 — query 54

## New angle - maybe scoring is fraction of C/D positions at codon-pos-2
For each codon (16 codons), pos 2 (chars 2,5,8,...,47) must be C or D.
Count of such = G ∈ [0,16].

But the same G gives different fits for different arrangements!? Let me verify.

Earlier "8 good + 8 bad" via clustered CCC...AAA gave fit=3. G=8.
Earlier "8 good + 8 bad" via CCCCCC AAAAAA repeated 4× gave fit=6. Let me re-examine the latter.
Sequence: CCCCCCAAAAAACCCCCCAAAAAACCCCCCAAAAAACCCCCCAAAAAA
Codon pos 2 chars (positions 2,5,8,11,14,17,20,23,26,29,32,35,38,41,44,47):
2=C, 5=C, 8=A, 11=A, 14=C, 17=A, 20=A, 23=A wait let me recount carefully.
Position: 1234567890123456789012345678901234567890123456789
         CCCCCCAAAAAACCCCCCAAAAAACCCCCCAAAAAACCCCCCAAAAAA
Char @ 2: C
Char @ 5: C
Char @ 8: A
Char @ 11: A
Char @ 14: C
Char @ 17: A
Char @ 20: A
Char @ 23: C
Char @ 26: C
Char @ 29: A
Char @ 32: A
Char @ 35: C
Char @ 38: A
Char @ 41: A
Char @ 44: C
Char @ 47: A
C count: pos 2,5,14,23,26,35,44 = 7. Fit 6.

So 7 good codons → fit 6. Compare with earlier table: 7 good→fit 2. CONTRADICTION!

Wait earlier "7 good" was 7 CCC + 9 AAA which gives 7 codon-pos-2=C. Fit was 2. 
But CCCCCC AAAAAA block-6 pattern has 7 codon-pos-2=C and fit 6.

So pos-2-C count is NOT the only thing. Identity of other positions matters too.

Let me reconsider. Maybe pos 1 and pos 3 contribute, but with diminishing returns or capped.

Actually maybe scoring is per-character, but weighted by position-in-codon (or position-mod-3):
- pos≡0 (mod 3) where 0=pos 3,6,9... — i.e. position 3 of codon
- pos≡1 (mod 3) where positions 1,4,7... — position 1 of codon
- pos≡2 (mod 3) where positions 2,5,8... — position 2 of codon

Weights w1, w2, w3. C and D contribute, A and B don't.

Per-position contribution: w_pos * (1 if char in {C,D} else 0).
Total = sum, capped at 9.

For all-C: 16*(w1+w2+w3) capped at 9 → 9.
For ACA*16 (only pos2=C): 16*w2 capped at 9 = 9, so w2 ≥ 9/16 = 0.5625.
For CACA period 2 (pos 1,3 C, pos 2 A): 16*w1 + 16*w3, but score = 0. So w1=w3=0? But then how does block-6 get 6 with only 7 pos-2-C?

Hmm. Let me check more carefully:
- For CAC codon (pos1=C, pos2=A, pos3=C): 16x = score 0. So pos1+pos3 C contribute 0.
- For CACACA period 2: same — pos 1,3 are alternately C,A. Half the codons have pos1=C, half have pos3=C... actually in any aligned 3-frame on period-2 CACA, codon pos2 alternates A,C,A,C... wait no.

Let me recount CACACACA... actually if seq is CACACACACA... position 1=C,2=A,3=C,4=A,5=C,6=A,... so even positions are A, odd are C.
Codon positions: pos 1=C,2=A,3=C; codon 2: pos4=A,5=C,6=A; codon 3: 7=C,8=A,9=C;...
So pos 2 of codons alternates: A,C,A,C,A,C,A,C... = 8 C's at codon-pos-2.
Got score 0! But 8 good codons by my counting.

That contradicts the earlier table (8 good→3). So position context within codon DOES matter.

Hypothesis: codon (X,C,X) where pos 2 = C — must this codon also have specific pos1/pos3? Like only certain codons "count" as good?
- CCC, CCA, ACC, ACA, BCB all give 9 when repeated.
- CAC,AAC,AAA,ABA,BAB all give 0.

What about ACA repeated, which is 16 codons of ACA (pos 1,3 = A, pos 2 = C)? Score 9.
What about pattern CACACACA which when read in codons = codon1 CAC, codon2 ACA, codon3 CAC, codon4 ACA... Mixed CAC and ACA. CAC is bad (=0 alone), ACA good (=9 alone). 8 good + 8 bad codons.
But score is 0! Whereas clustered 8 CCC + 8 AAA = 3.

So context across codons matters. The CAC codon between two ACA's poisons things.

Maybe scoring involves checking that the codon doesn't start with C (when codon "good" by pos2 rule)? Or maybe alignment is dynamic / overlapping windows?

Let me think about TRIPLET WINDOWS at every position (not just every 3rd position): scan all 46 triplets.
For ACA repeated (ACAACAACA...): triplets: ACA,CAA,AAC,ACA,CAA,AAC,... 
Window content cycles ACA,CAA,AAC.
For CCC*16: all triplets CCC.
For CAC repeated (CACCACCAC...): triplets CAC,ACC,CCA,CAC,ACC,CCA,...
Interesting! CAC repeated has triplets CAC, ACC, CCA. But score 0.
ACA repeated has triplets ACA, CAA, AAC. Score 9.

Difference: ACA's triplets include "ACA" (which alone scored 9). CAC's triplets include CAC (scored 0), ACC (scored 9), CCA (scored 9).

If we count fraction of windows that are "good" (have middle=C/D):
- ACA repeated triplets ACA(mid=C),CAA(mid=A),AAC(mid=A) → 1/3 good. Score 9?
- CAC repeated triplets CAC(mid=A),ACC(mid=C),CCA(mid=C) → 2/3 good. Score 0?
This is reversed.

Hmm.

Maybe scoring relates to non-aligned codons, but only specific frame?
Or maybe it's something else entirely. Need more experiments.

## 2026-06-28 15:11 — query 59

## Block-size sweep with equal 8g/8b codon composition
- k=1 (CCCAAA repeated): 0
- k=2 (CCCCCC AAAAAA repeated): 6
- k=4 (12g+12b alternating once → wait that's k=4 codons = 12 chars): 4
- k=8 (clustered): 3

So k=2 is OPTIMAL. Why?

Maybe scoring involves PAIRS of consecutive codons. If both codons in a pair are good, count it. If one good one bad, doesn't help.
k=2: 4 good-good pairs (CCC,CCC), 4 bad-bad pairs (AAA,AAA), 0 mixed. But that's 4 good-pairs → if fit ≈ pairs * 9 / 8 = 4.5 → maybe 4 or 5. Got 6.

Or maybe "dimer" reading frame at codon level - codons read in pairs from start.
k=2: pairs are (CCC,CCC), (AAA,AAA), (CCC,CCC), (AAA,AAA)... = 4 good pairs out of 8. fit=6. → 4 pairs * 1.5 = 6? Or 4 → ~6 mapping.
k=1: pairs are (CCC,AAA), (CCC,AAA)... = 0 good pairs. fit=0 ✓
k=4: pairs depend on alignment. 8 pairs total. CCC,CCC|CCC,CCC|AAA,AAA|AAA,AAA|CCC,CCC|CCC,CCC|AAA,AAA|AAA,AAA. = 4 good pairs. fit=4? Got 4 ✓!
k=8: CCC,CCC|CCC,CCC|CCC,CCC|CCC,CCC|AAA,AAA|...|AAA,AAA. = 4 good pairs. fit=4? Got 3 ✗
All good: 8 good pairs → fit=9.
0 good pairs: fit=0.

Hmm k=8 expectation was 4 from this model but got 3. Close though.

Let me check the standard table:
- 16 good codons = 8 pairs = 9
- 15 good codons + 1 bad at end: pairs (g,g)*7 + (g,b)*1 = 7 good pairs → fit=8. So 7→8.
- 14 good + 2 bad: 7 good pairs (CCC,CCC)*7 + (AAA,AAA)*1, wait if bad at end and bad are consecutive: pairs (g,g)*7 + (b,b)*1 = 7 gp → fit=7. So 7→7? But 15g→8 also has 7gp. So model fails.

Different. Maybe not pairs.

Let me think about it as: scoring requires both pos2 of codon AND pos2 of NEIGHBORING codon to be C/D?
- Define G_i = 1 if codon i has pos2 ∈ {C,D}, else 0.
- Score per codon = G_i * G_{i-1} or sum of some product?

16 codons all G=1: sum of G_i*G_{i+1} for i=1..15 = 15. fit=9. 
15 good (codon 16 bad): pairs 1-15 good, pair 15-16 = 1*0 = 0. Sum = 14. fit=8.
14 good (codons 15,16 bad): pairs 1-14 = 13 good (i=1..13 give 1, i=14 gives 0, i=15 gives 0). Sum=13. fit=7.
13 good (codons 14,15,16 bad): pairs 1-13 good (i=1..12 give 1, i=13,14,15 give 0). Sum=12. fit=6.
12 good: sum=11. fit=6 (got 6).
11 good: sum=10. fit=5 (got 5 ✓).
10 good: sum=9. fit=5 (got 4).
9 good: sum=8. fit=4 (got 4).
8 good: sum=7. fit=4 (got 3).
4 good: sum=3. fit=2 (got 1).

Pretty close. Map sum→fit looks like fit = floor(sum*9/15)?
sum=15: 9 ✓
sum=14: 8.4→8 ✓
sum=13: 7.8→7 ✓
sum=12: 7.2→7 (got 6) close
sum=11: 6.6→6 ✓
sum=10: 6 (got 5) close
sum=9: 5.4→5 (got 4)
sum=7: 4.2→4 (got 3) close
sum=3: 1.8→1 ✓

Hmm always off by 1 in middle. Could be floor((sum-1)*9/14)?
14:9·(1)/14*9 hmm. (15-1)/14*9=9 ✓
14: 13/14*9 = 8.36→8 ✓
13: 12/14*9 = 7.71→7 ✓
12: 11/14*9 = 7.07→7 (got 6)
11: 10/14*9=6.43→6 ✓
Still off.

OR maybe sum of G_i * G_{i+1} mapped via lookup or floor((sum)/15 * 9 with bias).

Now check k=2 block (CCCCCC AAAAAA *4): codons CCC,CCC,AAA,AAA × 4 = ggbbggbbggbbggbb. G sequence: 1,1,0,0,1,1,0,0,...
Pairs G_i*G_{i+1}: (1,1)=1, (1,0)=0, (0,0)=0, (0,1)=0, (1,1)=1, ... Pattern: 1,0,0,0 repeating. 15 pairs: 1,0,0,0,1,0,0,0,1,0,0,0,1,0,0. Sum=4. Predicted fit ≈ floor(4*9/15)=2. Got 6. ✗

So pair-product model fails for k=2 block. Back to drawing board.

Maybe scoring involves runs of good codons:
- max run g of length L scores something like L?
- All 16: L=16, fit=9
- 15g+1b: L=15, fit=8
- 14g+2b: L=14, fit=7
- 12g+4b: L=12, fit=6
- 10g+6b: L=10, fit=4 
- 8g+8b clustered: L=8, fit=3
- 4g+12b: L=4, fit=1
- k=2 alt block: max L = 2 → fit=6?? doesn't fit if it's just max

Sum of run lengths squared? 
k=2: 4 runs of length 2 each → sum L² = 4*4=16. /something=6.
all 16: 16²=256. =9.
8g 8b: 8²=64. =3.
Ratio: 256→9, 64→3, 16→6. Doesn't scale.

Maybe sum of L*(L+1)/2 (triangular)?
16: 136 → 9
12: 78 → 6
8: 36 → 3
10: 55 → 4
4: 10 → 1
k=2: 4*(2*3/2)=4*3=12 → 6? Hmm 12 vs 16 gives 6 vs 6. close.
k=4: 2 runs of 4: 2*10=20 → ? Got 4. 
k=8: 1 run of 8: 36 → 3 ✓

Linear interp 136→9, 0→0: 136/9 ≈ 15.1 per fit unit.
16→1.06, 36→2.39, 78→5.17, 136→9.
fit=floor(sum/15)? 
16/15=1 → got 6 (k=2). Way off.

Maybe each run contributes max(0, L-1)?
16: 15 → 9
15: 14 → 8
14: 13 → 7
12: 11 → 6
11: 10 → 5 (got 5) ✓
10: 9 → 4 (got 4) ✓
9: 8 → 4
8: 7 → 3 (got 3) ✓
7: 6 → 2 (got 2) ✓
6: 5 → 2 (got 2) ✓
5: 4 → 1 (got 1) ✓
4: 3 → 1 (got 1) ✓
3: 2 → 0 (got 0) ✓
2: 1 → 0 ✓
1: 0 → 0 ✓
0: 0 → 0 ✓

YES! Sum over runs of max(0, L-1) divided by something close to scale to 9.
Map sum → fit:
15→9
14→8
13→7
11→6
10→5
9→4
8→4 (need check 9g, predicted 8 from above)
7→3
6→2
5→2
4→1
3→1
2→0
1→0
0→0

Let me check k=2 case: 4 runs of length 2 each, sum (L-1)=4*1=4 → fit 1? But got 6. ✗

Damn. Still doesn't work for k=2.

OK, the k=2 case (block of 6 chars CCCCCC AAAAAA) giving fit 6 is mysterious. Let me re-verify it.

## 2026-06-28 15:13 — query 71

## Single run of L good codons embedded in bad → fitness:
L=1: 0
L=2: 0 (one run of 2, fit=0)  -- wait
L=3: 0
L=4: 1
L=5: 1
L=6: 2
L=7: 2
L=8: 3
L=10: 4
L=11: 5
L=12: 6
L=14: 7
L=15: 8
L=16: 9

Pattern: fit = floor((L-1)/2)? 
L=2: floor(1/2)=0 ✓
L=3: floor(2/2)=1 (got 0) ✗

Try floor((L-2)/2)?
L=2: 0 ✓
L=3: 0 ✓
L=4: 1 ✓
L=5: 1 ✓
L=6: 2 ✓
L=7: 2 ✓
L=8: 3 ✓
L=10: 4 ✓
L=11: 4 (got 5) ✗
L=12: 5 (got 6) ✗
L=14: 6 (got 7) ✗
L=16: 7 (got 9) ✗

Off above L=10. Maybe (L-2)/2 for low and different above?

Actually L=11→5, L=12→6, L=14→7, L=15→8, L=16→9. That's L-6 for L≥11.
And (L-2)/2 for L≤10:
L=4:1, L=5:1.5→1, L=6:2, L=7:2.5→2, L=8:3, L=9:?, L=10:4.

Match point: at L=10: (10-2)/2=4 vs L-6=4. Same. L=11: 4.5 vs 5. 
So fit = max(floor((L-2)/2), L-6)? Then for L=16: max(7,10)=10 but got 9, capped at 9. Cap at 9.

L=11: max(4, 5)=5 ✓
L=12: max(5, 6)=6 ✓
L=13: max(5.5, 7)=7
L=14: max(6, 8)=8 (got 7) ✗

Doesn't work. Try different formula.

L  fit
1  0
2  0
3  0
4  1
5  1
6  2
7  2
8  3
9  ?
10 4
11 5
12 6
13 ?
14 7
15 8
16 9

L-fit: 1,2,3,3,4,4,5,5, ?,6,6,6, ?,7,7,7
Or fit/L: 0, 0, 0, .25, .2, .33, .29, .375, ?, .4, .45, .5, ?, .5, .53, .5625

It looks more like fit ≈ floor(L * (L-1) / 30) or similar:
L=2: 2/30=0 ✓
L=3: 6/30=0 ✓
L=4: 12/30=0 (got 1) ✗

Try fit ≈ round((L*9-3)/16)? 
L=16: 141/16=8.8→9 ✓
L=15: 132/16=8.25→8 ✓
L=14: 123/16=7.7→8 (got 7) ✗

Maybe table-based, related to dimers/trimers of good codons inside the run? Within a run of L good codons there are L-1 consecutive pairs of good. 
L=2: 1 pair, fit 0
L=3: 2 pairs, fit 0
L=4: 3 pairs, fit 1
L=5: 4 pairs, fit 1
L=6: 5 pairs, fit 2
L=7: 6 pairs, fit 2
L=8: 7 pairs, fit 3
L=10: 9 pairs, fit 4
L=11: 10 pairs, fit 5
L=12: 11 pairs, fit 6
L=14: 13 pairs, fit 7
L=15: 14 pairs, fit 8
L=16: 15 pairs, fit 9

pairs→fit:
1→0, 2→0, 3→1, 4→1, 5→2, 6→2, 7→3, 9→4, 10→5, 11→6, 13→7, 14→8, 15→9

For low: fit = floor((pairs-1)/2). Check: 1→0, 2→0 (got 0), 3→1 ✓, 4→1 ✓, 5→2 ✓, 6→2 ✓, 7→3 ✓, 9→4 ✓
For 10→5: (10-1)/2 = 4.5 → 4. Got 5. Hmm jumps.

pairs 9→4, 10→5, 11→6, 13→7, 14→8, 15→9. 
That's fit=pairs-5 for pairs≥10. So:
fit = max(floor((pairs-1)/2), pairs - 5)?
pairs=10: max(4,5)=5 ✓
pairs=11: max(5,6)=6 ✓
pairs=13: max(6,8)=8 (got 7) ✗

Still off. Let me try fit = floor(pairs/2) + maybe correction:
1→0, 2→1 (got 0), 3→1, 4→2 (got 1)... ✗

Look at the actual sequence: 0,0,0,1,1,2,2,3,?,4,5,6,?,7,8,9
Diffs: 0,0,1,0,1,0,1,?,?,1,1,?,?,1,1
The pattern from L=4 to L=10 looks like +1 every 2. Then from L=10 to L=16 it's +1 every 1.
Possibly: fit = floor((L-2)/2) for L≤10, and L-6 for L>10.
L=10: floor(8/2)=4 ✓ and 10-6=4. Junction works.
L=11: 11-6=5 ✓
L=12: 6 ✓
L=14: 8. Got 7. ✗

Damn L=14 breaks this. Let me verify L=14 measurement: AAAAAAAAAAAACCCCCCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAA
Wait — that sequence isn't a clean run. Let me count: 12 A's + 21 C's + 15 A's = 48. 21 C's. 

But codons are aligned at positions 1-3, 4-6, etc. So a 12-A prefix = 4 AAA codons. Then 21 C's. Codons 5-onwards starting position 13. Codon 5: 13-15 = CCC. Codon 6: 16-18 = CCC. ... 21 C's span positions 13-33. Codon positions covered: codon5 (13-15) all C, codon6 (16-18) all C, codon7 (19-21) all C, codon8 (22-24) all C, codon9 (25-27) all C, codon10 (28-30) all C, codon11 (31-33) all C. That's 7 codons fully C. Then position 34-48 = 15 A's. Codons 12-16 all A. So run of GOOD codons = 7, not what I called L=7 earlier...

Wait I previously thought L=14 was the run length but I may have miscounted. Let me recount each.

For L=7: AAAAAAAAAAAACCCCCCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAA = 12+21+15=48. Wait same as L=14? Let me recount the L=14 query.

L=14: AAAAAAAAAAAACCCCCCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAA — 12 A + 21 C + 15 A. Same as L=7?!

I made an error. Let me redo carefully.

## 2026-06-28 15:14 — query 80

## Cleaned L (length of single good-codon run) → fitness:
L=1:0, L=2:0, L=3:0, L=4:1, L=5:1, L=6:2, L=7:2, L=8:3, L=9:4, L=10:4, L=11:5, L=12:6, L=13:6, L=14:7, L=15:8, L=16:9

Diffs: 0,0,1,0,1,0,1,1,0,1,1,0,1,1,1
That's +1 on L=4,6,8,9,11,12,14,15,16 → roughly +1 every other L but with shifts.

Try fit = round((L-2.5)*9/14)?
L=4: 1.5*9/14=0.96→1 ✓
L=5: 2.5*9/14=1.6→2 (got 1) ✗

Try fit ≈ round(L²/30)?
L=4:0.53→1 ✓
L=5: 0.83→1 ✓
L=6: 1.2→1 (got 2) ✗

Try formula: fit = floor((L*(L-1))/30) hmm
L=4: 12/30=0 ✗

Try fit = floor((L-3)(L+something)/something):
Look at it as L→fit pairs:
4,1 / 6,2 / 8,3 / 10,4 / 12,6 / 14,7 / 16,9
Even L: 4→1, 6→2, 8→3, 10→4, 12→6, 14→7, 16→9
Diff (L=12-L=10) = 2! Skip a value. Odd L: 5→1, 7→2, 9→4, 11→5, 13→6, 15→8
Diff (L=9-L=7)=2

So fitness jumps by 2 somewhere — non-monotonic in increments. 
Maybe fit = floor(L/2) + bonus for very high L?

L/2 floor: 2,2,3,3,4,4,5,6,6,7,7,8
L=4:2 (got 1) ✗

Hmm. Maybe fit = floor((L² - something)/something):
L²: 1,4,9,16,25,36,49,64,81,100,121,144,169,196,225,256
fit*32 ish: 0,0,0,32,32,64,64,96,128,128,160,192,192,224,256,288
L² vs fit*32: pretty close to L² - some constant.

Actually let me try fit = floor((L-1)²/something) - I think bisection isn't worth it. Let me focus on what's predictive.

Look — maybe scoring is based on length of run minus some offset for "boundary" codons. Like first and last good codon in a run "don't count" because they're adjacent to bad codons:
- effective good = max(0, L-2) — but with L=4 → 2 effective, fit=1 = effective/2?
- L=16 → 14 effective, fit=9 ≠ 7.

If endpoints don't count: scoring = (L-2)² / 16?
L=4: 4/16 = 0.25, fit=1 ✗

Sum of contributions where each good codon contributes (1 - distance_to_edge/some)?
For run of L, contributions = sum over each position of f(min(left,right) from edge).

Let me just commit to a more practical understanding and use experiments to fill in. Single run table:
L: 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
f: 0 0 0 1 1 2 2 3 4 4  5  6  6  7  8  9

Diffs: 0 0 1 0 1 0 1 1 0 1 1 0 1 1 1
Cumulative match: fit = number of "+1" steps through L.

Maybe f(L) = floor((L²-2L)/14) for some range?
L=4: 8/14=0.57→0 ✗

Or maybe it's truly just an integer lookup. Anyway I have data. Now, what about multiple runs?

I tested 2 runs of 2 → fit=2 (block of 6 with 2 runs of 2)... wait let me check. Earlier "Two runs of 2 good codons" gave fit 2 (exp 64). Three runs of 2 → fit 4 (exp 65). Four runs of 2 (k=2 block pattern) → fit 6.

So #runs of 2 → fit: 1→0, 2→2, 3→4, 4→6.
That's 2*(runs-1)? 1→0, 2→2, 3→4, 4→6 ✓

So sum of f(L) isn't right since f(2)=0 but 2 runs give 2.

Maybe it's about interactions between runs! Maybe the scoring depends on number of good-codon transitions (run starts/ends)?

Or maybe the metric counts something like "good codon adjacent to bad" PAIRS at boundaries.

Hmm, single run of 2: 2 boundaries (start, end). 
2 runs of 2: 4 boundaries. fit=2.
3 runs: 6 boundaries. fit=4.
4 runs: 8 boundaries. fit=6.

Each additional run adds 2 boundaries and +2 fit. So fit ≈ boundaries - 2? 4-2=2, 6-2=4, 8-2=6 ✓. Single run of L=2: 2-2=0 ✓.

But single run of L=16: 2 boundaries (or 0 if no surrounding bad)? Actually if all 16 are good, the run extends to ends. Maybe 0 boundaries? Fit=9. Doesn't fit.

Maybe the formula counts contributions across all kinds of structures. I'll save and continue experimenting.

## 2026-06-28 15:15 — query 87

## Spacing study (2 runs of L=2)
spacing s (bad codons between): 0,1,2,3,4,5 → fit 1,1,2,1,2,2

Strange parity. Maybe each codon position effective from a different angle. Maybe positions of good codons matter (e.g., even-indexed codons paired with odd-indexed).

Let me note codon indices (1-based) of good codons:
s=0: codons 1,2,3,4 good (=run of 4 also). fit=1
s=1: 1,2,4,5 good. fit=1
s=2: 1,2,5,6 good. fit=2
s=3: 1,2,6,7 good. fit=1
s=4: 1,2,7,8 good. fit=2
s=5: 1,2,8,9 good. fit=2

Examine codon-index parity (odd/even):
s=0: 1,2,3,4 (oo,e,o,e). 2 odd, 2 even.
s=1: 1,2,4,5 (o,e,e,o). 2o,2e
s=2: 1,2,5,6 (o,e,o,e). 2o,2e
s=3: 1,2,6,7 (o,e,e,o). 2o,2e
All same. Different fits.

Pairs of codons (i,j) where j=i+1 AND i is odd (i.e., aligned in pairs (1,2),(3,4),...)?
s=0: aligned pairs in {1,2,3,4}: (1,2) and (3,4) both gg → 2 aligned. fit=1
s=1: codons 1,2,4,5. Aligned (1,2)=gg, (3,4)=bg, (5,6)=gb. 1 aligned. fit=1
s=2: codons 1,2,5,6. Aligned (1,2)gg, (5,6)gg = 2. fit=2 ✓
s=3: codons 1,2,6,7. Aligned (1,2)gg, (5,6)bg, (7,8)gb = 1. fit=1 ✓
s=4: codons 1,2,7,8. Aligned (1,2)gg, (7,8)gg = 2. fit=2 ✓
s=5: codons 1,2,8,9. Aligned (1,2)gg, (7,8)bg, (9,10)gb = 1. But fit=2 ✗

Hmm s=5 fails. Could be a "shifted alignment" too?

What if scoring counts aligned pairs in BOTH frame 0 (codons 1-2, 3-4, 5-6,...) and frame 1 (codons 2-3, 4-5, 6-7,...)? Sum?

frame0 + frame1:
s=0 codons{1,2,3,4}: f0 pairs (1,2)+(3,4)=2; f1 (2,3)=1. Sum=3. fit=1.
s=1 codons{1,2,4,5}: f0 (1,2)=1, (3,4)?cd3 not g, (5,6)cd6 not g. f0=1. f1 (2,3)?cd3 no=0; (4,5)gg=1. Sum=2. fit=1.
s=2 codons{1,2,5,6}: f0 (1,2)=1, (5,6)=1. Sum f0=2. f1 (2,3)0; (6,7)cd7 no =0. f1=0. Sum=2. fit=2 ✓
s=3 codons{1,2,6,7}: f0 (1,2)=1, (5,6)0 (cd5 no), (7,8)0. f0=1. f1 (6,7)=1. Sum=2. fit=1 ✗

Still inconsistent.

Let me think completely differently. Maybe the rule isn't even codon-based.

Consider individual position contributions. Position 2 of codon (i.e., positions 2,5,8,...,47) IS critical for "C/D required". But maybe other rules apply too.

Maybe fitness is based on per-position contribution where each position contributes a weight depending on neighbors:
weight(i) = 1 if seq[i] ∈ {C,D} AND seq[i+1] ∈ {C,D}? Like 2-mer requirement.

Count CC/CD/DC/DD adjacent pairs in some pattern.

For s=2 (CCCCCCAAAAAACCCCCC...): 
CC pairs in first block (CCCCCC at positions 1-6): pairs (1,2),(2,3),(3,4),(4,5),(5,6) = 5 CC pairs
CC pairs in second block (positions 13-18): 5 pairs. Total CC pairs = 10. fit=2.

For all-C: 47 pairs. fit=9. 47/some=9 → some=5.2.
For CCC alone (run of L=2): 1 CCC codon = positions x,x+1,x+2. 2 CC pairs (x,x+1) and (x+1,x+2). fit=0.
For L=4 (CCCCCCCCCCCC = 12 C in a row): 11 CC pairs. fit=1.
For L=8 (24 C): 23 CC pairs. fit=3.
For L=16 (48 C): 47 CC pairs. fit=9.

Map CC-pairs → fit:
2:0, 5:1, 8:2 (extrapolating L=3), 11:3, ... 47:9.

Single run length L = 3L characters, with 3L-1 CC pairs.
L=2: 5 pairs (got 0)
L=3: 8 pairs (got 0)
L=4: 11 pairs (got 1)
L=5: 14 pairs (got 1)
L=6: 17 pairs (got 2)
L=7: 20 pairs (got 2)
L=8: 23 pairs (got 3)
L=10: 29 pairs (got 4)
L=11: 32 pairs (got 5)
L=12: 35 pairs (got 6)
L=14: 41 pairs (got 7)
L=15: 44 pairs (got 8)
L=16: 47 pairs (got 9)

Maybe fit = floor((pairs-2)/5)?
5:0, 8:1 (got 0)✗

floor((pairs-5)/5)?
5:0, 8:0, 11:1✓, 14:1✓, 17:2✓, 20:3 (got 2)✗

floor((pairs-3)/4.5)? pairs=5:0, 8:1 ✗

floor(pairs/5)?
5:1 (got 0)✗

Maybe more position-specific. Maybe scoring is: count of positions p such that all of seq[p-2], seq[p-1], seq[p] ∈ {C,D} (i.e., 3 consecutive C/D's)?
L=2 (6 C's in a row): positions 3,4,5,6 have CCC ending → 4 such positions. fit=0.
L=4 (12 C's): positions 3..12 → 10. fit=1.
L=8 (24 C's): 22. fit=3.
L=16: 46. fit=9.

Map: 0:0, 4:0, 10:1, 22:3, 46:9. 
Linear 46→9 means 0.196/count. 22*0.196=4.3. fit=3, off.

Not a great fit. Different approach needed. Let me try larger k-mers.

Count of consecutive CCCC (k=4 C's)?
L=2 (6 C): positions 4,5,6 (each ending position of CCCC). = 3. fit=0.
L=4 (12 C): 9. fit=1.
L=8 (24 C): 21. fit=3.
L=16 (48 C): 45. fit=9.
0:0, 3:0, 9:1, 21:3, 45:9
slope 45/9=5. Try fit=floor(count/5):
3:0✓ 9:1✓ 21:4 (got 3)✗

CCCCC (k=5)?
L=2 (6 C): 2. fit=0
L=4 (12C): 8. fit=1
L=8 (24 C): 20. fit=3
L=16: 44. fit=9
2:0, 8:1, 20:3, 44:9. 44/9=4.9. floor/5:
2:0✓, 8:1✓, 20:4 (got 3)✗

Hmm I'm grasping. Let me just survey all single-run L values to determine f(L), then survey multi-run interactions empirically.

I have f(L) table. Now let me test 2 runs of various L,L' to see if f(L)+f(L') ≈ fit_total.

Then with that I can predict and test more.

## 2026-06-28 15:16 — query 94

## 3 runs of L=2 with various spacing:
spacing s=1: fit 3 (codons 1,2,4,5,7,8 good)
spacing s=2: fit 4 (codons 1,2,5,6,9,10 good)
spacing s=3: fit 3 (codons 1,2,6,7,11,12 good)

Even-spaced (s even) → higher. Suggests positions matter.

Good codon positions:
s=1: 1,2,4,5,7,8 — codons at odd & even mixed
s=2: 1,2,5,6,9,10 — all (4k+1, 4k+2)
s=3: 1,2,6,7,11,12 — varied

Maybe scoring counts pairs of good codons at specific positions.

Actually wait. Let me think about modular position. Codon position mod 4? mod 2?

For s=2: codons {1,2,5,6,9,10}. mod 4: {1,2,1,2,1,2}. All in classes 1 and 2.
For s=1: codons {1,2,4,5,7,8}. mod 4: {1,2,0,1,3,0}. Mixed.
For s=3: codons {1,2,6,7,11,12}. mod 4: {1,2,2,3,3,0}.

Hmm s=2 gives uniform mod-4. Higher fit.

Maybe the scoring is: count pairs of good codons (i,j) with j-i = 4? Or based on hexamers of 12 chars (4 codons)?

Let's check: 12-char block = 4 codons. 48/12=4 blocks.
s=2 blocks: codons 1-4 (g,g,b,b), 5-8 (g,g,b,b), 9-12 (g,g,b,b), 13-16 (b,b,b,b). Pattern: 3 "ggbb" blocks + 1 "bbbb" block.
s=1 blocks: codons 1-4 (g,g,b,g), 5-8 (g,b,b,g), 9-16 all b. Mixed.
s=3 blocks: codons 1-4 (g,g,b,b), 5-8 (b,g,g,b), 9-12 (b,b,g,g), 13-16 (b,b,b,b). 

Could be 12-char ("super-codon") matters. Let me test what 12-char patterns score.

Actually, let me try a totally different hypothesis: alignment in HEXAMERS (6 chars = 2 codons). 48/6 = 8 hexamers. Each hexamer must have its position-2 char (and pos-5 char) both be C/D?

Hexamer test: chars at positions {2,5,8,11,...,47} (codon pos 2) — i.e., every 3rd starting at 2.

For each HEXAMER (positions 6k+1 to 6k+6 for k=0..7), the "good positions" are 6k+2 and 6k+5.

For a hexamer to score, maybe both pos 6k+2 and 6k+5 must be C/D?

Check k=2 pattern (CCCCCC AAAAAA repeated): hexamers are CCCCCC, AAAAAA, ... = 4 good hexamers. fit=6. 4 hex → 6?

CCC*8+AAA*8 (clustered): hexamers are CCCCCC, CCCCCC, CCCCCC, CCCCCC, AAAAAA*4. 4 good hex. fit=3. ✗ Same hex count, different fit.

So not just hexamer count.

Maybe hexamer-level AND codon-level both matter.

Let me try another angle: maybe scoring uses overlapping windows of 6 chars. 43 windows. Each window scores 1 if pos 2 AND pos 5 are C/D.

For all C: 43 windows, all good. fit=9. 43/some=9.
For ACA*16: every position 2 of codon is C, all others A. In windows of 6:
Window 1 (pos 1-6): pos 2=C, pos 5=A. Window pos 2,5 chars: C,A. Not both good. Score 0.
So all windows score 0. fit=9?? But ACA*16 = 9.
Contradiction.

So that's not it.

Maybe it's just per-codon scoring but with COMPOSITION matters within codon.
Let me enumerate per-codon scores:
- CCC: ? (homogeneous all CCC = 9 / 16 codons = some)
- CCA: from CCA repeated = 9, so each contributes 9/16
- ACA: 9/16 each
- ACC: 9/16 each
- BCB: 9/16

Hmm all same. What if codon has internal score 9/16 if pos2∈{C,D} and certain positions match too?

All same internal scoring (capped at 9 total). 

The k=2 block pattern (CCCCCC AAAAAA): 8 good codons (pos2=C in codons 1,2,5,6,9,10,13,14), 8 bad (pos2=A in codons 3,4,7,8,11,12,15,16). 
Looking at boundaries: codon 2 ends pos 6 = C; codon 3 starts pos 7 = A. Transition C→A within codon 3.

Maybe scoring sees CONSECUTIVE C/D characters in seq, not by codon:
For CCCCCC AAAAAA *4: runs of C are length 6, 4 runs. Runs of A are length 6, 4 runs.
For CCC*8+AAA*8: 1 run of 24 C's, 1 run of 24 A's.
For all C: 1 run of 48.

Maybe scoring = sum f(L_C) where L_C = length of each C/D run, with f giving more for medium-length runs?

f(48) = 9 (all C)
f(24) = 3? (just C side; A side contributes 0 obv)
f(12) → ? Run of 4 codons all C. Earlier L=4 fit=1. So f(12)=1.
f(L_C=6) → 2? since 4 runs of 6 (in k=2 block) gave fit=6. So 4*f(6) = 6 → f(6) = 1.5. Hmm not integer.

But f sum might allow non-integer. Then total floored?
All C f(48)=9. 
Two runs of 24 (would happen if A's in middle of two C blocks): 4 (from earlier "bad in middle" exp 46 → fit 4 with 24C+24A+24C split. Wait that was "CCCC×12 AAAA×24 CCCC×12" = 12C+24A+12C. Two C runs of 12. fit=4. So f(12)+f(12)=4, f(12)=2. But earlier I said L=4 (12 C's run = 12 chars) gave fit=1. Contradiction... unless the surroundings matter!

Let me check exp 46: "Bad codons in middle, good codons at ends." Sequence: CCCCCCCCCCCCAAAAAAAAAAAAAAAAAAAAAAAACCCCCCCCCCCC = 12C + 24A + 12C. Two runs of 12 C's. fit=4.

But L=4 single-run (12 C's, 4 codons) gave fit=1. So 2 runs of 12 C's = 4, single run of 12 C's = 1.

f(12) alone = 1, but 2*f(12) = 4? Means non-additive (interaction).

Yet 4 runs of 6 C's gave fit=6, f(6)=1.5 → 6 total. f(6) seems consistent if floor isn't applied.

Maybe each run contributes L/some, and there's a bonus for separation?

Let me tabulate single C-run lengths (in chars) and their fitness contributions:
3 chars (1 codon): from L=1, single CCC in middle of A's → fit 0
6 chars (2 codons): from L=2 → 0
9 chars (3 codons): from L=3 → 0
12 chars (4 codons): from L=4 → 1
15 chars: 1
18 chars: 2
21 chars: 2
24 chars: 3
27 chars: ?
30 chars: 4
33: 5
36: 6
39: ?
42: 7
45: 8
48: 9

Now multiple runs: 2 runs of 12 chars = fit 4. 4 runs of 6 chars = fit 6. Maybe sum of L/X?
4*6/X = 6 → X=4. 2*12/X = 4 → X=6. Inconsistent.

OR maybe total fit = floor((sum of L²) / some_constant)?
4 runs of 6: sum L² = 4*36 = 144. fit 6. 144/24 = 6 ✓
2 runs of 12: 2*144 = 288. fit 4. 288/24 = 12 ≠ 4. ✗

(sum L)² / something:
4 runs of 6 chars: sum=24. 24²=576. /96 = 6.
2 runs of 12: sum=24. 24²=576. ≠4.

Hmm not just sum-based.

OK let me just take many more measurements and try to find the formula computationally in my head.

## 2026-06-28 15:17 — query 101

## Plenty of data, hard to find formula. Will try fitting via direct experimentation.

Trying: maybe scoring works like a PROTEIN that depends on the alternation pattern of good/bad codons.

Maybe scoring is just like: number of good codons MINUS some penalty for boundary transitions?

g=8, trans=1 (clustered) → 3 = 8 - 5
g=8, trans=7 (k=2 block) → 6 = 8 - 2
g=8, trans=15 (alt 1/1) → 0 = 8 - 8

So penalty = g - fit:
clustered (1 trans): penalty 5
k=2 (7 trans): penalty 2
alt (15 trans): penalty 8

Penalty doesn't monotonically increase with transitions. Weird.

Let me try framing differently. Think of g positions as 1's in length-16 binary string. Maybe fit = something like longest k-mer pattern. 

Actually try: fit ≈ count of pairs (i, i+2) both good (skip-1 dimer)?
- 16g: i=1..14 with both g. 14 pairs. fit=9.
- 15g (last=b): 13 pairs. fit=8. 
- 14g (15,16=b): 12 pairs. fit=7.
- 13g (14,15,16=b): 11. fit=6.
- 12g: 10. fit=6.
- 11g: 9. fit=5.
- 10g: 8. fit=4.
- 8g cluster: 6. fit=3.
- 4g cluster: 2. fit=1.
- 1g: 0. fit=0.

Map (i,i+2 pairs)→fit:
14→9, 13→8, 12→7, 11→6, 10→6, 9→5, 8→4, 6→3, 2→1, 0→0

Approx fit ≈ pairs*9/14? 14:9 ✓ 13:8.36→8 ✓ 12:7.7→7 ✓ 11:7.07→7 (got 6) ✗

Hmm. fit = floor(pairs/1.5)? 14: 9.3→9 ✓ 13:8.67→8 ✓ 12:8 (got 7) ✗

Now for k=2 block (ggbbggbbggbbggbb): pairs (i,i+2) both g: 
codons 1,2 g; 5,6 g; 9,10 g; 13,14 g.
Pairs at dist 2: (1,3)gb=0, (2,4)gb=0, (3,5)bg=0, (4,6)bg=0, (5,7)gb=0, (6,8)gb=0, (7,9)bg=0, (8,10)bg=0, ... → 0 pairs. fit=6? Way off.

Need different model. Maybe scoring is more complex: weighted positional sum.

Let me think this: maybe the rule is per-position weight w_i for each of the 16 codon slots, and fit = sum(w_i * g_i) capped at 9?
All g: sum w_i = 9. 
g only at slot 1: contribution w_1.
g only at slot 8: contribution w_8.

Test by making single good codon at different positions.

Single CCC at codon 1: AAAAAA...CCCAAA → wait actually I should put CCC at the leading position and AAA elsewhere. Already tested: CCC + 45 A = fit 0. So w_1 ≤ 0?

But more good codons could be needed. Let me think additive model: it's not just position weight.

What about positional pairs? Maybe fit = sum over (i,j) pairs of w_{ij} * g_i * g_j.

This is getting complex. Let me try to be more systematic and use the budget to gather data.

KEY INSIGHT TO TEST: Is the fitness actually a function only of which codon slots are "good"? Let me test same g-string but different bad-codon identities or different good-codon identities, to see if g-string fully determines fit.

## 2026-06-28 15:17 — query 105



## 2026-06-28 15:19 — query 124

## Big insight! Codons every 3rd position give high fitness.
Codons 1,4,7 (g=3) → fit 2
Codons 1,4,7,10,13,16 (g=6, all every-3rd) → fit 6
Codons 1,4 (g=2) → fit 1
Codon 1 alone → 0
Codons 1,16 (g=2) → 1

So with positions every 3rd starting at 1: each pair contributes? 6 codons in pattern give 6. 

Hypothesis: maybe fitness = count of good codons where codon-index ≡ 1 (mod 3)? 
Positions 1,4,7,10,13,16: indices ≡ 1 (mod 3). 6 such → fit 6 ✓
1,4,7: 3 such → fit 2. Hmm, but ✓ would predict 3.

Maybe fit = count_mod1 × something or there's a chain bonus.

Codons 1,16: 1 has idx≡1, 16 has idx≡1 (16=3*5+1). Both ≡1 mod 3. fit=1 (not 2).
Codons 1,4: both ≡1. fit=1.
Codons 1: just 1. fit=0.
Codons 1,4,7: all ≡1. fit=2.
Codons 1,4,7,10,13,16: all ≡1. fit=6.

So count of g at idx≡1 mod 3 → fit:
1 → 0
2 → 1
3 → 2
6 → 6

Not linear. Maybe fit = count - 1 capped at something? 1→0✓, 2→1✓, 3→2✓, 6→5. Got 6.

Or maybe fit = max(0, count - 1) for these, but 6→6 suggests something else takes over.

Actually wait — perhaps the rule is broader. Let me check what happens with other modular classes.

Test codons 2,5,8,11,14 (all idx≡2 mod 3): 5 such.

## 2026-06-28 15:20 — query 133

## Correction
Previous "single C" experiments may have had codon-frame errors. Let me redo carefully using positions 3i-1 for codon i pos2.

Confirmed measurements:
- Codon 1 only good: fit 0
- Codons 1,4 good (positions 2,11): fit 1 (exp 110)
- Codons 1,4,7 good (positions 2,11,20): fit 2 (exp 123) [need to re-verify]
- Codons 1,4,7,10 (positions 2,11,20,29): fit 4 (exp 127)
- Codons 1,4,7,10,13,16 (all 6 mod-1): fit 6 (exp 124)
- Codons 1,16 (positions 2, 47): fit 1 (exp 107)
- Codons 1,7,10,13,16 (skip codon 4): fit 1 (just verified) — even though 5 good codons!

So "every-3rd starting at 1" pattern is special. Breaking it reduces drastically.

Maybe fit depends on consecutive mod-1 codons? Like a chain of good codons at positions 1,4,7,10... — if all present, contributes.

Wait let me verify exp 123 (codons 1,4,7): I wrote "ACAAAAAAAACAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAA". Positions of C:
1:A 2:C 3-10:A (8), 11:C, 12-19:A (8), 20:C, 21-48:A. So C at 2,11,20. Codon pos2 positions: 2,11,20 — these are codons 1,4,7. Yes, 3 good codons. fit=2. ✓

And exp 127 (codons 1,4,7,10): "ACAAAAAAAACAAAAAAAACAAAAAAAACAAAAAAAAAAAAAAAAAAA". C at 2,11,20,29. fit=4. ✓

So pattern (consecutive 1,4,7,...,n): n codons in chain → fit?
n=1: 0
n=2 (1,4): 1
n=3 (1,4,7): 2
n=4 (1,4,7,10): 4
n=5 (1,4,7,10,13): 4
n=6 (1,4,7,10,13,16): 6

Hmm 4→5→6: 4,4,6. Plateau then jump. Like fit ≈ chain_length - 1 with cap?

Let me carefully test 5 chain length again.

## 2026-06-28 15:20 — query 135

## Major revision needed
- DCDDDDDDDDDCDDDDDDDDDCDDDDDDDDDCDDDDDDDDDCDDDDDC → fit 9
- BCBBBBBBBBBCBBBBBBBBBCBBBBBBBBBCBBBBBBBBBCBBBBBC → fit 0
- The C's are at the same positions (2, 11, 20, 29, 38, 47); only the fillers differ.

So having ALL D's gives fit 9 even when only 6 codons have C at pos2... but D fills everywhere. Actually pos 2 of every codon = either C or D.

For DCDDDDDDDDDCDDD...: positions of codon pos2 (2,5,8,...,47). At pos 2=C, pos 5=D, pos 8=D, pos 11=C, ... All ∈{C,D}. So all 16 codons are good! fit=9 expected ✓.

For BCB...: pos 2=C, pos 5=B, ... B is not good. So good codons are only at pos 2,11,20,29,38,47 = 6 good codons. Got fit 0!

But earlier with ACA fillers giving same 6 good codons → fit 6. Now with B fillers → fit 0!

So the fillers' character DOES matter beyond just being "good codon" or not. B vs A makes a difference!

Hmm, but I confirmed earlier that g-string fully determined fitness when comparing ACA/AAA vs CCC/AAA vs DDD/BBB. Let me re-examine.

Earlier exp 102: DDDDDDDDDDDDDDDDDDDDDDDDBBBBBBBBBBBBBBBBBBBBBBBB → fit 3. Same g-string as CCC+AAA (clustered 8g+8b) which also gave 3.

Earlier exp 105: ACAACAAAAAAAACAACAAAAAAAACAACAAAAAAAACAACAAAAAAA (k=2 block with ACA/AAA) → fit 6. Same as CCCCCC+AAAAAA pattern.

So those didn't distinguish. But now with new pattern (6 good codons spaced every 3), filler matters!

Maybe filler matters when bad codons separate good ones. Let me test: codons 1,4,7,10,13,16 good with various fillers.

## 2026-06-28 15:20 — query 135

## Reset
ACA repeated has codon-pos-2 char = C for EVERY codon (positions 5,8,11,...,47 all C). So 16 good codons → fit 9.

The "codons 1,4,7,10,13,16 good" pattern I made was BCB filler with C at positions 2,11,20,29,38,47, which means codon pos-2 at codons 1,4,7,10,13,16 was C, but pos-2 at codons 2,3,5,6,8,9,11,12,14,15 was B (not C/D).

Earlier ACAAAAAAAACAAAAAAAACAAAAAAAACAAAAAAAACAAAAAAAACA was meant to be 6 good codons. Let me verify.
ACAAAAAAAACAAAAAAAACAAAAAAAACAAAAAAAACAAAAAAAACA
positions: A(1)C(2)A(3)... 
Let me carefully count: ACA (3) AAAAAA (6) CA (2) AAAAAA (6) CA (2) AAAAAA (6) CA (2) AAAAAA (6) CA (2) AAAAAA (6) CA (2) wait that's 43 not 48.

Original: ACAAAAAAAACAAAAAAAACAAAAAAAACAAAAAAAACAAAAAAAACA
A-C-A-A-A-A-A-A-A-A-C-A-A-A-A-A-A-A-A-C-A-A-A-A-A-A-A-A-C-A-A-A-A-A-A-A-A-C-A-A-A-A-A-A-A-A-C-A
1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22-23-24-25-26-27-28-29-30-31-32-33-34-35-36-37-38-39-40-41-42-43-44-45-46-47-48

C at positions: 2, 11, 20, 29, 38, 47
Codon-pos-2 positions: 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47
C∩codon-pos-2: 2,11,20,29,38,47 → codons 1,4,7,10,13,16 are good
Other positions (5,8,14,17,23,26,32,35,41,44) have A → those codons bad.

So 6 good codons → fit 6 with A filler.
With B filler (BCBBBBBBBBBCBBBB...): same codon pattern (1,4,7,10,13,16 good) but other positions have B. fit=0.
With D filler: ALL codon pos2 are D → all 16 good. fit=9.

So when fillers are A or B (both "not good"), and we have 6 specific good codons, why does A give 6 but B give 0?

Maybe A and B have DIFFERENT roles. Let me test.

## 2026-06-28 15:20 — query 138

## Need cleaner tests of A vs B
Let me re-examine the 6-good-codon case:
- A filler: ACAAAAAAAACAAAA...CA → fit 6
- B filler: BCBBBBBBBBBCBBBB...BC → fit 0
- D filler: actually D filler makes all codons good → fit 9 (different)

Need a test with similar good codon pattern but pure B filler (where filler positions aren't good codons).

Wait — let me look at BCB...BCB filler more carefully:
Sequence: B-C-B-B-B-B-B-B-B-B-B-C-B-B-B-B-B-B-B-B-B-C-B-B-B-B-B-B-B-B-B-C-B-B-B-B-B-B-B-B-B-C-B-B-B-B-B-C
position: 1-2-3-4-5-6-7-8-9-10-11-12-...

Hmm let me recount: BCBBBBBBBBBCBBBBBBBBBCBBBBBBBBBCBBBBBBBBBCBBBBBC
B(1)C(2)B(3-11=9 B's)C(12)... wait position 12 not 11?

ACAAAAAAAACAAAA... in the A version: A(1)C(2)A(3)A(4)A(5)A(6)A(7)A(8)A(9)A(10)C(11)... so C at position 11 in A version. In B version I need same: B(1)C(2)B(3)B(4)B(5)B(6)B(7)B(8)B(9)B(10)C(11)... 

But I wrote "BCBBBBBBBBBCBB..." Let me count that: B(1)C(2)B(3)B(4)B(5)B(6)B(7)B(8)B(9)B(10)B(11)C(12)... So C at position 12, not 11! I had an extra B.

Let me redo.

## 2026-06-28 15:21 — query 140

## Settled: fitness = f(g-string) where g_i = 1 iff char at position 3i-1 ∈ {C,D}.
A and B are equivalent (both make codon bad). C and D are equivalent (both make codon good).

Now systematically explore g-string space. Key data points:
G-string (16 bits) → fit
1111111111111111: 9
1111111111111110: 8
1111111111111100: 7
1111111111111000: 6 (13g, all clustered start)
1111111111110000: 6 (12g start)
1111111111100000: 5 (11g)
1111111111000000: 4 (10g)
1111111100000000: 3 (8g clustered)
1111000000000000: 1 (4g clustered)
1000000000000000: 0 (1g)
1000000000000001: 1 (codons 1,16)
1001001001001001: 6 (every-3rd starting at 1, 6 codons)
1001001001001000: 4 (1,4,7,10,13 = 5 codons)
1001001001000000: 4 (1,4,7,10 = 4 codons)
1001001000000000: 2 (1,4,7)
1001000000000000: 1 (1,4)
1101101101101101: ? (would be 6 codons too, different pattern)

ggbbggbbggbbggbb: 6 (k=2 alt block) -- but only 8 good
ggbbbbbbbbbbbbbb: ? need to test
ggggggggbbbbbbbb: 3 (8g cluster)
gbgbgbgbgbgbgbgb: 0 (1/1 alt)
ggggbbbbggggbbbb: 4 (4/4 alt)

Hmm interesting that 1001001001001001 (6 codons spaced 3 apart) gives 6, same as 1111111111110000 (12 codons clustered). And gives more than 1111111111100000 (11 codons → 5)!

Let me explore: maybe the SPACING matters greatly. Pattern with spacing 3 seems golden.

Let me test 1001001001001000 (5 codons spaced 3): got 4. And 1001001001000000 (4 codons) got 4. Plateau!

Actually wait, I need to verify these again with proper sequences.

## 2026-06-28 15:22 — query 145

## Need careful sequence construction
For codon i good: char(3i-1) ∈ {C,D}.
For codon i bad: char(3i-1) ∈ {A,B}.
Other positions (3i-2, 3i) can be anything (use A for simplicity).

For pattern 110110110110110110... over 16 codons (good codons at i mod 3 ∈ {1,2}):
codon 1 (i=1, mod3=1): good. char 2 = C.
codon 2 (mod3=2): good. char 5 = C.
codon 3 (mod3=0): bad. char 8 = A.
codon 4: good. char 11 = C.
codon 5: good. char 14 = C.
codon 6: bad. char 17 = A.
codon 7: good. char 20 = C.
codon 8: good. char 23 = C.
codon 9: bad. char 26 = A.
codon 10: good. char 29 = C.
codon 11: good. char 32 = C.
codon 12: bad. char 35 = A.
codon 13: good. char 38 = C.
codon 14: good. char 41 = C.
codon 15: bad. char 44 = A.
codon 16: good. char 47 = C.

So all chars are A except at positions 2,5,11,14,20,23,29,32,38,41,47 = 11 C's.

Sequence (48 chars):
1A 2C 3A 4A 5C 6A 7A 8A 9A 10A 11C 12A 13A 14C 15A 16A 17A 18A 19A 20C 21A 22A 23C 24A 25A 26A 27A 28A 29C 30A 31A 32C 33A 34A 35A 36A 37A 38C 39A 40A 41C 42A 43A 44A 45A 46A 47C 48A

= ACAAC AAAAAC AACAA ACAAC AAAAA CAACA AAACA ACAAA AACAA C A
Let me string it: ACAACAAAAACAACAAACAACAAAAACAACAAACAACAAAAACAACAA wait that's getting messy. Let me write straight:
Positions of C: 2,5,11,14,20,23,29,32,38,41,47
All others A.

I'll generate by hand: starting with all A's: "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" (48 A's)
Replace position 2→C, 5→C, 11→C, 14→C, 20→C, 23→C, 29→C, 32→C, 38→C, 41→C, 47→C.

Resulting: ACA AC AAAAA C AA C AAAAA C AA C AAAAA C AA C AAAAA C AA C AA
Hmm let me build with explicit char list:
A,C,A,A,C,A,A,A,A,A,C,A,A,C,A,A,A,A,A,C,A,A,C,A,A,A,A,A,C,A,A,C,A,A,A,A,A,C,A,A,C,A,A,A,A,A,C,A

= "ACAACAAAACAACAAAAACAACAAAACAACAAAAACAACAAAAACAACA" wait that's 49 chars.

Let me count my array: positions 1-48: 
1:A 2:C 3:A 4:A 5:C 6:A 7:A 8:A 9:A 10:A 11:C 12:A 13:A 14:C 15:A 16:A 17:A 18:A 19:A 20:C 21:A 22:A 23:C 24:A 25:A 26:A 27:A 28:A 29:C 30:A 31:A 32:C 33:A 34:A 35:A 36:A 37:A 38:C 39:A 40:A 41:C 42:A 43:A 44:A 45:A 46:A 47:C 48:A

Concatenate: "ACAACAAAACAACAAAAACAACAAAAACAACAAAAACAACAAAAACAACA"
Count: A(1)C(2)A(3)A(4)C(5) = 5 chars. AAAAA(6-10)C(11)AA(12,13)C(14) = chars 6-14, 9 more chars, total 14. AAAAA(15-19)C(20) = 6 more = 20. AA(21,22)C(23) = 23. AAAAA(24-28)C(29) = 29. AA(30,31)C(32) = 32. AAAAA(33-37)C(38)= 38. AA(39,40)C(41)=41. AAAAA(42-46)C(47)A(48) = 48. Total 48 ✓.

So string: A C A A C A A A A A C A A C A A A A A C A A C A A A A A C A A C A A A A A C A A C A A A A A C A
Concatenating no spaces: "ACAACAAAACAACAAAAACAACAAAAACAACAAAAACAACAAAAACA"
Let me count that: A-C-A-A-C-A-A-A-A-A-C-A-A-C-A-A-A-A-A-C-A-A-C-A-A-A-A-A-C-A-A-C-A-A-A-A-A-C-A-A-C-A-A-A-A-A-C-A
1   2 3 4 5 6 7 8 9 10 11 12 13 14 15...

Hmm matches what I want. Let me string it without confusion using actual concatenation:
chars[1..48] = A,C,A,A,C, A,A,A,A,A, C,A,A,C,A, A,A,A,A,C, A,A,C,A,A, A,A,A,C,A, A,C,A,A,A, A,A,C,A,A, C,A,A,A,A, A,C,A

Group of 5: ACAAC AAAAA CAACA AAAAC AACAA AAACA ACAAA AACAA CAAAA ACA (3) = 48 chars ✓
Sequence string: "ACAACAAAAACAACAAAAACAACAAAAACAACAAAAACAACAAAAACA"

Test this.

## 2026-06-28 15:22 — query 148

## Refined g-string data
g-string → fit (16-bit g, msb=codon 1):
1111111111111111 (16g): 9
1111111111111110 (15g): 8
1111111111111100 (14g): 7
1111111111111000 (13g): 6
1111111111110000 (12g): 6
1111111111100000 (11g): 5
1111111111000000 (10g): 4
1111111100000000 (8g): 3
1111000000000000 (4g): 1
1000000000000000 (1g): 0
1000000000000001 (1,16): 1
1001001001001001 (every 3rd from 1, 6g): 6
1001001001001000 (1,4,7,10,13): 4
1001001001000000 (1,4,7,10): 4
1001001000000000 (1,4,7): 2
1001000000000000 (1,4): 1
1101101101101101 (110 pattern, 11g): 7
0110110110110110 (011 pattern, 10g): 6
1010101010101010 (8g spaced 2): 0
1000010000100001 (4g spaced 4): 0
1100110011001100 (8g pairs spaced 2): 6
1111000011110000 (8g pairs of 4): 4

Let me think about this in terms of codon-position modulo 3:
Codon i mod 3:
i: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
mod3: 1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1

Sequence (16 codons) of mod3 values: 1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1

Number of codons with mod3=0: 5 (codons 3,6,9,12,15)
Number with mod3=1: 6 (codons 1,4,7,10,13,16)
Number with mod3=2: 5 (codons 2,5,8,11,14)

For 1001001001001001 (mod3=1 codons all good): 6 good, fit=6.
For pattern 110110110... = mod3 ∈ {1,2} good (11 good), fit=7.
For pattern 011011011... = mod3 ∈ {2,0} good (10 good), fit=6.

Maybe fit relates to which mod3 classes are "good".

Let me define n1, n2, n0 = # good codons with mod3=1,2,0.
- 16g: n1=6, n2=5, n0=5. fit=9.
- 15g (codon 16 bad): n1=5, n2=5, n0=5. fit=8.
- 14g (codons 15,16 bad): n1=5, n2=5, n0=4. fit=7.
- 13g (codons 14,15,16 bad): n1=5, n2=4, n0=4. fit=6.
- 12g (codons 13,14,15,16 bad): n1=4, n2=4, n0=4. fit=6.
- 11g: n1=4, n2=4, n0=3. fit=5.
- 10g: n1=4, n2=3, n0=3. fit=4.
- 8g cluster: n1=3, n2=3, n0=2. fit=3.
- 4g cluster (1,2,3,4 good): n1=2, n2=1, n0=1. fit=1.
- 1g (codon 1): n1=1,n2=0,n0=0. fit=0.
- (1,16): both mod3=1. n1=2,n2=0,n0=0. fit=1.
- mod3=1 only (6g): n1=6,n2=0,n0=0. fit=6.
- (1,4): n1=2. fit=1.
- (1,4,7): n1=3. fit=2.
- (1,4,7,10): n1=4. fit=4.
- (1,4,7,10,13): n1=5. fit=4.

Hmm n1 count of mod3=1: 1→0, 2→1, 3→2, 4→4, 5→4, 6→6. Not linear.

For n1=2 (just codons 1,4): fit=1. n1=2 (codons 1,16): also fit=1. So same n1 → same fit (for pure n2=n0=0 cases).

Hmm 1,4 vs 1,16 — both have n1=2. Both give fit 1. So maybe true.

Maybe fit = n1 (count of good mod3=1 codons)?
For pure-mod-1: 
n1=1→0, 2→1, 3→2, 4→4, 5→4, 6→6. Not just n1.

Maybe fit depends on consecutive RUNS of mod3=1 codons?
1,4: consecutive (both mod3=1, adjacent in mod3=1 sequence). 
1,7: not consecutive.
1,4,7,10: 4 consecutive.
1,4,7,10,13: 5 consecutive.
1,4,7,10,13,16: 6 consecutive.
1,7,10,13,16: 4 consecutive (7,10,13,16) plus 1.

Let me restate: in the "mod3=1 chain" of 6 slots (codons 1,4,7,10,13,16), good codons form some pattern. The fit might be calculated on this 6-bit chain.

Chain 111111 (all 6): fit 6.
Chain 111110 (1,4,7,10,13): fit 4.
Chain 111100 (1,4,7,10): fit 4.
Chain 111000 (1,4,7): fit 2.
Chain 110000 (1,4): fit 1.
Chain 100000 (1): fit 0.
Chain 100001 (1,16): fit 1.

OK this 6-element chain has its own fit function. Let me see:
111111: 6
111110: 4
111100: 4 (= same)
111000: 2
110000: 1
100001: 1
100000: 0

This looks like... hmm.

For all-good chain (length n): chain n=1→0, n=2→1, n=3→2, n=4→4, n=5→4, n=6→6. 

Actually look at the data: I claimed (1,7,10,13,16) gives 1 (exp 132 — but wait the sequence was botched). Need to re-test cleanly.

Plan: more cleanly enumerate g-string patterns. Even better, develop a small dataset to fit the formula.

## 2026-06-28 15:23 — query 152

## Mod3 chains: each chain has its own scoring
mod3=1 chain (codons 1,4,7,10,13,16, 6 slots):
- 6/6 good: fit contribution? in g-string 1001001001001001 (only this chain good): fit 6.
mod3=2 chain (codons 2,5,8,11,14, 5 slots):
- 5/5 good: fit 4.
mod3=0 chain (codons 3,6,9,12,15, 5 slots):
- 5/5 good: fit 4.

If contributions are additive: total fit = sum. But for all-good (16g) we get 9, while 6+4+4=14, capped at 9?
- 11g (110 pattern, mod1+mod2 all good): 6+4+0=10 capped → 9? Got 7. ✗

So not additive cap. Maybe sum or sum-with-overlap.

Wait, let me recheck mod3 chain scoring.

Maybe fit isn't computed per chain, but rather per RUN OF CONSECUTIVE good codons in the original codon order.

Hmm but earlier I showed 8g cluster (1-8 good) gives 3, while 8g in (1,4,7,...) pattern but only 6 codons gives 6.

Let me think about RUNS within mod3 chains. The mod3=1 chain has 6 positions. Codons go 1,4,7,10,13,16 — separated by 3 in codon index, but ADJACENT within the chain.

For chain "all good" (length n): fits I have:
n=1: fit (for codon 1 only) = 0. But chains are length 5 or 6.

Wait — within just the mod3=1 chain:
- 1/6 good: codon 1 only → fit 0
- 2/6 good: (1,4) → fit 1, (1,16) → fit 1, (1,7) → fit 0
- 3/6 good: (1,4,7) → fit 2
- 4/6 good: (1,4,7,10) → fit 4, but (1,7,10,13) → ? (consecutive in chain but skipping codon 4)
- 5/6 good: (1,4,7,10,13) → fit 4
- 6/6 good: → fit 6.

(1,16) gave 1 — these are first and last of mod3=1 chain (chain positions 1 and 6). NOT consecutive in chain. Yet fit=1.
(1,4) = chain positions 1,2 (consecutive in chain). fit=1.
(1,7) = chain positions 1,3 (skip 1). I haven't tested cleanly.

Let me test (1,7) carefully.

## 2026-06-28 15:23 — query 163

## Pair (1,k) spacing → fit:
spacing 1 (1,2): 0
spacing 2 (1,3): 0
spacing 3 (1,4): 1 ⭐
spacing 4 (1,5): 0
spacing 5 (1,6): 0
spacing 6 (1,7): 0
spacing 7 (1,8): 0
spacing 8 (1,9): 0
spacing 9 (1,10): 1 ⭐
spacing 10 (1,11): ? need test
spacing 11 (1,12): ?
spacing 12 (1,13): 0
spacing 13 (1,14): ?
spacing 14 (1,15): ?
spacing 15 (1,16): 1 ⭐

Pattern: spacings 3, 9, 15 → 1. Spacings 6, 12 → 0. So odd multiples of 3 are special, even multiples are not. But also 1,2,4,5,7,8 give 0.

So only spacings ≡ 3 (mod 6)? 3, 9, 15 ≡ 3 mod 6 ✓. 6, 12 ≡ 0 mod 6.

Need to test spacings 10, 11, 13, 14 to be sure no other special values.

## 2026-06-28 15:24 — query 174

## mod3=1 chain (6 slots) analysis
Treating the 6 slots as a binary string b1b2b3b4b5b6:
- 000000: 0
- 100000: 0 (codon 1 alone)
- 110000 (1,4): 1
- 100001 (1,16): 1
- 100100 (1,10): 1
- 101000 (1,7): 0 (failed earlier)
- 110100 (1,4,10): 2
- 110001 (1,4,16): 2
- 101001 (1,7,16): 2
- 100101 (1,10,16): 2
- 111000 (1,4,7): 2
- 011110 (4,7,10,13): 4
- 111100 (1,4,7,10): 4
- 111110 (1,4,7,10,13): 4
- 111111: 6

Also (4,7) = 011000: 1
(7,10) = 001100: 1
(5,8) (mod2 chain): 1 (in its chain)
(1,16) chain dist 5: 1
(1,10) chain dist 3: 1
(1,7) chain dist 2: 0 (this is two non-adjacent slots)
(1,4) chain dist 1: 1

So pair in chain:
chain dist 1 (adjacent): 1
chain dist 2: 0
chain dist 3: 1
chain dist 4: ? (1,13)
chain dist 5: 1

Let me test (1,13): chain positions 1,5. Dist 4.

## 2026-06-28 15:25 — query 174



## 2026-06-28 15:26 — query 178



## 2026-06-28 15:27 — query 189

## Pair scoring is position-dependent, not just spacing
- (1,4): 1
- (1,7): 0
- (1,10): 1
- (1,13): 0
- (1,16): 1
- (4,7): 1
- (4,10): 0
- (4,13): 0
- (4,16): 0
- (7,10): 1
- (7,16): 1
- (10,13): 1
- (13,16): 1

Pattern? Let me think modulo 6:
Codons modulo 6:
1:1, 4:4, 7:1, 10:4, 13:1, 16:4
For mod3=1 chain: alternating 1,4,1,4,1,4 mod 6.

Pairs giving fit 1: pairs where one codon ≡1 (mod 6) and other ≡4 (mod 6)?
(1,4): 1,4 ✓ → 1
(1,7): 1,1 → 0 ✓
(1,10): 1,4 → 1 ✓
(1,13): 1,1 → 0 ✓
(1,16): 1,4 → 1 ✓
(4,7): 4,1 → 1 ✓
(4,10): 4,4 → 0 ✓
(4,13): 4,1 → should be 1, but got 0 ✗
(4,16): 4,4 → 0 ✓
(7,10): 1,4 → 1 ✓
(7,16): 1,4 → 1 ✓
(10,13): 4,1 → 1 ✓
(13,16): 1,4 → 1 ✓

(4,13): codons 4 and 13, mod 6 = 4 and 1. Should be a "1,4 pair" giving 1. But got 0!

Hmm let me recheck (4,13).
Sequence "AAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAA"
A x 10 + C(11) + A x 26 + C(38) + A x 10. Total 10+1+26+1+10=48 ✓.
But wait — between 11 and 38 should be 26 A's. 12-37 = 26 positions ✓.

So C is at 11 (codon 4 pos 2) and 38 (codon 13 pos 2). Got fit 0.

But model predicts 1 (pair 4,13 in chain).

So model is incomplete. The position WITHIN the chain matters somehow.

mod3=1 chain order: 1, 4, 7, 10, 13, 16.
Pairs that gave 1: (1,4), (4,7), (7,10), (10,13), (13,16), (1,10), (1,16), (7,16) (chain pos 1-2, 2-3, 3-4, 4-5, 5-6, 1-4, 1-6, 3-6) 
Pairs that gave 0: (1,7), (1,13), (4,10), (4,13), (4,16) (chain pos 1-3, 1-5, 2-4, 2-5, 2-6)

Chain-pos differences for 1's: 1,1,1,1,1,3,5,3
For 0's: 2,4,2,3,4

Wait (4,13) is chain pos 2 to 5, diff 3. But (1,10) is chain pos 1 to 4, diff 3. Both diff 3, but different fit. So even chain-pos-diff isn't enough.

Hmm. Let me look at PARITY of chain positions:
Chain pos 1 = codon 1, parity odd
Chain pos 2 = codon 4, parity even
Chain pos 3 = codon 7, parity odd
Chain pos 4 = codon 10, parity even
Chain pos 5 = codon 13, parity odd
Chain pos 6 = codon 16, parity even

Pairs giving 1: chain (1,2)oe, (2,3)eo, (3,4)oe, (4,5)eo, (5,6)oe, (1,4)oe, (1,6)oe, (3,6)oe
All these have OPPOSITE parity ✓

Pairs giving 0: (1,3)oo, (1,5)oo, (2,4)ee, (2,5)eo!, (2,6)ee

Wait (2,5) is even-odd, opposite parity, but gives 0!

Hmm. (2,5) = chain pos 2 to 5 = codons 4 to 13. Got 0.

But (1,4) chain pos 1-4 = codons 1 to 10. Got 1.

So chain-pos-diff 3: (1,4) o-e → 1, (2,5) e-o → 0. Same parity composition. Different fit.

Maybe it's about the LEFT codon (earlier in chain):
- pairs where left chain-pos is ODD (1,3,5): mostly fit 1
- pairs where left chain-pos is EVEN (2,4): often fit 0

Pairs with left odd:
(1,2)→1, (1,3)→0, (1,4)→1, (1,5)→0, (1,6)→1
(3,4)→1, (3,5)→?, (3,6)→1
(5,6)→1
Pairs with left even:
(2,3)→1, (2,4)→0, (2,5)→0, (2,6)→0
(4,5)→1, (4,6)→0

For left=odd: pair to right-pos r:
r-l = 1: 1
r-l = 2: 0 (need to check (3,5))
r-l = 3: 1
r-l = 4: 0
r-l = 5: 1
For left=even:
r-l=1: 1
r-l=2: 0
r-l=3: 0
r-l=4: 0

So for left=odd, fit at odd r-l. For left=even, fit only at r-l=1.

Hmm this isn't a clean pattern. Let me re-examine. Maybe I have errors.

Actually let me reconsider via raw codon indices: pair (i,j) gives 1 iff?
Pairs (i,j) giving 1: (1,4),(1,10),(1,16),(4,7),(7,10),(7,16),(10,13),(13,16)
Pairs giving 0 with j-i ≡ 0 mod 3: (1,7),(1,13),(4,10),(4,13),(4,16),(7,13),(10,16)?

Need test (7,13). And (10,16).

## 2026-06-28 15:27 — query 189

## Block-diff observation
Pair (i,j) of codons in mod3=1 chain. Block(i) = (i-1)/3 (0-indexed). All pairs with block-diff 1 give 1. Pairs with block-diff 2 give 0. Block-diff 3 mixed: (1,10)=1, (4,13)=0, (7,16)=1.

What if block diff 3 needs MOD-6 alignment of codon? 
codons 1,7 have codon idx mod 6 = 1
codons 4,10,16 have codon idx mod 6 = 4
codon 13 has codon idx mod 6 = 1

Pair (1,10): mods 1,4 → 1
Pair (4,13): mods 4,1 → 0
Pair (7,16): mods 1,4 → 1

Interesting! Pairs where first codon has mod-6=1 and second has mod-6=4 give 1. But (4,13) is (mod-6=4, mod-6=1) → 0.

So ordering matters: must be (1 then 4) mod-6.

Pair (1,4): (1, 4) mod 6 → 1 ✓
Pair (1,16): (1, 4) mod 6 → 1 ✓
Pair (4,7): (4, 1) mod 6 → would predict 0, but got 1 ✗

Hmm contradicts.

Wait (4,7): codon 4 idx mod 6 = 4, codon 7 idx mod 6 = 1. So (4,1) → predicted 0. But got 1. Doesn't fit.

I'm getting tangled. Let me approach this differently — maybe scoring is some kind of XOR/parity computation on the binary g-string viewed in blocks.

Let me write 16-bit g-string in 6-bit blocks (last block incomplete). 48 chars / 18 chars per 6-codon block.

Hmm 48 chars / 18 doesn't divide evenly. Try 48/6 = 8 (codons per block of 6 chars = 2 codons).

OK time to try a totally fresh approach. Let me sample many g-strings and try to deduce a formula computationally.

Actually let me check if maybe the rule has to do with C/D characters at SPECIFIC absolute positions only.

Earlier ACA repeated gives 9 → C at positions 2,5,8,...,47.
What if only positions 2, 11, 20, 29, 38, 47 matter (every 9 chars)? Plus other positions add nothing or hurt nothing?

Pair (1,10): C at 2, 29 → BOTH at "essential" positions. fit 1.
Pair (1,4): C at 2, 11 → BOTH at "essential". fit 1.
Pair (4,13): C at 11, 38 → BOTH at "essential". fit 0.

Wait same essential positions. So not that.

Let me try yet another angle — maybe the experiment results are sometimes affected by something I'm not modeling. Let me try comparing same g-string with different actual chars.

## 2026-06-28 15:28 — query 195

## A and B are NOT equivalent!
- C at pos 11 and 38, A filler: fit 0
- C at pos 11 and 38, B filler: fit 1

Major revision. Filler characters DO matter.

What about C vs D as "good" char? Already showed they're equivalent for some cases. Let me test more.

Maybe the rule is more complex with all 4 chars having different effects. Let me restart systematic exploration with a focus on understanding each character's role.

Need to retest: when we said g-string fully determined fit earlier, we were just lucky with the comparisons. Now I need to consider full 4-char alphabet.

Plan:
1. Test each character individually as filler in known-good patterns
2. Determine role of each character
3. Reconstruct theory

For 8g clustered (CCC*8 + AAA*8 = 3), with B instead of A:
- DDD*8 + BBB*8 = 3 (tested exp 102)
Good codon could be CCC,DDD,CCA,ACC,ACA,CCD,DCD etc (anything with pos2=C or D).
Bad codon = anything with pos2=A or B.

Hmm but now A filler vs B filler in same position gives different fit. So beyond pos2.

## 2026-06-28 15:29 — query 207

## Discovery: A vs B at non-codon-pos-2 positions matters!
- (4,13) good codons (C at pos 11, 38):
  - all A elsewhere: fit 0
  - all B elsewhere: fit 1
  - BAA...A (1 B + rest A): fit 0
  - all B's right of 1st C: fit 1
  - all B's left of 2nd C with A's left of 1st C: fit 1
  - mixed B/A throughout (ABAB pattern): fit 1
  - codon-pos-2 = A (others B): fit 0! ← interesting

So having ANY B at a codon-pos-2 position elsewhere (codons other than 4,13 having pos-2=B) doesn't help. Wait it's the opposite: codon-pos-2 being A definitively scored 0 when others were B.

Let me reconsider. Maybe the rule involves both pos-2 char (must be C/D) AND something about all codons or transitions.

Hmm wait — maybe codon-pos-2 char being B treats codon as "different" from A. Like 4 categories not 2.

Let me test pure-A codon (AAA) vs pure-B codon (BBB) etc as "bad codons" in critical positions.

For (4,13) good with everything else AAA codons → 0.
For (4,13) good with everything else BBB codons → ??

I tested "all B's right of 1st C" which means codons 5-16 have BBB? Let me re-examine the sequence: "AAAAAAAAAACBBBBBBBBBBBBBBBBBBBBBBBBBBCBBBBBBBBBB"
Positions:
1-10 A, 11 C, 12-37 B (26 chars), 38 C, 39-48 B (10 chars).
Codon 1: AAA (chars 1-3)
Codon 2: AAA (4-6)
Codon 3: AAA (7-9)
Codon 4: ACB (10-12): pos 11=C ✓ good
Codon 5: BBB (13-15)
Codon 6: BBB (16-18)
Codon 7: BBB (19-21)
Codon 8: BBB (22-24)
Codon 9: BBB (25-27)
Codon 10: BBB (28-30)
Codon 11: BBB (31-33)
Codon 12: BBB (34-36)
Codon 13: BCB (37-39): pos 38=C ✓ good
Codon 14: BBB (40-42)
Codon 15: BBB (43-45)
Codon 16: BBB (46-48)

So codons 1-3 are AAA, 5-12 BBB, 14-16 BBB.
fit=1.

For all-A version, all "bad" codons are AAA. fit=0.

So having BBB codons instead of AAA codons between the two good codons gives fit 1.

Test: replace just ONE AAA with BBB and see when fit jumps.

## 2026-06-28 15:30 — query 218

## Major rethink needed
A and B aren't equivalent as fillers. Maybe think of it as: chars have roles.

Possibilities:
- A = "stop" codon component
- B = "filler"
- C, D = "active" amino acid

In biology, having stop codons in the middle of a gene truncates the protein. Maybe each AAA codon is a "stop" that kills translation downstream.

Let me test: (1,4) with A filler = fit 1. With B filler should give same? Wait, with single-pair tests near start I think I always used A filler. Let me test (1,4) with B filler.

## 2026-06-28 15:30 — query 228

## With B filler, pair (i,j) → fit:
spacing 3: (1,4)1, (4,7)1, (4,13)? wait (4,13) is spacing 9. Let me organize by spacing:
- Spacing 3: (1,4)=1, (2,5)=1, (4,7)=1, (5,8)=1, (10,13)=1 (with A), (13,16)=1 (with A) - all 1
- Spacing 6: (1,7)=0, (2,8)=0, (4,10)=0 (with A)
- Spacing 9: (1,10)=1, (2,11)=0, (4,13)=1, (7,16)=1
- Spacing 12: (1,13)=0
- Spacing 15: (1,16)=1

So with B filler:
- spacing 3: 1 ✓
- spacing 6: 0
- spacing 9: depends on position
- spacing 12: 0
- spacing 15: 1

Spacing 9 pairs:
(1,10): C at 2,29 → 1
(2,11): C at 5,32 → 0
(4,13): C at 11,38 → 1
(7,16): C at 20,47 → 1

Hmm 3 of 4 give 1. (2,11) gives 0.

Codons (1,10),(4,13),(7,16) all have first codon ≡ 1 mod 3. (2,11) has first codon ≡ 2 mod 3.

So spacing 9, first codon mod 3 = 1 → 1; mod 3 = 2 → 0. What about mod 3 = 0?

Test (3,12) and (6,15).

## 2026-06-28 15:30 — query 229

## Strategy reset
I have 271 experiments. Let me hypothesize the rule and test it efficiently.

Working theory:
- The seq encodes 16 codons (3 chars each).
- A codon is "good" if pos2 ∈ {C,D}.
- BUT the fitness depends on more than just the binary g-string — fillers also matter.

OR maybe my "g-string" idea is wrong and the rule is different.

Let me try: maybe fitness is computed from the COUNTS of each character at specific positions.

Or maybe: fitness depends on the alternation pattern of "active" vs "inactive" tokens in a more complex way.

Let me revisit: ACA*16 = 9, but ACAACAACA... reads as codons ACA. Maybe the "good codon" ACA is special because position1=A,pos2=C,pos3=A.

What about codon ACB? AAB? ABA? Let me characterize codons individually.

## 2026-06-28 15:31 — query 240

## g-string DOESN'T fully determine fit
- (4,13) good as CCC, AAA bad: fit 1
- (4,13) good as ACA, AAA bad: fit 0

Different! So composition matters beyond just pos-2 char.

Let me reconsider. Maybe scoring counts C/D characters at multiple positions per codon, not just pos2. Or maybe entire codons interact.

For CCC at codon 4: pos 10,11,12 all C.
For ACA at codon 4: only pos 11 is C.

So total C/D count differs: 3 vs 1 for that codon.

Earlier observations:
- All-C: 9 (48 C's)
- CCA repeat (32 C): 9
- ACA repeat (16 C): 9
- CAC repeat (32 C, but pos2=A): 0

So C count alone doesn't determine, but pos2=C is essential.

Maybe rule: count of "good codons" weighted by C/D content?
- CCC = full good (3 C's)
- ACC, CCA = partial good (2 C's)  
- ACA = minimal good (1 C)

For (4,13) both CCC: 2*3 = 6 "good chars at good codons". fit 1.
For (4,13) both ACA: 2*1 = 2 "good chars at good codons". fit 0.

Maybe fit = floor((good_char_count - threshold)/scaling)?

For all CCC*16 = 48 C's all at good codons. fit 9.
For ACA*16 = 16 C's at good codons. fit 9 (same!).

So can't be just count.

Maybe rule involves PAIRS of C/D at specific positions.

Actually let me re-examine. The L=2 single run test: CCC at codons 4,5 with AAA bad = fit 0.
What if I use ACA at codons 4,5 with AAA bad? Same g-string but different chars.

## 2026-06-28 15:32 — query 248

## More refined model
The character at codon i pos 1 matters for some "linking" function.

For pair (4,13):
- ACA at 4, ACA at 13: fit 0
- CCA at 4, CCA at 13: fit 1
- ACA at 4, CCC at 13: fit 1 (C at pos 37 = codon 13 pos 1)
- CCC at 4, ACA at 13: fit 0 (C at pos 10 = codon 4 pos 1, doesn't help)
- ACC at 4, ACC at 13: fit 0 (C at pos 12 and 39, not pos 10 or 37)

So C at pos 37 (codon 13 pos 1) = critical for pair (4,13) scoring.

Maybe the rule is: a "good codon" at slot i has full effect only if it's "connected" to neighbors via C/D at certain interface positions.

Codon 13 pos 1 is char 37 (=3*13-2). For pair (4,13), maybe codon 13 needs codon 12 pos 3 = char 36 to be C/D too? Or the connection is at char 37 itself.

Let me test:
- (4,13) with C at pos 37 ALONE (not at pos 38, so codon 13 not "good"): expect 0 (since codon 13 needs pos 2 = C/D to count).
- (4,13) with CCA at 13 = C at pos 37 and pos 38 → 1
- (4,13) with C at pos 38 only (ACA at 13) → 0

So both pos 37 AND pos 38 must be C for codon 13 to "activate" this pair.

Hmm. Let me think more abstractly: maybe codons aren't 3 chars; maybe the encoded units are larger.

What if codons are 4 chars? 48/4 = 12 codons. Let me see.

Pos 38 (codon 13 pos 2) and pos 37 (codon 13 pos 1) in 3-char codon. But in 4-char codon: chars 37-40 would be codon 10 (1-indexed: codons start at 1,5,9,...,45). So char 38 = codon 10 pos 2 (if 4-char).

For ACAACAACAACA...(repeating ACA) with 16 reps, that's 48 chars. C at position 5 (= codon 2 pos 2 if 3-char). In 4-char codons: codons start at 1,5,9,... char 5 is start of codon 2. C at pos 5,11,17,23,29,35,41,47 — not aligned with 4-char codons either.

Hmm. Let me think: maybe code reads in BLOCKS OF 9 (= 3 codons)? 48/9 = 5.33, not clean. 

Or blocks of 6? 48/6 = 8. Let me check.

For (4,13) good codons, positions 10-12 and 37-39. In 6-block (positions 1-6, 7-12, 13-18, ...): codon 4 = block 2. Codon 13 = block 7.

Maybe "good block" = block has at least one C/D in position 2 of an internal codon? 

I'll keep exploring with focus on the linking pos 37 = codon 13 pos 1.

What if the rule is: codon i pos 1 must be C/D AND codon i pos 2 must be C/D for codon i to "count" if it's not connected to a similarly-good neighbor?

## 2026-06-28 15:33 — query 257

## (4,13) summary:
- CCC + AAA bad: 1
- CCA + AAA: 1 (C at pos 37 helps)
- ACA + AAA: 0
- ACC + AAA: 0 (C at 39 doesn't help)
- ACA + CCC at 13: 1 (C at 37 from CCC helps)
- ACA + ACA + C at 37 from neighboring: 1

Key: char at position 37 (codon 13 pos 1) must be C/D for pair (4,13) to score 1.

But wait — for pair (1,4), I haven't tested if char at pos 10 (codon 4 pos 1) is required.
For pair (1,4), ACA at both gave 1. So pos 10 = A. Pair still scored.

So requirement isn't universal "pos 1 = C/D". It depends on the pair.

Maybe the rule for pair scoring involves "linking" via specific positions.

For pair (i,j), maybe need C/D at position 3j-2 (codon j pos 1)? For (1,4): 3*4-2=10. ACA case has A at 10, fit=1. So not required for this pair.

Hmm so it's not consistent. Let me look at where (4,13) differs from (1,4):

(1,4) is between block 1 (codon 1, first block) and block 2 (codon 4).
(4,13) is between block 2 and block 5.

Maybe pos 37 in (4,13) ACA case has special role I'm missing.

Let me test more systematically: for pair (4,13) ACA+ACA (fit 0), what positions do I need to flip to get fit 1?

I'll test each position 1-48 individually (replacing A with C). Too many.

Or test specific candidates: positions in codons around 13.

Already tested:
- Pos 37 (codon 13 pos 1) flipped to C: → 1
- Pos 36 (codon 12 pos 3) flipped to C: → 0
- Pos 39 (codon 13 pos 3) flipped to C: → 0

What about pos 35, 34?

## 2026-06-28 15:33 — query 263

## Pos 37 is special for (4,13) pair
Only flipping pos 37 → C transforms (4,13) ACA pair from fit 0 to fit 1.

What's special about position 37? 
- Position 37 mod 3 = 1 (codon-pos-1).
- It's char 37/48 ≈ 77% of the way through.

For pair (1,4) ACA case, what position would be analogous?
Position 37 is 1 before pos 38 (codon 13 pos 2). The analog for codon 4 = position 11-1 = 10 (codon 4 pos 1).

But (1,4) ACA case (with pos 10 = A) gives fit 1. So the position 10 analog doesn't need to be C.

What's different? (1,4) ACA: chars... position 1 = A, 2 = C, then A's, position 11 = C, rest A's. Position 10 = A.

Hypothesis: maybe codon 1 doesn't need linker (since it's at start)? Maybe each "interior" pair (not involving codon 1) needs special linkage?

Test: (10,13) ACA — does it need pos 28 (codon 10 pos 1) = C?

## 2026-06-28 15:34 — query 265

## Pair compatibility table (mod3=1 chain, ACA filler):
Chain slots 1-6 = codons 1,4,7,10,13,16
Pair → fit:
(1,2)=(1,4): 1
(1,3)=(1,7): 0
(1,4)=(1,10): 1
(1,5)=(1,13): 0
(1,6)=(1,16): 1
(2,3)=(4,7): 1
(2,4)=(4,10): 0
(2,5)=(4,13): 0
(2,6)=(4,16): 0
(3,4)=(7,10): 1
(3,5)=(7,13): ?
(3,6)=(7,16): 1
(4,5)=(10,13): 1
(4,6)=(10,16): ?
(5,6)=(13,16): 1

Treating chain slots as 1-6, give label (s1,s2) → fit:
(1,2):1, (1,3):0, (1,4):1, (1,5):0, (1,6):1
(2,3):1, (2,4):0, (2,5):0, (2,6):0
(3,4):1, (3,5):?, (3,6):1
(4,5):1, (4,6):?
(5,6):1

Most adjacents (s,s+1) give 1.
Special: (1,4):1, (1,6):1, (3,6):1
Special 0: (2,4):0, (2,5):0, (2,6):0

So slot 2 doesn't pair with slot 4,5,6 (only adjacents 1 and 3).
But slot 1 pairs with 2,4,6. Slot 3 pairs with 2,4,6. Slot 5 pairs with 4,6 (and (3,5)? to test).

OK strange structure. Need to test (3,5)=(7,13) and (4,6)=(10,16).

## 2026-06-28 15:34 — query 266

## MAJOR ERROR FOUND
My earlier "(4,13)" tests had a counting error - I had C at position 39, not 38. That means codon 13 was actually BAD (pos2=A). So those tests were really (4,?) with only 1 good codon.

After correctly constructing (4,13) [C at 38], fit=1 as expected.

So the simple model holds: pair (i,j) gives fit 1 when both are good, regardless of position! Let me re-verify other "anomalies".

Wait, I should re-verify (1,4) and (1,16) and (1,10) too. And re-verify chain mod3=1 cases.

Let me also re-examine what "(spacing 9)" meant. With proper construction:
(1,4) C at 2,11: fit 1
(4,7) C at 11,20: fit 1
(1,10) C at 2,29: fit 1
(4,13) C at 11,38: fit 1 (NEW correct value)
(7,16) C at 20,47: fit 1

So all spacing-9 pairs may give 1.

And the earlier "(1,7)" = spacing 18 — C at 2, 20. fit 0.
And the "(1,13)" = spacing 36 — C at 2, 38. fit 0.

But "(1,10) = spacing 27" → fit 1, "(1,16) = spacing 45" → fit 1.

Char-distance pattern: 9, 18, 27, 36, 45 → fits 1, 0, 1, 0, 1. Char distance ≡ 9 (mod 18) → 1.

That's actually = codon distance ≡ 3 (mod 6) → 1 (which I noted earlier).

So maybe my "(4,13) = 0" anomaly was just a sequencing error. Let me re-verify all the pair tests with careful construction.

## 2026-06-28 15:35 — query 276

## Spacing 9 pairs:
- (1,10): 1
- (2,11): 0 (mystery)
- (3,12): 1
- (4,13): 1
- (5,14): 1
- (6,15): ?
- (7,16): 1

Only (2,11) is anomalous! Maybe my test was wrong somehow. Let me re-verify with different chars.

Actually let me investigate more carefully — could there be A's interfering somewhere?

Actually let me think about it: maybe the "stop codon" idea has merit. If certain sequences read as "stop codons" (like AAA), they truncate the gene. The (2,11) case has CCC at codon 2 and codon 11 = many AAA stop codons in between, and others above.

But other pairs also have AAA between. So why is (2,11) special?

Maybe the "open reading frame" starts at certain positions. If reading starts at position 1, codons are aligned 1-3, 4-6, etc. But if reading is shifted, codon framing differs.

Let me test (2,11) with D's instead of C's, to see if that changes anything.

## 2026-06-28 15:36 — query 281

## (2,11) anomaly
codon dist 9, mod3=2:
- (2,11): 0
- (5,14): 1

(2,11) goes from codon 2 (early) to codon 11. (5,14) goes 5→14.

Both span 9 codons. (2,11) crosses chain boundaries somehow?

Actually I wonder if the rule has to do with how many "passes" through certain chains.

OR maybe I made an error in (5,14). Let me reverify.

(5,14) sequence: "AAAAAAAAAAAAAC AAAAAAAAAAAAAAAAAAAAAAAAAA CAAAAAAA"
Wait that should be: A(1-13)=13 A's, C(14), A(15-40)=26 A's, C(41), A(42-48)=7 A's. Total 13+1+26+1+7=48 ✓.

Codon 5 pos 2 = 14 ✓
Codon 14 pos 2 = 41 ✓

Looks correct.

(2,11): A(1-4)=4, C(5), A(6-31)=26, C(32), A(33-48)=16. 4+1+26+1+16=48 ✓.
Codon 2 pos 2 = 5 ✓
Codon 11 pos 2 = 32 ✓

Both correct. Yet different fits.

Hmm. Let me think...
- (5,14): codons 5 and 14. 5=2*3-1, 14=5*3-1.
- (2,11): codons 2 and 11. 2=1*3-1, 11=4*3-1.

Codon numbers:
2 → (2-1)/3 = chain position 1 in mod3=2 chain. Chain order: 2,5,8,11,14.
11 → chain pos 4 in mod3=2.
So (2,11) = chain dist 3 in mod3=2 chain.

5 → chain pos 2. 14 → chain pos 5. Chain dist 3.

Same chain dist! Yet different fits.

Argh.

Different starting chain position:
(2,11) = chain[1..4]
(5,14) = chain[2..5]

Within mod3=2 chain (5 slots: 2,5,8,11,14):
chain pair → fit:
(1,2)=(2,5): 1 ✓
(1,3)=(2,8): 0 ✓
(1,4)=(2,11): 0
(1,5)=(2,14): ?
(2,3)=(5,8): 1 ✓
(2,5)=(5,14): 1
(3,4)=(8,11): 1
(3,5)=(8,14): ?
(4,5)=(11,14): 1

Same pattern as mod3=1 chain! In mod3=1 chain (6 slots), chain dist 3 worked sometimes. In mod3=2 chain (5 slots), chain dist 3 = (1,4) → 0, (2,5) → 1.

In mod3=1 chain, chain dist 3 results: (1,4)=(1,10)→1, (2,5)=(4,13)→1, (3,6)=(7,16)→1. So all three pairs at chain dist 3 in mod3=1 give 1. But in mod3=2 chain, (1,4) gives 0 while (2,5) gives 1.

Different structure for different chains.

Maybe the chains have different "sizes" — mod3=1 has 6 codons spanning whole 16, mod3=2 has 5 codons.

Actually maybe the rule is at the level of CHAIN POSITION 1 — chain dist 3 from chain pos 1 doesn't work in mod3=2 chain. But that means (2,11) is across two chains in some sense.

Maybe the rule depends on absolute positions, not chain positions.

(1,10) ✓: chars 2, 29
(2,11): chars 5, 32 ✗
(3,12) ✓: chars 8, 35
(4,13) ✓: chars 11, 38
(5,14) ✓: chars 14, 41
(6,15): chars 17, 44 → ✓
(7,16) ✓: chars 20, 47

So (2,11) is the only spacing-9 pair giving 0. Anomaly.

Position 5 and 32: positions mod some N?
- mod 9: 5 mod 9 = 5, 32 mod 9 = 5
- mod 18: 5 mod 18 = 5, 32 mod 18 = 14
- mod 6: 5 mod 6 = 5, 32 mod 6 = 2

Other pairs:
(1,10): 2,29 mod 18 = 2, 11
(3,12): 8,35 mod 18 = 8, 17
(4,13): 11,38 mod 18 = 11, 2
(5,14): 14,41 mod 18 = 14, 5
(6,15): 17,44 mod 18 = 17, 8
(7,16): 20,47 mod 18 = 2, 11
(2,11): 5,32 mod 18 = 5, 14

Hmm (2,11) mod 18 = 5, 14. Compare (5,14) mod 18 = 14, 5. Different order!

Maybe the "first" char's position mod 18 needs to be ≤ second? Let's check:
(1,10): 2 ≤ 11 ✓ fit 1
(3,12): 8 ≤ 17 ✓ fit 1
(4,13): 11 ≤ 2 ✗ → would be 0. But fit 1!

So that's not the rule either.

Let me think about it yet differently. Maybe scoring is computed as a weighted count of certain "good" k-mer patterns. The complexity is getting beyond easy fitting. Let me brute test more pair patterns to characterize the rule's symmetry.

## 2026-06-28 15:36 — query 287

## Pair (i,j) ACA + AAA → fit (definitively tested):
Adjacent: (1,2)=0, (15,16)=0
Spacing 2: (1,3)=0, (2,4)=0
Spacing 3: (1,4)=1, (2,5)=1, (3,6)=1, (4,7)=1, (5,8)=1, (8,11)=1, (10,13)=1, (11,14)=1, (13,16)=1
Spacing 6: (1,7)=0, (2,8)=0, (4,10)=0, (8,14)=0
Spacing 9: (1,10)=1, (3,12)=1, (4,13)=1, (5,14)=1, (6,15)=1, (7,16)=1, (2,11)=0 ⚠ANOMALY⚠
Spacing 12: (1,13)=0, (2,14)=0
Spacing 15: (1,16)=1

So mostly pair gives 1 iff codon-spacing is odd multiple of 3 (3,9,15) [≡3 mod 6].

Anomaly: (2,11) gives 0 despite spacing 9.

Maybe I have an error in (2,11). Let me re-test once more with different config.

## 2026-06-28 15:37 — query 290

## Hypothesis: maybe scoring involves "phase" of position modulo some larger number
Let me look at codon spacing 9 pairs and their starting char positions:
(1,10): start char 1 (codon 1 starts at char 1)
(2,11): start char 4
(3,12): start char 7
(4,13): start char 10
(5,14): start char 13
(6,15): start char 16
(7,16): start char 19

Wait, "codon i starts at char 3i-2":
codon 1: char 1
codon 2: char 4
codon 3: char 7
codon 4: char 10
codon 5: char 13
codon 6: char 16
codon 7: char 19
codon 8: char 22

start char positions:
(1,10) → starts 1,28
(2,11) → starts 4,31
(3,12) → starts 7,34
(4,13) → starts 10,37
(5,14) → starts 13,40
(6,15) → starts 16,43
(7,16) → starts 19,46

Modulo 18:
(1,10) → 1,10
(2,11) → 4,13
(3,12) → 7,16
(4,13) → 10,1
(5,14) → 13,4
(6,15) → 16,7
(7,16) → 1,10

Same as (1,10). Hmm.

Modulo 6 of codon i:
i mod 6:
1→1, 2→2, 3→3, 4→4, 5→5, 6→0, 7→1, 8→2, 9→3, 10→4, 11→5, 12→0, 13→1, 14→2, 15→3, 16→4

Pair (i,j) → (i mod 6, j mod 6):
(1,10) → (1,4)
(2,11) → (2,5) → fit 0!
(3,12) → (3,0)
(4,13) → (4,1)
(5,14) → (5,2)
(6,15) → (0,3)
(7,16) → (1,4)

So (2,11) has mod6 = (2,5). Others have (1,4),(3,0),(4,1),(5,2),(0,3). All others are "complementary mod 6"? Pairs:
(1,4): 1+4=5
(2,5): 2+5=7
(3,0): 3
(4,1): 5
(5,2): 7
(0,3): 3
(1,4): 5

Sums mod 6: 5, 7→1, 3, 5, 7→1, 3, 5.

For fit 1: sums 5, 3, 5, 1, 3, 5 (excluding (2,11)).
For fit 0: (2,11) sum 7→1.

Mixed. Not clean.

Let me think more concretely. (2,11): codon 2 and codon 11. 
2 is in mod3=2 class, 11 is in mod3=2 class.
Within mod3=2 chain (codons 2,5,8,11,14): 
- chain pos 1: codon 2
- chain pos 4: codon 11

Maybe the rule for chain dist 3 in mod3=2 chain is: only pair (chain pos 2,5)=(5,14) gives 1, not (chain pos 1,4)=(2,11)?

But chain has only 5 slots so (chain 1,4) and (chain 2,5) are only chain-dist-3 pairs.

Let me check mod3=0 chain (codons 3,6,9,12,15):
chain dist 3 = (chain 1,4)=(3,12) → 1 (already tested)
chain dist 3 = (chain 2,5)=(6,15) → 1 (already tested)

Both work in mod3=0 chain. So why does (2,11) in mod3=2 chain fail?

Hmm. Maybe my (2,11) test had an unnoticed error. Let me triple-verify with very simple sequence.

## 2026-06-28 15:37 — query 291



## 2026-06-28 15:38 — query 291

## REVISED MODEL (after fixing errors)
Pair (i,j) of good codons with ACA (or any C/D in pos2, A/B elsewhere) → fit 1 iff j-i ∈ {3,9,15}.

Actually I should check: maybe rule is just "j-i ≡ 3 mod 6" (i.e., odd multiple of 3).
- spacing 3 ✓ (1)
- spacing 9 ✓ (1)
- spacing 15 ✓ (1)
- spacing 6 ✗ (0)
- spacing 12 ✗ (0)
- spacing 1,2,4,5,7,8,10,11,13,14 ✗ (0)

So pair contributes 1 iff spacing ≡ 3 mod 6.

Now multi-codon fitness: 
- Total pairs with valid spacing: count them
- Map count → fit

For all 16 good: 
- spacing 3 pairs: 13 (pairs (i,i+3) for i=1..13)
- spacing 9 pairs: 7
- spacing 15 pairs: 1
- Total: 21. fit = 9.

For 12 consecutive good (1-12):
- spacing 3: 9 pairs
- spacing 9: 3
- spacing 15: 0
- Total: 12. fit = 6.

For chain mod3=1 (codons 1,4,7,10,13,16, 6 codons):
- spacings: among these, j-i values are all multiples of 3: 3,6,9,12,15.
- Valid (mod 6 = 3): 3, 9, 15.
- Pairs at spacing 3: (1,4),(4,7),(7,10),(10,13),(13,16) = 5
- Spacing 9: (1,10),(4,13),(7,16) = 3
- Spacing 15: (1,16) = 1
- Total: 9 valid pairs. fit = 6.

For (1,4,7,10,13) chain (5 good codons):
- spacing 3: 4 pairs (1,4),(4,7),(7,10),(10,13)
- spacing 9: 2 pairs (1,10),(4,13)
- spacing 15: 0
- Total: 6. fit = 4.

For (1,4,7,10):
- spacing 3: 3 pairs
- spacing 9: 1 pair (1,10)
- Total: 4. fit = 4.

For (1,4,7):
- spacing 3: 2 pairs (1,4),(4,7)
- Total: 2. fit = 2.

For (1,4):
- 1 pair. fit = 1.

So mapping pair_count → fit:
21:9, 18:8, 16:7, 14:6, 12:6, 10:5, 8:4, 6:4, 5:3, 4:4 (??), 4:2 (??), 2:2, 1:1, 0:0

Wait (1,4,7,10) has 4 valid pairs and fit 4. (1,4,7,10,13) has 6 pairs and fit 4. Inconsistent!

Let me check: for (1,4,7,10) I got fit 4 (exp 127).
Pairs: (1,4)s3, (4,7)s3, (7,10)s3, (1,7)s6 NO, (4,10)s6 NO, (1,10)s9 YES = 4 valid.
fit 4 / 4 pairs = 1 each.

For (1,4,7,10,13): pairs = 4 from before + new ones with 13:
(1,13)s12 NO, (4,13)s9 YES, (7,13)s6 NO, (10,13)s3 YES = 2 new.
Total = 6 pairs. fit = 4. So 6 pairs → 4 fit (not 6).

Inconsistency! Maybe pair count isn't directly the fit.

Hmm, but for 4 pairs → 4 fit, that's 1:1. And for (1,4) 1 pair → 1 fit. For chain mod3=1 9 pairs → 6 fit. Not 1:1 generally.

Maybe there's "diminishing returns" or saturation. Let me look at single-run data:
k=4: 1 pair (s3) → fit 1
k=5: 2 pairs (2 s3) → fit 1 (got 1)
k=6: 3 pairs (3 s3) → fit 2
k=7: 4 pairs (4 s3) → fit 2
k=8: 5 pairs (5 s3) → fit 3
k=9: 6 pairs (6 s3) → fit 4
k=10: 7 s3 + 1 s9 = 8 → fit 4
k=11: 8 s3 + 2 s9 = 10 → fit 5
k=12: 9+3=12 → fit 6
k=13: 10+4=14 → fit 6
k=14: 11+5=16 → fit 7
k=15: 12+6=18 → fit 8
k=16: 13+7+1=21 → fit 9

Map pairs to fit:
1→1, 2→1, 3→2, 4→2, 5→3, 6→4 (!), 8→4, 10→5, 12→6, 14→6, 16→7, 18→8, 21→9

Hmm 6→4 but 4→2. Let me check 6 again. k=9 gave fit 4 (exp 178).
k=10 had 8 pairs → fit 4 (exp 79 measured 4 for L=10).
k=9 has 6 pairs → fit 4 (exp 178 = 4).

So 6→4 and 8→4. Then 10→5, 12→6.

Could it be fit = floor((pairs+1)/2.5) or some other formula?
1: (2)/2.5=0.8→0. Got 1. ✗

Let me look at increments. pairs: fit:
1: 1
2: 1
3: 2
4: 2
5: 3
6: 4
7: ? (k=9 has 6 pairs, no test for 7 pairs directly... but k=10 has 8 pairs)
8: 4
9: ?
10: 5
12: 6
14: 6
16: 7
18: 8
21: 9

Strange: 6→4, 8→4 (no change), 10→5, then steady.

Maybe fit isn't pair-count based but something else.

Let me think about RUNS at codon-spacing 3. Maybe scoring counts "chains" of good codons spaced 3 apart.

For k consecutive good codons (1..k), the codons spaced 3 apart form 3 chains:
chain A (mod 3=1): 1,4,7,...
chain B (mod 3=2): 2,5,8,...
chain C (mod 3=0): 3,6,9,...

For k=9: chains have ceil(9/3)=3 codons each (3,3,3 codons). Runs of 3 each.
For k=8: chains have 3,3,2.
For k=10: 4,3,3.

Run length L in chain → contribution?
For 6-codon mod3=1 chain (k=16, ranges 1,4,7,10,13,16): contribution to fit = 6
For 5-codon mod3=2 chain (k=16, 2,5,8,11,14): contribution = ?
For 5-codon mod3=0 chain (k=16, 3,6,9,12,15): contribution = ?

If total fit = sum of chain contributions, and 16g gives fit 9: 
6 + ? + ? = 9 → ? + ? = 3. So each non-mod3=1 chain contributes 1.5 → wait but full chain mod3=2 alone gave fit 4. So that contradicts additive.

Unless full chains alone is "max possible" not actual contribution.

Hmm this is intricate. Let me explore more.

## 2026-06-28 15:38 — query 291

## Within-chain run analysis
Each codon belongs to one of 3 chains (mod 3 of codon index, considering 1-based):
chain A (i ≡ 1 mod 3): codons 1,4,7,10,13,16 (6 slots)
chain B (i ≡ 2 mod 3): codons 2,5,8,11,14 (5 slots)
chain C (i ≡ 0 mod 3): codons 3,6,9,12,15 (5 slots)

Within each chain, good codons form runs (consecutive good slots).
Run of length L in a chain contributes some f(L) to fitness.

For 16 consecutive good (k=16): 
- chain A: one run of 6, contributes f(6)
- chain B: one run of 5, contributes f(5)
- chain C: one run of 5, contributes f(5)
- Total: f(6) + 2*f(5) = 9

For chain A alone all good (6 codons): f(6) = 6
For chain B alone all good (5 codons): f(5) = 4
For chain C alone all good (5 codons): f(5) = 4

Then 16g would be f(6)+f(5)+f(5) = 6+4+4 = 14. Capped at 9. Hmm but maybe capped.

For k=12 consecutive (codons 1-12):
- chain A: codons 1,4,7,10 → 4 in chain, contiguous → run length 4
- chain B: 2,5,8,11 → run length 4
- chain C: 3,6,9,12 → run length 4
- Total = 3*f(4) = fit 6 → f(4) = 2

For (1,4,7,10) only: 
- chain A: 1,4,7,10 = 4 contiguous → f(4) = 2
- chain B,C: 0
- Total = 2. But got fit 4 ✗

Doesn't fit additive model.

Hmm.

What if scoring is by chain but each chain has its own max contribution?
Chain A: max contribution 6 (when all 6 codons good)
Chain B: max contribution 4 (when all 5 good)
Chain C: max contribution 4 (when all 5 good)

For (1,4,7,10): chain A has 4 codons (run of 4). Without rest of chain, run is internal.
For chain A alone with 4 codons: fit 4. So a run of 4 in chain A → contribution 4.

Run of 5 in chain A: codons 1,4,7,10,13 → fit 4 (tested).
Run of 6 in chain A: → fit 6.

Hmm run 4 → 4, run 5 → 4, run 6 → 6.

For chain B with 5 codons all good (run 5): fit 4.

For (4,7,10,13) — chain A run starting at position 2 of chain (length 4): fit was 4 (tested earlier). Same as (1,4,7,10).

So a run of 4 in chain A (anywhere) gives 4 alone. Run of 3 in chain A?
(1,4,7) gave fit 2.

So within-chain run length contribution table for chain A:
L=1: 0
L=2: 1 (e.g., (1,4))
L=3: 2 ((1,4,7))
L=4: 4 ((1,4,7,10))
L=5: 4 ((1,4,7,10,13))
L=6: 6

For chain B (5 slots):
L=2 ((2,5)): 1
L=3 ((2,5,8)): ?
L=5 (all): 4

For chain C similar.

Test L=3 in chain B and L=4 in chain B.

## 2026-06-28 15:39 — query 295

## Run-in-chain contribution f(L):
L=1: 0
L=2: 1
L=3: 2
L=4: 4
L=5: 4
L=6: 6

For total fit when multiple chains involved:
16 good (each chain fully populated): chain A run 6 + chain B run 5 + chain C run 5 = 6+4+4=14, capped at 9.
Predicted: 9 ✓

12 good (1-12): each chain has run 4. 4+4+4=12, capped 9. fit = 6. 
✗ Hmm got 6 but predicted 12 (or 9 if capped). 

So additive doesn't work. Hmm.

Maybe MIN instead of SUM?
12 good: 4+4+4 - probably not min either since all chains contribute.

For (1,4,7,10): chain A run 4, B and C empty. Just chain A = 4. fit 4. ✓
For (1-12) all good: chain A run 4, B run 4, C run 4. fit 6. So contribution 4+4+4=12 → 6. Maybe avg? 12/2=6. Or max(4,4,4)+min/2?

Sum/2 = 6 ✓
For 16 good: (6+4+4)/2 = 7. Got 9. ✗

Hmm. Other formula.

Let me get more data points.

For k=15 (codons 1-15):
- chain A: 1,4,7,10,13 = run 5
- chain B: 2,5,8,11,14 = run 5
- chain C: 3,6,9,12,15 = run 5
- f values: 4+4+4=12. Got 8. 12 → 8.

For k=14:
- chain A: 1,4,7,10,13 = 5
- chain B: 2,5,8,11,14 = 5
- chain C: 3,6,9,12 = 4
- f: 4+4+4=12. Got 7.

For k=13:
- chain A: 1,4,7,10,13 = 5
- chain B: 2,5,8,11 = 4
- chain C: 3,6,9,12 = 4
- f: 4+4+4=12. Got 6.

For k=10:
- chain A: 1,4,7,10 = 4
- chain B: 2,5,8 = 3
- chain C: 3,6,9 = 3
- f: 4+2+2=8. Got 4.

For k=8:
- chain A: 1,4,7 = 3
- chain B: 2,5,8 = 3
- chain C: 3,6 = 2
- f: 2+2+1=5. Got 3.

For k=4:
- chain A: 1,4 = 2
- chain B: 2 = 1
- chain C: 3 = 1
- f: 1+0+0=1. Got 1 ✓

For k=6 (1-6):
- chain A: 1,4 = 2 (run 2)
- chain B: 2,5 = 2
- chain C: 3,6 = 2
- f: 1+1+1=3. Got 2.

Pattern for sum of chain-f values → actual fit:
k=4: 1 → 1
k=6: 3 → 2
k=8: 5 → 3
k=10: 8 → 4
k=12: 12 → 6
k=13: 12 → 6
k=14: 12 → 7
k=15: 12 → 8
k=16: 14 → 9

Hmm map is non-monotonic in k vs sum (k=12,13 both sum 12, fits 6 both).

Actually wait, k=14 has chain A 5, B 5, C 4 = 4+4+2 = 10 (not 12). Let me recompute f(5)=4, f(4)=2. So sum = 4+4+2 = 10. Got 7.

k=15: 4+4+4 = 12. Got 8.
k=16: 6+4+4 = 14. Got 9.

Let me redo all:
k=4: f(2)+f(1)+f(1) = 1+0+0 = 1. fit 1.
k=5: chain A 1,4 (2), B 2,5 (2), C 3 (1). f=1+1+0=2. fit 1.
k=6: 2,2,2. f=1+1+1=3. fit 2.
k=7: A=1,4,7(3), B=2,5(2), C=3,6(2). f=2+1+1=4. fit 2.
k=8: A=1,4,7(3), B=2,5,8(3), C=3,6(2). f=2+2+1=5. fit 3.
k=9: A=3, B=3, C=3. f=2+2+2=6. fit 4.
k=10: A=4, B=3, C=3. f=4+2+2=8. fit 4.
k=11: A=4, B=4, C=3. f=4+4+2=10. fit 5.
k=12: A=4, B=4, C=4. f=4+4+2=... wait f(4)=4 for chain B too. f=4+4+4=12. fit 6.
k=13: A=5, B=4, C=4. f=4+4+4=12. fit 6.
k=14: A=5, B=5, C=4. f=4+4+4=12. fit 7.
k=15: A=5, B=5, C=5. f=4+4+4=12. fit 8.
k=16: A=6, B=5, C=5. f=6+4+4=14. fit 9.

Wait k=13 and k=14 both have f sum 12, but fit 6 vs 7. So sum isn't determining.

Difference: k=14 has chain B run 5 (one more than k=13).

Maybe f(5) ≠ f(4). I had f(5)=4 and f(4)=4 in chain alone test. But they're equal in isolation. Maybe they differ in combination.

Actually let me redo: chain A run 5 → fit 4 (alone). chain A run 4 → fit 4 (alone). Same!

But in combination, having run 5 vs run 4 affects total. Hmm.

Maybe the formula involves PRODUCTS or MAX/MIN.

Let me try: fit = max(over chains of run length)?
k=4: max(2,1,1)=2. Got 1.✗

fit = sum_chains f(L_chain) - overlaps?

Let me try: fit = floor(sum * 9/14) or rescale:
k=16: 14*9/14=9 ✓
k=15: 12*9/14=7.7 → 7. Got 8.
k=12: 12*9/14=7.7 → 7. Got 6.

Doesn't fit.

I'll need a more nuanced model. Let me look at it as a function of (L_A, L_B, L_C) when there's one run per chain:

(0,0,0)=0, (1,1,1)=? wait that doesn't happen with k consecutive.

For k consecutive starting at codon 1:
k → (L_A, L_B, L_C):
1 → (1,0,0): fit 0
2 → (1,1,0): fit 0 (need test)
3 → (1,1,1): fit 0 (need test, k=3 not tested)
4 → (2,1,1): fit 1
5 → (2,2,1): fit 1
6 → (2,2,2): fit 2
7 → (3,2,2): fit 2
8 → (3,3,2): fit 3
9 → (3,3,3): fit 4
10 → (4,3,3): fit 4
11 → (4,4,3): fit 5
12 → (4,4,4): fit 6
13 → (5,4,4): fit 6
14 → (5,5,4): fit 7
15 → (5,5,5): fit 8
16 → (6,5,5): fit 9

This looks like... maybe fit = floor((L_A + L_B + L_C - 3) * something)?
k=4: L sum=4, fit=1 → (4-3)*1=1 ✓
k=5: 5, 1 → (5-3)*0.5=1 ✓
k=6: 6, 2 → (6-3)*0.667=2 ✓
k=7: 7, 2 → 2.67→2 ✓
k=8: 8, 3 → 3.33→3 ✓
k=9: 9, 4 → 4 ✓
k=10: 10, 4 → 4.67→4 ✓
k=11: 11, 5 → 5.33→5 ✓
k=12: 12, 6 → 6 ✓
k=13: 13, 6 → 6.67→6 ✓
k=14: 14, 7 → 7.33→7 ✓
k=15: 15, 8 → 8 ✓
k=16: 16, 9 → 8.67→8. Got 9. ✗

Almost! Maybe (k-3)*2/3:
k=16: 13*2/3=8.67 → 8 (not 9)
Off by 1 at k=16.

Or maybe fit = floor((k-3)*2/3) for k<16, and ceil or +1 at k=16? Or maybe fit = floor((k-3)/3*2 + small)?

Let me try fit = (k-3) - floor((k-3)/3) for k ≥ 3:
k=4: 1 - 0 = 1 ✓
k=5: 2 - 0 = 2 (got 1) ✗

Try fit = k - 4 + max(0, k-12)?
k=4: 0+0=0 (got 1) ✗

Try fit = number of triplets-of-3-codons spanning k consecutive good:
For k=4: 1 "triplet" of 3 spanning + 1 single? 
For k=16: 5 triplets (3+3+3+3+3+1 = 16)? = 5. Got 9. ✗

Maybe fit ≈ floor((k-3) * 2 / 3) + extras?
k=4 to 16: 0.67,1.33,2,2.67,3.33,4,4.67,5.33,6,6.67,7.33,8,8.67
Floored: 0,1,2,2,3,4,4,5,6,6,7,8,8
Actual: 1,1,2,2,3,4,4,5,6,6,7,8,9

Pattern: floor + 1 at certain points. Specifically k=4 and k=16.

Hmm or maybe fit = floor((k-3)*2/3) + (1 if k=4) + (1 if k=16)?
Pretty ad hoc.

Or fit = round((k-3)*2/3)?
k=4: 0.67→1 ✓
k=5: 1.33→1 ✓
k=6: 2→2 ✓
k=7: 2.67→3 (got 2) ✗

Or actually try fit = floor((2k-5)/3)?
k=4: 3/3=1 ✓
k=5: 5/3=1 ✓
k=6: 7/3=2 ✓
k=7: 9/3=3 (got 2) ✗

floor((2k-7)/3)?
k=4: 1/3=0 ✗

Maybe fit = k - max codons (1, ceil((16-k)/something))?

This is getting hairy. Let me just stick with the data and find best fit formula later. Time to move on and test variations.

## 2026-06-28 15:39 — query 299

## Adding (codon 2) to (1,4,7,10): fit still 4. 
g-string change: 1010010010000000 → 1110010010000000. 
Pairs: (2,5)=3 not present, (2,8)=6 NO, (2,11)=9 NO (codon 11 not good), (2,14)=12 NO. 
Adding codon 2 alone creates no new valid pair (since 2 is alone in chain B). fit unchanged ✓.

Now test adding (2,5) - chain B run 2.

## 2026-06-28 15:40 — query 301

## Adding (2,5) to (1,4,7,10) doesn't change fit
Old: codons 1,4,7,10. Pairs valid: (1,4)3, (4,7)3, (7,10)3, (1,10)9 = 4 pairs. Fit 4.
New: codons 1,2,4,5,7,10. Added pairs with codon 2: (2,5)3 = 1 new valid. Added pairs with codon 5: (2,5) already, (5,8) bad (8 not good), etc.

Actually wait — let me think about pairs more carefully. 
Pairs involving codon 5: (2,5)3, (5,8)3 — 8 not good, (5,14)9 — 14 not good. So just (2,5).
Pairs involving codon 2: (2,5)3.

Total new = 1. Should be 5 pairs total. Fit should go up if pair counting works.

But fit stayed at 4. So adding 1 pair didn't help.

Maybe the formula counts something else. Let me think about chain-based scoring:
Old: chain A = {1,4,7,10} run 4 → contrib 4. B/C empty. Total 4.
New: chain A = {1,4,7,10} run 4 (contrib 4), chain B = {2,5} run 2 (contrib 1). C empty. 
Predicted total = 5 (if additive), fit got 4.

Hmm not additive either.

Maybe MAX of chain contributions?
Old: max(4,0,0) = 4. ✓
New: max(4,1,0) = 4. ✓
For 16g: max(6,4,4) = 6. Got 9. ✗

Or fit = max + something based on others?

For k=16 (chains 6,5,5): fit 9 = 6+3? Or fit = max + count of other non-empty chains? max(6) + 2 contributing = 8 ≠ 9.

For k=12 (chains 4,4,4): fit 6 = max(4) + 2? Or 4+1+1=6 ✓
For k=11 (chains 4,4,3): fit 5 = 4+1+0? hmm
For k=10 (chains 4,3,3): fit 4 = 4 + 0 + 0?
For k=9 (chains 3,3,3): fit 4 = max(2,2,2) + 2 = 4? Sum 6, half 3, plus 1?
For k=8 (chains 3,3,2): fit 3 = max(2)+ ?

Maybe fit = floor(sum / 2)?
k=12: sum=12, /2=6 ✓
k=11: 10/2=5 ✓
k=10: 8/2=4 ✓
k=9: 6/2=3 (got 4) ✗
k=16: 14/2=7 (got 9) ✗

Maybe fit = sum/2 except for runs ≥ 5?

I think we need to test more configurations.

## 2026-06-28 15:41 — query 305

## Chain combinations:
- Just chain A run 4: 4
- Chain A run 4 + chain B run 4: 5
- Chain A run 4 + chain C run 4: 5
- Chain A,B,C run 4 each (k=12 consecutive): 6

Pattern: chains contribute independently? 1 chain gives 4, 2 chains give 5, 3 chains give 6?

Let me see chain A run 5 only (codons 1,4,7,10,13): fit 4 (tested).
Chain A run 6 only (codons 1,4,7,10,13,16): fit 6.
Chain B run 5 (codons 2,5,8,11,14): fit 4.

So mid-large runs cap at 4, then jump.

For run 6 in chain A: fit 6. Big jump.

Maybe the run-length contribution is non-monotonic. Let me think:
L=1: 0
L=2: 1
L=3: 2
L=4: 4
L=5: 4 (plateau)
L=6: 6

If we then add other chain contributions:
1 chain run 4: 4
2 chains run 4 each: 5 (= 4+1)
3 chains run 4 each: 6 (= 4+2)

So additional chains add 1 each.

For all-good (chain A 6, B 5, C 5): fit 9. 
Predict: f(A=6) + extra(B=5) + extra(C=5) = 6 + ? + ? = 9 → extras sum to 3, ~ 1.5 each?

If extras are floor((L+1)/2) or something:
extra(L=5) = 1.5 each ≈ 1 or 2.

Hmm. Let me test chain A only run 6 (codons 1,4,7,10,13,16) = 6.
Plus chain B run 5 (codons 2,5,8,11,14): together?
That's codons 1,2,4,5,7,8,10,11,13,14,16 = 11 codons.

Let me build this:
C at codon-pos-2 for those codons: 2,5,11,14,20,23,29,32,38,41,47.

I'll test this.

## 2026-06-28 15:41 — query 307

## Final theory test using pair count
For each pair (i,j) of good codons with j-i ∈ {3,9,15}: counts as 1 "valid pair".

Predict fit = some function of valid pair count.

Single-run k consecutive good codons:
k=1: 0 pairs, fit 0 ✓
k=2: 0 pairs, fit 0 ✓
k=3: 0 pairs, fit 0
k=4: 1 pair (1,4), fit 1 ✓
k=5: 2 pairs (1,4),(2,5), fit 1 ✓
k=6: 3 pairs (1,4),(2,5),(3,6), fit 2 ✓
k=7: 4 pairs +(4,7), fit 2 ✓
k=8: 5 pairs +(5,8), fit 3 ✓
k=9: 6 pairs +(6,9), fit 4 (jump!)
k=10: 7+(1,10)spacing9 = 8 pairs, fit 4 ✓
k=11: 8+(2,11) = 10 pairs, fit 5 ✓
k=12: 9+(3,12) = 12 pairs, fit 6 ✓
k=13: 10+(4,13) = 14 pairs, fit 6 ✓
k=14: 11+(5,14) = 16 pairs, fit 7 ✓
k=15: 12+(6,15) = 18 pairs, fit 8 ✓
k=16: 13+7+1 = 21 pairs, fit 9 ✓

Map pair count → fit:
0:0, 1:1, 2:1, 3:2, 4:2, 5:3, 6:4, 8:4, 10:5, 12:6, 14:6, 16:7, 18:8, 21:9

Increments: +1, 0, +1, 0, +1, +1, 0(skip), +1, +1, 0, +1, +1, +1
At pair counts: 0→1, 1→2, 2→3, 3→4, 4→5, 5→6, 6→8, 8→10, 10→12, 12→14, 14→16, 16→18, 18→21

Hmm hard to see pattern. Let me try fit = floor(pairs * f) with adjustments.

Actually look at it: fit = floor((pairs + something) * 9 / 21)?
pair=21: 21*9/21=9 ✓
pair=18: 7.71→7 (got 8) ✗

fit = ceil(pairs * 9 / 21)?
21: 9 ✓
18: 7.71→8 ✓
16: 6.86→7 ✓
14: 6 ✓
12: 5.14→6 ✓
10: 4.29→5 ✓
8: 3.43→4 ✓
6: 2.57→3 (got 4) ✗

Almost works except for pair=6 (k=9).

For k=9, fit was 4 but predicted 3.

Maybe there's something special about pair count 6 (3 chains of 3 = symmetric). Let me check whether k=9 measurement was definitely 4.

Or fit = round(pairs * 9/21):
21: 9 ✓
18: 8 ✓ (.71 rounds to 8)
16: 7 ✓
14: 6 ✓
12: 5 (got 6) ✗

OK formula's hard. Let me accept partial understanding and proceed to maximize the function with what I know.

For maximum fit, want maximum pairs = all 16 codons good = all chars = C/D at codon-pos-2 positions. The simplest: ACA repeated or CCC repeated → fit 9.

## 2026-06-28 15:42 — query 311

## Pair count isn't unique determinant
- k=9 (codons 1-9): 6 valid pairs, fit 4
- (1,4,7,10,16): 6 valid pairs, fit 5

So additional structural element matters.

Difference: (1,4,7,10,16) has codons more "spread out" with longer-range pairs.

In k=9: all pairs are spacing-3 (within chain). 3 chains × 2 pairs each.
In (1,4,7,10,16): 3 spacing-3 + 2 spacing-9 + 1 spacing-15 = 6 pairs. All within chain A.

Maybe scoring depends on COUNT of distinct pair-spacings, or weighting:
- spacing-3 pair: weight 1
- spacing-9 pair: weight ?
- spacing-15 pair: weight ?

For k=9 (6 s3 pairs, 0 s9, 0 s15): fit 4. weight_3 * 6 = 4 → w3 = 2/3.
For (1,4,7,10,16) (3 s3 + 2 s9 + 1 s15): fit 5. 3*2/3 + 2*w9 + w15 = 5 → 2 + 2w9 + w15 = 5 → 2w9 + w15 = 3.

For k=10 (codons 1-10, 7 s3 + 1 s9 + 0 s15): fit 4. 7*2/3 + w9 = 4 → 4.67 + w9 = 4 → w9 = -0.67. Negative? Weird.

Hmm, maybe weights aren't constants. Let me try:
fit = ceil(s3 * a) + ceil(s9 * b) + ceil(s15 * c) for some a,b,c.

For chain A run 6 (codons 1,4,7,10,13,16): s3=5, s9=3, s15=1. Fit 6.

For pure s3 case: fit = f(s3). 
k=4: s3=1, fit 1
k=5: s3=2, fit 1
k=6: s3=3, fit 2
k=7: s3=4, fit 2
k=8: s3=5, fit 3
k=9: s3=6, fit 4 (jump again — extra +1)

For k=9 fit is 4 but ceil(6*2/3)=4 works.
For k=10: s3=7, s9=1. Fit 4. ceil(7*2/3)=ceil(4.67)=5. +s9?
ceil(7*2/3) = 5, but fit=4. So s9 might subtract or my formula wrong.

Or maybe fit = floor(s3*2/3) + s9 stuff:
k=4: floor(2/3)=0+0=0 (got 1) ✗

Let me try: fit = ceil((s3+s9+s15)/2.4)?
k=9 (6+0+0=6): ceil(2.5)=3. Got 4. ✗

OK I'll just keep gathering data. My theory isn't crystallizing.

Let me focus on the big picture: the function is non-trivial but I have lots of empirical data. Let me try to use the remaining experiments to:
1. Verify the maximum fit (=9) is achievable many ways
2. Test if any character/pattern gives >9 (probably not)
3. Look at edge cases

## 2026-06-28 15:42 — query 315

## Sequence construction is challenging. Let me develop a method.

For codons k1, k2, ..., I need C at positions 3*k_i - 1 for each.

Algorithm: start with 48 A's. For each codon i in good list, set position 3i-1 to C.

Implementing manually is error-prone. Let me think of it as 16 slots and the chars in the codon's middle.

For codons 1,2,3,4,5,7,8,10,11,13,14,16 good. C positions: 2,5,8,11,14,20,23,29,32,38,41,47.

Between consecutive C positions, count A's needed:
- before 2: pos 1 = 1 A
- 2→5: pos 3,4 = 2 A's
- 5→8: pos 6,7 = 2 A's
- 8→11: pos 9,10 = 2 A's
- 11→14: pos 12,13 = 2 A's
- 14→20: pos 15-19 = 5 A's
- 20→23: pos 21,22 = 2 A's
- 23→29: pos 24-28 = 5 A's
- 29→32: pos 30,31 = 2 A's
- 32→38: pos 33-37 = 5 A's
- 38→41: pos 39,40 = 2 A's
- 41→47: pos 42-46 = 5 A's
- after 47: pos 48 = 1 A

Total chars: 1 + 12 (C count) + 2+2+2+2+5+2+5+2+5+2+5 + 1 = 1+12+34+1 = 48 ✓

Sequence: A + C + AA + C + AA + C + AA + C + AA + C + AAAAA + C + AA + C + AAAAA + C + AA + C + AAAAA + C + AA + C + AAAAA + C + A

Let me concat: A C AA C AA C AA C AA C AAAAA C AA C AAAAA C AA C AAAAA C AA C AAAAA C A

= "ACAACAACAACAACAAAAACAACAAAAACAACAAAAACAACAAAAACA"

Length: 1+1+2+1+2+1+2+1+2+1+5+1+2+1+5+1+2+1+5+1+2+1+5+1+1 = let me add: 1+1=2, +2=4, +1=5, +2=7, +1=8, +2=10, +1=11, +2=13, +1=14, +5=19, +1=20, +2=22, +1=23, +5=28, +1=29, +2=31, +1=32, +5=37, +1=38, +2=40, +1=41, +5=46, +1=47, +1=48 ✓

So the correct sequence is "ACAACAACAACAACAAAAACAACAAAAACAACAAAAACAACAAAAACA"

## 2026-06-28 15:43 — query 316

## 12 codons good (missing 6,9,12,15) → fit 9!
Codons missing: 6,9,12,15 = chain C indices 2,3,4,5 (chain C codons are 3,6,9,12,15).

So chain C had only codon 3 good (1 codon), chain A: all 6, chain B: all 5.

Per chain run model: chain A run 6 (=6) + chain B run 5 (=4) + chain C run 1 (=0) = 10 by my f values. capped at 9 → 9.

Hmm. Let me check chain A + chain B with no chain C entries:
codons 1,2,4,5,7,8,10,11,13,14,16 = 11 codons → tested earlier (110 pattern) → fit 7.

Difference: with chain C codon 3 added → fit 9 (jump of 2).

So adding codon 3 (just 1 codon!) bumped fit by 2.

That suggests pairs (3,6)NO (6 not good), (3,12)NO (12 not good), (3,15)NO... actually pairs of 3 with anything spacing 3,9,15: (3,6),(3,12) etc — all need 6,12,etc to be good. They aren't.

But wait — pairs of 3 with chain A or B codons: (3,?)— 3 is in chain C. j-i ∈ {3,9,15}: j ∈ {6,12,18(N/A)}. None are good (except maybe with multi-chain numbers? No).

So adding 3 alone adds 0 valid pairs. But fit jumped 7→9. Why?

Maybe my pair model is wrong and the actual rule involves something else.

Let me test with codon 3 removed: codons 1,2,4,5,7,8,10,11,13,14,16 (11 codons) — already 7.
With codon 3: 12 codons → 9.

So codon 3 adds 2 to fit?

Try removing different codons:
Codons 1,2,3,4,5,7,8,10,11,13,14,16 (12 codons) = 9.
Remove codon 3: 11 codons = 7.
Remove codon 8: ?
Remove codon 13: ?

## 2026-06-28 15:43 — query 319

## 12 codons → 9, 11 codons → 7 or 8 depending which removed
- {1,2,3,4,5,7,8,10,11,13,14,16}: fit 9 (full chain A, B; chain C only codon 3)
- Remove 16: fit 7
- Remove 13: fit 8  
- Remove 8: fit 8

So codon 16 removal drops by 2 (9→7). Codon 13 or 8 drops by 1.

Lots of variability. Let me reconsider.

Actually maybe the model is per-chain with chain "completion" bonus.

Chain A (codons 1,4,7,10,13,16): 6 slots
Chain B (codons 2,5,8,11,14): 5 slots
Chain C (codons 3,6,9,12,15): 5 slots

For each chain, count good codons = n. Run structure?

For 12-codon set {1,2,3,4,5,7,8,10,11,13,14,16}:
- Chain A: 1,4,7,10,13,16 = 6 (full)
- Chain B: 2,5,8,11,14 = 5 (full)
- Chain C: 3 = 1

Remove 16:
- Chain A: 1,4,7,10,13 = 5
- Chain B: 5
- Chain C: 1
fit 7

Remove 13:
- Chain A: 1,4,7,10,16 = 5 (with gap at slot 5)
- Chain B: 5
- Chain C: 1
fit 8

Remove 8:
- Chain A: 6
- Chain B: 2,5,11,14 = 4 (with gap at slot 3)
- Chain C: 1
fit 8

Different chain configurations give different fits. Hmm.

Wait — remove 16 (chain A → run 5) vs remove 13 (chain A → 1,4,7,10,16 broken into runs of 4 and 1). Same total chain A good = 5, but different RUNS.

For chain A alone, run 5 (contiguous): fit 4.
For chain A alone, runs (4,1) — e.g., (1,4,7,10,16): tested = 5 (got fit 5 in exp 310). Interesting — broken into (4,1) gives MORE than run 5!

Run 5 contiguous: 4
Runs (4,1) split with gap: 5 (?)

Let me also test runs (5) split (e.g., (1,4,7,10,13) chain A = 4, vs (1,4,7,10,16) = 5).

Actually let me check (1,4,7,10,16): is fit really 5?

Exp 310: "ACAAAAAAAACAAAAAAAACAAAAAAAACAAAAAAAAAAAAAAAAACA" → fit 5.

C positions: 2, 11, 20, 29, 47. Codons 1,4,7,10,16. Yes 5 codons in chain A. Fit 5.

Versus run-5 contiguous (1,4,7,10,13) — fit 4 (multiple tests).

So with 5 codons in chain A, (1,4,7,10,16) > (1,4,7,10,13). Position matters.

Interesting. Maybe the rule treats chain ends specially. Codon 16 = chain end = bonus?

Let me test: (4,7,10,13,16) chain A run 5 starting at slot 2. Got fit 4 in exp 129.

vs (1,4,7,10,13) = fit 4.

So including codon 1 or codon 16 (chain endpoints) doesn't help by itself with contiguous run.

But (1,4,7,10,16) (skipping 13) = 5. Skipping interior helps?

## 2026-06-28 15:44 — query 324

## Chain A patterns (within just chain A):
6 codons all: 6
5 codons:
- (1,4,7,10,13) run-5: 4
- (4,7,10,13,16) run-5: 4
- (1,4,7,10,16) skip 13: 5
- (1,4,7,13,16) skip 10: 5
- (1,4,10,13,16) skip 7: 5
- (1,7,10,13,16) skip 4: 5
4 codons:
- (1,4,7,10): 4
- (1,7,10,16) skip 4,13: 3

Hmm runs in chain A → fit:
For 5 codons:
- contiguous run-5 (e.g., 1,4,7,10,13): 4
- 1 gap (e.g., 1,4,7,10,16 = run 4 + run 1): 5
- runs 4+1 split: 5

For 4 codons:
- run-4 (1,4,7,10): 4
- runs 1+1+1+1 — like just codons 1,7,10,16 (gaps at 4,13): 3? Let me see: (1,7,10,16) has runs of (1, 2, 1). f sum?

(1,7,10,16) = chain slots 1,3,4,6. Runs in chain order: 1, 2, 1 (slot 1 isolated, slots 3-4 = run 2, slot 6 isolated).
3 separate runs.

If f(1)=0, f(2)=1: sum = 0+1+0 = 1. Got 3. ✗

Or by pair count: in this set, pairs of good codons with j-i ∈{3,9,15}:
(1,7)=6 NO
(1,10)=9 YES
(1,16)=15 YES
(7,10)=3 YES
(7,16)=9 YES
(10,16)=6 NO
Valid pairs: 4. fit=3.

For (1,4,7,10,16): pairs:
(1,4)3 YES, (1,7)6 NO, (1,10)9 YES, (1,16)15 YES, (4,7)3 YES, (4,10)6 NO, (4,16)12 NO, (7,10)3 YES, (7,16)9 YES, (10,16)6 NO
Valid: 6. fit=5.

For (1,4,7,10,13) consecutive: pairs (1,4),(4,7),(7,10),(10,13),(1,10),(4,13) = 6 valid. fit=4.

Same 6 pairs, fit 5 vs 4. Different by case.

Difference: (1,4,7,10,16) has a spacing-15 pair (1,16). (1,4,7,10,13) doesn't.

So spacing-15 pair might be "worth more" than others.

Let me weigh: maybe spacing-3 worth 1, spacing-9 worth 1, spacing-15 worth more.

(1,4,7,10,16): 4 s3 + 2 s9 + 0 s15... wait I had (1,16)=spacing 15. Let me recount.
(1,4)3, (4,7)3, (7,10)3 = 3 s3 pairs.
(1,10)9, (1,16)15, (7,16)9 = 1 s9, 1 s15, 1 s9 = 2 s9 + 1 s15.

3 s3 + 2 s9 + 1 s15 = 6 pairs, fit 5.

(1,4,7,10,13): 4 s3 (1,4),(4,7),(7,10),(10,13) + 2 s9 (1,10),(4,13) + 0 s15 = 6 pairs, fit 4.

Diff: 4 vs 5 with same total pairs. The s15 pair from first gives +1.

For (1,7,10,16): 
s3: (7,10) = 1
s9: (1,10), (7,16) = 2
s15: (1,16) = 1
Total: 4 pairs, fit 3.

If s15 = 2 points: 1+2+2 = 5? No, fit 3.

Hmm. Let me try fit = s3 + s9 + 2*s15 - something:
(1,4,7,10,13): 4 + 2 + 0 = 6, fit 4. So formula = pairs - 2? But k=4 (1 pair) → 1 fit, not -1.

Try fit = number of valid pairs in chain A (or any single chain), capped:
(1,4,7,10,16): pairs in chain A = (1,4),(1,10),(1,16),(4,7),(7,10),(7,16) = 6 valid. fit 5.
Hmm but k=9 has chain A pairs (1,4),(4,7),(7,10) + chain B (2,5),(5,8) + chain C (3,6),(6,9). All s3. Total 7. Wait I counted 6 earlier. Let me recount.

k=9 valid pairs:
chain A {1,4,7}: (1,4),(4,7) — wait 9 codons consecutive includes chain A 1,4,7 (run 3). Pairs in chain A: (1,4),(4,7) = 2 spacing-3 pairs.
chain B {2,5,8}: (2,5),(5,8) = 2.
chain C {3,6,9}: (3,6),(6,9) = 2.
Total: 6 spacing-3 pairs.
s9: none (need codon ≥10).
s15: none.
Total 6 valid. fit 4.

Compare (1,4,7,10,16) chain A only with 6 pairs. fit 5.

So 6 pairs in single chain → 5, 6 pairs across 3 chains → 4. 

Maybe single-chain pairs are worth more than cross-chain? But all my pairs are within chain (j-i = 3,9,15 always preserves chain).

Wait — pair spacings 3 mean i,j differ by 3, so same mod-3 class. So all valid pairs are within-chain. ✓

So all pairs are "within-chain pairs". Yet different fit for k=9 (3 chains with 2 pairs each = 6) vs (1,4,7,10,16) (single chain with 6 pairs).

Maybe fit depends on max pairs in any single chain + bonus for additional chains?

k=9: max chain pairs = 2. Bonus for B and C = 2 each? 2 + 2 = 4? ✓
(1,4,7,10,16): max = 6 (all in chain A). Bonus = 0. Predict 6. Got 5.

Nope.

Or fit = max_chain_pairs + extra_chains_pairs * weight?
k=9: 2 + 2*2*weight = 4. weight = 0.5.
(1,4,7,10,16): 6 + 0 = 6. Got 5.

Inconsistent.

Let me move on and look at the broader pattern. I'll keep testing.

## 2026-06-28 15:44 — query 324

## New approach: enumerate specific "scoring pairs"
There are 16 codon slots. Pairs with spacing ∈ {3,9,15}:
spacing 3 pairs: (1,4),(2,5),(3,6),(4,7),(5,8),(6,9),(7,10),(8,11),(9,12),(10,13),(11,14),(12,15),(13,16) = 13 pairs
spacing 9 pairs: (1,10),(2,11),(3,12),(4,13),(5,14),(6,15),(7,16) = 7 pairs  
spacing 15 pairs: (1,16) = 1 pair
Total = 21 pairs.

Each pair has unique structural role. Maybe scoring is sum over (specific subsets) of "AND" of good codons.

Earlier: chain A run 6 (all 6 chain A codons): valid pairs in chain A only:
spacing-3: 5 pairs (1,4),(4,7),(7,10),(10,13),(13,16)
spacing-9: 3 (1,10),(4,13),(7,16)
spacing-15: 1 (1,16)
Total 9. fit 6.

For chain A subset (1,4,7,10,13): valid pairs:
s3: 4 (1,4),(4,7),(7,10),(10,13)
s9: 2 (1,10),(4,13)
s15: 0
Total 6. fit 4.

For chain A subset (1,4,7,10,16): 
s3: 3 (1,4),(4,7),(7,10)
s9: 2 (1,10),(7,16)
s15: 1 (1,16)
Total 6. fit 5.

For chain A subset (4,7,10,13,16):
s3: 4 (4,7),(7,10),(10,13),(13,16)
s9: 2 (4,13),(7,16)
s15: 0
Total 6. fit 4.

For (1,4,7,13,16):
s3: 2 (1,4),(4,7),(13,16) wait (13,16) is in this set... (1,4)3, (4,7)3, (13,16)3 = 3 s3
s9: (4,13)9, (7,16)9 = 2 s9
s15: (1,16)15 = 1 s15
Total 6. fit 5.

For (1,4,10,13,16):
s3: (1,4),(10,13),(13,16) = 3
s9: (1,10),(4,13) = 2
s15: (1,16) = 1
Total 6. fit 5.

For (1,7,10,13,16):
s3: (7,10),(10,13),(13,16) = 3
s9: (1,10),(7,16) = 2
s15: (1,16) = 1
Total 6. fit 5.

For (1,7,10,16):
s3: (7,10) = 1
s9: (1,10),(7,16) = 2
s15: (1,16) = 1
Total 4. fit 3.

So 5-codon chain A subsets with (1,16) pair present give fit 5, without give fit 4. The s15 pair adds 1!

And the 4-codon (1,7,10,16) with s15 pair → fit 3.

Pattern: fit = (s3 + s9 + 2*s15) approximately, but with cap.

Wait: 
(1,4,7,10,13) consecutive: 4+2+0 = 6 + 0 bonus = 6, but fit 4. 
(1,4,7,10,16): 3+2+2 = 7, fit 5.

Let me try: fit = s3 + s9 + s15 weight 2, minus some penalty for "missing" pairs?

Or maybe think it's about cap:
chain A run 5 contiguous: 6 weighted pairs (4s3+2s9). fit 4. 
chain A 5 codons with s15: 7 weighted. fit 5.
chain A all 6: 5+3+2 = 10 weighted. fit 6 (capped at 6 for some reason).

Maybe fit per chain ≤ # codons in chain - 0? Chain A has 6, fit 6. Chain A 5 codons, fit ≤ 5.

For chain A 5 codons subset:
(1,4,7,10,13): fit 4 ≤ 5
(1,4,7,10,16): fit 5 = 5 (max)
(1,4,7,13,16): fit 5 = 5
(1,4,10,13,16): fit 5 = 5
(1,7,10,13,16): fit 5 = 5
(4,7,10,13,16): fit 4 ≤ 5

So (1,4,7,10,13) and (4,7,10,13,16) — the two that exclude the "endpoints" of chain (1 AND 16, or one of them) — give fit 4. Others give 5.

(1,4,7,10,13) excludes codon 16. (4,7,10,13,16) excludes codon 1. Both have all 5 contiguous in middle/end.

If chain A subset must include BOTH endpoints (codons 1 AND 16) to hit max fit, that fits.

Let me think: maybe fit per chain = number of codons in chain × something, BUT with bonus when endpoints are included.

Or maybe fit = (number of codons that form chain-spanning pattern).

Let me just test predictions.

For (1,16) only: fit 1. Both endpoints. 2 codons → 1.
For (1,4,16): need to test.

## 2026-06-28 15:45 — query 332

## More puzzling data
- (1,4,7): fit 2
- (1,4,7,8): fit 3 (+1 from codon 8)
- (1,4,7,10) (instead of 8): fit 4 (+2 from codon 10)
- (1,4,7,10,13): fit 4 (codon 13 doesn't add)
- (1,2,4,7,10,13): fit 5 (codon 2 adds)

Hmm. Maybe my entire model is wrong. Let me consider whether the actual rule involves DIFFERENT features.

What if scoring counts the number of "complete codons" where pos2 ∈ {C,D} AND pos1 ∈ {C,D}? Earlier tests showed pos1 doesn't matter when pos2 is C/D for "homogeneous" patterns.

Actually let me reconsider: A and B as fillers... maybe in some cases A's at certain positions function as "stops" that truncate the read.

Let me test: codons AAA in middle of CCC. If AAA stops, then good codons after AAA don't count.

Sequence CCC*6 + AAA + CCC*9 = good codons 1-6, stop at 7, then would-be-good codons 8-16 don't count?
Actually CCC*6 + AAA + CCC*9 = 18 + 3 + 27 = 48 chars. Codons: 1-6 good, 7 bad (AAA), 8-16 good. So 15 good codons total. If stop kicks in, only first 6 count.

Earlier 6g cluster (codons 1-6) → fit 2. So if stop hypothesis right, this CCC*6+AAA+CCC*9 should give fit 2 (only first 6 count).

## 2026-06-28 15:46 — query 340

## Chain importance
- All 3 chains: fit 9
- Skip chain A: fit 6 (10g)
- Skip chain B: fit 6 (11g)
- Skip chain C: fit 7 (11g)
- Skip chain C codons 6,9,12,15 (only chain C codon 3 kept): fit 9!

Wait, "skip codons 4,7,10,13" left codon 1, 16 + chain B all + chain C all = 1+1+5+5=12 codons → fit 9.

The model is getting too complex. I should just accept that the formula is complex and use remaining experiments efficiently.

Let me also test a few practical patterns to discover any new behaviors:
- Mixed C and D characters
- D's at non-pos-2 positions
- Patterns with B's

Actually I'm running low. Let me move toward confirming the basic understanding and exploring edge cases of the codon model.

## 2026-06-28 15:46 — query 344

## Confirmed: max fit = 9.

Let me record summary findings:
1. Sequence is 48 chars, parsed as 16 codons of 3 chars each.
2. Each codon's pos 2 must be C or D for the codon to be "good".
3. A "good codon" alone gives fit 0. Multiple good codons combine non-trivially.
4. The combination function depends on the pattern of which slots are good.
5. Maximum fitness = 9, achieved when all 16 codons are good (e.g., all-C, all-D, CD alt, ACA repeated, BCB repeated).
6. Skip patterns: skipping chain C codons doesn't reduce fit as much as skipping chain A or B.

For practical purposes: to get fitness 9, ensure pos 2 of every codon (positions 2,5,8,...,47) is C or D.

I'll spend remaining experiments stress-testing this and exploring edge cases.

## 2026-06-28 15:47 — query 346

## Sequence construction is fragile and I keep introducing errors.

Given remaining experiments (154), let me focus on confirming the rule and finding any anomalies, rather than testing complex patterns I'll mis-construct.

I have strong evidence:
1. Max fit = 9 when all codons good.
2. Codon "good" = pos2 ∈ {C,D}.
3. Function from g-string → fit is complex, depends on which slots are good.
4. Single good codons give 0; need multiple "compatible" good codons.
5. Compatibility favors spacings 3, 9, 15 between good codons.

I'll use remaining experiments to:
- Sanity-check max fit with diverse sequences
- Probe boundary cases
- Try unusual char combinations

## 2026-06-28 15:47 — query 354

## Final attempt at the formula:
Define g_i = 1 if codon i has pos2 ∈ {C,D}, else 0. 

Empirically:
- f(empty) = 0
- f(all good) = 9
- Function is non-linear, non-additive in g_i

Let me try: fit = floor(g_total / 2)?
g=16: 8 (got 9) ✗
g=12 consecutive: 6 ✓
g=8 consecutive: 4 (got 3) ✗

Try fit = floor((g - g_chain_C) / something)?

Actually let me approach via what I know:
- Adding a single codon to certain configurations can bump by 1-2.
- Spacing-3, 9, 15 pairs of good codons matter.

Given my limited time and the complexity, my best practical understanding is:
**To achieve maximum fitness (9): ensure every codon position 2 (chars 2, 5, 8, ..., 47) is C or D. The 3*i-1 positions are critical.**

Let me use remaining experiments to test more patterns and confirm.

## 2026-06-28 15:48 — query 361

## Chain A endpoint observations
Chain A has slots {1,4,7,10,13,16}.
- All 6 slots good: fit 6
- 5 slots, missing slot 6 (codon 16): fit 4
- 5 slots, missing slot 1 (codon 1): fit 4
- 5 slots, missing interior slot 2,3,4, or 5: fit 5

So endpoints "matter more". Similar might hold for chains B, C.

For chain B (5 slots: 2,5,8,11,14):
- All 5: fit 4
- 4 codons, missing slot 1 (codon 2): fit ?
- 4 codons, missing interior (slot 2,3,4): fit ?

Got tests so far: (5,8,11,14) skip slot 1 (codon 2) → fit 4 (??)
Wait that's 4 codons in chain B. f(4) = 4 in isolation table. Got 4.

And (2,8,11,14) skip slot 2 (codon 5) → fit 2.

If skip slot 1 = full effective run 4 = fit 4.
If skip slot 2 = broken into runs 1+3 = fit 2.

So skipping endpoint of chain B preserves fit (still get f(run 4)=4). Skipping interior splits.

OK so the rule is: per chain, contribution = f(longest run)? Or sum of f(runs)?

Chain B (1)(3) — sum f(1)+f(3) = 0+2 = 2. ✓
Chain B (4) — f(4)=4. ✓
Chain A (5) — f(5)=4. ✓
Chain A (4)(1) — f(4)+f(1) = 4+0 = 4. But got 5! ✗

Hmm.

Let me test chain A (3)(2) — codons 1,4,7,13,16. Run 3 + run 2. f(3)+f(2)=2+1=3. Got 5.

So chain A subsets where ENDPOINTS are both present give bonus.

For chain A (1,4,7,13,16): contains codon 1 AND codon 16. → fit 5.
For chain A (1,4,7,10,13): contains codon 1, not 16. → fit 4.
For chain A (4,7,10,13,16): contains 16, not 1. → fit 4.
For chain A (1,4,7,10,16): contains both. → fit 5.

So having both endpoints adds something.

For chain A (1,16) only: contains both endpoints. fit 1.
For chain A (1,16) + interior: ?

## 2026-06-28 15:49 — query 369

## 3-codon chain A subsets all give fit 2 if they have at least one s3 or s9 pair, EXCEPT (4,10,16) which gave 0.

(4,10,16): pairs (4,10)s6 NO, (4,16)s12 NO, (10,16)s6 NO. ZERO valid pairs!
(7,10,13): pairs (7,10)s3, (10,13)s3, (7,13)s6 NO = 2 valid pairs. fit 2.
(1,4,16): (1,4)s3, (1,16)s15, (4,16)s12 NO = 2 valid pairs. fit 2.
(1,7,16): (1,7)s6 NO, (1,16)s15, (7,16)s9 = 2 valid pairs. fit 2.
(1,10,16): (1,10)s9, (1,16)s15, (10,16)s6 NO = 2 valid pairs. fit 2.
(1,4,7): 2 valid pairs (s3 each). fit 2.
(1,7,10): (1,7)s6 NO, (1,10)s9, (7,10)s3 = 2 valid pairs. fit 2.
(4,7,16): (4,7)s3, (4,16)s12 NO, (7,16)s9 = 2 valid pairs. fit 2.
(4,13,16): (4,13)s9, (4,16)s12 NO, (13,16)s3 = 2 valid pairs. fit 2.

So 3-codon subsets with 2 valid pairs → fit 2.
With 0 valid pairs → fit 0.

The PAIR COUNT model works for 3-codon subsets!

Earlier discrepancy with (1,4,7,10,13) (6 pairs → fit 4) and (1,4,7,10,16) (6 pairs → fit 5):

Wait let me recount.
(1,4,7,10,13) pairs: (1,4)3,(4,7)3,(7,10)3,(10,13)3 = 4 s3 + (1,10)9,(4,13)9 = 2 s9. Total 6. fit 4.
(1,4,7,10,16) pairs: (1,4)3,(4,7)3,(7,10)3 = 3 s3 + (1,10)9,(7,16)9 = 2 s9 + (1,16)15 = 1 s15. Total 6. fit 5.

Both have 6 pairs. Different fits. So pair count alone isn't always the determinant.

But maybe spacing 15 pair is worth +1? Or specific positions matter.

Let me also verify:
(1,4) → 1 pair → fit 1
(1,4,7) → 2 pairs → fit 2
(1,4,7,10) → 4 pairs → fit 4
(1,4,7,10,13) → 6 → fit 4
(1,4,7,10,13,16) → 9 → fit 6

So:
1 pair = 1
2 pairs = 2
4 pairs = 4
6 pairs = 4 (in this sequence)
9 pairs = 6

Differences depend on which pairs. Maybe specifically: fit = number of DISTINCT codons "involved in valid pairs"?

(1,4): both involved. Distinct = 2. fit 1.
(1,4,7): all 3 involved. Distinct = 3. fit 2.
(1,4,7,10): all 4 involved. Distinct = 4. fit 4. Hmm 4≠4-1.
(1,4,7,10,13): all 5 involved. Distinct = 5. fit 4. ≠5.
(1,4,7,10,13,16): all 6 involved. Distinct = 6. fit 6. =6.

For 3-codon subsets with 2 pairs: distinct = 3. fit 2.
For 3-codon subsets with 0 pairs (e.g. (4,10,16)): distinct = 0. fit 0.

So fit = distinct codons involved in valid pairs? Almost, but (1,4,7,10) had 4 → fit 4 but (1,4,7,10,13) had 5 → fit 4.

For (1,4,7,10,13): codons involved in pairs include all 5. fit 4. distinct=5≠4.

Maybe fit caps at certain value or formula = distinct - 1?
(1,4) 2-1=1 ✓
(1,4,7) 3-1=2 ✓
(1,4,7,10) 4-1=3 (got 4) ✗

Hmm. Or fit = floor((distinct + pairs)/2)?
(1,4) (2+1)/2=1.5→1 ✓
(1,4,7) (3+2)/2=2.5→2 ✓
(1,4,7,10) (4+4)/2=4 ✓
(1,4,7,10,13) (5+6)/2=5.5→5 (got 4) ✗

Close but not.

I'll give up trying to find clean formula. Let me record what I know for posterity.

## 2026-06-28 15:50 — query 372

## Summary of findings (Lab Notebook Final):

### Rules of this world's biology:
1. **Sequence parsing**: 48-char sequence read as 16 codons of 3 chars each.
2. **Good codon**: A codon is "good" if its position 2 (chars 2,5,8,...,47) contains C or D.
3. **Bad codon**: A codon with position 2 = A or B.
4. **A vs B and C vs D**: 
   - At pos 2: C ≡ D (good), A ≡ B (bad)
   - At pos 1, 3: char identity doesn't seem to affect fit alone (in well-defined tests)
5. **Single good codon = 0 fitness**. Multiple good codons combine non-linearly.
6. **Maximum fit = 9**, achieved when all 16 codons are good.

### Pattern of pair scoring:
- Pair (i,j) of good codons contributes (approximately) 1 to fit when j-i ∈ {3, 9, 15}.
- Other spacings (1,2,4,5,6,7,8,10,11,12,13,14) contribute 0.

### Single-run consecutive good codons L → fit table:
L: 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
f: 0 0 0 1 1 2 2 3 4 4 5 6 6 7 8 9

### To maximize fit (=9): 
- Use any sequence where char 3i-1 ∈ {C,D} for all i=1..16
- e.g., "DCDDCD..." or "ACAACA..." (repeated) or all-C/all-D

### Limitations:
- Could not derive a closed-form formula relating arbitrary g-string to fitness.
- The function appears to involve weighted pair contributions plus other structural features I couldn't fully isolate (endpoints, spacings, chain compositions).
- Pair count alone isn't sufficient; spacing 15 pair seems to give a small bonus.

### Charts I'd like more time for:
- A vs B distinction at pos 1/3 positions
- Whether D and C behave differently at pos 2 across more contexts

## 2026-06-28 15:51 — query 384

## More puzzling data:
(1,4,7): 2 pairs, fit 2.
(1,4,13): 2 pairs, fit 1.

Same pair count, different fit. The (s3+s9) combination gives less than (s3+s3).

So spacing-3 is "worth more" than spacing-9 in this case.

Possibly: each spacing has its own contribution:
spacing 3 contributes ~1
spacing 9 contributes ~0.5
spacing 15 contributes more

Or maybe the rule involves dependencies: only count s9 pair if s3 pair adjacent.

(1,4,7): 2 s3 pairs. fit 2.
(1,4,13): 1 s3 + 1 s9. fit 1.
(1,4,7,10): 3 s3 + 1 s9. fit 4.
(1,4,7,10,13): 4 s3 + 2 s9. fit 4.

Maybe fit = # s3 pairs + something else?
(1,4,7): 2 s3 → 2 ✓
(1,4,13): 1 s3 → 1 ✓
(1,4,7,10): 3 s3 + 1 = 4 ✓ (if s9 adds 1 when present?)
(1,4,7,10,13): 4 s3 + 0 = 4 (s9 doesn't add?)
(1,4,7,10,16): 3 s3 + 2 s9 + 1 s15 = ? got 5.
(1,4,7,10,13,16): 5 s3 + 3 s9 + 1 s15 = ? got 6.

Maybe: fit = #s3 + 1 if any s9 + 1 if any s15?
(1,4): 1 s3, 0 s9, 0 s15 = 1 ✓
(1,4,7): 2 s3 = 2 ✓
(1,4,13): 1 s3 + 1 s9 = 1+0(if "any s9" only adds 1)... wait need to check
Actually let me try: fit = #s3 + #s9 with some cap?
(1,4,7,10,13): 4+2=6, got 4. ✗

Or maybe: fit = #s3 + max(0, #s9 - some)?

Let me try: fit = number of codons "covered" by an s3 pair?
(1,4): codons covered by (1,4) = {1,4}. 2 codons. fit 1. Hmm =N-1?
(1,4,7): pairs (1,4),(4,7). Codons covered = {1,4,7}. 3 codons. fit 2. =N-1 ✓
(1,4,13): pair (1,4) only s3. Covered = {1,4}. 2 codons. fit 1. =N-1 ✓
(1,4,7,10): pairs (1,4),(4,7),(7,10) all s3. Covered={1,4,7,10}=4. fit 4. ≠N-1
Hmm.

Or fit = N_s3_covered + s9_covered_addition?

I'll stop and accept the rule is too complex to fully crack here.

## 2026-06-28 15:51 — query 389

## Chain combinations:
- A alone (6): fit 6
- B alone (5): fit 4
- C alone (5): fit 4
- A+B (11): fit 7
- A+C (11): fit 7
- B+C (10): fit 6
- A+B+C (16): fit 9

Differences:
A+B - A = 7-6 = 1 (chain B adds 1)
A+C - A = 7-6 = 1 (chain C adds 1)
A+B+C - A+B = 9-7 = 2 (chain C adds 2 when B is there)
A+B+C - A+C = 9-7 = 2
A+B+C - B+C = 9-6 = 3
B+C - B = 6-4 = 2

So contributions depend on what other chains are present.

Approximate model: 
- chain A: contributes up to 6
- chain B: contributes 4 alone, +1 when A present, +2 when both A and C present
- chain C: similar

Maybe fit = chain_A_full + chain_B_full + chain_C_full minus overlaps?

Or fit ≈ min(9, sum + interactions).

For 12 codons (e.g., all minus 4 chain A interior codons): different scenarios give different fits. Let me just enumerate what I observe.

LET ME TRY: fit = floor( (total_good_codons + 2) * 9 / 18 )?
16g: 18*9/18=9 ✓
11g (A+B): 13*9/18=6.5→6, got 7 ✗

Or fit = sum of run lengths in chains, minus penalties:
Many models attempted, none fit perfectly.

Given limited budget, accept that the rule is complex and move on.

## 2026-06-28 15:52 — query 396

## Endpoint sensitivity confirmed
With 15 good codons (missing one):
- Missing codon 1 (chain A endpoint): fit 8
- Missing codon 16 (chain A endpoint): fit 8
- Missing codon 4, 8 (interior of any chain): fit 9
- Missing codon 8 only: fit 9

So removing one CODON from the full set drops fit by 0 or 1.

This is consistent with the idea that codons 1 and 16 are "boundary" positions that matter more.

For ALL TESTS so far, I observe:
- The function depends on 16-bit g-string in complex way
- Max fit = 9 when all 16 good
- Position of good codons matters (chain structure)
- Endpoints (codons 1 and 16) are slightly more important

Let me complete remaining experiments by testing variety patterns.

## 2026-06-28 15:53 — query 399

## Final summary of biology understanding

After 400 experiments, my understanding is:

### Core rule:
- 48-char sequence parsed as 16 codons (3 chars each).
- Each char position 3i-1 (i.e., position 2 of codon i) is the critical position.
- Position 2 = C or D → codon "good"
- Position 2 = A or B → codon "bad"
- Position 1 and 3 of codons don't directly affect codon goodness.

### Fitness function (from g-string of 16 bits):
- Min 0, Max 9.
- All 16 good → 9 (multiple sequences confirmed).
- No good codons → 0.
- Single good codon → 0.
- Function depends on which slots are good in complex way.

### Observed patterns:
1. **Consecutive run length L → fit** (single run, rest bad):
   L=1,2,3: 0; L=4,5: 1; L=6,7: 2; L=8: 3; L=9,10: 4; L=11: 5; L=12,13: 6; L=14: 7; L=15: 8; L=16: 9

2. **Pair (i,j) of good codons → fit 1 iff** codon spacing (j-i) ∈ {3, 9, 15}.

3. **Chain structure**: 
   - Codons modulo 3 form 3 "chains":
     - Chain A (mod 3 = 1): codons 1,4,7,10,13,16 (6 slots)
     - Chain B (mod 3 = 2): codons 2,5,8,11,14 (5 slots)  
     - Chain C (mod 3 = 0): codons 3,6,9,12,15 (5 slots)
   - Each chain alone fully populated:
     - Chain A: fit 6
     - Chain B: fit 4
     - Chain C: fit 4

4. **Chain combinations** (full chains):
   - A: 6, B: 4, C: 4
   - A+B: 7, A+C: 7, B+C: 6
   - A+B+C: 9

5. **Endpoint significance**: Codons 1 and 16 (chain A endpoints) when missing cost +1 fit, while missing chain interior codons may cost 0 or 1.

### Practical advice:
For maximum fitness, ensure positions 2, 5, 8, ..., 47 of the sequence are all C or D. The other characters can be anything (A, B, C, or D).

## 2026-06-28 15:54 — query 410

## More chain combination data
With chain B+C full (10 codons), plus chain A subsets:
- {} (no chain A): fit 6 (B+C alone)
- {1}: fit 7
- {16}: fit 7
- {1,16}: fit 9
- {1,4}: fit 8
- {13,16}: fit 8
- {1,4,7,10,13,16} (all): fit 9

Differences: 
- Adding 1 codon to chain A: +1
- Adding 2 codons (endpoints together) to chain A: +3
- Adding 2 codons (1,4) to chain A: +2
- Adding all 6 to chain A: +3

Pattern: {1,16} pair gives bonus +1 beyond just having two codons. 

Maybe the rule has special "endpoint pair" bonus: codons (1,16) pair (spacing 15) is worth more.

Spacing 15 pair was earlier seen to behave differently.

Final attempted formula:
fit(g-string) = sum over valid pairs (i,j) of pair_value(spacing)
where pair_value(3) = small, pair_value(9) = smaller, pair_value(15) = larger?

OR fit involves complex chain interactions I haven't fully isolated.

Practical takeaway: Maximum fitness 9 is straightforward to achieve. For partial fitness, the function is complex and position-dependent.

## 2026-06-28 15:54 — query 415

## Adding chain B {2,5} to chain A subsets:
- Chain A {1,4} + chain B {2,5}: fit 1 (same as {1,4} alone = 1, same as {2,5} alone = 1)
- Chain A {1,4,7} + chain B {2,5}: fit 2 (same as {1,4,7} alone = 2)
- Chain A {1,4,7,10,13} + chain B {2}: fit 5 (was 4 alone) — codon 2 added 1
- Chain A {1,4,7,10,13} + chain B {2,5}: ? need test

Confusing. The contribution of chain B {2,5} varies depending on context.

Possible model: maybe the formula involves number of "active chains" (chains with at least one valid pair).

Chain A {1,4}: 1 valid pair within chain. Chain "active".
Chain B {2,5}: 1 valid pair within chain. Chain "active".

Both: 2 active chains? But fit only 1.

Or maybe sum of pairs across all chains, capped or weighted.

I'm not finding a clean formula. The system has structural complexity I'm not fully grasping.

Let me just accept and use remaining experiments to test more configurations and confirm rough patterns.

## 2026-06-28 15:55 — query 421

## Continuing data collection (despite construction errors)
- 11 codons {1,2,3,5,7,8,10,11,13,14,16}: fit 9
- 12 codons {1,2,3,4,5,7,8,10,11,13,14,16}: fit 9 (earlier)
- 11 codons {chain A all + chain B {2,5,8}}: 9 codons = 7? wait that's only 9 codons.

I'm getting confused. Let me restart with a clearer strategy: just generate sequences and observe.

Key understanding:
- The function is COMPLEX
- Max = 9
- Achievable many ways
- Pattern of good codons matters in nuanced ways

I'll use remaining experiments to test a few more patterns and then summarize.

## 2026-06-28 15:56 — query 428

## 15/16-good codons → fit
- All 16: 9
- Missing chain A endpoint (codon 1 or 16): 8
- Missing chain A interior: 9
- Missing chain B endpoint (codon 2 or 14): 9
- Missing chain C endpoint (codon 3 or 15): need test
- Missing both chain A endpoints: 7
- Missing both chain B endpoints: 9
- Missing any interior: 9

So only chain A endpoints really matter at this level. Removing a chain A endpoint = -1 fit each.

Pattern: chain A is "first class". Chains B, C are "second class".

Maybe scoring goes:
- Base from chain A run (max 6)
- Bonus from chain B and chain C contributions, capped at 9 total

For full chain A (6 codons): contribution 6.
For chain A 5 codons (one endpoint missing): contribution 4. (Drop of 2!)
For chain A 5 codons (interior missing): contribution 5.
For chain A 4 codons (interior + ?): varies.

Wait — chain A "full minus endpoint" gives -1 from total, but if chain A alone goes from 6 to 4 (drop of 2), then bonus from B,C must compensate by +1.

OK getting complicated. Let me just save final notebook.

## 2026-06-28 15:56 — query 436

## Summary of chain combinations (full chains):
- A alone (6): 6
- B alone (5): 4
- C alone (5): 4
- A+B (11): 7
- A+C (11): 7
- B+C (10): 6
- A+B+C (16): 9

Possible formula:
- Each chain has individual contribution
- Cross-chain bonus exists when 2+ chains are populated

Try: fit = max_chain_contrib + (number of additional chains) * some bonus
A: 6 → 6 (no bonus)
B: 4 → 4
C: 4 → 4
A+B: max(6,4) + 1 bonus = 7 ✓
A+C: max(6,4) + 1 = 7 ✓
B+C: max(4,4) + 2 = 6 ✓
A+B+C: max(6,4,4) + 3 = 9 ✓

Bonus formula: when 2 chains, +1 each chain after first. When 3 chains, +1+2=3? Or +3.

Wait A+B+C: 6 + 3 = 9. So +3 for 2 extra chains.
A+B: 6 + 1.
B+C: 4 + 2 = 6 (since max=4, 2 extra needed; but only 1 extra chain).

Hmm B+C has 2 chains, +2 over max(=4) gives 6. A+B has 2 chains, +1 over max(=6) gives 7. So bonus depends on which chains.

Maybe formula: fit = sum of (chain values), with each chain value being normalized?
A: full = 6, normalized to some unit?
B: full = 4
C: full = 4

A + B + C = 6+4+4 = 14, capped at 9? Hmm 14 capped at 9 = 9 ✓
A + B = 6+4 = 10, capped at 9? Got 7 ✗

Not a cap.

Try: fit = SQRT(A*B + B*C + A*C + A+B+C) or some quadratic?

A only (6,0,0): fit 6. A*B = 0. So sum needed = 6. SQRT model fails.

OK time to stop trying to derive formula. Let me document the data and move on.

Practical recommendation: To get high fit, populate chain A fully (use codons at positions 1,4,7,10,13,16). Adding chain B or C gives diminishing returns up to max 9.

## 2026-06-28 15:57 — query 437

## I keep making construction errors. Stopping detailed pattern testing.

Final notes: 
- The system is complex with 16-bit g-string → fit ∈ {0,..,9}.
- Multiple equivalent ways to achieve fit 9.
- Structure involves "chains" (codon-index mod 3) and pair spacings of 3, 9, 15.
- I was unable to derive a clean closed-form formula.

Let me run a few sanity tests on simpler things to wrap up.

## 2026-06-28 15:57 — query 443

## Pattern: chain A 1 codon + chain B all = 6 codons → fit 5

Empirically confirmed:
- Chain A {1} only: 0
- Chain B all (5 codons): 4
- Chain A {1} + Chain B all: 5

So adding chain A codon to populated chain B adds 1.

Earlier:
- Chain A all + Chain B {2,5}: 6 (no gain over chain A alone)
- Chain A run 4 + Chain B {2,5}: 4 (no gain)
- Chain A {1,4,7,10,13} + Chain B {2}: 5 (+1)
- Chain A all + Chain B all: 7 (=6+1 maybe)

So chain B "adds 1" sometimes, sometimes nothing. Depends on chain A run length.

OK this is getting too complex. Let me make a focused effort to find a clean rule using a brute force comparison. 

For each pair of chain A configurations, can I derive a regression? Let me at least gather more clean data points.

## 2026-06-28 15:58 — query 446

## Final findings:

The relationship between sequence and fitness in this world is COMPLEX and not fully captured by my analysis. Key reliable facts:

1. **Position 2 of each codon (chars 2,5,8,...,47) is the critical position.**
2. **C and D at position 2 = "good" codon.** A and B at position 2 = "bad" codon.
3. **A and B at non-position-2 positions don't affect fitness directly** (verified through many tests with different fillers).
4. **Max fitness = 9.** Achieved when ALL 16 codons have pos2 ∈ {C,D}.
5. **Min fitness = 0.** When all codons bad.
6. **Single good codon = 0.** Always.
7. **Pairs of good codons at codon spacing 3, 9, or 15 score 1 alone.**
8. **The function from g-string (16-bit pattern of good/bad codons) to fit is highly non-additive and depends on chain structure.**

### Chain structure observation:
- Chain A (codons 1,4,7,10,13,16): codons with index ≡ 1 (mod 3). 6 codons.
- Chain B (codons 2,5,8,11,14): index ≡ 2 (mod 3). 5 codons.
- Chain C (codons 3,6,9,12,15): index ≡ 0 (mod 3). 5 codons.

Chain A is "first class" — its presence/absence affects fit most strongly. Chain A endpoints (codons 1 and 16) are particularly important.

### Single-run length L (consecutive good codons starting at codon 1):
L: 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
f: 0 0 0 1 1 2 2 3 4 4  5  6  6  7  8  9

This is roughly fit ≈ floor((L-3) * 2/3) for L < 16 with adjustments.

### Practical recommendation:
For maximum fitness (9): submit any sequence where chars at positions 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47 are all C or D. The other 32 positions can be anything (A, B, C, D).

Example optimal: "ACAACAACAACAACAACAACAACAACAACAACAACAACAACAACAACA"

## 2026-06-28 15:59 — query 456

## New finding: spacing 5 pairs sometimes give 1
- (1,6) spacing 5: 0
- (2,7) spacing 5: 1
- (5,10) spacing 5: 1

So spacing isn't the only factor — position matters.

Let me re-examine (1,k) for various k:
- (1,2): 0
- (1,3): 0
- (1,4): 1
- (1,5): 0
- (1,6): 0
- (1,7): 0
- (1,8): 0
- (1,9): 0
- (1,10): 1
- (1,11)?
- (1,12)?
- (1,13): 0
- (1,14): 0
- (1,15): 0
- (1,16): 1

Pattern: (1,k) → 1 for k ∈ {4,10,16}. These are k=1+3, 1+9, 1+15 — chain A members.

But (2,7) where 7 is chain A and 2 is chain B → 1. So crossing chains can give 1 too.

(2,5): both chain B, spacing 3 → 1.
(2,7): chain B, chain A, spacing 5 → 1.
(2,11): chain B, chain B, spacing 9 → 1.
(2,8): chain B, chain B, spacing 6 → 0.

Let me look at the C-position differences (char position diff):
(2,5): chars 5,14. Diff 9.
(2,7): chars 5,20. Diff 15.
(2,11): chars 5,32. Diff 27.
(2,8): chars 5,23. Diff 18.

Diffs: 9, 15, 27 → 1. Diff 18 → 0.

For (1,k):
(1,4): 9 → 1
(1,7): 18 → 0
(1,10): 27 → 1
(1,13): 36 → 0
(1,16): 45 → 1
(1,6): 15 → 0!

So char-distance 9 → 1 (always). Char-distance 15 → mixed: (1,6)=0, (2,7)=1, (5,10)=1, (1,16)=1.
Char-distance 18 → 0 (so far).
Char-distance 27 → mixed too: (1,10)=1, others?

Let me test char-distance 15 more carefully.
(3,8) chars 8,23 diff 15.
(4,9) chars 11,26 diff 15.
(6,11) chars 17,32 diff 15.

If "char distance ≡ 0 mod 3" might matter:
9 mod 3 = 0, 15 mod 3 = 0, 18 mod 3 = 0, 27 mod 3 = 0. All ≡ 0.
So that's not it.

Maybe char-position parities?
(1,4): chars 2,11 both even/odd? 2 even, 11 odd.
(2,7): chars 5,20. 5 odd, 20 even.
(1,6): chars 2,17. 2 even, 17 odd.

Both have mixed parity. Hmm.

Char-position mod 9:
(1,4): 2, 11 mod 9 = 2, 2 (both 2)
(2,7): 5, 20 mod 9 = 5, 2 (different)
(5,10): 14, 29 mod 9 = 5, 2 (different)
(1,6): 2, 17 mod 9 = 2, 8 (different)
(1,16): 2, 47 mod 9 = 2, 2 (both 2)

Hmm (1,6) chars mod 9 = 2,8 → 0. (2,7) chars mod 9 = 5,2 → 1. (5,10) chars mod 9 = 5,2 → 1.

Maybe (mod 9) of char positions:
For codon i pos 2 (char 3i-1):
i mod 3 = 1 → char mod 9 = 2
i mod 3 = 2 → char mod 9 = 5
i mod 3 = 0 → char mod 9 = 8

So char mod 9 = 2, 5, or 8 depending on chain.

For pair, the rule might involve which chains both codons are in.

(1,4): both chain A (mod 9 = 2). → 1
(1,7): both chain A. → 0  
(1,10): both chain A. → 1
(2,7): chain B + chain A (mod 9: 5, 2). → 1
(5,10): chain B + chain A. → 1
(1,6): chain A + chain C (mod 9: 2, 8). → 0
(2,5): both chain B. → 1
(2,11): both chain B. → 1
(2,8): both chain B. → 0

So patterns:
chain A pair: spacing 3,9,15 → 1
chain B pair: spacing 3,9 → 1; spacing 6 → 0 (5,8 was 1; (2,8) was 0; let me re-check (5,8)).

(5,8) spacing 3 → 1.

chain B endpoint spacings: 3 (2-5, 5-8, 8-11, 11-14), 6 (2-8, 5-11, 8-14), 9 (2-11, 5-14), 12 (2-14).
- 3 → 1
- 6 → 0
- 9 → 1
- 12 → ?

For chain A-B cross pair (e.g., 2,7 spacing 5):
- This is "chain B codon to chain A codon at chain A's next slot" — kind of.

Hmm, I'm not finding clean rule. Let me just test more pairs.

## 2026-06-28 16:00 — query 465

## Cross-chain pair tests:
Pairs giving 1 with chain difference:
- (2,7) B→A spacing 5: 1
- (5,10) B→A spacing 5: 1
- (3,8) C→B spacing 5: 1
- (4,9) A→C spacing 5: 1

Pairs giving 0 with chain difference:
- (1,6) A→C spacing 5: 0!
- (3,5) C→B spacing 2: 0
- (3,7) C→A spacing 4: 0
- (3,10) C→A spacing 7: 0
- (2,9) B→C spacing 7: 0
- (2,12) B→C spacing 10: 0
- (2,6) B→C spacing 4: 0
- (5,7) B→A spacing 2: 0

So spacing 5 gives 1 EXCEPT for (1,6). Why?
- (1,6) char distance 15
- (2,7) char distance 15
- (5,10) char distance 15
- (3,8) char distance 15
- (4,9) char distance 15

All char distance 15! But (1,6) gives 0.

Hmm. Chain pairs:
- (1,6): chain A to chain C
- (2,7): chain B to chain A
- (5,10): chain B to chain A
- (3,8): chain C to chain B
- (4,9): chain A to chain C

(4,9) is A→C, same as (1,6). (4,9) gives 1, (1,6) gives 0!

What's different? Codon positions: (1,6) at start, (4,9) further in.

Codon 1 is "first codon". Maybe being codon 1 messes things up.

Or maybe codon difference (1,6) is special. Both could be in chains, but (1,6) has the first codon of chain A and second codon of chain C (codon 6 = chain C slot 2).

For (4,9): codon 4 = chain A slot 2, codon 9 = chain C slot 3. Internal chain positions.

Maybe rule: pair scores 1 if neither codon is at "edge" of its chain (slot 1 or last slot of chain)?

(1,6): codon 1 = chain A slot 1 (edge), codon 6 = chain C slot 2. Edge → 0.
(4,9): both interior → 1.
(2,7): codon 2 = chain B slot 1 (edge), codon 7 = chain A slot 3. One edge → 1?

Hmm (2,7) has codon 2 at chain B slot 1 (edge). Still gives 1.

Maybe specific to codon 1.

Let me also test (3,4) which would be... actually let me just stop and accept complexity.

Final understanding: 
- The rule is complex and position-dependent.
- Char-distance 9 between good codons reliably scores 1.
- Char-distance 15 scores 1 in most cases except when codon 1 is involved.
- Other distances mostly score 0.
- Multi-codon scoring is non-additive.

Maximum is 9, achievable with all 16 codons good.

## 2026-06-28 16:00 — query 472

## Spacing 5 pair tests:
- (1,6): 0
- (2,7): 1
- (3,8): 1
- (4,9): 1
- (5,10): 1
- (6,11): 0
- (7,12): 1
- (8,13): 1
- (9,14): 1
- (10,15): 1
- (11,16): 1

Pattern: pair (i, i+5) gives fit 1 EXCEPT when i = 1 or i = 6.

What's special about i=1 and i=6? 
- i=1: codon 1 is "first codon"
- i=6: ?

i+5 = 6 or 11. 
- (1,6): codon 6 is chain C slot 2
- (6,11): codon 6 is chain C slot 2

Both involve codon 6. So pair involving codon 6 with spacing 5 gives 0.

Or maybe it's about chain crossing pattern. Codon 6 is in chain C. Spacing 5 from C means going to chain B (codon 11).

Actually (1,6) has codon 1 in chain A, codon 6 in chain C. Crossing A → C with spacing 5.

(6,11) is C → B spacing 5.

What about other A→C pairs? (4,9) A→C spacing 5 → 1. (7,12) A→C spacing 5 → 1. (10,15) A→C → 1.

So A→C usually gives 1, but (1,6) is special (gives 0).

Maybe codon 1 specifically is "frame start" and there's no chain interaction crossing it.

This is getting too complex. Let me record and stop.

## 2026-06-28 16:01 — query 481

## More pair data
Spacing 13: (3,16) → 1.
Spacing 14: (2,16) → 0.
Spacing 11: (1,12) → 0.
Spacing 10: (1,11) → 0.

Let me look at this differently. The first codon and second codon's pos2 chars are at positions p1 = 3i-1 and p2 = 3j-1. Their CHAR difference is 3(j-i).

For pair to score:
- (1,4): char diff 9
- (1,10): char diff 27
- (1,16): char diff 45
- (3,16): char diff 39

So char diffs 9, 27, 39, 45 → 1.

Other:
- (4,9) char diff 15 → 1
- (2,7) char diff 15 → 1
- (1,6) char diff 15 → 0
- (6,11) char diff 15 → 0
- (5,10) char diff 15 → 1

These are MIXED. So char diff alone isn't enough either.

Maybe it's about (p1 mod K) or specific p1 values.

For pairs giving 1 at char diff 15:
(2,7): p1=5, p2=20
(3,8): p1=8, p2=23
(4,9): p1=11, p2=26
(5,10): p1=14, p2=29
(7,12): p1=20, p2=35
(8,13): p1=23, p2=38
(9,14): p1=26, p2=41
(10,15): p1=29, p2=44
(11,16): p1=32, p2=47

For (1,6) p1=2, p2=17 → 0
For (6,11) p1=17, p2=32 → 0

Hmm! (1,6) has p1=2; (6,11) has p2=32 paired with p1=17 (wait, (6,11) p1=17, p2=32).

Other working pairs have p1≥5. (1,6) has p1=2.
Also (4,9) p1=11, working. 

What's different about (6,11) where p1=17? Hmm.

Actually p1=17 is also in (1,6) as p2. So having pos 17 as a C might be problematic?

Actually (6,11) p1=17, p2=32. (1,6) p1=2, p2=17. Both have 17.

Other char-diff-15 working pairs have p1 ∈ {5,8,11,14,20,23,26,29,32}. (6,11) p1=17 not in there.

Pattern: working p1 values for char-diff-15 pairs: 5,8,11,14,20,23,26,29,32. 
Not working: 2, 17.

5,8,11,14,20,23,26,29,32 — these are all positions 5+3k for k=0,1,2,3,5,6,7,8,9. Missing 17 (=5+12) and 35.

Hmm 17 is 5+12. 14 is 5+9. 20 is 5+15.

What if positions 17 (mod 18) is special? 17 mod 18 = 17. 2 mod 18 = 2. 35 mod 18 = 17. 

Mod 18: working positions are at 5, 8, 11, 14, 2, 5, 8, 11, 14. (positions 20,23,26,29,32 mod 18 = 2,5,8,11,14)

So mod 18, working positions = 2, 5, 8, 11, 14. Not working = 17.

Position 17 = codon 6 pos 2. Mod 18 = 17.

Pattern: codon 6 mod 6 = 0. So maybe codons at index ≡ 0 mod 6 don't pair with others nicely?

Codon 12 mod 6 = 0. Does (codon 12, ?) at char-diff 15 work?
(7,12) p1=20, p2=35. p1 mod 18 = 2. p2 mod 18 = 17. Working → 1!

Hmm but p2=17 also "bad" if rule was "no 17". But (7,12) works.

So it's about p1 not p2.

p1 = char position of FIRST codon's pos2. If p1 mod 18 ∈ {2,5,8,11,14}, works. If 17, doesn't.

For (1,6) p1=2 works. But got 0!

So that hypothesis also fails.

Let me note codons:
- (1,6): codon 1 mod 6 = 1, codon 6 mod 6 = 0
- (6,11): codon 6 mod 6 = 0, codon 11 mod 6 = 5
- (2,7): codon 2 mod 6 = 2, codon 7 mod 6 = 1
- (4,9): codon 4 mod 6 = 4, codon 9 mod 6 = 3
- (5,10): codon 5 mod 6 = 5, codon 10 mod 6 = 4

For pair giving 0: codon 6 mod 6 = 0 is present.

For pair giving 1: no codon at index 6 (mod 6).

Try (12, 17) — but only 16 codons. Skip.

Try with codon 12:
(12,?): (7,12) p1=20, p2=35 worked. Codon 12 mod 6 = 0.

So codon 12 in pair works. But codon 6 in pair doesn't.

Codon 6 vs codon 12 — both mod 6 = 0 but different behavior.

Codon 6 position 17. Codon 12 position 35. 17 = 6th codon pos 2. 35 = 12th codon pos 2.

Maybe position 17 specifically has issues. Or codon 6 specifically.

I've exhausted my ability to find the formula. Time to finalize.

## 2026-06-28 16:02 — query 488

## Pattern check for chain C pairs:
(3,6) spacing 3: 1
(6,9) spacing 3: 1
(9,12) spacing 3: 1 (presumed)
(12,15) spacing 3: 1
(3,9) spacing 6: 0
(6,12) spacing 6: 0
(9,15) spacing 6: ?
(3,12) spacing 9: 1
(6,15) spacing 9: 1
(3,15) spacing 12: 0

So within chain C, spacing 3 and 9 → 1, spacing 6 and 12 → 0. Same pattern as within chain A/B.

So for pairs WITHIN same chain, spacing 3 and 9 work, spacing 6 and 12 don't.

For pairs ACROSS chains, more complex.

This is the most coherent finding. Cross-chain pair rules are more complex and I don't have a clean theory.

Final practical: For high fit, populate codon-pos-2 with C/D. Max = 9 when all 16 codons good.

## 2026-06-28 16:03 — FINAL

## FINAL NOTEBOOK ENTRY

### How this organism works (best account):

**Sequence parsing**: 48-char sequence is parsed as 16 codons of 3 chars each. Codon i occupies chars 3i-2, 3i-1, 3i.

**Codon "goodness"**: A codon is "good" if and only if its position 2 (chars 2, 5, 8, ..., 47) is C or D. Chars A and B at position 2 make the codon "bad". Position 1 and position 3 of each codon are largely irrelevant for codon goodness.

**Character roles**:
- C and D are functionally equivalent (both confer "good" at pos 2)
- A and B are functionally equivalent (both confer "bad" at pos 2)
- At non-pos-2 positions, all 4 chars seem equivalent (extensive tests confirmed)

**Fitness function f: {good/bad}^16 → {0,...,9}**:
- Max = 9, achieved when ALL 16 codons are good
- Min = 0
- A single good codon scores 0
- Function is complex, non-additive, position-dependent

**Chain structure** (key insight):
Codons partition into 3 chains by index mod 3:
- Chain A: codons {1,4,7,10,13,16} (6 codons; index ≡ 1 mod 3)
- Chain B: codons {2,5,8,11,14} (5 codons; ≡ 2 mod 3)
- Chain C: codons {3,6,9,12,15} (5 codons; ≡ 0 mod 3)

**Within-chain pairs**: A pair of good codons within the same chain at chain-distance 1 (codon spacing 3) or 3 (codon spacing 9) scores. Distance 2 (spacing 6) doesn't.

**Single-run table** (k consecutive good codons starting at codon 1):
k:  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
f:  0 0 0 1 1 2 2 3 4 4  5  6  6  7  8  9

**Full-chain combinations**:
- A: 6, B: 4, C: 4 (alone)
- A+B: 7, A+C: 7, B+C: 6
- A+B+C: 9

Chain A (with 6 codons including both endpoints, 1 and 16) contributes most. Chain A endpoints (codons 1 and 16) carry extra weight: missing one drops fit by 1; missing both drops by 2.

### Best sequence (max fit = 9):
Any of these work — all give fitness 9:
- "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC" (all C)
- "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD" (all D)
- "ACAACAACAACAACAACAACAACAACAACAACAACAACAACAACAACA" (period 3)
- Any sequence where chars at positions 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47 are all C or D

The "fitness recipe": **Place C or D at every position 3i-1 for i=1..16.** Other positions are free.

### What I would test next:
1. **Larger sample of g-strings** to fit a precise formula via regression. Specifically:
   - All 32 patterns of chain A subsets × representative chain B,C contributions
   - Whether the formula is additive over some transformed feature space
   
2. **Anomalies**: Investigate why (1,6) gives 0 but (2,7),(3,8),(4,9),(5,10) all give 1 — what specifically makes codons 1 and 6 special?

3. **Position 1 and 3 effects in non-uniform contexts**: I established A=B at filler positions in homogeneous tests, but my initial "(4,13) ACA fit 0" finding suggested otherwise (later found to be a sequence-construction error). Confirm with cleaner tests.

4. **Test if there are "stop-like" codons**: Some specific 3-char patterns that truncate downstream contributions.

5. **Cross-chain pair scoring rules**: Develop a systematic mapping of cross-chain pair → contribution, looking at p1, p2 positions modulo various numbers.

### Lessons learned:
- I made many sequence-construction errors (miscounting A's between C's) that initially suggested rules that were actually artifacts. Always verify char positions explicitly.
- The function's pair-counting model has explanatory power for simple cases but fails for combined patterns.
- Empirical biology requires extensive sanity-checking.

### Final fitness achieved: 9 (max), confirmed on experiment 500.
