
## 2026-06-28 15:06 — query 0

## Initial Setup
- Alphabet: {A,B,C,D,E,F}, length 48, 500 experiments, maximize score.
- No prior knowledge of this world's rules.

## Starting assumptions to test
- Score could depend on: composition (counts of each letter), positional preferences, motifs/k-mers, structural features (palindromes/repeats), or interactions between positions.
- First experiments: test homopolymers of each letter to see per-letter baseline contribution and whether any letter is strongly preferred. This gives 6 datapoints cheaply.

## Plan
1. Six homopolymers (A*48, B*48, ..., F*48) — establish per-letter baseline.
2. Then a uniform mix and a random-ish sequence to compare.
3. Based on results, probe positional vs compositional structure.

First experiment: A*48.

## 2026-06-28 15:06 — query 6

## Homopolymer results
- A: 0, B: 9, C: 0, D: 9, E: 0, F: 9
- Pattern: A,C,E score 0; B,D,F score 9.
- Hypothesis: B,D,F are "good" letters; A,C,E are "bad" (score 0). Possibly each letter contributes 9/48 = 0.1875 per position, and total = count(B,D,F).
- Or even/odd character index in {A=0,B=1,C=2,D=3,E=4,F=5}: B,D,F odd-indexed. Could be parity-based.

## Next test
- Mix BDF: alternating B/D/F to see if mixing matters or if just count of {B,D,F} matters.
- Then half-and-half (24 B + 24 A) to test linearity.

## 2026-06-28 15:06 — query 8

## More data
- BDFBDF... = 9 (same as homopolymers of B/D/F).
- 24B+24A = 3. Not 4.5. Not 9. Interesting.
- 24/48 = 0.5 fraction. Score 3, vs 9 at 100% B. Not linear in count.
- Maybe score = 9 * (frac_good)^2? 0.5^2*9 = 2.25. Or 9*(frac_good - 0.5)*2 if frac>0.5? Doesn't fit.
- Or maybe penalty for A,C,E presence. 24 bad chars → −6 from max? 9−6=3. Could be: score = good_count − bad_count, capped to 0? 24−24=0, not 3.
- Or score = (good_count * 9) / (good_count + 2*bad_count)? 24*9/(24+48)=3. Possibly.
- Or score = 9 * good_count/(good_count + k*bad_count) with k=2.
- Let me test 36B+12A: predicted 9*36/(36+24)=5.4 or maybe integer 5.

## Next
Test 36B+12A.

## 2026-06-28 15:07 — query 10

## Linearity check
- 48B: 9, 36B/12A: 6, 24B/24A: 3, 12B/36A: 1, 0B/48A: 0
- Differences: 9-6=3, 6-3=3, 3-1=2, 1-0=1. Not linear count.
- Counts: 48→9, 36→6, 24→3, 12→1, 0→0
- 48/9=5.33, 36/6=6, 24/3=8, 12/1=12. Not simple ratio.
- 9 = floor(48*48/(48+0))/... hmm
- Try: score ≈ good^2 / 48? 48²/48=48 no. /256? 
- 48,36,24,12,0 → 9,6,3,1,0
- 9-6-3-1-0. Differences 3,3,2,1. 
- Try score = floor((good/48)^k * 9)? (1)^k=9. (.75)^k=6 → k = log(6/9)/log(.75) = log(.667)/log(.75) = 1.41. (.5)^1.41 = .376, *9=3.39≈3. (.25)^1.41=0.141 *9=1.27≈1. Works!
- Or simpler: floor(9*good/48*something)... maybe score = floor(good*(good+1) / something).
- 48*49/something=9? 2352/9=261. 36*37=1332/6=222. Not matching.
- Try: score = floor(good²/256): 48²/256=9. 36²/256=5.06≈5 but obs 6. Nope.
- 48²/256=9, 36²=1296, /something=6→216. 24²=576/3=192. Not constant.
- Maybe positional: only certain positions count? But homopolymer 48 gives 9, meaning at most 9 "good" positions, OR scoring caps at 9.
- Hypothesis: there are 9 special positions where having a "good" letter (B/D/F) gives +1. Test: with 48B all 9 are filled → 9. With 24B+24A (first 24 B), if those 9 positions are all in first 24, score=9. But observed 3. So good positions aren't all in first 24. Maybe distributed: of 9 good slots, ~half in first 24 and half in last 24. Expected score with first 24=B: ~4-5. Got 3. Possible but need to test position.

## Next: test position. Last 24 B, first 24 A.

## 2026-06-28 15:07 — query 12

## Big discovery
- 24B+24A (block): 3
- 24A+24B (block): 3
- BABABA... (alternating, also 24B+24A): 0!
- So composition alone doesn't determine score. The arrangement/contiguity matters!
- Alternating BA pattern gives 0 despite same composition.

## New hypothesis
- Maybe runs of "good" letters matter. Longest run of B/D/F?
- 48B: run length 48 → 9
- 24B run → 3
- 12B run → 1
- alternating (run 1) → 0
- 36B run → 6
- 0B → 0
- Mapping: run 48→9, 36→6, 24→3, 12→1, 1→0
- That looks like floor((run-?)/something) or maybe sum-based.
- 48→9, 36→6, 24→3, 12→1: differences 3,3,2,1. Maybe score = number of "good runs of length ≥ k" summed? 
- Or maybe score counts overlapping windows of all-good. Run of L has L-k+1 windows of size k that are all-good.
- Try k=6: 48→43, no.
- Try: number of non-overlapping k-mers? Run L → floor(L/k). 48/k=9 → k≈5.33. 36/k=6 → k=6. 24/k=3 → k=8. Not consistent.
- Try: max run of B/D/F divided by something? 48/5=9.6→9. 36/6=6. 24/8=3. 12/12=1. Doesn't fit one rule.
- Try: count of "good 6-mers" (length-6 substrings all good): 48 → 43 of them. No.
- Try sum: score = sum over runs of f(L). Maybe f(L) = floor(L/k) where the function gives 9,6,3,1,0 for L=48,36,24,12,1.
  - f(48)=9, f(36)=6, f(24)=3, f(12)=1. f(L)=floor((L)*(L+1)/(2*48)) maybe? 48*49/96=24.5 no.
  - f(L)=floor(L²/256): 48²/256=9, 36²/256=5.06→5 (but we got 6), no.
  - f(L)=floor(L²/something): 48²=2304. /9=256. 36²=1296/6=216. 24²=576/3=192. 12²=144/1=144. Not constant.
  - Maybe cubic or triangular: 9=C(9,1), 6=C(4,2), 3=C(3,2), 1=C(2,2)? No pattern.
  - Try f(L) = floor((L-3)/5): 48→9, 36→6.6→6, 24→4.2→4. Close but no.
  - f(L) = floor(L/6) + something? 48/6=8, 36/6=6, 24/6=4, 12/6=2. Off by +1,0,-1,-1.
  - Try counts of letters that come in pairs/triples: run of 48 has 47 pairs of consecutive B. /5=9.4→9. 36→35/5=7. No.
  - Try (L choose 2)/something: 48*47/2=1128. /9=125.3. 36*35/2=630/6=105. 24*23/2=276/3=92. No.

Need more datapoints. Let me try runs of different lengths.

## 2026-06-28 15:08 — query 15

## More data
- Run 6 (alone): 0
- Run 18 (alone): 2
- Two runs of 12: 4 (vs. single run of 12 = 1; vs. one run of 24 = 3)
- Run 36: 6, Run 48: 9
- Run 24: 3
- Run 12: 1

So 12+12=4 but 24=3 and 12=1. Two separate runs of 12 give more than one run of 24. So additivity holds across runs! 12 alone gives 1, but two 12s give 4. Wait that's not additive (1+1=2≠4). Maybe boundary effects, or maybe it's based on something else.

Wait, "two runs of 12" — actually has 24 B total. Same composition as 24B+24A block. Block gave 3, but two runs give 4. So position/spacing matters.

Let me reconsider. List datapoints (good_count, pattern → score):
- 48 good, all run: 9
- 36 good run, 12A: 6
- 24 good run, 24A: 3
- 24 good split 12+12 separated by A: 4
- 18 good run: 2
- 12 good run: 1
- 6 good run: 0
- 24 alternating BA: 0

Hmm, 24 alternating BA gives 0 but 24 in single block gives 3. Run length matters a lot.

Maybe score = sum over runs of f(L) where f(1)=0, f(6)=0, f(12)=1, f(18)=2, f(24)=3, f(36)=6, f(48)=9.
f(L): 1→0, 6→0, 12→1, 18→2, 24→3, 36→6, 48→9.

Differences: 1→6 (no change), 6→12 (+1), 12→18 (+1), 18→24 (+1), 24→36 (+3), 36→48 (+3).
Per unit L: 12-6=6, +1; 18-12=6, +1; 24-18=6, +1; 36-24=12, +3; 48-36=12, +3.
So roughly +1 per +6, except later doubled. Maybe f(L) = floor((L-6)/6) for small? (12-6)/6=1✓, (18-6)/6=2✓, (24-6)/6=3✓, (36-6)/6=5 (but observed 6). 

Maybe f(L) = floor(L²/256)? L=12: 144/256=0✓1? no. 

f(L) = L*(L-6)/something? 12*6=72, 18*12=216, 24*18=432, 36*30=1080, 48*42=2016. 72→1, 216→2, 432→3, 1080→6, 2016→9. 72/1=72, 216/2=108, 432/3=144, 1080/6=180, 2016/9=224. Not constant but increasing.

Try f(L) = C(L,2) - C(L-?,2)?

Try f(L) = floor(L^2 / 256):
- 48²/256 = 9 ✓
- 36²/256 = 1296/256 = 5.06 (got 6) ✗

Try f(L) = round(L²/256): 5.06→5 ✗

Try f(L) = ceil((L-6)²/?)? 
- L=12: 36; L=18: 144; L=24: 324; L=36: 900; L=48: 1764
- /scores: 36/1=36, 144/2=72, 324/3=108, 900/6=150, 1764/9=196. Increasing.

Try f(L) = number of length-6 windows fully in run: max(0, L-5):
- L=6: 1 (got 0). ✗

Try f(L) = max(0, L-6)*something:
- 12→6, 18→12, 24→18, 36→30, 48→42
- /scores: 6, 6, 6, 5, 4.67. Not constant.

Hmm, look at it differently. Maybe score for run = (L choose 2) / something or triangular.
- T(12)=78, T(18)=171, T(24)=300, T(36)=666, T(48)=1176
- Scores: 1,2,3,6,9. Ratios: 78, 85.5, 100, 111, 130. Increasing.

What if f(L) involves how many non-overlapping 8-mers (or 6-mers): floor(L/k).
- k=8: floor(L/8): L=12→1✓, 18→2✓, 24→3✓, 36→4 (got 6)✗
- k=6: 12→2, ✗
- k=5: 12→2 ✗

Mixed model: maybe (L/8)² isn't it.

What if score = sum over positions where there's a B/D/F that is preceded by at least 5 B/D/F? Run of L gives max(0, L-5).
- L=6→1 (got 0)
- L=12→7 (got 1) ✗

What if score = floor((L-6)/6) for L≤24, and something else >24?
- L=12: 1✓, 18: 2✓, 24: 3✓, 36: 5 (but got 6). 
- (L-6)/6 = (36-6)/6=5. Off by 1.
- Maybe floor(L/6) - 1: 12→1✓, 18→2✓, 24→3✓, 36→5 ✗

What if score is the count of contiguous all-good windows of size 6, sliding?
- Run L: max(0, L-5). L=6: 1 (got 0).
- Maybe windows of size 7: L=6→0✓, 12→6 (got 1) ✗

OK what about windows of size 12 (sliding)? L=6→0✓, 12→1✓, 18→7 (got 2) ✗

Test single window of size 6 in different way? L=12→1: think this is "run length floor divided by 12, then... hmm 12/12=1, 18/12=1.5→1 (got 2). 

f(L) = floor((L²-36)/?) ? 
- L=12: 144-36=108; L=18: 324-36=288; L=24: 576-36=540; L=36: 1296-36=1260; L=48: 2304-36=2268
- /scores: 108, 144, 180, 210, 252. Growing.
- Diff: 36, 36, 30, 42. Not constant.

Maybe try L: 12, 18, 24, 36, 48 → 1, 2, 3, 6, 9. Note 12→1, 24→3, 36→6, 48→9.
- 1, 3, 6, 9 vs L = 12, 24, 36, 48 (multiples of 12)
- 1,3,6,9 → diffs 2,3,3. Hmm.
- Actually L/12: 1,2,3,4. Scores: 1, 3, 6, 9. Ratios 1, 1.5, 2, 2.25. Looks like (L/12)*(L/12+1)/2 for n=1,2,3,4? T(1)=1, T(2)=3, T(3)=6, T(4)=10. Close! 1,3,6,10. We have 1,3,6,9. Off by 1 at 48.

Hmm but 48 homopolymer giving 9 — maybe there's a hard cap at 9, or it's actually T(L/12).

What is 18 in this? L=18: 18/12=1.5. Score 2. T(1.5)=1.5*2.5/2=1.875→2 ✓

So f(L) ≈ T(L/12) = (L/12)*(L/12+1)/2 = L(L+12)/288
- L=6: 6*18/288 = 108/288 = 0.375 → 0 ✓
- L=12: 12*24/288 = 1 ✓
- L=18: 18*30/288 = 540/288 = 1.875 → 2 (floor or round?) ✓
- L=24: 24*36/288 = 864/288 = 3 ✓
- L=36: 36*48/288 = 1728/288 = 6 ✓
- L=48: 48*60/288 = 2880/288 = 10. But observed 9!

Hmm, off by 1 for L=48. Maybe cap at 9, or maybe formula slightly different.

Try L²/256:
- 48²/256=9 ✓
- 36²/256=5.06 → 5 (obs 6) ✗

Try (L²+something)/256:
- 48: 2304/256=9 ✓; for 36 to give 6: 1536/256=6, so need 1536 from 1296, +240.
- 24 to give 3: 768/256=3, need 768 from 576, +192.
- 12 to give 1: 256/256=1, need 256 from 144, +112.
- Differences 240, 192, 112. Doesn't follow a single rule.

Try f(L) = floor(L(L+a)/b):
- L(L+12)/288: 48*60/288=10, 36*48/288=6, 24*36/288=3, 18*30/288=1.875, 12*24/288=1, 6*18/288=0.375
- So this gives 10,6,3,1.875,1,0.375 → floor 10,6,3,1,1,0. We observed 9,6,3,2,1,0. Discrepancies at 48 (got 9 vs 10) and 18 (got 2 vs 1).

For the two-runs-of-12 case: 1+1=2 but observed 4. So NOT additive per run with f(12)=1!

Wait — two runs of 12 with 12A between them and then 12 something? Let me recount my "two runs of 12" sequence:
"AAAAAAAAAAAABBBBBBBBBBBBAAAAAAAAAAAABBBBBBBBBBBB" = 12A + 12B + 12A + 12B. Last B group has no terminator on right, just goes to end. That's still a run of 12. So we have two runs of 12 and got 4. But f(12)+f(12)=2 (or 1+1).

So additivity fails — 2 runs of 12 = 4, not 2. So there's some interaction. Or maybe being adjacent to end matters.

Or perhaps the model isn't run-based, it's something else entirely.

Let me think differently. Maybe score depends on count of each good letter, with positional weights. With only B used, positions matter.

Let me try: 36B+12A but arrange as 12A+36B (run at end).

## 2026-06-28 15:08 — query 18

## More data
- Run of 36 in middle: 6 (same as 36 at start/end)
- Three runs of 8: 4. Single 8-run we haven't tested. 
- Run 24 = 3; two runs of 12 = 4; three runs of 8 = 4; single run of 24 elements split many ways.

Hmm, run of L scoring is unclear. Let me reconsider: maybe score isn't about good letters and runs but about specific patterns.

Observations:
- All same letter (B/D/F): 9
- Any single letter only of A/C/E: 0
- Compositions matter and arrangement matters.

Let me try a completely different angle: maybe pairs/triples matter. Let me try various small patterns.

Key test: what if the score is based on count of certain k-mers? E.g., "BB" pairs.
- 48B: 47 BB pairs → 9
- 36B (run): 35 BB pairs → 6
- 24B run: 23 BB → 3
- 12B run: 11 BB → 1
- 18B run: 17 BB → 2
- 6B run: 5 BB → 0
- Two 12B runs: 22 BB → 4
- Three 8B runs: 21 BB → 4
- 24 alternating BA: 0 BB → 0 ✓

Counts of BB: 47, 35, 23, 11, 17, 5, 22, 21
Scores:       9, 6, 3, 1, 2, 0, 4, 4

Ratios: 47/9≈5.2, 35/6≈5.8, 23/3≈7.7, 11/1=11, 17/2=8.5, 22/4=5.5, 21/4=5.25
Not constant ratio. But monotonic-ish.

Maybe BB count divided by 5 floored? 
- 47/5=9.4→9 ✓
- 35/5=7 (got 6) ✗

Maybe (BB count - threshold)/something. 

What about BBB count?
- 48B run: 46 BBB
- 36B: 34
- 24B: 22
- 12B: 10
- 18B: 16
- 6B: 4
- Two 12B: 20
- Three 8B: 18
Scores: 9, 6, 3, 1, 2, 0, 4, 4
Ratios: 46/9≈5.1, 34/6≈5.7, 22/3≈7.3, 10/1=10, 16/2=8

Try BBBBBB (6-mer all B) count:
- 48B run: 43; 36B: 31; 24B: 19; 12B: 7; 18B: 13; 6B: 1; two 12B: 14; three 8B: 9
- Scores: 9, 6, 3, 1, 2, 0, 4, 4
- 43/9=4.8, 31/6=5.2, 19/3=6.3, 7/1=7, 13/2=6.5, 1/0=∞, 14/4=3.5, 9/4=2.25
- Not constant.

Try BBBBBBBB (8-mer):
- 48B: 41; 36B: 29; 24B: 17; 12B: 5; 18B: 11; 6B: 0; two 12B: 10; three 8B: 3
- 6B: 0 ✓ (score 0)
- Three 8B: 3 (got 4)

Closer with some k. Let me try the count of "BBBBBBBBBB" (10-mer):
- 48B: 39; 36B: 27; 24B: 15; 12B: 3; 18B: 9; 6B: 0; two 12B: 6; three 8B: 0
- Scores: 9, 6, 3, 1, 2, 0, 4, 4
- 39, 27, 15, 3, 9, 0, 6, 0 vs 9, 6, 3, 1, 2, 0, 4, 4
- Three 8B count 0 but score 4. Doesn't fit.

Hmm let me try: count of letters that are part of some pattern.

Actually look at three 8B = 4 vs two 12B = 4 vs single 24B = 3 vs single 36B = 6. 
Total B counts: 24, 24, 24, 36.

Maybe score = sum over "groups" of some function. 
- 3 groups of 8: 4
- 2 groups of 12: 4  
- 1 group of 24: 3
- 1 group of 36: 6

If f(8)=4/3≈1.33, f(12)=2, f(24)=3, f(36)=6, f(48)=9, f(18)=2, f(12)=1 (single).

Wait f(12)=1 single but f(12)=2 in two-12 case? That's inconsistent.

So not strictly run-additive. Something else.

Maybe the score depends on overall structure. Let me try a very different test: a "perfect" pattern.

Hypothesis: maybe it's about alternation between good and bad, or specific k-mers, or maybe specific letters (only B counts, not D or F). Let me confirm with mixed.

## 2026-06-28 15:09 — query 21

## Confirmed: B, D, F are interchangeable "good", A, C, E are "bad"
- 24B+24D blocks = 9 (same as 48 of any good)
- 4-blocks of B,D,F repeated = 9
- BDFBDF... = 9
- So scoring depends on positions being good (∈{B,D,F}) vs bad (∈{A,C,E})

## Simplifies: treat as binary string. Good = 1, Bad = 0.
Recapping with this binary view:
- All 1s (48): 9
- 1×36 then 0×12: 6
- 0×12 then 1×36: 6
- 0×6 then 1×36 then 0×6: 6
- 1×24 then 0×24: 3
- 0×24 then 1×24: 3
- 0×15 then 1×18 then 0×15: 2
- 0×12 then 1×12 then 0×12 then 1×12: 4
- 1×8 then 0×8, three times: 4
- 0×21 then 1×6 then 0×21: 0
- 1×12 then 0×36: 1
- 0×36 then 1×12: ? (haven't tested)
- alternating (10)*24: 0
- all 0s: 0

Pure binary problem now. Let me think about what feature gives these scores.

Recap (pattern, good_count, score):
- All1s, 48, 9
- 36 contiguous, 36, 6
- 24 contiguous, 24, 3
- 12 contiguous, 12, 1
- 6 contiguous, 6, 0
- 18 contiguous, 18, 2
- 24=12+12 split: 4
- 24=8+8+8 split: 4
- 24 alternating: 0

It looks like having multiple medium-sized runs is good, and one long run is good, but one short run is bad.

Maybe score counts something like "number of (i,j) pairs both good within distance d"?

Let me try: score = number of pairs (i,j) i<j, both good, j-i ≤ 8 (some window).
- All1s: for each i in 1..48, pairs with j in i+1..min(48,i+8). Count = sum over i of min(8, 48-i) = 8*40 + 7+6+5+4+3+2+1 = 320+28=348. /something=9? 348/9=38.7. 
- This won't easily produce small ints like 0,1,2,3.

Maybe number of windows of size W that contain at least K goods?
- Window size 12, contain all 12 good. 
  - 48 of 1s: 37 windows
  - 36 contig: 25
  - 24 contig: 13
  - 12 contig: 1
  - 6 contig: 0
  - 18 contig: 7
  - 24=12+12 split with 12A between then 12B: depends on placement. "AAAAAAAAAAAA BBBBBBBBBBBB AAAAAAAAAAAA BBBBBBBBBBBB" — positions 13-24 are B, 37-48 are B. 12-windows that are all B: positions 13-24 and 37-48. 2 windows.
  - 8+8+8 split: 0 windows of 12 all-good.
- Scores: 9, 6, 3, 1, 0, 2, 4, 4
- Counts: 37, 25, 13, 1, 0, 7, 2, 0
- Not matching well.

Maybe sliding windows of size 6 containing all good?
- 48: 43; 36: 31; 24: 19; 12: 7; 6: 1; 18: 13; 12+12: 14; 8+8+8: 9
- Scores: 9, 6, 3, 1, 0, 2, 4, 4
- 48→43→9: maybe 43/5≈9? 
- 31/5=6.2→6 ✓
- 19/5=3.8→3 ✓
- 7/5=1.4→1 ✓
- 1/5=0.2→0 ✓
- 13/5=2.6→2 ✓
- 14/5=2.8→2 (got 4!) ✗

Close but not right. Maybe divisor different. Let me check if just count divided by 5 explained single-run cases.

OK actually for the single-run cases f(L) = floor((L-5)/5) works:
- L=48: 43/5=8.6→8 (got 9) ≠
- L=48: (48-5)/5=8.6→8 ✗

But windows of length 6 = L-5 fits all single-run cases as floor((L-5)/5)? Let me recompute:
- L=48: L-5=43, /5=8.6→8 (got 9)

Hmm, off by 1 there too.

Maybe windows of length 5? Count = L-4 for run L.
- L=48: 44, /5=8.8→8
- Or just count all such windows and apply some other transform.

OK let me try: score = floor((BB count) / something) where BB = consecutive same-good pairs (length-2 windows).
Run L gives L-1 BB pairs.
- 48: 47, 36: 35, 24: 23, 12: 11, 6: 5, 18: 17
- 12+12 split: 11+11 = 22
- 8+8+8 split: 7+7+7 = 21
- Scores: 9, 6, 3, 1, 0, 2, 4, 4
- 47/9≈5.22, 35/6≈5.83, 23/3≈7.67, 11/1=11, 5/0=∞, 17/2=8.5, 22/4=5.5, 21/4=5.25
- Not constant.

Maybe count of length-k all-good windows for varied k. Try k=7:
- Run L: max(0, L-6). L=48:42, 36:30, 24:18, 12:6, 6:0, 18:12.
- 12+12: 6+6=12; 8+8+8: 2+2+2=6.
- Scores: 9,6,3,1,0,2,4,4. /something:
- 42/9=4.67, 30/6=5, 18/3=6, 6/1=6, 0/0=NA, 12/2=6, 12/4=3, 6/4=1.5.

Try k=8 (max(0,L-7)):
- 48:41, 36:29, 24:17, 12:5, 6:0, 18:11
- 12+12: 5+5=10; 8+8+8: 1+1+1=3
- Scores: 9,6,3,1,0,2,4,4
- Hmm 8+8+8 gives 3 windows but score 4. 

What if score = some function involving good count AND number of runs?
- (24,1 run): 3
- (24,2 runs): 4
- (24,3 runs): 4
- (24,24 runs alternating): 0
- (12,1 run): 1
- (36,1 run): 6
- (18,1 run): 2
- (6,1 run): 0

Maybe score = (sum L_i² ) / something:
- 1×48² = 2304 → 9. 2304/9=256.
- 1×36² = 1296 → 6. 1296/6=216.
- 1×24² = 576 → 3. 576/3=192.
- 1×12² = 144 → 1. 144/1=144.
- 1×18² = 324 → 2. 324/2=162.
- 2×12² = 288 → 4. 288/4=72.
- 3×8² = 192 → 4. 192/4=48.
- 24×1² = 24 → 0. 24/0=undef.

Not constant. But increasing.

How about (sum L_i² / 48²) * something:
- 2304/2304=1, *9=9 ✓
- 1296/2304=0.5625, *9=5.06 (got 6) ✗

OK perhaps something nonlinear. Try (sum L_i (L_i+1)/2):
- 48: 1176 → 9, /9=130.67
- 36: 666 → 6, /6=111
- 24: 300 → 3, /3=100
- 12: 78 → 1, /1=78
- 18: 171 → 2, /2=85.5

Not constant either. Diverging.

Idea: maybe the score uses both count of goods and a "complexity"/structure measure, OR maybe I should try to fit a simpler formula and look at it differently.

Look: scores for runs are 0,0,1,2,3,6,9 for L=1,6,12,18,24,36,48 (treating 1 alt as L=1).
Actually 1 alt isn't a "run of 1", it's many runs of 1.

For just runs (single), L → score:
6→0, 12→1, 18→2, 24→3, 36→6, 48→9

What about f(L) = number of (i,j) with i<j, both in run, and j-i = something?

Or just: f(L) = floor(L/6) × something? 
- 6/6=1→0
- 12/6=2→1
- 18/6=3→2
- 24/6=4→3
- 36/6=6→6
- 48/6=8→9 (not 8!)

Or f(L)= max(0, floor(L/6)-1) for small, then increasing fast?
- 6: 0 ✓
- 12: 1 ✓
- 18: 2 ✓
- 24: 3 ✓
- 36: 5 (got 6) ✗
- 48: 7 (got 9) ✗

Hmm what about f(L) = sum of length-6 chunks where each chunk contributes increasing?

OK let me just try test points. I need single runs of intermediate lengths.

## 2026-06-28 15:09 — query 23

## More single-run data
L: 6, 12, 18, 24, 30, 36, 42, 48
f: 0, 1, 2, 3, 4, 6, 7, 9

Hmm interesting. Diffs: 1,1,1,1,2,1,2. Not linear.

Try f(L) = floor(L²/256)?
- 36: 1296/256=5.0625→5 (got 6) ✗
- 48: 2304/256=9 ✓
- 42: 1764/256=6.89→6 (got 7) ✗

Try f(L) = round(L²/256)?
- 36: 5.06→5 (got 6) ✗

Try f(L) = floor((L²+128)/256) = round(L²/256, half-up)?
- 36: (1296+128)/256 = 1424/256 = 5.56→5
- Still no.

Try f(L) = floor(L*(L+a)/b):
Solve from points: f(48)=9, f(36)=6, f(24)=3, f(12)=1, f(6)=0
- 9 = floor(48*(48+a)/b)
- 6 = floor(36*(36+a)/b)
- 3 = floor(24*(24+a)/b)

If exact: 48(48+a)/b = 9, 36(36+a)/b = 6, 24(24+a)/b = 3 (treat as continuous).
Divide first two: [48(48+a)]/[36(36+a)] = 9/6 = 1.5
48(48+a) = 54(36+a)
2304 + 48a = 1944 + 54a
360 = 6a → a = 60
Then b = 48*(48+60)/9 = 48*108/9 = 576.
Check 36: 36*96/576 = 3456/576 = 6 ✓
Check 24: 24*84/576 = 2016/576 = 3.5 (got 3) - off
Check 12: 12*72/576 = 864/576 = 1.5 (got 1) ✓ floor
Check 18: 18*78/576 = 1404/576 = 2.44 → 2 ✓
Check 30: 30*90/576 = 2700/576 = 4.69 → 4 ✓
Check 42: 42*102/576 = 4284/576 = 7.44 → 7 ✓
Check 6: 6*66/576 = 396/576 = 0.69 → 0 ✓
Check 48: 48*108/576 = 9 ✓ (exact)
Check 24: 3.5 → 3 (floor) ✓
Check 36: exactly 6 ✓

So f(L) = floor(L*(L+60)/576) fits all single-run data points! Let me verify split runs:
- 12+12 split (24 good total): if score = sum f(L_i), 1+1=2 (got 4!) ✗
- 8+8+8: f(8) = 8*68/576 = 544/576 = 0.94→0. 0+0+0=0 (got 4!) ✗

So not just sum of single-run f. But formula works perfectly for single runs.

Maybe score = f(total_good_count) if all goods form one run, but reduces if scattered? No — 12+12=4 > f(24)=3.

What if score = f(total good count adjusted for arrangement)? 
24 in one run: 3
24 in two runs: 4
24 in three runs: 4
24 alternating: 0

Maybe score = f(some "effective length" computed from arrangement). f^-1(4) = solve x(x+60)/576 ≥ 4 → x²+60x ≥ 2304 → x ≈ 26.4. So effective length ~27 for 12+12. And ~27 for 8+8+8. And 0 for alternating.

Hmm. Let me try: maybe score depends on max run length AND total count?
- Max run, total → score
- 48, 48 → 9
- 36, 36 → 6
- 24, 24 → 3
- 12, 12 → 1
- 18, 18 → 2
- 6, 6 → 0
- 12, 24 (two runs of 12) → 4
- 8, 24 (three runs of 8) → 4

So max run 12 + total 24 → 4 (but max run 24 + total 24 → 3). Higher max run doesn't always help if it costs goodness. 

Maybe: score depends on (count of good)² / 48 + small correction?
- 48²/48=48? Nope too big.

Maybe score = f(count) - penalty(arrangement)?
- 48 goods, 1 run: f(48)=9, score 9. penalty 0.
- 36, 1: f(36)=6, score 6. penalty 0.
- 24, 1: f(24)=3, score 3. penalty 0.
- 24, 2 runs of 12: score 4. f(24)=3. So bonus +1 for splitting.
- 24, 3 runs of 8: score 4. f(24)=3. Bonus +1.
- 24, 24 runs: score 0. f(24)=3, penalty -3.
- 12, 1 run: f(12)=1, score 1.

So splitting helps moderately but extreme fragmentation hurts.

Theory: maybe the formula depends on count of good AND count of "good blocks" or similar.

Let me think: maybe score = floor(N * (N + a*R - b) / c) where N=good count, R=number of runs.
Or maybe score = floor((N - bad_neighbors) * (...) / ...).

Let me try test: 24 goods as 6+6+6+6 split (4 runs of 6).

## 2026-06-28 15:10 — query 26



## 2026-06-28 15:10 — query 26

## Runs data refinement
24 goods arrangement → score:
- 1×24: 3
- 2×12: 4
- 3×8: 4
- 4×6: 6 (!)
- 6×4: 5
- 8×3: 0
- 24×1 (alternating): 0

Interesting! 4×6 with 6 spacers gives 6. 6×4 with 4 spacers gives 5. 8×3 with 3 spacers gives 0.

The 4×6 is essentially a period-12 pattern (B^6 A^6 repeated). The 6×4 is period-8 (B^4 A^4). The 8×3 is period-6.

Maybe there's a periodicity preference. Periods 12, 8 give good scores; period 6 doesn't.

Let me also check: 3×8 = period 16 (B^8 A^8). 2×12 = period 24. Could be that periodicity matters with block size ≥ 4.

Hypothesis: score = number of pairs of good letters at distance exactly some d (or in window of certain size)? 
- Period 12 with B^6 A^6: 4 B-blocks of 6. Pairs of B at distance ≤ k:
  - within a block: lots of close pairs
  - between blocks: distance ≥ 6+1 = 7+ 

Let me try: maybe score counts pairs of B at distance exactly 12.
- 4×6 pattern: positions 1-6, 13-18, 25-30, 37-42. Pairs at distance 12: (1,13),(2,14)...(6,18), (13,25)...(18,30), (25,37)...(30,42). 6+6+6=18 pairs. Score 6. 18/3=6.
- 3×8 split (positions 1-8, 17-24, 33-40): pairs at distance 12? (5,17)...(8,20), no (8,20) — 20 is in second block? 17-24 yes. So pairs of distance 12 between first and second block: (5,17),(6,18),(7,19),(8,20) = 4 pairs. Between second and third (17-24 and 33-40): (21,33)...(24,36) = 4 pairs. Plus internal: within an 8-block, distance 12 impossible. Total 8. /3=2.67. Got 4 actual. Hmm.

Let me try pairs at distance exactly some d.

Hmm I need to think more carefully. Let me try a few well-designed experiments.

## 2026-06-28 15:10 — query 29

## More tests
- B^4 A^8 period 12 (16 goods): 0
- B^8 A^4 period 12 (32 goods): 6
- B^4 A^2 period 6 (32 goods): 0
- 4×6 period 12 (24 goods): 6
- Old: B^6 A^6 period 12 → 6.

Interesting! B^4 A^2 (period 6, 32 goods) is 0 but B^4 A^8 (period 12, 16 goods) is 0.

Pattern: period 6 patterns score 0; period 12 patterns score ≥ 6 when block ≥ 6.

Maybe key threshold: each B block needs length ≥ 5 or 6 to contribute, and they need to be far enough apart (≥6 spacing) so they don't "interfere".

Let me check: B^4 A^8: B blocks of length 4 (< 6 perhaps required) → 0.
B^8 A^4: B blocks of 8 with A spacers of 4. Score 6. But B^4 A^2 (B blocks of 4) score 0.

So spacer length 4 between B^8 → 6. Spacer of 2 → 0. Spacer requirement.

Hmm and 3×8 with A^8 spacers gave score 4. Same B^8 but A^8 → 4 vs B^8 A^4 → 6. Different.

Let me think differently. Maybe it's about specific motifs. Let me try BAB or BABB patterns.

## 2026-06-28 15:10 — query 30

## MAJOR DISCOVERY
CDCDCDCD... = 9! But BABABA... = 0! Both alternating good/bad.

So C and A are NOT both "bad" in the same way. CD alternating gives full score!

Let me reconsider. The earlier homopolymers:
- A: 0, B: 9, C: 0, D: 9, E: 0, F: 9

But CD alternating: 9. So C is not simply bad.

Maybe what matters isn't just letter identity but pairs/adjacency. Let me think: CD = c+d, which alternates. Maybe certain bigrams score.

Let me test more bigrams:
- AB alt: 0
- CD alt: 9
- EF alt: ?
- BA alt: 0 (same as AB)
- AC alt: 0
- DC alt: same as CD = 9

Maybe pattern: pairs (X,X+1) where X is even? A=0,B=1,C=2,D=3,E=4,F=5. AB:(0,1), CD:(2,3), EF:(4,5). So CD has letters (2,3); AB has (0,1).

Maybe what matters is the actual letters used and there's a "score table" for bigrams or maybe just one positional bigram preference. Let me test EF alternating.

## 2026-06-28 15:10 — query 33

## Specific pair test
- CD alternating: 9
- DC alternating: 9
- EF alternating: 0
- FE alternating: 0
- BA / AB alternating: 0
- CDCDCD... vs DCDCDC... both 9

So C+D combo is special. Maybe specific letter combos are scoring patterns.

Let me test more pairs:
- BC, BE, BF, CE, CF, DE, DF, AD, AE, AF
- Maybe CD is the only special one, or there are several.

## 2026-06-28 15:11 — query 38

## Pair alternation results (score 9 = good, 0 = bad)
- AB: 0
- BC: 9
- CD: 9
- DE: 0
- EF: 0
- BD: 9
- BE: 0
- CE: 0

So scoring 9: BC, CD, BD. Scoring 0: AB, DE, EF, BE, CE.

What's special about B,C,D? They all give 9 when alternated together (BC, CD, BD). 

Maybe the rule is: positions 1,2,3,4 alternate, but only if all letters used are from {B,C,D}?

Wait BC has C (which homopolymer gave 0). So it's not just about "good letters". BC together = 9, but B alone = 9 and C alone = 0. So C is rescued by B's presence?

Or maybe the rule is something like: each position contributes based on the letter at that position AND something about its neighbors.

Test: maybe what matters is consecutive pairs that satisfy some constraint, like "different letters from {B,C,D}".

Let me test some other patterns:
- AAAAA...BCBC...AAAAA — see if BC region scores within a larger context
- BBCCBBCC — same letters but blocks

Or maybe the score is based on the SET of letters used somehow:
- {B}: 9
- {D}: 9
- {C}: 0
- {B,D}: 9
- {C,D}: 9
- {B,C}: 9
- {A,B}: 0
- {D,E}: 0
- {E,F}: 0
- {C,E}: 0
- {B,E}: 0

Sets giving 9: {B}, {D}, {F}, {B,D}, {B,D,F}, {B,C}, {C,D}, {B,C,D} likely
Sets giving 0: {A}, {C}, {E}, {A,B}, {C,E}, {D,E}, {E,F}, {B,E}

Hmm, presence of E or A or F in non-pure form might hurt? But {F} alone = 9, {B,D,F} = 9. So F alone is fine but maybe F+something hurts? 

Wait, {E,F}: 0. And {F}: 9. So F is fine alone but E+F = 0. Similarly D alone fine, D+E = 0.

Hypothesis: maybe E is "poison" that kills score for any sequence containing E (and similarly A poisons). Let me check: {C,E}=0, {B,E}=0, {D,E}=0, {E,F}=0, {E}=0. Pattern: presence of E → 0. Similarly, presence of A → 0? {A}=0, {A,B}=0. Yes.

What about C? {C}=0, but {B,C}=9, {C,D}=9. So C alone = 0 but C+(B or D) = 9.

So C requires B or D to be present?

Let me test: pure F vs F+A.

## 2026-06-28 15:11 — query 44

## C is NOT bad in B background — gives 9 even with C's spread.
- 4 C's in B: 9
- 4 A's in B: 7 (decreased)
- 1 A in B: 9 (no penalty)
- 1 E in B: 9
- 1 A in F: 9
- alternating FA: 0

So one bad letter is tolerated. Multiple A's reduce score. But C doesn't reduce score.

Let me revisit: 
- CD alternating (24 C's, 24 D's): 9. So lots of C's are fine if mixed with D.
- AB alternating (24 A's, 24 B's): 0. Lots of A's are bad.

So maybe A is genuinely "bad" and C is neutral/good in some contexts.

Let me classify:
- A: bad
- B: good  
- C: neutral (good in context of B/D, bad alone)
- D: good
- E: bad
- F: good

So {B,D,F}: strongly good; {A,E}: strongly bad; {C}: neutral.

Let me verify by testing more E mixtures.

## 2026-06-28 15:11 — query 47

## A specifically penalizes!
- 8 A's spaced (period 6): 0
- 8 E's spaced (period 6): 9
- 4 E's (period 12): 9
- 4 A's (period 12): 7

So A is much worse than E. E seems mostly neutral when sparse. But EF alternating (24 E's) = 0. Maybe E in large amount becomes bad, or E+F is specifically bad.

Wait, BE alternating = 0. So 24 E's mixed with B = 0. But 8 E's in B = 9. So E becomes problematic at higher density.

Let me test threshold of E in B.

## 2026-06-28 15:11 — query 51

## A count vs score in B background
- 0 A: 9
- 1 A: 9
- 2 A: 9
- 3 A: 8
- 4 A: 7
- 8 A: 0

Looks like score ≈ 9 - (A count - 2) for A_count > 2, with cliff at 8.

Actually, 9, 9, 9, 8, 7, ..., 0 at 8. So between 4 and 8 A's, it drops by 7 over 4 steps. Maybe non-linear.

E count vs score in B:
- 0 E: 9
- 1 E: 9
- 4 E: 9
- 8 E: 9
- 12 E: 9
- 16 E: 9
- 24 E (BE alt): 0

E is much less penalizing than A.

Let me try larger E counts.

## 2026-06-28 15:12 — query 53

## Hmm
- 24B + 24E (block): 3 (same as 24B + 24A block!)
- 24B + 24A (block): 3
- BE alt: 0
- BA alt: 0
- 21 E's (mostly alt-BE start): 8

So when bad letters form a long run, the bad portion is just "wasted" but good portion still scores. When mixed in, they kill structure.

OK I think the model is more subtle. Let me reconsider: maybe what matters is just RUNS of B-or-D-or-F (good), and A/C/E are all "bad" but different bad letters have different interaction with the surrounding chars.

Wait, I had: 1 C in B (with several C's spread): 9. And CDCD: 9.

So C is special. Let me re-examine:
- BBBBB...CCCCC... ? haven't tested

Let me think more globally. Maybe the scoring rule involves consecutive same letters or specific bigrams.

Let me test specific bigrams: count occurrence of "BB" in scoring.
- 48B: 47 BB → 9
- BABABA: 0 BB → 0
- CDCDCD: 0 BB → 9 (but no BB!)

So it's not about BB count alone. CDCDCD has zero BB but scores 9. Maybe what matters is "transitions" or something.

Let me think: CDCD has the property that every position is different from its neighbor and all letters are from {B,C,D,F}? Let me check.

Hypothesis: score = 9 if every position contains a letter from {B,C,D,F} (i.e., no A and no E)?
- AB: has A, 0 ✓
- BC: B,C — no A/E, all from valid set. Score 9 ✓
- CD: 9 ✓
- DE: has E, 0 ✓
- EF: has E, 0 ✓
- BD: 9 ✓
- BE: has E, 0 ✓
- CE: has E, 0 ✓
- 4 C's spread in B: 9 ✓
- 8 E's in B: 9? But E is "bad" by this rule, should be 0! But we got 9.

Hmm, doesn't fit. So {A, E} aren't both equally bad.

Actually 8 E's in B scored 9. So E isn't bad in moderation. But EF gave 0 (24 E's).

What about FFFFF...EEEEE...?

## 2026-06-28 15:12 — query 55

## Block patterns
- 24B + 24C block: 3
- 24B + 24A block: 3
- 24B + 24E block: 3
- 24B + 24D block: 9 (D is good!)
- 24F + 24E block: 3

So when split into 24+24 blocks, only good+good (B+D or B+F etc.) gives 9. Otherwise gives 3.

CDCD alternating: 9 (despite half C's). C in 24-block with B: 3. So C alternated with D is special.

Hmm, maybe the rule is: consecutive pairs (i, i+1) are scored. Each (i,i+1) bigram contributes some score. Total = sum / something.

Let me think about which bigrams = good (give 9 when whole sequence is alternating):
- BB: 9 (homopolymer B)
- DD: 9
- FF: 9
- CC: 0 (homopolymer C)
- AA: 0
- EE: 0
- BC: 9 (BCBC also has CB)
- CB: 9 (in BCBC)
- CD: 9 (CDCD has DC too)
- DC: 9
- BD: 9 (BDBD has DB)
- DB: 9
- BA: 0
- AB: 0
- DE: 0
- ED: 0
- EF: 0
- FE: 0
- BE: 0
- EB: 0

Hmm, so bigrams from {B,C,D} are scoring, bigrams with A or E or F mixed with C are not tested. Wait, BF: not tested. Let me see what's the pattern.

Maybe the scoring is based on letter→number mapping where A,C,E=odd? No, A,C,E gave 0.

Look at letter values: A=0, B=1, C=2, D=3, E=4, F=5.
Bigrams giving 9: BB(1,1), DD(3,3), FF(5,5), BC(1,2), CB(2,1), CD(2,3), DC(3,2), BD(1,3), DB(3,1).
Bigrams giving 0: AA(0,0), CC(2,2), EE(4,4), AB(0,1), DE(3,4), EF(4,5), BE(1,4), CE(2,4), BA, ED, FE, EB.

Sum mod something? BB=2, BC=3, BD=4, CC=4, CD=5, DD=6, FF=10, BE=5, CE=6, DE=7, EF=9, BA=1, AA=0.

Sum % 3? BB=2, BC=0, BD=1, CD=2, DD=0, DC=2, FF=1, BC=0. Hmm scoring bigrams have mixed values.

Maybe based on |i-j|: differences for scoring bigrams: BB=0, DD=0, FF=0, BC=1, BD=2, CD=1. For non-scoring: AA=0, CC=0, EE=0, AB=1, DE=1, EF=1, BE=3, CE=2.

So |i-j|=0 for B,D,F: 9. |i-j|=0 for A,C,E: 0.

|i-j|=1 for BC: 9. |i-j|=1 for AB: 0. |i-j|=1 for CD: 9. DE: 0. EF: 0.
|i-j|=2 for BD: 9. CE: 0.

Hmm patterns: bigrams "good" are those where both letters are in {B,C,D,F}? But CC=0. So not just about set.

Bigrams good ↔ at least one of the two letters is in {B,D,F} AND the other is NOT A or E (i.e., in {B,C,D,F})? Let me check:
- BC: B is in {B,D,F}, C is in {B,C,D,F}. ✓ 9
- BD: both in {B,D,F}. ✓ 9
- CD: D in {B,D,F}, C in {B,C,D,F}. ✓ 9
- DC: same. 9
- BB: ✓ 9
- AB: A not in good. ✗ 0
- DE: E not in valid set. ✗ 0
- EF: E not in valid set. ✗ 0
- BE: E not in valid set. ✗ 0
- CE: E not in valid set. ✗ 0
- CC: C is not in {B,D,F}. So bigram needs at least one in {B,D,F}? CC has neither. ✗ 0

So rule for bigram (X,Y) to score: X ∈ {B,D,F} OR Y ∈ {B,D,F}, AND neither is in {A,E}.

Equivalently: both letters in {B,C,D,F}, and at least one in {B,D,F}.

OR: both letters good or C-adjacent-to-good.

Let me restate: "bad" letters are A and E. C is neutral. {B,D,F} are good.
A bigram scores if it contains no bad letter AND at least one good letter.

Alternatively: a position is good if it's in {B,D,F}; tolerable if C; bad if A or E. Bigram scoring requires no bad and at least one good.

Now what about the full-sequence score? Let me check: 
- BBBB...: every bigram BB, all score. 47 good bigrams → score 9.
- CDCD...: every bigram CD or DC. All score. 47 good bigrams → 9.
- BC alternating: 47 good bigrams (BC or CB) → 9.
- CC homopolymer: 47 CC bigrams, none score → 0.

Let me test the count-of-good-bigrams hypothesis with single B-run cases:
- Run of 12 B in 36 A: bigrams = AA*?, BB*11, AB, BA. Good bigrams = 11 BB's = 11. Score observed 1.
  - 11 → 1. Maybe (good_bigrams - 9) / 4 = 0.5? Or floor((good_bigrams-2)/5)?
- Run of 24: 23 BB. → 3. Ratio 23/3 ≈ 7.7.
- Run of 48: 47 BB → 9. 47/9 ≈ 5.2.
- 12+12 split (24 goods): 11 + 11 = 22 BB. → 4. 22/4 = 5.5.
- 8+8+8 split: 7+7+7 = 21. → 4. 21/4 = 5.25.
- 4 runs of 6: 5*4=20 BB. → 6. 20/6 = 3.33.

Wait that doesn't match a single ratio. Let me reconsider.

But what about CC? In a run of B's surrounded by C's, the BC bigrams score too! 

Let me reconsider single-run B with A surroundings:
- 36 A's + 12 B run: bigrams of interest: AA*many, AB or BA (boundary), BB*11. With A as "bad", only BB bigrams score. So 11 good bigrams.

Let me revisit 4×6 pattern (B^6 A^6 ×4): 
- bigrams within each B^6 block: 5 BB. Total 4*5=20 BB. 
- Plus boundary: BA, AB at each block edge: don't score.
- Total good bigrams = 20. Score 6.

vs 1×24 run: 23 BB. Score 3. So fewer bigrams but more score! Doesn't fit just bigram count.

Hmm. The pattern still isn't bigram-based linearly.

Wait but maybe what matters is the count of bigrams (i, i+k) for various k, weighted? Or trigrams?

Let me try a different angle: count of GOOD positions, where good = in {B,D,F}. 
- 4×6 B blocks: 24 good positions. Score 6.
- 1×24 run: 24 good. Score 3.

Same good count, different scores. So position arrangement matters.

What about: count of positions where left neighbor is good AND right neighbor is good?
- 1×24 run: positions 2-23 have both neighbors B (=good). That's 22. Score 3.
- 4×6 split with A^6 spacers: each B^6 block has positions in middle (2nd through 5th of block) with both B neighbors. = 4 per block × 4 blocks = 16. Score 6.

16 vs 22, but scores 6 vs 3. So less is more? Doesn't make immediate sense.

Let me try yet another approach: maybe each "transition" from good to bad costs nothing but each pure-good run contributes a quadratic function and there's bonus for having multiple runs.

Or maybe the scoring involves the BAD positions explicitly. Count of bad positions:
- 1×24 B run (with A's): 24 bad. Score 3.
- 4×6 B blocks (with A spacers): 24 bad. Score 6.

Same bad count, different. So just count doesn't help.

Let me check: in 4×6 (B^6 A^6 × 4), the A's form 4 runs of 6 too. So both B and A are in 4 runs of 6.
In 1×24 (B^24 A^24), both B and A are in 1 run of 24.

Maybe scoring rewards "more runs" of good?

Going to try test "many small runs" deliberately.

## 2026-06-28 15:13 — query 58

## More data
- 4×6 B with C spacers (B^6 C^6): 6 (same as A spacers!)
- 4×6 B with E spacers (B^6 E^6): 6
- BBBC repeat (36 B + 12 C): 9!

So having lots of C's mixed with B's gives 9 perfectly. But B^6 C^6 gives only 6, not 9. The difference: in BBBC, every 4th letter is C, but C is always adjacent to B's. In B^6 C^6, the middle of each C-block has CC pairs (C surrounded by C).

This strongly suggests: every position needs a "good neighbor" (B/D/F adjacent). C is OK if it has good neighbors; bad if isolated from good.

Hypothesis: score = function of how many positions are "satisfied" where:
- {B,D,F} positions are always satisfied
- C positions need a {B,D,F} neighbor
- {A,E} positions are never satisfied (and may penalize)

Let me check:
- All B: 48 satisfied → 9
- CDCD: every C has D neighbor, every D has C-and-D neighbors. All 48 satisfied. → 9 ✓
- BC alternating: every C has B neighbors, every B has C neighbors. All satisfied. → 9 ✓
- CC (homopolymer): no C has good neighbor. 0 satisfied. → 0 ✓
- BBBC repeat: B's all satisfied (B neighbors); C is at position 4,8,...,48. Each C has B left, B right (or end). Position 48 is C with B at 47 and no right. 47 satisfied? Let's say boundary OK with one neighbor. All satisfied → 9 ✓.
- B^6 C^6: B's good. C's: middle C's have C neighbors only — NOT satisfied. Each C^6 block: positions are C, neighbors C-C, C-C, C-C, C-C, C-C, C-B (last C). So only the C adjacent to B is satisfied. So in each C^6 block, only 1 C (the one adjacent to B) is satisfied; 5 C's are unsatisfied. Actually need to think about both sides. 
- 4 C-blocks each 6 long. Boundary C's (first and last of each block) are adjacent to B. Middle 4 C's are between C's only. So 2 satisfied + 4 unsatisfied per block = 4*2 = 8 satisfied C's, 4*4 = 16 unsatisfied C's. Plus 24 B's all satisfied. Total satisfied = 32. Score 6.

For 48 satisfied → 9. For 32 → 6. Ratio fits: 9 * 32/48 = 6 ✓!

Test 1 B-run of 12 in 36 A:
- B's all satisfied (B neighbors), except endpoint B's which have A neighbor on one side. All 12 B's satisfied (need at least one good neighbor? then all B's satisfied if they have any B neighbor; endpoint B's have B on one side).
- A's never satisfied (A is bad). 
- Total satisfied: 12. Score = 9 * 12/48 = 2.25 → 2? But observed 1.

Hmm off. Let me reconsider B's at boundaries. Maybe B needs B neighbor too? Or maybe A's adjacent count?

In 1B run of 12: middle B's have B neighbors. Endpoint B's have one A neighbor. If B needs all neighbors good, endpoints fail. 10 satisfied. 9*10/48=1.875→1. Closer.

Run of 24: 22 satisfied. 9*22/48 = 4.125 → 4. But observed 3.

Hmm still off. Let me think.

Maybe rule: a position is satisfied if BOTH neighbors are non-bad (where A, E are bad)?
- B in 1×24 run with A on both sides: middle 22 B's have B neighbors (non-bad). 2 endpoint B's have A on one side (bad). So 22 satisfied B's. A's: never (A itself is bad).
- 22 → score 3. 22/48 *9 = 4.125. Not 3.

Try (satisfied^2) / 256: 22²/256 = 484/256 = 1.89. No.

Try floor(satisfied / something):
- 48 sat → 9: divisor 5.33
- 22 sat → 3: divisor 7.33
- Variable.

Maybe the rule is more complex: count satisfied minus count "bad". 
- 1×24 B run + 24 A: 22 satisfied, 24 bad. 22-24 = -2 → 0? Got 3.
- Doesn't fit.

Let me check 4×6 with A spacers more carefully.
- Positions 1-6: B's. Position 1 has nothing left, position 7 is A. So position 1 B has 1 B neighbor. Position 2-5 B's have 2 B neighbors. Position 6 B has B left, A right.
- "Satisfied" if both neighbors non-bad? Position 1: only right neighbor (B). Satisfied. Position 6: A on right, fail. Position 2-5: satisfied.
- Per B^6 block: positions 1,2,3,4,5,6 (of block). Satisfied = 5 (position 1 OK by being endpoint with B-right; position 6 fails). Hmm wait position 1 of block is preceded by A or nothing.
- Actually for B^6 A^6: block 1 positions 1-6 (B), block 2 positions 7-12 (A). B at pos 1 has no left, A right? No wait, pos 1 has no left, pos 7 is A. So pos 1's right is pos 2 (B). Pos 6's right is pos 7 (A).
- Hmm hard to track. Let me just count B's with at least one bad neighbor (= "edge" B's).

Maybe the rule is: penalize each B that has a bad neighbor. Or count pure-good-context positions.

Need more systematic experiments. Let me create a scoring model and test.

## 2026-06-28 15:14 — query 62



## 2026-06-28 15:14 — query 63

## BC pattern data
- BC repeat (period 2, 24B 24C): 9
- BCC (period 3, 16B 32C): 9
- BCCC (period 4, 12B 36C): 7
- BCCCC (period 5, 9B 39C): 7 (wait, BCCCC has B's at positions 1,6,11,...; with length 48: ⌊48/5⌋ = 9, plus position 46 starts BCC = 10 B's, no actually re-count. Pattern BCCCC repeated 9 times = 45 chars, plus BCC=3 → 10 B's? Sequence is BCCCCBCCCCBCCCC...BCCCCBCC. Count B's: 10.)
- BCCCCCC (period 7): 6

So with B every 2,3 positions: score 9. Every 4-5: 7. Every 7: 6.

Each C needs to be within distance 1 of a B (or within distance ≤ k for some k).

In BCCC: positions of C: 2,3,4. Position 2 is adjacent to B (1). Position 3 is between C(2) and C(4). Position 4 is adjacent to B(5). So middle C (pos 3) is not adjacent to B.

Each "BCCC" block of length 4 has 1 unsatisfied C (middle).

For period 4 with 12 B's: 36 C's total. Of these, how many are "next to B"? In each BCCC: C2 next to B1, C4 next to B5 (next block). C3 only has C neighbors. So 2/3 C's satisfied. Total satisfied C's = 24. Plus B's = 12. Total satisfied = 36.
Score = 9 * 36/48 = 6.75 → 7 ✓ (with rounding/flooring)

For period 5 (BCCCC): C's at positions 2,3,4,5. C2 adj B1. C3 adj C only. C4 adj C only. C5 adj B6. So 2/4 C's satisfied per block. 
With 10 B's (approximate, edge handling): roughly 10 B's + 20 satisfied C's = 30. Score = 9*30/48 = 5.6 → 6? But got 7.

Hmm. Let me recount BCCCC sequence: "BCCCCBCCCCBCCCCBCCCCBCCCCBCCCCBCCCCBCCCCBCCCCBCC"
- That's 48 chars. Let me count B's: positions 1,6,11,16,21,26,31,36,41,46. So 10 B's, 38 C's.
- C's adjacent to B: C2 (B1), C5 (B6), C7 (B6), C10 (B11), C12 (B11), C15 (B16), C17 (B16), C20 (B21), C22 (B21), C25 (B26), C27 (B26), C30 (B31), C32 (B31), C35 (B36), C37 (B36), C40 (B41), C42 (B41), C45 (B46), C47 (B46), C48 (B46 at distance 2 - no).
- Actually C47 is adj to C46... wait no, position 46 is B. C47 is adj to B46 and C48. So C47 satisfied.
- C48 is adj to C47 only. Not satisfied.
- So satisfied C's: C2, C5, C7, C10, C12, C15, C17, C20, C22, C25, C27, C30, C32, C35, C37, C40, C42, C45, C47. That's 19. 
- Unsatisfied C's: C3, C4, C8, C9, C13, C14, ..., C48. Let me count: per 5-block (BCCCC), the unsatisfied are positions 3,4. 9 full blocks → 18. Plus C48 unsatisfied. Total 19.
- Total satisfied = 10 B + 19 C = 29. 9 * 29/48 = 5.44 → 5? But got 7.

Hmm doesn't match. Maybe the threshold is different — distance 2?

If C needs B within distance 2: C2 (B1: d1) ✓, C3 (B1: d2) ✓, C4 (B5: wait, but there's B at pos 6 — d2 from C4) ✓, C5 (B6: d1) ✓. So all C's in BCCCC satisfied!
Then for BCCCC period 5: 10 B + 38 satisfied C = 48. Score should be 9. But got 7.

So distance 2 too generous. Maybe distance 1 with continuous propagation? Or each C between two C's gets a "reduced" satisfaction?

Try BCCCCCC (period 7, 7 B's, 41 C's). 
- C2: B1 d1 ✓
- C3: C2,C4 — no B nearby (d2 to B1)
- C4: C only adjacent
- C5: C only adjacent
- C6: C only
- C7: B8 d1 ✓
- So 2/6 C's per block satisfied → wait 6 C's per block actually, positions 2-7 if block is BCCCCCC.
- 2/6 satisfied = 1/3.
- Total satisfied: ~7 B + 41*(2/6) = 7 + 13.67 = 20.67. Score 9*20.67/48 = 3.88. Got 6.

So my model is wrong. Real score is higher than predicted by "adjacent to B" rule.

Let me try another model: maybe a sliding window scoring. E.g., the score for each position depends on its window.

Maybe each position contributes based on how many B/D/F are in its 5-window (positions ±2).

Try: in BCCC (period 4), at each position consider window of ±2.
- Pos 1 (B): window 1-3 = BCC. 1 good. 
- Pos 2 (C): window 1-4 = BCCC. 1 good.
- Pos 3 (C): window 1-5 = BCCCB. 2 good.
- Pos 4 (C): window 2-6 = CCCBC. 1 good.
- ...

Avg good per window ~ 1.something. Multiply by 48 and divide... unclear.

Let me try a really different hypothesis: maybe score = max_run_of_good_or_C-adjacent / 5, capped at 9.

Actually let me try a completely different model: SCAN-based scoring.

A position is "active" if it's B/D/F. C is active if adjacent to B/D/F. Then we look at runs of active positions.

Let me try this for BCCC period 4:
- B's active. C2 adj B1 active. C3: adj C2(active via B), but C3 not adj B → maybe not active? Or active if within reach.

This is getting hacky. Let me just measure more carefully.

Let me try BCC (period 3) — score 9.
Active under "C if adj B": all positions. Active run length 48. Score 9 ✓.

BCCC (period 4) — score 7.
Active C's: only edge C's. Layout per block BCCC:
- B C C C | B C C C | ...
- B active. C2 active (adj B1). C3 between C2,C4 — C3 adj to C (active, but C3 itself not adj to B directly). C4 adj to next-block B → active.
- So active: B, C2, _, C4. Active runs: B C2 (length 2), then C4 B5 C6, ...
- Actually full active map: B(1)C(2)_(3)C(4)B(5)C(6)_(7)C(8)B(9)...
- Active runs: 1-2 (length 2), 4-6 (length 3), 8-10 (length 3), ..., 44-46 (length 3), 48 alone? 
- Sequence position 1-48: BCCC BCCC BCCC BCCC BCCC BCCC BCCC BCCC BCCC BCCC BCCC BCCC
- 12 blocks, B at 1,5,9,...,45.
- Active positions: B's (1,5,...,45) and C's adjacent to B's: positions 2 (adj B1), 4 (adj B5), 6 (adj B5), 8 (adj B9), 10 (adj B9), ... 44 (adj B45), 46 (adj B45). Wait position 48 is C, adjacent to C47 only. Not active.
- Active position map: 1,2, _, 4,5,6, _, 8,9,10, _, 12,13,14, _, ..., _, 44,45,46, _, _
- Runs: 1-2 (2), then 4-6 (3), 8-10 (3), 12-14 (3), 16-18 (3), 20-22 (3), 24-26 (3), 28-30 (3), 32-34 (3), 36-38 (3), 40-42 (3), 44-46 (3). 
- 1 run of 2 + 11 runs of 3.
- Score = f-something? f(2)=0 likely. f(3)=? Let me use single-run table: f(L)=floor(L(L+60)/576). f(3) = 3*63/576 = 189/576 = 0.328 → 0. 
- Sum: 0+0×11 = 0. But observed 7. Doesn't fit.

OK my run-based model with that f formula was likely just a coincidence on those points.

Let me just take a step back and try to find a cleaner pattern.

Let me try a simpler hypothesis based on counting good positions weighted by neighborhood.

I'll continue experiments to pin down the rule.

## 2026-06-28 15:15 — query 67

## Half-pattern data
- BCBC*24 + AAA*24: 3
- BCBC*24 + CCC*24: 3 
- BCBC*36 + CCC*12: 6
- BCBC*48: 9

Hmm, in BCBC*24 + CCC*24: the first 24 are alternating BC (all "satisfied" via my rule), the last 24 are CCC (none satisfied). 24 satisfied / 48 → 3. Fits ratio!

Score = 9 * (satisfied / 48)?
- 24/48 *9 = 4.5 → 3 (floor)? No, 4 or 5 typically.
- 48 sat = 9, 24 sat = 3? That's not 9*24/48=4.5.
- Maybe 9 * (sat/48)^2? 9*(0.5)^2 = 2.25 → 2 not 3.
- Maybe floor((sat-?)²/?):
- 24 → 3, 36 → 6 (from BCBC*36 + CCC*12 which has 36 satisfied first part + 0 satisfied last part... but actually the boundary C might still be next to B).

Let me re-examine BCBC*36 + CCC*12:
- Positions 1-36: BCBCBC...BC. Last char is C (at position 36).
- Position 37-48: all C.
- Position 36: C, adjacent to B(35) and C(37). Has B neighbor — satisfied.
- Position 37: C, adjacent to C(36) and C(38). Both C. C36 has B nearby, but does that help C37? Probably not directly.
- So satisfied: positions 1-36 (all B/D/F or C-adjacent-to-B/D/F). Position 36 OK. Positions 37-48 not satisfied.
- 36 satisfied. Score 6.
- 9*36/48 = 6.75 → 6 (floor) ✓!

And 24/48*9 = 4.5 → got 3. Hmm floor gives 4 not 3.

Let me recheck: BCBC*24 + CCC*24. Positions 1-24 BC alternating. Position 24 is C, adj to B(23) and C(25). C satisfied. Position 25-48: all C. Position 25 adj to C(24) and C(26). But C(24) is itself satisfied. Hmm — does satisfaction propagate?

If C is satisfied only if directly adjacent to B/D/F:
- Position 25: C, adjacent to C(24) and C(26). Neither B/D/F. Not satisfied.
- So satisfied positions: 1-24 (24 total).
- 24/48 * 9 = 4.5. Floor = 4. But got 3.

Maybe formula is different. Try 24 → 3, 36 → 6, 48 → 9. Score = max(0, 3*(sat-12)/12)?
- 24: 3*(12)/12 = 3 ✓
- 36: 3*(24)/12 = 6 ✓
- 48: 3*(36)/12 = 9 ✓
- 12: 3*(0)/12 = 0
- Pattern: score = max(0, (sat - 12)/4)? 
- 24: (24-12)/4 = 3 ✓
- 36: 24/4 = 6 ✓
- 48: 36/4 = 9 ✓
- 12: 0/4 = 0 ✓

Beautiful! Let me verify with more datapoints.

Earlier single B-run data:
- 48 B's, all sat: score 48-12)/4 = 9 ✓
- 36 B run + 12 A: 36 sat (all 36 B's have B neighbors except endpoints which have A — but if "sat" means just being a good letter, then 36 sat). Score = (36-12)/4 = 6 ✓
- 24 B run + 24 A: 24 sat → (24-12)/4 = 3 ✓
- 12 B run: 12 sat → 0 ✓
- 18 B run: 18 sat → (18-12)/4 = 1.5 → 1 (got 2). Close but not exact.
- 6 B run: 6 sat → 0 ✓
- 30 B run: 30 sat → 18/4 = 4.5 → 4 ✓
- 42 B run: 42 sat → 30/4 = 7.5 → 7 ✓
- 12+12 split: 24 B sat → 3? But observed 4.
- 8+8+8 split: 24 sat → 3? Observed 4.

So formula doesn't fit splits perfectly. Need adjustment for arrangement.

But maybe "sat" depends on whether B has B neighbors? Let me check single 18-run:
- Positions 1-15: A. Positions 16-33: B. Positions 34-48: A.
- B's: 16-33. B16 has A left, B right (one A neighbor). B17 has B left, B right (no A neighbor).
- If sat = position where the letter is in {B,D,F} AND neither neighbor is A/E:
  - B17-B32: 16 satisfied.
  - B16, B33: 2 unsatisfied.
- 16 sat → (16-12)/4 = 1 (got 2). Still off.

What if sat = good letters + good letters next to good letters? No, that's circular.

Let me try yet another definition: sat = (# good letters with at least one good neighbor) + (# good letters - boundary effects).

Or maybe formula isn't (sat-12)/4. Let me revisit:
- 48 → 9
- 42 → 7
- 36 → 6
- 30 → 4
- 24 → 3
- 18 → 2
- 12 → 1
- 6 → 0

Differences: 48-42: -2, 42-36: -1, 36-30: -2, 30-24: -1, 24-18: -1, 18-12: -1, 12-6: -1.

Like floor((L-?)/?). 
- (L-3)/5: 48→9, 42→7.8→7, 36→6.6→6, 30→5.4→5 (got 4), 24→4.2→4 (got 3). Off.
- (L-6)/6: 48→7, no.

Hmm let me compute floor(L*L/256):
- 48: 9, 42: 6.89→6 (got 7) ✗

Let me revisit: f(L) = floor(L(L+60)/576):
- 48: 9, 42: 42*102/576=7.44→7 ✓
- 36: 6 ✓
- 30: 30*90/576=4.69→4 ✓
- 24: 24*84/576=3.5→3 ✓
- 18: 18*78/576=2.44→2 ✓
- 12: 1.5→1 ✓
- 6: 0.69→0 ✓

f(L) = floor(L*(L+60)/576) fits single runs perfectly.

Note: L*(L+60)/576 = (L² + 60L)/576 = L²/576 + 60L/576 = L²/576 + 5L/48.

Now for splits: 2×12 → 4, 3×8 → 4, 4×6 → 6, 6×4 → 5, 8×3 → 0, 24×1 → 0.

If sum of f(L_i):
- 2×12: 2*1 = 2 (got 4)
- 3×8: 3*0 = 0 (got 4)
- 4×6: 4*0 = 0 (got 6)
- 6×4: 6*0 = 0 (got 5)
- 8×3: 0 (got 0 ✓)
- 24×1: 0 ✓

So clearly not additive across runs. Splits give MORE than sum.

What if score considers each pair of (B,B) somehow? Maybe number of (i,j) pairs both good with separation ≤ some?

Let me count pairs at distance ≤ 11 (window 12) both good:
- Run of L: count = sum_{d=1}^{11} max(0, L-d) if L > d.
  - For L=12: sum d=1..11 of (12-d) = 11+10+...+1 = 66.
  - For L=48: sum d=1..11 of (48-d) = 47+46+...+37 = 11*42 = 462.
  - For L=24: sum = 23+22+...+13 = 11*18 = 198.
- Scores 1, 9, 3. Ratios 66, 51.3, 66. Not constant.

How about f(L) = #pairs at distance ≤ d, for various d?
- L=12: distance≤1 → 11. /1 = 11.
- L=48: distance≤1 → 47. /9 ≈ 5.2.
- Not constant.

Let me try: score related to sum of squares of good-runs.
- 2×12: 2*144 = 288. → 4. 288/4 = 72.
- 3×8: 3*64 = 192. → 4. 192/4 = 48.
- 4×6: 4*36 = 144. → 6. 144/6 = 24.
- 6×4: 6*16 = 96. → 5. 96/5 = 19.2.
- 8×3: 8*9 = 72. → 0. 
- 24×1: 24*1 = 24. → 0.

Maybe score depends on (sum_squares + boost_from_runs). For 4×6: 4 runs of 6, score 6. For 4×6 with C spacers: also 6. For 4×6 with E spacers: also 6.

What does the 4×6 pattern have in common? B^6 A^6 ×4. Total B count = 24. Number of runs = 4. Spacing between runs = 6.

Maybe scoring rewards SPACED arrangement. Like a Fourier/periodic preference.

Let me think about this from a different angle: position-specific scoring. What if positions are scored individually based on a "template" that doesn't repeat uniformly?

## 2026-06-28 15:15 — query 74

## B in C background data
- 1 B in C: 0
- 2 B at ends: 1
- 4 B every 12 (period 12): 0
- 8 B every 6 (period 6): 0
- 12 B every 4 (period 4): 7
- 16 B every 3 (period 3): 9
- 24 B every 2 (BC alt): 9
- 32 B every 1.5 (BBC): 9

Big jump from period 6 (0) to period 4 (7).

So spacing matters a lot. B's need to be within distance ≤ 3 of each other for the C's between them to "count".

Hypothesis: a C is "satisfied" if there's a B (or D/F) within distance ≤ 2 (i.e., within a 5-window centered on it).
- Period 4 (BCCC): C2 (B at 1, d=1) ✓, C3 (B at 1, d=2) ✓, C4 (B at 5, d=1) ✓. All C's sat.
- Period 5: C2 (d1 B1) ✓, C3 (d2 B1) ✓, C4 (d2 B5) ✓, C5 (d1 B5) ✓. All sat.
  - But period 5 not tested for B/C only. We tested BCCCC (which has period 5).
  - Period 5 BCCCC: all C's adjacent within distance 2 of B → all sat? 48 sat → score 9. But actually got 7.
  - Hmm.
- Period 6 (BCCCCC): C2 (d1) ✓, C3 (d2) ✓, C4 (d2 from B at 7? d=3) ✗, C5 (d2 from B7) ✓, C6 (d1 from B7) ✓.
  - 4/5 C's sat per block. Hmm but score was 0!

So distance-2 model also doesn't fit. Period 6 scored 0 but should have most C's near B.

Wait — BCCCCC period 6 = "BCCCCCBCCCCC..." 8 B's, 40 C's. Score 0.

Maybe the rule is even stricter: B must be within distance 1 OR there's some run requirement.

Let me hypothesize: a position is "satisfied" if it's in {B,D,F}, OR (it's C AND has a {B,D,F} neighbor at distance 1).

Period 6 BCCCCC: 
- B (1, 7, 13, ...): satisfied.
- C2: adj B1 ✓
- C3: adj C2, C4. No B adj. ✗
- C4: adj C3, C5. ✗
- C5: adj C4, C6. ✗
- C6: adj C5, B7. ✓
- So 2 sat C per block (positions 2, 6), 3 unsat. Plus 1 B per block.
- 8 blocks: 8 B + 16 sat C = 24 sat. 24 unsat C.
- 24/48*9 = 4.5 → 4 or 5. But got 0!

So even 24 sat → 0 here. But other configs with 24 sat give 3-4.

OH WAIT. Maybe unsatisfied C's (isolated from B) act as a PENALTY (bad like A).

Hypothesis: "Effective bad" letters are A, E, AND C that's not adjacent to {B,D,F}.

Period 6: 24 effective good (8 B + 16 adjacent-C), 24 effective bad (isolated C). Same as 24B+24A. Score should be 3. But got 0.

Hmm, unless isolated C's are worse than A. Or the rule is more strict.

Maybe isolated C is "very bad" — penalizes more strongly.

Let me revisit BCCCC period 5 sequence: BCCCCBCCCC... 10 B's, 38 C's.
- B1 sat. C2 adj B1 ✓. C3 adj C2, C4: ✗. C4 adj C3, C5: ✗. C5 adj C4, B6: ✓.
- Per block: 1 B + 2 sat C + 2 unsat C. 
- 9 full blocks + partial (BCC at end): 9 B + 18 sat C + 18 unsat C, plus last partial "BCC": B + 2 sat C (C46, C48? Actually let me recount).
- Actually I'll skip exact count. Net: significant unsat C count, but score = 7.

Inconsistent with "isolated C very bad" since 7 is decent.

Hmm, maybe the rule depends on the LENGTH of unsatisfied C runs.

Period 6 has C-only runs of length 3 (C3,C4,C5 in middle).
Period 5 has C-only runs of length 2 (C3,C4).
Period 4 has C-only runs of length 1 (C3).
Period 3 has C-only runs of length 0.

So when isolated-C runs are >= 3, score drops to 0! When length 2, score moderate (7). When length 1, score 7-9. Length 0, score 9.

Let me also check single B in C: many isolated C's, run length up to 23. Score 0. ✓
2 B at ends in C: C runs of length 46. Score 1. Hmm not 0?

Wait re-check 2 B at ends: "BCCC...CCCB" (48 chars). The middle C's form a run of 46 C's. Score 1.

And 1 B in middle: 23+24 C runs. Score 0.

Hmm 2 B's slightly better than 1 B. And many B's at right spacing is much better.

This problem is complex. Let me try a more systematic understanding by testing more "varying spacing in C" experiments.

Actually I think we have enough. Let me state the working model:
- {B,D,F} = strong good
- A, E = bad
- C = neutral filler when near good, harmful in long isolation

Score depends heavily on a "good network" being densely connected.

Let me look for highest score now and ensure I get 9. CDCD already gives 9. Let me check if anything could give >9.

## 2026-06-28 15:16 — query 79

## Key findings so far
Max score appears to be 9. Many patterns reach it: pure {B,D,F} homopolymer, alternating with C, BCBC, BDBD, CDCD, BCD repeats, BBC repeat, BCC repeat, BBBC, 1 A scattered in any of these, etc.

The score 9 is the ceiling. Penalties happen from:
- A or E in any quantity (esp. heavy)
- C isolated from {B,D,F} (long C runs)

Now, since I have a maximizing target and the ceiling is 9 (which I already reach with many sequences), my main task for remaining experiments is to understand the rule better.

Let me investigate edge cases:
- Is the max really 9, or can it go higher?
- What's the worst case (most negative)?
- Does position 1 vs position 48 matter?

Also: maybe single A in B background gave 9. So A is OK if alone. Same for E. So penalty kicks in after threshold.

Let me check single B-only with varying number of A's more carefully, to understand penalty.

## 2026-06-28 15:16 — query 83

## A in B background
- 0 A: 9
- 1: 9
- 2: 9
- 3: 8
- 4: 7
- 5: 9 (5 spaced)
- 6: 9 (6 spaced)
- 8 (period 6): 0
- 12 (period 4 BBBA): 7
- 16 (period 3 BBA): 0

Inconsistent! 5 and 6 give 9 spaced, but 8 spaced gives 0; 12 spaced gives 7; 16 spaced gives 0.

The 8 A's case was period 6 (BBBBBA): A every 6. Got 0.
The 12 A's case was period 4 (BBBA): A every 4. Got 7.
The 16 A's case was period 3 (BBA): A every 3. Got 0.

Period 4 OK, period 3 and 6 bad? Surprising.

But wait — let me also recheck 3 and 4 A cases:
"BBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBA" (3 A's at pos 17, 33, 48? Let me count): score 8.
"BBBBBBBBBBBABBBBBBBBBBBABBBBBBBBBBBABBBBBBBBBBBA" (4 A's at pos 12, 24, 36, 48 period 12): score 7.

So 3 A's give 8, 4 A's spaced widely give 7, 5/6 A's spread give 9 (??).

This is suspicious — let me re-examine the 5 and 6 A sequences I sent:
- 5 A's: "BBBBBBBBBABBBBBBBBABBBBBBBBABBBBBBBBABBBBBBBBABB" — count A's: positions 10, 19, 28, 37, 46. That's 5 A's at period 9. Score 9.
- 6 A's: "BBBBBBBABBBBBBABBBBBBABBBBBBABBBBBBABBBBBBABBBBB" — A's at positions 8, 15, 22, 29, 36, 43. Period 7. Score 9.

So A's at period 7 or 9: 9. A's at period 12: 7. A's at period 4: 7. A's at period 6: 0. A's at period 3: 0.

Maybe scoring is based on "longest run of consecutive B's" or "min spacing"?

Period 6 (BBBBBA): B-runs of length 5. Score 0.
Period 4 (BBBA): B-runs of length 3. Score 7.
Period 3 (BBA): B-runs of length 2. Score 0.
Period 12 (BBBBBBBBBBBA): B-runs of length 11. Score 7.
Period 7 (BBBBBBA): B-runs of length 6. Score 9.
Period 9 (BBBBBBBBA): B-runs of length 8. Score 9.

So B-run length 5 (period 6) gave 0 but B-run length 3 (period 4) gave 7? That's bizarre.

Wait — let me reconsider. Period 6 BBBBBA means B's at positions where (pos-1)%6 < 5, i.e., BBBBBABBBBBABBBBBA... Actually let me look at what I sent:
- "BBBBBABBBBBABBBBBABBBBBABBBBBABBBBBABBBBBABBBBBA" = period 6 BBBBBA. B's at positions 1-5, 7-11, etc. A's at 6, 12, 18, 24, 30, 36, 42, 48. Yes 8 A's, B-runs of 5.

And "BBBABBBABBBABBBABBBABBBABBBABBBABBBABBBABBBABBBA" = period 4 BBBA. B-runs of 3, A's at 4, 8, 12, ..., 48. 12 A's.

So 12 A's (period 4) → 7. 8 A's (period 6) → 0. Fewer A's but worse score!

OK maybe it's not A count but something about resulting B-run structure or something else.

Let me consider: number of B-runs of length 3 vs 5.
- Period 4: 12 B-runs of length 3.
- Period 6: 8 B-runs of length 5.

Hmm. 

Maybe each run contributes f(L) but capped/reduced?
- Period 4: 12 × f(3). f(3) = 3*63/576 = 0.328. ×12 = 3.94 → 3 (got 7).
- Period 6: 8 × f(5). f(5) = 5*65/576 = 0.564. ×8 = 4.5 → 4 (got 0).

Doesn't fit.

Maybe scoring uses count of certain k-mers. Specifically maybe BBBB or BBBBB?

Period 4 (BBBABBBA): BBB exists yes; BBBB never (since A breaks at 4th).
- Number of BBBB substrings: 0. Score 7.
Period 6 (BBBBBA): BBBBB exists at start. BBBBBB? No, A at 6. So BBBBB appears: starting at position 1, 7, 13, ..., 43. = 8 times. Number of BBBBB substrings = 8. Score 0.
Period 7 (BBBBBBA): BBBBBB substrings = 8. Score 9.

Hmm BBBBBB count: period 7 has 8 BBBBBB. period 6 has 0 BBBBBB.

Maybe key motif is BBBBBB (6-mer of same good letter). 
- 48B: 43 BBBBBB. Score 9.
- 36B run: 31 BBBBBB. Score 6.
- 24B run: 19 BBBBBB. Score 3.
- 12B run: 7 BBBBBB. Score 1.
- 6B run: 1 BBBBBB. Score 0.
- 18B run: 13 BBBBBB. Score 2.

Ratios: 43/9=4.78, 31/6=5.17, 19/3=6.33, 7/1=7, 1/0=∞, 13/2=6.5. Not constant.

Maybe number of length-k all-good windows scaled. Let me try 7-mer BBBBBBB:
- 48: 42, 36: 30, 24: 18, 12: 6, 6: 0, 18: 12. Scores: 9, 6, 3, 1, 0, 2.
- 42/9=4.67, 30/6=5, 18/3=6, 6/1=6, 12/2=6.
- Hmm, the latter all equal 6! Except 42/9=4.67 (48B). Possibly the score is min of (count/6, 9)? Let me check:
- 48: 42/6 = 7. Got 9. ✗

But for L ≤ 36, score = count_of_7mer / 6.
- 6B: 0 → 0 ✓
- 12B: 6/6=1 ✓
- 18B: 12/6=2 ✓
- 24B: 18/6=3 ✓
- 30B: ? count of 7-mer = 30-6 = 24. 24/6 = 4. Observed 4 ✓!
- 36B: 30/6=5. Observed 6. ✗

Hmm off at 36. Let me try ceiling:
- 36B: ceil(30/6) = 5. Still off.

Maybe it's count_of_7mer / 6 floor with something else?

Wait let me recompute for 36B with f(L)=floor(L(L+60)/576): 6 ✓.
And count of length-7 all-B windows: 30. 30/6=5. Off by 1.

How about (count_of_BBBBBB) / something?
- 48: 43, score 9. 43/9 = 4.78.
- 36: 31, 6. 31/6 = 5.17
- 24: 19, 3. 19/3 = 6.33

Try max number of (consecutive good positions): just L itself.
- L=48: 9. L=36: 6. L=24: 3. f(L) = floor((L-6)*9/42)?
- L=6: 0; L=48: 42*9/42 = 9 ✓; L=36: 30*9/42 = 6.43→6 ✓; L=24: 18*9/42 = 3.86→3 ✓; L=12: 6*9/42 = 1.29→1 ✓; L=18: 12*9/42 = 2.57→2 ✓; L=30: 24*9/42 = 5.14→5 (got 4) ✗.

Doesn't fit L=30.

What about f(L) = floor((L-3)/5)?
- 48: 45/5=9 ✓; 42: 39/5=7.8→7 ✓; 36: 33/5=6.6→6 ✓; 30: 27/5=5.4→5 (got 4) ✗.

Or floor((L-3)/5) with L=30 actually scoring 4? Let me re-test 30.

Re-test single 30 B run for confidence.

## 2026-06-28 15:17 — query 89

## Comprehensive single-B-run table (L = run length, rest A):
L=6: 0
L=12: 1
L=18: 2
L=24: 3
L=30: 4
L=35: 5
L=36: 6
L=40: 6
L=42: 7
L=44: 7
L=46: 8
L=47: 8
L=48: 9

Looks like score = floor(L/k) - offset? 
- L=6: 0, L=12: 1: jump at L=12. 
- L=12 to L=18: +1 (jump at 18).
- L=18 to L=24: +1 (at 24).
- L=24 to L=30: +1 (at 30).
- L=30 to L=35: +1 (at 35!?). 
- L=35 to L=36: +1 (at 36).
- L=36 to L=40: 0 (still 6).
- L=40 to L=42: +1 (at 42).
- L=42 to L=44: 0.
- L=44 to L=46: +1 (at 46).
- L=46 to L=47: 0.
- L=47 to L=48: +1 (at 48).

Score jumps at: 12, 18, 24, 30, 35, 36, 42, 46, 48. Hmm let me find pattern.

Maybe score = floor(L²/256)?
- 12: 144/256=0.56→0 (got 1) ✗

Or score = floor((L+a)*(L+b)/c):

Let me fit (L,score):
6,0; 12,1; 18,2; 24,3; 30,4; 35,5; 36,6; 40,6; 42,7; 44,7; 46,8; 47,8; 48,9

Or score = number of complete "blocks" in some sense. Let me check:
- Maybe score = floor((L-6)/6) for small L, then accelerating:
  - 12: 1 ✓; 18: 2 ✓; 24: 3 ✓; 30: 4 ✓; 36: 5 (got 6); 42: 6 (got 7); 48: 7 (got 9). Off by accelerating amount.

Maybe score = ceil((L-?)/6)?
- 12: ceil(6/6)=1 ✓; 18: ceil(12/6)=2 ✓; ... all the same.

Try score = floor(L/6) + bonus(L):
- L=12: 2 → 1. Bonus -1.
- L=48: 8 → 9. Bonus +1.

Hmm. Let me try: score = floor(L² / 256):
- L=12: 144/256=0.56 → 0 (got 1)
- L=48: 2304/256=9 ✓
- L=42: 1764/256=6.89 → 6 (got 7)
- L=36: 1296/256=5.06 → 5 (got 6)

Off.

Try score = round(L²/256):
- L=12: 0.56 → 1 ✓
- L=18: 324/256 = 1.27 → 1 (got 2) ✗

Hmm.

Try score = floor((L+a)²/b):
Solve from L=48: (48+a)²/b = 9. L=24: (24+a)²/b = 3. 
(48+a)² = 9b, (24+a)² = 3b. Ratio: (48+a)²/(24+a)² = 3. (48+a)/(24+a) = √3 ≈ 1.732. 48+a = 1.732(24+a) → 48+a = 41.57 + 1.732a → 6.43 = 0.732a → a ≈ 8.78. So a≈9. b = (48+9)²/9 = 57²/9 = 3249/9 = 361.

Check: f(L) = floor((L+9)²/361):
- L=6: 225/361 = 0.62 → 0 ✓
- L=12: 441/361 = 1.22 → 1 ✓
- L=18: 729/361 = 2.02 → 2 ✓
- L=24: 1089/361 = 3.016 → 3 ✓
- L=30: 1521/361 = 4.21 → 4 ✓
- L=35: 1936/361 = 5.36 → 5 ✓
- L=36: 2025/361 = 5.61 → 5 (got 6) ✗

Close but not.

Try (L+10)²/something:
(48+10)²/9 = 3364/9 = 373.78. (24+10)²/3 = 1156/3 = 385.3. Not consistent.

Maybe non-quadratic. Let me look at score = round((L/16)²)? 
- 48: 9 ✓; 32: 4 (haven't tested); 24: 2.25→2 (got 3) ✗

Try score = floor(L²/250):
- 48: 9.216 → 9 ✓; 42: 7.06 → 7 ✓; 36: 5.18 → 5 (got 6) ✗

Try score = floor((L+6)²/something):
- (48+6)² = 2916; (36+6)² = 1764; (24+6)² = 900; (12+6)² = 324
- For score 9, 6, 3, 1: 2916/9=324, 1764/6=294, 900/3=300, 324/1=324. Mean ~310.
- floor((L+6)²/310): 48: 9.4→9; 36: 5.69→5 (got 6).

Doesn't fit cleanly.

Maybe the formula is just empirical and I should focus on what works.

Actually, look: f(L) for L = 6,12,18,24,30,36 → 0,1,2,3,4,6. Almost a stride of 6 = +1, but jumps +2 at 36.

What if f(L) = floor(L/6) - 1 for L < 36, then jumps?
- L=6: 0 ✓; 12: 1 ✓; 18: 2 ✓; 24: 3 ✓; 30: 4 ✓; 36: 5 (got 6) ✗

Try f(L) = floor((L^2 + cL)/d). Going to just use empirical table for single runs.

OK I'll stop trying to fit f(L) and use my notes to design strong sequences. We've found many 9-scoring patterns. Let me just confirm 9 is max and explore some edge cases.

## 2026-06-28 15:17 — query 90

## BCDF pattern (period 4) gives 7, not 9!
Surprising. Let me think... BCDF has letters B(good), C(neutral), D(good), F(good). All non-bad. 
What's different from BCBC (9), BDBD (9), CDCD (9), BCD (9)?

Maybe specific letter pairs disturb. Let me test BDFC, BFDC, DFBC...

## 2026-06-28 15:17 — query 94

## Period-2 alternations from {B,C,D,F}:
BC: 9, BD: 9, BF: 9, CD: 9, CF: 9, DF: 9. All 9.

But BCDF period 4 → 7. Why lower?

In BCDFBCDF: positions:
1:B, 2:C, 3:D, 4:F, 5:B, 6:C, 7:D, 8:F, ...
Bigrams: BC, CD, DF, FB. All four bigrams are between non-bad letters.

Hmm but score is 7 not 9. So maybe specific bigrams matter.

Let me test specific bigrams: FB.

## 2026-06-28 15:17 — query 96

## Interesting!
FDCB (reverse of BCDF) period 4: 9. But BCDF: 7. Different scores for the same letters in different orders!

So position/order matters in a non-trivial way. There's directionality.

FDCB has bigrams: FD, DC, CB, BF
BCDF has bigrams: BC, CD, DF, FB

Maybe specific bigram FB is bad? No, FBFB scored 9. Maybe DF is bad?

Wait, DF period 2: DFDFDF — bigrams DF, FD. Score 9. So DF alone is fine.

So bigram BCDF vs FDCB different. Maybe it's not bigrams but trigrams.

BCDF trigrams: BCD, CDF, DFB, FBC
FDCB trigrams: FDC, DCB, CBF, BFD

Maybe DFB or FBC trigrams are bad. Let me try DFBDFB...

## 2026-06-28 15:18 — query 100

## BCDF period 4 deterministic at 7. CBCDF at 9.

So something about the BCDF cycle specifically is suboptimal. Let me hypothesize it's about exact letter values: A=0, B=1, C=2, D=3, E=4, F=5.

BCDF: 1,2,3,5. Diff cyclically: +1, +1, +2, -4 (or +2 mod 6).
FDCB: 5,3,2,1. Diff: -2, -1, -1, +4.

Hmm, maybe scoring penalizes large jumps in letter value? But CFCF has jumps of 3 and -3, scored 9.

Try maybe positions matter: BCDF starts with B; FDCB starts with F. Position 1 = F gives more...?

Let me test by shifting: DFBC, FBCD, CDFB.

## 2026-06-28 15:18 — query 102

## All cyclic shifts of BCDF give 7. Reverse (FDCB) gives 9.
- BCDF: 7
- CDFB: 7
- DFBC: 7
- FBCD: not tested but likely 7
- FDCB: 9 (reverse)

The cycle BCDF (1→2→3→5→1) is bad. Cycle FDCB (5→3→2→1→5) is good.

These differ only in direction. Maybe scoring is direction-aware.

Letter values BCDF = +1, +1, +2, then wrap.
FDCB = -2, -1, -1, then wrap.

What's different about going up vs down? Let me test ascending vs descending sequences more.

## 2026-06-28 15:18 — query 105

## More period-4 data
- BCDF: 7
- BDFC: 7
- BDFE: 7
- FDCB: 9
- CBCDF: 9 (period 5)

So BDFE (with E!) and BCDF (no bad) both give 7. Interesting.

Maybe the rule isn't about specific letters but about period 4 having a specific structure that hits 7 vs 9.

Wait, BCDFC period 5 = 9. Period 4 BCDF = 7. Period 4 with E mixed = 7. Period 3 with D,F,B = 9.

Maybe length 48 / period: 48/4 = 12 full cycles, 48/3 = 16, 48/2 = 24. 48 is divisible by 1,2,3,4,6,8.

Hmm let me try non-cyclic period 4 patterns.

Actually I'll be practical: I have so many sequences scoring 9, the max is clearly 9. Let me confirm this thoroughly and stop trying to fit a complex rule. I'll dedicate remaining experiments to discovering edge cases and key features but I've established enough.

Key findings so far:
1. Letter classes: {B,D,F} = strong-good, C = neutral, {A,E} = bad
2. Max score = 9 (appears to be a hard cap)
3. Many sequences achieve 9; some patterns get 7 (subtle)
4. Long isolated runs of C → bad (treated like A/E?)
5. Long runs of A or E → very bad
6. Adjacent good letters help

Let me explore a few more things:
- Is the max really 9, or some sequences higher?
- What are min scores?
- Specific positions: are positions 1 or 48 special?

## 2026-06-28 15:18 — query 109

## Period 4 patterns
- BBDD: 9 ✓
- BBCD: 9 ✓
- BDCD: 9 ✓
- BCBD: 7
- BCDF: 7
- BDFC: 7
- BDFE: 7
- CDFB: 7
- DFBC: 7

Patterns giving 7 vs 9 — what differs?
- BCBD: has letters {B,C,D}. So is BCDF... no, contains F. BBCD: {B,C,D} → 9.
- BCBD pattern at positions: B,C,B,D,B,C,B,D...

In BCBD: bigrams BC, CB, BD, DB. Same as BC/CB/BD/DB which all individually scored 9. But combined → 7.

Hmm, maybe it's about trigrams. BCBD trigrams: BCB, CBD, BDB, DBC.

BBCD (=9) trigrams: BBC, BCD, CDB, DBB.

BCBD has CBD; BBCD has BCD. Different order.

Or maybe: the rule penalizes consecutive C separated by exactly 2. In BCBD: C at positions 2,6,10... gap of 4. Not really separated by 2.

Actually maybe scoring is related to how many distinct letters appear, or to specific 4-mers.

OK let me take a different practical approach: I'll catalog winning sequences. Many patterns reach 9. The maximum I can find appears to be 9.

I have 391 experiments left. Let me explore some specific hypotheses:
1. Maybe scoring uses specific 4-mer or k-mer count.
2. Maybe scoring uses a position-specific scoring matrix.

Let me try a few more experiments to understand the cap.

## 2026-06-28 15:19 — query 111

## BBBCCC period 6 = 0!
But BBBBBB CCCCCC ×4 (period 12) = 6.
And BBCBBC period 3 = 9.

So C-runs of length 3 (in BBBCCC) → 0. C-runs of length 6 (in B^6 C^6 ×4) → 6. C-runs of length 1 → 9.

Strange — longer C runs sometimes better than length-3. 

Wait, period 6 BBBCCC: C runs of length 3. The C's in middle have only C neighbors.
B^6 C^6 ×4 = period 12: C runs of length 6. Middle 4 C's have only C neighbors.

Number of C's with NO adjacent good letter:
- BBBCCC ×8: per block, C4 (in CCC) is between C3 and C5. Both C. Position 5 is C, between C4 and B7. Position 6 is C, between C5 and B7 (yes). So per CCC: C4 isolated (1), C5 has B-right (✓), C6 has B-right (✓). Wait positions: B1B2B3C4C5C6 B7B8B9C10... C4: neighbors B3, C5. Has B! Satisfied. C5: neighbors C4, C6. No B. Unsat. C6: neighbors C5, B7. Has B. Sat.
- So C4 sat, C5 unsat, C6 sat. 1/3 unsat C per block × 8 = 8 unsat C. Total good positions: 24 B + 16 sat C = 40. Score 0.
- B^6 C^6 ×4: per CCC of length 6. C positions: 7,8,9,10,11,12. C7 adj B6,C8 → sat. C8 adj C7,C9 → unsat. C9 adj C8,C10 → unsat. C10 adj C9,C11 → unsat. C11 adj C10,C12 → unsat. C12 adj C11,B13 → sat. So 2/6 sat, 4/6 unsat per block. 4 blocks × 4 unsat = 16 unsat C. Sat positions: 24 B + 4×2 = 32. Score 6.

Even though BBBCCC has fewer unsat C (8) and more sat positions (40), it scored 0! Versus B^6C^6 with more unsat (16) and fewer sat (32) scoring 6.

So it's not about total satisfaction count. The arrangement and run structure matter.

Maybe the rule involves alternation periodicity. Specifically:
- B^6C^6: blocks of 6+6, period 12 — somehow "scoring"
- BBBCCC: blocks of 3+3, period 6 — fails

Maybe specific window-size scan:
- The function looks at sliding windows of size 6 and counts how many have at least k goods?

Let me count for each pattern: sliding window of size 6, count windows where ≥X goods exist.
- 48B: 43 windows, all have 6 goods.
- 24B+24A (block): 19 windows entirely B, 4 mixed B-A, 19 entirely A. 19 windows with 6 goods. Score 3.
- 12+12 split: each 12 block has 7 all-B windows. 2 blocks → 14 windows. Score 4.
- 8+8+8 split: each 8 block has 3 all-B windows. 3 × 3 = 9 all-B windows. Score 4.
- 6+6+6+6 split: each 6 block has 1 all-B window. 4 × 1 = 4. Score 6.
- BBBCCC ×8: each BBB block has 0 all-B 6-windows. Score 0. ✓
- B^6 C^6 ×4: each B^6 has 1 all-B 6-window. 4 windows. Score 6. ✓!

Hmm let me check more:
- 1 B-run of L: max(0, L-5) all-B windows.
  - L=48: 43 → 9. But should be 43 if just count. Need scaling.
- 18 B run: 13 all-B 6-windows. Score 2.
- 24 B run: 19 all-B. Score 3.
- 12 B run: 7 all-B. Score 1.
- 6 B run: 1 all-B. Score 0.

Hmm 6 B run has 1 all-B 6-window but score 0. So "all-B 6-window count" alone isn't the rule.

But: B^6 C^6 ×4 has 4 all-B 6-windows and scores 6. While single 24B run has 19 all-B 6-windows and scores 3.

What about all-good 6-windows where "good" includes C? Let me try with that. But CCC homopolymer scored 0 even though many "all-good" 6-windows.

Maybe rule: count of "good-content" 6-windows where good-content = "contains at least one of B/D/F".
- BBBCCC ×8: any 6-window: starts at pos 1-43. Windows are like positions 1-6 (BBBCCC: has B), 2-7 (BBCCCB: has B), 3-8 (BCCCBB: has B), 4-9 (CCCBBB: has B), 5-10 (CCBBBC: has B), 6-11 (CBBBCC: has B). All windows contain B. 43 windows.
- B^6 C^6 ×4: window 1-6 (BBBBBB has B), 2-7 (BBBBBC has B), ..., 6-11 (BCCCCC has B), 7-12 (CCCCCC no B), 8-13 (CCCCCB has B). So window 7-12 has NO B. Per period 12: only 1 out of 12 windows has no B (starting position 7+12k). For 4 periods, count of "good" windows = 43 - 3 = 40. Score 6.

Hmm BBBCCC has 43 good windows, score 0. B^6C^6 has 40 good windows, score 6. Doesn't match counts.

Maybe rule: count of "all-good" 6-windows where ALL must be in {B,D,F}.
- BBBCCC: 0 such windows. ✓ Score 0.
- B^6C^6: 4 such windows. Score 6 — hmm 6 ≠ 4.
- 6B run alone: 1 such window. Score 0. ❌

So 6B alone has 1 all-B window but score 0. While B^6C^6 ×4 has 4 such windows and score 6.

Maybe rule involves the windows summing in a more complex way. Maybe each "all-B 6-window" gives 1 point if also surrounded by good, and 0 otherwise?

Actually maybe rule is: count of "all-good 7-windows" or larger.
- 6B alone: 0 all-B 7-windows. Score 0 ✓
- B^6C^6 ×4: 0 all-B 7-windows (each B block is only 6). Score 6. ❌

OK try: count of length-6 windows that are entirely in {B,C,D,F} AND contain at least one of {B,D,F}.
- BBBCCC ×8: all 43 windows contain B, all are in {B,C}. 43 windows. Score 0. ✗

Hmm.

Maybe sliding window of size 12 with B count requirement?
- BBBCCC ×8: window of 12 has 6 B's. Score should fit somehow.
- B^6C^6 ×4: window of 12 has 6 B's.

Same B count per 12-window for both. Different scores. So window count isn't it.

Maybe it's about position-specific score: B at certain positions contributes more than B at others. Let me test specific position scoring.

## 2026-06-28 15:19 — query 113

## Both 2×12B split patterns → 4. Matches previous (2×12 in middle).
So position-of-runs doesn't matter much, just structure.

OK let me try totally different framing. Maybe Fourier-like: score = response to some periodic test.

Actually, I'll switch strategy: focus on remaining experiments to refine theory and probe known anomalies (e.g., why BCDF=7 but FDCB=9).

The peak score is 9. I've shown many ways to reach it. For the user's goal, I'm already at max. For science, let me dig more.

Let me try systematic tests:
- A bunch of period-4 patterns to map which score 9 vs 7.

## 2026-06-28 15:19 — query 117

## Period 4 score map (using {B,C,D,F}):
9: BBDD, BBCD, BDCD, FDCB (rev BCDF), CBFD, BDFB
7: BCBD, BCDF, BDFC, BDFE, CDFB, DFBC, BDFC, CBDF, DBFC

Score-7 sequences mostly have B at position 1, then C at 2 (BCBD, BCDF), or specific order like CDFB, DFBC.

Score-9 sequences with similar letters: BBDD, BBCD, BDCD, FDCB, CBFD, BDFB.

Hmm CBFD = 9, CBDF = 7. They differ only at last two: FD vs DF. So FD bigram ≠ DF bigram in this 4-mer context!

Let me test CB DF as period 4 vs CB FD:
- CBDF: 7
- CBFD: 9

So CBFD>CBDF. The trigram BFD vs BDF — BFD scores higher?

Or the bigram FD before C vs DF before C: 
- CBDF tetragram: ends with DF, next char is C (cycle). DF-C is "DFC" trigram.
- CBFD tetragram: ends with FD, next char is C. FD-C = "FDC" trigram.

Trigram FDC was tested: FDCFDC = 9 (in pattern FDCB if cycle is 4, the trigrams seen are FDC, DCB, CBF, BFD).

Hmm. Maybe just direction matters.

Without a clean theory, let me try to find any sequence that scores >9.

## 2026-06-28 15:19 — query 119

## Random good-only sequence scored 7. So just being all-good isn't enough.

Max observed = 9. Many patterns reach it. Many random-good arrangements only reach 7.

Hypothesis upgrade: Maybe scoring is about a sequence having a certain symmetry, periodicity, or low-complexity structure.

Let me categorize 9-scorers:
- All homopolymer B/D/F: 9
- Alternating with any two of {B,D,F}, or one with C: 9
- Period-3 with all combinations of {B,C,D,F}: 9 (BCD, BDF, CDF, DCB)
- Period-2 with any of {BC,BD,BF,CD,CF,DF}: 9
- Period-3 BBC, BCC, BBD, BDD etc: probably 9
- Some period-4: BBDD, BBCD, BDCD, FDCB, CBFD, BDFB

9-scorers all seem highly periodic with small periods, OR have certain structures.

Let me test: a long sequence with a perfect mathematical structure.

## 2026-06-28 15:20 — query 124

## 9 is robust. Many patterns reach it. Max is 9.

Let me try to understand what makes BCDF score 7 specifically. Maybe it's specific bigram/trigram counts.

Hypothesis: scoring counts the number of "bad" substrings of some length k. Score = 9 - (bad substring count weighted).

BCDF period 4 has trigrams BCD, CDF, DFB, FBC and 4-grams BCDF, CDFB, DFBC, FBCD.

What's odd here: a 4-letter "alphabet" cycle BCDF doesn't include double letters. While BCD period 3 also doesn't.

Maybe specific 4-mer like BCDF is bad while CBFD isn't?

Let me check by inserting BCDF as a substring in an otherwise-9 sequence.

## 2026-06-28 15:20 — query 126

## OK so BCDF as a small substring is fine. Only when repeated as period-4 does it score 7.

I think the issue with period-4 BCDF is some kind of "resonance" where the period-4 pattern doesn't align well with a 48-length scoring window. 

Let me hypothesize: maybe the score involves a count of something across an 8-window, and period-4 patterns can hit a suboptimal alignment with that 8-window.

Or: maybe the scoring uses position-specific weights. Specifically: position i has weight w_i, and the score = function of (sum over positions where letter is good) * w_i.

Let me test position-specificity: single B at each of various positions, rest C.

## 2026-06-28 15:20 — query 130

## Spread B in C data:
- 1B (mid): 0
- 2B (ends): 1
- 3B (1,25,48): 2
- 6B every 8: 4
- 6 BB pairs every 8: 6 (more B's)
- 8B every 6: 0 (very different from 6B every 8 = 4!)
- 12B every 4 (BCCC): 7
- 16B every 3 (BCC): 9
- 24B every 2: 9
- 32B every 1.5 (BBC): 9

So B's at period 8 gives 4 (6 B's). B's at period 6 gives 0 (8 B's). That's strange — more B's, worse score.

Wait period 8 is BCCCCCCC. period 6 is BCCCCC. So C-run lengths: 7 vs 5.

8B every 6 (period 6) = BCCCCC × 8: 0
6B every 8 (period 8) = BCCCCCCC × 6: 4

Hmm. Period 6 fails (similar to BBBCCC fail).

Maybe the "good" regions need to have length compatible with a specific block size. Like 12-block?

Let me observe: 48 / period values:
- Period 2 (=9): 24 periods.
- Period 3 (=9): 16 periods.
- Period 4 (=mostly 9, some 7): 12 periods.
- Period 5: 9.6 periods (not divisible).
- Period 6 (=0): 8 periods.
- Period 7: 6.86.
- Period 8 (=4-6 range): 6 periods.
- Period 12: 4 periods.

48 divisible by: 1,2,3,4,6,8,12,16,24,48. Some give 9, some don't.

Hmm I'm stuck on a clean formula. Let me try one more set of related experiments and then move on to mostly exploitation.

## 2026-06-28 15:20 — query 134

## Period 6 with B & C: gets 9 when at least 4 B's per block:
- BBBBBC: 9
- BBBBCC: 9
- BBBCCC: 0
- BBCCCC: 0
- BCCCCC: 0
- BBCCDD (mix of goods, period 6): 9

So scoring requires no C-run ≥ 3. C runs of length 1 or 2 are OK; length 3+ kills it (if continuous CCC).

That's consistent: longest C-run threshold.

Test for the previously confusing patterns:
- BBBCCC: C-run of 3 → 0.
- BBCCCC: C-run of 4 → 0.
- BBBBCC: C-run of 2 → 9.
- BBBBBC: C-run of 1 → 9.
- B^6 C^6 ×4: C-run of 6 → score 6 (not 0!).

Wait B^6C^6 has C-run of 6 but scored 6, not 0. So C-run length isn't the only factor.

Maybe context: longer C-runs surrounded by longer B-runs are OK, while shorter B-runs with mid-length C-runs are bad.

In B^6C^6: B-runs of 6.
In BBBCCC: B-runs of 3.

So maybe rule: max(C-run) must be ≤ max(B-run)? 
- B^6C^6: B=6, C=6. Equal → OK score 6.
- BBBCCC: B=3, C=3. Equal → but score 0!
- BBBBCC: B=4, C=2. B > C → 9.
- BBBBBC: B=5, C=1. B > C → 9.
- BBCCCC: B=2, C=4. C > B → 0.
- BBBBBB: B=48, C=0. → 9.

So the rule isn't just B ≥ C, since BBBCCC fails despite equal.

Maybe B-run length must be ≥ 5? 
- B^6C^6: B-run = 6 ≥ 5 → some score.
- BBBCCC: B-run 3 < 5 → 0.
- BBBBCC: B-run 4 < 5 → should be 0 but got 9.

Nope.

Maybe rule: total B count > some threshold AND no isolated C runs ≥ 3?
- BBBBCC: 32 B, no C-run ≥ 3 → 9.
- BBBCCC: 24 B, C-run = 3 → 0.
- BBCCCC: 16 B, C-run = 4 → 0.
- B^6C^6: 24 B, C-run = 6 → 6 (NOT 0!).

So C-run of 6 in some context = 6, but C-run of 3 in BBBCCC = 0. Strange.

Wait, B^6C^6 might have effectively different "tolerance" because B-blocks are longer.

Hmm let me look at this:
- B^6C^6 ×4 = 24 B + 24 C, score 6.
- BBBCCC ×8 = 24 B + 24 C, score 0.

Same composition. Different arrangement.
- Number of "long runs" of B: 4 (of length 6) vs 8 (of length 3).
- Number of C-runs: 4 (length 6) vs 8 (length 3).

Maybe each "long run" of B contributes... actually we saw 4 runs of 6 B's separated by 6 A's also gave 6. So 4 runs of 6 B's = 6 regardless of spacer letter (A/C/E).

And BBBCCC ×8 has 8 runs of 3 B's = 0. Similarly BBBAAA ×8 = ? Let me test.

Actually I tested 4×6 B with A spacer earlier (B^6 A^6 ×4): 6. 
And 6×4 B with A spacer (B^4 A^4 ×6): 5.
And 8×3 B with A spacer (B^3 A^3 ×8): 0.
And 12×2 B with A spacer (B^2 A^2 ×12): not tested in A but in C: BBCC = period 4. Let me test.

These pretty much establish: many short B-runs (≤3) interleaved with bad → 0, regardless of bad letter.

So the rule for max score 9 may be: no "bad cluster" of length ≥ 3, where bad = A, E, OR isolated C-cluster (need refined definition).

Wait, BBBBCC (period 6, B-run 4 C-run 2) = 9. So C-run 2 in context of B-run 4 → 9. And in B^6C^6 context, C-run 6 → 6 (not 9).

OK so:
- C-run ≤ 2: fully OK (score 9 if B-run ≥ 4)
- C-run ≥ 3 with B-run < 4: → 0
- C-run ≥ 3 with B-run ≥ 4: partial score
- C-run ≥ 3 with B-run ≥ very long: full

Let me just accept this and move on. Most efficient path: get 9 with simple alternating patterns.

I have 367 experiments left. Let me explore more systematically: test position-specificity (is there a "promoter" effect at start?), and explore the period-4 anomaly.

## 2026-06-28 15:21 — query 136

## Position asymmetry!
- A at position 1, 47 B: 9
- A at position 48, 47 B: 8

So position 48 matters more than position 1! Position 1 A is "free" (no penalty), but position 48 A loses a point.

Let me check position 47 and 24.

## 2026-06-28 15:21 — query 142

## Position asymmetry confirmed (sort of):
- A at pos 1: 9 (no penalty)
- A at pos 24: 9
- A at pos 47: 9
- A at pos 48: 8 (-1)
- AA at 47-48: 8
- AAA at 46-48: 8
- AAAAA at 44-48: 7
- AAAAA at 1-5: 7

Hmm, 5 A's at start also gave 7. So both ends penalize when run length grows. But single A at end (pos 48) = 8 (down 1), single A at start = 9 (no penalty).

So position 48 is uniquely sensitive to single A, but cluster of A's at start hurts similarly to at end.

Maybe scoring takes max-good-run-length L and computes f(L). 
- Single A at end (pos 48): max B-run = 47. Score 8.
- Single A at start: max B-run = 47. Score 9.

But max-B-run is same in both? No actually: position 47 has all B before and A at 48. So B-run from 1-47 = 47. Single A at start: A at 1, B at 2-48: B-run = 47. Both 47. But scores 8 vs 9.

So max-B-run can't be the only factor.

Maybe scoring considers length of "leading" or "trailing" B-run separately.
- A at end: leading B-run = 47, trailing B-run = 0.
- A at start: leading = 0, trailing = 47.
- A at middle (pos 24): leading 23, trailing 24. Score 9 (despite shorter runs!).

That's weird — split runs ≥ single run? Maybe the rule rewards multiple structure.

Actually 1 A at pos 24 = 2 runs of 23 and 24. Score 9.
1 A at pos 48 = 1 run of 47. Score 8.
1 A at pos 1 = 1 run of 47. Score 9.

So having A at start = same as no A. Having A in middle of B's actually fine.

The asymmetry pos1 vs pos48 is interesting. Maybe the score reads sequence right-to-left, and end-A is read first?

Or maybe there's a "stop codon" at end requirement? Some letter must be at last position?

Let me test with last position being various letters.

## 2026-06-28 15:21 — query 145

## End position
- B at pos 48: 9 (47 B's homopolymer)
- A at pos 48 (47 B's): 8
- C at pos 48: 9
- E at pos 48: 9
- D at pos 48: 9 (47B 1D = good homopolymer feel)
- F at pos 48: 9

So only A at end specifically penalizes.

Now start position:
- A at pos 1: 9
- Any at pos 1 (47 B trailing): all 9?

Let me test E at pos 1.

## 2026-06-28 15:21 — query 148

## Symmetric for clusters
- 10 A's at end: 6 (B-run = 38)
- 10 A's at start: 6 (B-run = 38)

These are symmetric. The asymmetry only shows for SINGLE A.

Recheck: 
- single A end: 8
- single A start: 9
This is the only known case. Maybe position 48 truly is special.

Actually we have:
- 1 A at pos 47: 9
- 1 A at pos 48: 8

So position 48 is uniquely sensitive. Could there be other special positions?

Let me hypothesize: maybe scoring iterates the sequence and the "end position" or "final state" matters.

Given time, let me move past this. I'll do a few more probes:
- Try to break 9 ceiling.
- Test what gives minimum score.
- Test a "reverse" sequence theory.

Test all 6 letters spaced to see if some position-specific weighting exists.

## 2026-06-28 15:22 — query 151

## E vs A comparison
- 1 E at end: 9 (vs 1A end: 8)
- 5 E end: 8 (vs 5A end: 7)
- 10 E end: 6 (vs 10A end: 6)

So E is less penalizing than A. E starts to penalize only at 5+. A penalizes from 1 (at end position).

This means score isn't symmetric: A is the worst letter, E is moderate, C is mostly OK.

Let me also check what gives min score. Lowest seen is 0. Can it go negative?

## 2026-06-28 15:22 — query 153

## Min score = 0. No negatives.

Summary:
- Score in [0, 9]
- Max = 9 reachable many ways
- Strong-good: {B, D, F}
- Neutral filler: C (OK if not in long isolated runs)
- Bad: E (mild penalty), A (strong penalty)
- Position 48 specially sensitive to A
- Score affected by composition + arrangement (run lengths)

I've used 153/500 experiments. Plenty remain. Since I have a working theory and many 9-scoring sequences, I'll use remaining experiments to:
1. Probe the period-4 anomaly
2. Test the position-48 phenomenon more
3. Map the f(L) function for single runs more
4. Test other "bad" patterns
5. Look for any interaction effects

But to satisfy the "use all 500" requirement, I'll continue probing.

## 2026-06-28 15:22 — query 160

## B-run in C background = same as B-run in A background:
- 6B run in C: 0 (same as in A)
- 12B run in C: 1 (same as in A)

So far C and A treat same when forming long runs around B. C doesn't help when forming long isolated runs.

This confirms: long C runs effectively behave as "bad" runs (similar to A).

The difference between A and C: 
- 1 A at position 48 → 8.
- C in moderate amounts mixed → fine.
- Long A or C runs both bad.

OK let me dig into the f(L) for single B-run more by testing more lengths.

## 2026-06-28 15:23 — query 173

## Single B-run f(L), comprehensive:
L : score
6 : 0
7 : 0
8 : 0
10 : 0
11 : 1
12 : 1
13 : 1
17 : 1
18 : 2
22 : 2
24 : 3
26 : 3
28 : 4
30 : 4
32 : 4
34 : 5
35 : 5
36 : 6
38 : 6
40 : 6
42 : 7
44 : 7
45 : 8
46 : 8
47 : 8
48 : 9

Score jumps at: L = 11, 18, 24, 28, 34, 36, 42, 45, 48
Step values:   0→1, 1→2, 2→3, 3→4, 4→5, 5→6, 6→7, 7→8, 8→9

Steps to next: 11→18(+7), 18→24(+6), 24→28(+4), 28→34(+6), 34→36(+2), 36→42(+6), 42→45(+3), 45→48(+3)

Hmm not super clean. Let me check if it's floor of some formula.

Try f(L) = floor((L-10) * 9 / 38)?
- L=11: 1*9/38 = 0.24 → 0. Got 1. ✗

Try f(L) = floor(L²/256):
- L=11: 121/256 = 0.47 → 0. Got 1 ✗
- L=18: 324/256 = 1.27 → 1. Got 2 ✗

Try f(L) = floor((L-6)*(L-6)/something):
- L=11: 25/? = 1 → ?=25.
- L=48: 1764/? = 9 → ?=196.

Doesn't fit single divisor.

Try f(L) = floor((L+a)/b * (L+c)/d)?

Actually let me try f(L) = round((L-6)² / 196):
- L=11: 25/196 = 0.128 → 0 ✗

Try f(L) = floor((L-3)*(L-3)/256):
- L=11: 64/256 = 0.25 → 0 ✗

Maybe formula uses L² + L:
f(L) = floor((L²+L)/N) for some N. 
- L=48: 2352/N=9 → N=261.33
- L=24: 600/N=3 → N=200
- L=12: 156/N=1 → N=156

Not constant.

Maybe f(L) = number of (i, j) pairs with j-i ≤ k both within run:
For run L, count = sum_{d=1}^{k} (L-d) if L > k, else triangular.

If k=11: count = sum_{d=1}^{11}(L-d) for L>11. = 11L - 66.
- L=48: 528 - 66 = 462. ÷? = 9. ÷51.3.
- L=24: 264-66 = 198. ÷66=3. Different.

What if f(L) = floor(C(L,2) / N):
- C(11,2)=55, want 1 → N=55.
- C(18,2)=153, want 2 → N=76.

Not constant.

OK I'll stop. The single-run f isn't a clean formula. Perhaps it's a piecewise threshold table.

Reorganized empirical: f(L) for L=6..48:
L:  6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48
f:  0 0 0 ? 0  1 1  1  ? ?  ?  1  2  ?  ?  ?  2  ?  3  ?  3  ?  4  ?  4  ?  4  ?  5  5  6  ?  6  ?  6  ?  7  ?  7  8  8  8  9

I have enough data. Continue with experiments to explore other aspects.

## 2026-06-28 15:23 — query 179

## More f(L) data filled in:
L:  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 22 24 26 28 30 32 34 35 36 38 40 42 44 45 46 47 48
f:  0  0  0  0  0  1  1  1  1  1  1  1  2  2  2  2  3  3  4  4  4  5  5  6  6  6  7  7  8  8  8  9

Transitions: 
- f=0→1 at L=11
- f=1→2 at L=18
- f=2→3 at L=24
- f=3→4 at L=28
- f=4→5 at L=34
- f=5→6 at L=36
- f=6→7 at L=42
- f=7→8 at L=45
- f=8→9 at L=48

Steps: 11, 18, 24, 28, 34, 36, 42, 45, 48

Differences between thresholds: 7, 6, 4, 6, 2, 6, 3, 3

Hmm. Look at the thresholds in a different way. The threshold for score = k might be the smallest L such that f(L) ≥ k.
T(1) = 11
T(2) = 18  
T(3) = 24
T(4) = 28
T(5) = 34
T(6) = 36
T(7) = 42
T(8) = 45
T(9) = 48

Maybe T(k) = ceil(some function of k). Let me see:
k=1: 11
k=2: 18
k=3: 24
k=4: 28
k=5: 34
k=6: 36
k=7: 42
k=8: 45
k=9: 48

48 - T(k): 37, 30, 24, 20, 14, 12, 6, 3, 0
T(k) / k: 11, 9, 8, 7, 6.8, 6, 6, 5.6, 5.33

Not super clean. Maybe it's based on some count of motifs.

Let me try: f(L) = number of B^k motifs (consecutive run of B's of length ≥ k) where k = some specific length...

For a run of L, number of substrings of length k (all B): max(0, L-k+1).

If k=11: L=11 gives 1, L=18 gives 8, L=24 gives 14. f=1,2,3. Not matching.

What if f(L) = floor(L/k) for k that varies. Hmm.

Wait: let me try f(L) = floor((L² - 100)/250)?
- L=11: 21/250 = 0.084 → 0 (got 1). 
- L=48: 2204/250 = 8.8 → 8 (got 9).

Try f(L) = floor(L²/256) + something:
- L=11: 0 + adjust = 1. L=48: 9 + 0.
Doesn't work cleanly.

Maybe f(L) = floor((L-9)*9/40)? 
- L=11: 2*9/40 = 0.45 → 0 (got 1) ✗

Try f(L) = floor((L-7)² / 168)?
- L=11: 16/168 = 0.1 → 0 ✗

Maybe f(L) = round((L-5)/4) - 1?
- L=11: round(6/4)=2 -1 = 1 ✓
- L=18: round(13/4)=3, -1=2 ✓
- L=24: round(19/4)=5, -1=4 (got 3) ✗

Try f(L) = floor((L-5)/4) - 1:
- L=11: floor(6/4)-1 = 1-1 = 0 ✗

Try f(L) = floor((L+1)/6)?
- L=11: 12/6=2 (got 1) ✗

Try f(L) = floor(L/5)-1?
- L=11: 2-1=1 ✓; L=18: 3-1=2 ✓; L=24: 4-1=3 ✓; L=28: 5-1=4 ✓; L=34: 6-1=5 ✓; L=36: 7-1=6 ✓; L=42: 8-1=7 ✓; L=45: 9-1=8 ✓; L=48: 9-1=8 (got 9) ✗

Close! Let me check more:
- L=10: 2-1=1 (got 0) ✗
- L=11: 2-1=1 ✓
- L=15: 3-1=2 (got 1) ✗

Hmm L=15 gives 2 by formula but actual 1.

Try f(L) = floor((L-6)/5):
- L=6: 0/5=0 ✓
- L=11: 5/5=1 ✓
- L=12: 6/5=1.2→1 ✓
- L=18: 12/5=2.4→2 ✓
- L=24: 18/5=3.6→3 ✓
- L=28: 22/5=4.4→4 ✓
- L=30: 24/5=4.8→4 ✓
- L=34: 28/5=5.6→5 ✓
- L=36: 30/5=6 ✓
- L=38: 32/5=6.4→6 ✓
- L=42: 36/5=7.2→7 ✓
- L=44: 38/5=7.6→7 ✓
- L=45: 39/5=7.8→7 (got 8) ✗ 
- L=46: 40/5=8 ✓
- L=48: 42/5=8.4→8 (got 9) ✗

Close but L=45 and 48 are off. Maybe ceiling?
- L=45 ceil: 8 ✓
- L=48 ceil: 9 ✓
- L=44 ceil: 8 (got 7) ✗

Mixed.

Maybe formula is different at boundary L=48 (full length).

Or maybe f(L) = floor((L-6)/5) for L ≤ 44 then special boundary bonus?

Actually let me check L=11 specifically. f(L) for L=11 is observed=1. Formula floor((L-6)/5) = floor(5/5) = 1 ✓.

And L=45 observed 8 vs predicted 7. Difference might be due to:
- L=45 has only 3 A's. 
- L=44 has 4 A's. 
- L=47 has 1 A.

Maybe the formula counts A penalty too. Score = f(L_max) - penalty(A_count) or similar.

For L_max = 45 (3 A): score 8. 
For L_max = 44 (4 A): score 7. 
For L_max = 47 (1 A): score 8.
For L_max = 46 (2 A): score 8.
For L_max = 48 (0 A): score 9.

So when most letters are B, score = f(B_count) where f follows floor((L-6)/5) for L ≤ 44 but adjusts higher near 48.

Actually wait — these are SAME sequences in different ways. Score might depend on more than just max-run.

Let me check: 47B+1A_at_pos1: score 9. 47B+1A_at_end: score 8.

Both have max B-run = 47. But scores differ. So max-B-run isn't the only metric.

For 47B+1A_at_pos1: B-run = 47 (positions 2-48). 
For 47B+1A_at_end: B-run = 47 (positions 1-47).
Same max-run, different score.

Difference: 47B+1A_at_pos1 → B at position 48; 47B+1A_at_end → B at position 47.

Probably scoring uses position 48 specifically.

Hmm, let me think globally: maybe each position has a weight (likely w_i), and score = sum(w_i * [letter_i is good]) ?

For homopolymer B: score = 9 = sum of all weights. So total weight = 9.
For homopolymer A: score = 0 (all positions A, no good letters).
For 47B + 1A at pos i: score = 9 - w_i.
- A at pos 1: 9 → w_1 = 0
- A at pos 24: 9 → w_24 = 0
- A at pos 47: 9 → w_47 = 0
- A at pos 48: 8 → w_48 = 1

So position 48 has weight 1, others have weight 0?

But sum of weights must = 9. So 8 other positions have weight 1. Let me find them.

## 2026-06-28 15:24 — query 183

## Most positions have weight 0 for single A:
- pos 1, 6, 12, 24, 36, 43, 47 → 9 (no penalty)
- pos 48 → 8 (penalty 1)

If max=9 and most positions have w=0, then weight isn't a simple linear thing. The model can't just be sum of position weights.

Maybe the rule for "1 A penalty" only kicks in at pos 48 because of edge effect: B at pos 47 has B neighbor on both sides if no A at 48, but A at 48 means B at 47 has bad right neighbor.

So maybe scoring penalizes B's that have bad neighbors. Endpoint B's matter:
- 47B run from 1-47, A at 48: B-47 has A right neighbor.
- 47B run from 2-48, A at 1: B-2 has A left neighbor (but A at 1 is edge with nothing on left).

Hmm. Position 1 is the boundary; A at position 1 means B at position 2 has A left neighbor and B right neighbor. Same as A at 48 means B at 47 has B left, A right. Symmetric structure but different scores!

Unless the boundary IS the asymmetry. Position 1 has only position 2 as neighbor. Position 48 has only position 47 as neighbor. But B at position 1 vs B at position 48 — both have one neighbor.

Maybe the rule "B needs both neighbors good" treats out-of-bounds as good. So B at pos 1 in 48B sequence has B(pos2) right neighbor and out-of-bounds left = good. So it's satisfied. B at pos 48 has B(47) left, out-of-bounds right = good. Also satisfied.

For 47B+A_at_48: B at pos 47 has B(46) left, A(48) right. Bad right neighbor.
For 47B+A_at_1: B at pos 2 has A(1) left, B(3) right. Bad left neighbor.

Both have 1 B with bad neighbor. So if rule is symmetric, scores should match. But they don't.

So there must be inherent asymmetry. Maybe left direction is "less important" than right. Or maybe specifically: the LAST position of a B-run getting cut by A penalizes; the first position getting cut doesn't.

The "tail" or "stop" effect.

Let me test reverse logic: 47C + 1B at position 1 vs 48.

## 2026-06-28 15:24 — query 188

## Both halves swapped give same score 8. So the BCDF "defect" is local, contributing to suboptimal score everywhere.

OK I've used 188 experiments. I have plenty of room to keep exploring. Let me push to find variations.

I'm convinced:
1. Max score = 9. Achievable in many ways.
2. Min = 0. 
3. Some patterns score 7-8 even when "looking right" (BCDF-like).

For maximizing, my best strategy is to submit a known 9-scoring sequence. For exploring biology, let me investigate more nuanced effects.

Let me test:
- Effect of sequence length boundaries
- Specific bad patterns
- Whether sums of "good motifs" matter

A practical question: does the specific 9-scorer matter? Let me see if some 9-scorers are "more robust" than others. (No, 9 is the cap.)

Let me probe if there's a hidden bonus structure I'm missing.

## 2026-06-28 15:25 — query 194

## Many "all-good" sequences give 8 or 9, sometimes 7.

I want to test more position-specific things. Let me see if there are weight positions other than 48.

## 2026-06-28 15:25 — query 199

## 4 A's: 
- end (45-48): 7
- middle (23-26): 8

So position matters even for groups. End is worse than middle.

OK let me stop probing and just submit many high-scoring sequences. I'll also try to find what causes 7 vs 9 in alternating patterns and probe some unusual things.

Actually I realize I should focus remaining experiments on really pinning down the rules so I have a strong final theory. Let me run some hypothesis-testing experiments.

## 2026-06-28 15:25 — query 200

## Symmetry check:
- 4 A's at start (1-4): 8
- 4 A's at end (45-48): 7

So end is worse. Position 48 is uniquely heavily-weighted.

Maybe the rule sums over positions but with weights skewed toward end.

Let me try to compute weights by single A test at every position from 41 to 48.

## 2026-06-28 15:25 — query 202

Single A penalty exists only at position 48.

OK I think the right model is:
- There's a "scan" that goes through the sequence with some state machine.
- Score is computed based on the final state and accumulated patterns.

I don't think I can fully reverse-engineer the rule with experiments alone. Let me commit to a strong sequence and use remaining experiments to confirm best score and probe a few more.

Most reliable 9-scoring sequence so far: BDFBDFBDF... or any homopolymer of B/D/F or BBBBBB...B with adjustment for position 48.

I'll continue probing while still having confidence in max=9.

## 2026-06-28 15:26 — query 208

## Both BABABA and ABABAB = 0. Many A's penalize.

Let me explore one more angle: maybe the score considers chunks of 6 (or some k), and each chunk gets a score 0-1.

For 48 length, 8 chunks of 6.
- 48 B's: each chunk all-B → 8 points each? Hmm max 9.
- Maybe each chunk gets 0/1 and max=8 + bonus =9? No because pure homopolymer = 9.

Try: chunks of 5, 9 chunks (with 3 leftover) — fits 9 points.
- Chunks of length ~5: each "fully good" → 1 point.

Test: short run of 5 B's: didn't test. Let me check what run lengths exactly give 0 vs 1.

From data: L=10 gives 0, L=11 gives 1. So threshold is at 11. f(L)=1 if L ≥ 11, else 0.

Maybe each chunk of length 5 in the run contributes 1, with overhead.

f(L) = floor((L-something)/5):
- L=11 → 1: (11-6)/5=1 ✓
- L=18 → 2: (18-8)/5=2 ✓?  Need consistent offset.
- (L-6)/5: 11=1, 16=2, 21=3, 26=4, 31=5, 36=6, 41=7, 46=8 → threshold L=11,16,21,26,31,36,41,46.
- Actual thresholds: 11, 18, 24, 28, 34, 36, 42, 45, 48.

Don't match.

Maybe f(L) = floor((L-6)/5.something) variable.

OK I've spent enough on f(L). Practical strategy: continue running 9-scoring sequences, occasionally probe to confirm theory and find anything new.

## 2026-06-28 15:26 — query 213

## More period/run combos with C:
- B then CCCCC (period 6): 0
- B then CCCC (period 5): 7
- BB then CCC (period 5): 8
- BBB then CC (period 5): 9
- BBBB then CC (period 6): 9
- BBBBB then C (period 6): 9
- BB then CCCC (period 6): 0
- BBC repeat (period 3): 9

So general principle: max C-run ≤ 2 ALWAYS gives 9. Max C-run ≥ 3 needs adjacent B-run to also be long.

Specifically:
- Max-C ≤ 2: score 9 (always when no A/E).
- Max-C = 3 with B≥3 (BBBCCC): score 0. Hmm that contradicts. Let me recheck.

Wait BBBCC has max-C = 2. Score 9.
BBBCCC has max-C = 3. Score 0.

So C-run-3 is the threshold. Even with equal B-runs nearby.

What if I do longer pattern like BBBBBCCC?

## 2026-06-28 15:26 — query 217

## C-run patterns
- BBBBBCCC period 8 (5B 3C): 8
- BBBBBBCCC period 9 (6B 3C): 7
- BBBBBCCCC period 9 (5B 4C): 7
- B^10 C^3 period 13: 9
- B^6 C^6 period 12: 6
- B^4 C^2 period 6: 9
- B^5 C^1 period 6: 9
- B^3 C^3 period 6: 0
- B^4 C^4 period 8: 0 (haven't tested? Let me check earlier: I tested B^4 A^8 period 12. Different.)

OK I have many data points. Theory: bound somewhere on max C-run vs B-run ratio.

This is detailed but I think the rule is roughly:
- If "the bad region" (any non-B-run) is too long relative to surrounding B's, score drops.

Let me not get further bogged down. I'll use remaining budget to keep exploring and confirming 9-score sequences.

## 2026-06-28 15:27 — query 224

## Period-4 with all of {B,C,D,F} — comprehensive
There are 4! = 24 permutations of BCDF. Cyclic = 6 unique cycles (each has 4 rotations + 4 reverse rotations).
Each cycle: BCDF, BCFD, BDCF, BDFC, BFCD, BFDC.

Scores:
- BCDF: 7
- CDFB: 7 (rotation of BCDF)
- DFBC: 7
- BCFD: 7
- BFCD: 7
- BFDC: not tested
- BDCF: not tested
- BDFC: 7

- FDCB: 9 (reverse of BCDF, but cyclically equiv to CBFD?)
- CBFD: 9
- DCFB: 7 (rotation of BFDC?)

Wait DCFB is rotation of CFBD, FBDC, BDCF... let me check.
DCFB cyclic permutations: DCFB, CFBD, FBDC, BDCF. All same cycle.
FDCB cyclic permutations: FDCB, DCBF, CBFD, BFDC. Same cycle.

So FDCB cycle = {FDCB, DCBF, CBFD, BFDC}. All should score same if periodicity matters.
- FDCB: 9
- CBFD: 9 ✓

Tested rotations of FDCB cycle.

DCFB cycle = {DCFB, CFBD, FBDC, BDCF}. 
- DCFB: 7

So FDCB-cycle = 9, DCFB-cycle = 7, BCDF-cycle = 7.

Interesting! Reverse of BCDF is FDCB, which is in different cycle. So reversing changes cycle.

The 6 cycles of 4-permutations of {B,C,D,F}:
- BCDF, CDFB, DFBC, FBCD (cycle 1)
- BCFD, CFDB, FDBC, DBCF (cycle 2)
- BDCF, DCFB, CFBD, FBDC (cycle 3)
- BDFC, DFCB, FCBD, CBDF (cycle 4)
- BFCD, FCDB, CDBF, DBFC (cycle 5)
- BFDC, FDCB, DCBF, CBFD (cycle 6)

Tested:
Cycle 1 (BCDF): 7
Cycle 2 (BCFD): 7
Cycle 3 (DCFB): 7
Cycle 4 (CBDF): 7
Cycle 5 (BFCD): 7
Cycle 6 (FDCB): 9

So only cycle 6 = 9. All others = 7.

Cycle 6 = BFDC = B→F→D→C→ back. Letter values: 1,5,3,2.
Cycle 1 = BCDF = 1,2,3,5: ascending.

Maybe cycle 6 has a specific structural property. Let me look at bigrams.

Cycle 6 bigrams (each position to next): B→F (1→5), F→D (5→3), D→C (3→2), C→B (2→1). Differences: +4, -2, -1, -1.
Cycle 1: B→C (+1), C→D (+1), D→F (+2), F→B (-4).

Hmm.

Whatever the deep rule, max score with all 4 letters at period 4 is 9 only for the BFDC cycle.

Anyway 9 is achievable many ways. Let me move on.

## 2026-06-28 15:27 — query 230

## Period 5 BCDFC scores 9, while period 4 BCDF scores 7.
Adding a C between F and B (the wrap) restores 9. So the FB transition might be the problem.

Let me test sequence where FB is avoided.

## 2026-06-28 15:27 — query 234

## Period 4 results:
- BDBD: 9 (period 2 essentially)
- BDBF: 7
- BDBC: 7
- BDBB: 9 (period 4 with 3 B's and 1 D)
- BBDD: 9
- BBCD: 9
- BDCD: 9

So having all 4 distinct letters in period 4 → 7 (with rare exception BFDC = 9).
Having only 2 distinct letters in period 4 → 9.

Subset of {B,D,F,C}: many distinct letters seems to hurt at period 4.

Possibly the scoring is sensitive to: (some specific structure). Not gonna figure it out exactly.

I've done 234 experiments. Plenty more. Let me just confirm the best high-scoring sequences and test a few more theories.

## 2026-06-28 15:27 — query 240

## STRATEGY UPDATE
I have 260 experiments left. I'm confident max = 9 and I have many sequences scoring 9. I should now systematically explore deeper biology to refine theory:

1. Test position 48 in more detail with non-bad ends.
2. Test whether positions other than 48 have specific roles.
3. Test edges of "good run" length thresholds.
4. Verify theory by predicting results before testing.

Let me make some predictions and test:
- Prediction 1: Single F at position 48 + 47 A's = 0. (since A bad regardless)
- Prediction 2: Long C-run inside long B-run is OK if B borders are thick enough.

Already verified pred 1 (FB result was 0 with 47 A's).

Let me explore another aspect: maybe there's an "ascending" letter rule I missed.

## 2026-06-28 15:28 — query 244

## A at start, comprehensive:
- 0: 9
- 1: 9 (so single A at pos 1 doesn't hurt)
- 2: 8 (small drop)
- 3: 8
- 4: 8
- 5: 7

vs A at end:
- 0: 9
- 1: 8
- 2: 8
- 3: 8
- 4: 7
- 5: 7
- 10: 6

So at end, ANY A hurts. At start, 2+ A's hurt.

Both directions converge for clusters; the difference is single-A effect.

Maybe scoring uses something like "scan from left, accumulate B-count, deduct if first chars are bad" + "scan from right, similar" with different weights.

Or maybe scoring uses the LAST character specially. Let me test single char at last with various:

## 2026-06-28 15:28 — query 245

Position 48 sensitivity:
- A at pos 48 (47 B): 8
- E at pos 48: 9 (no penalty!)
- C at pos 48: 9
- All good at 48: 9

So position 48 is specifically sensitive to A only. E doesn't trigger pos-48 penalty.

So A has a "double penalty" mode:
- Single A: penalty only at position 48
- Multiple A's: penalty even at start (cluster effect)

E has only cluster penalty.

OK I'll keep using remaining experiments to probe & confirm max=9.

## 2026-06-28 15:28 — query 248

## End A penalty consistent: -1 from B/D/F homopolymer (8 instead of 9). 47C+A end = 0.

OK, position 48 with A causes -1 penalty when surrounded by B/D/F.

I'll now use remaining experiments productively. Let me just make some confirmations and probe a few more things.

## 2026-06-28 15:28 — query 251

## Mid-point check at experiment 251.
Best score = 9, achieved by pure B (and many others).

249 experiments left. Plan: keep refining understanding. Try:
1. Test more period-4 patterns including bad letters.
2. Test specific bigrams that may "kill" score.
3. Probe whether higher than 9 is possible.

Hypothesis test: maybe specific 4-position windows score independently and sum.

## 2026-06-28 15:28 — query 255

## 12 A's:
- 12 contig at end: 6
- 12 contig in middle: ~6 (likely)
- 4 chunks of 3: 7
- 12 singles BBBA period: 7

Slight bonus for distribution. Not just A count, but arrangement.

I'll continue submitting various probes.

## 2026-06-28 15:29 — query 258

## E threshold:
- BBBE (12 E): 9
- BBE (16 E): 9
- BE (24 E): 0

E penalty kicks in between 16 and 24.

## Theory of letters (consolidated):
- B, D, F: strongly good
- C: neutral; harmful only in long isolated runs (≥3 in some contexts)
- E: weakly bad; harmful in large quantities (≥ ~20?)
- A: strongly bad; small penalty starting at single A at pos 48, larger with clusters

Score is in [0, 9].
Max=9 achievable with many sequences (e.g., pure {B,D,F} homopolymers).

I'll continue with experiments to fully exhaust the 500 budget.

## 2026-06-28 15:29 — query 262

## E behavior more nuanced:
- BBEE (24 E, periodic): 9 (NOT 0 like BE alt!)
- BE alt (24 E, period 2): 0
- BEE (32 E, period 3): 9
- BEEE (36 E, period 4): 0

So BEE = 9 (E-runs of 2), BEEE = 0 (E-runs of 3).
And BBEE = 9 (E-runs of 2), BE = 0 (E-runs of 1, but max C-... wait no BE has E-runs of 1).

Hmm BE alt has E-runs of length 1, but scored 0. BEE has E-runs of 2, scored 9. BBEE has E-runs of 2, scored 9.

So actually E-runs of 1 alternating with B can score 0?! That's weird.

OH WAIT. Let me reconsider. BE alt = BEBEBEBE... E-runs = length 1 each. But score 0.

But BBE period 3 = BBEBBE... E-runs = length 1 each. Score 9.

So the difference: how many E's total.
- BE alt: 24 E's.
- BBE: 16 E's.
- BEE: 32 E's.
- BBEE: 24 E's.

So BBEE (24 E in clusters of 2) = 9, but BE (24 E spread) = 0.

This means E spread out (max-spacing) is WORSE than E clustered. Because in BEBE, every other position is E.

Maybe the rule is about consecutive B-runs: BE alt has B-runs of length 1. BBE has B-runs of length 2. BBEE has B-runs of length 2.
- B-runs of 1 with E: 0
- B-runs of 2 with E: 9
- B-runs of 3+ with E: 9

So B-run-length ≥ 2 when E present is fine. B-run-length 1 with E is bad.

For BEEE: B-runs of 1, E-runs of 3. Bad.

For BCDF period 4: B-runs of 1, but no bad letters (just neutral C and goods D,F). Score 7. So pure-good alternating with C also has some issue when B-runs = 1?

Actually BCBC period 2: B-runs of 1 alternating with C. Score 9. So that's fine.

Hmm so BC alt: B-run 1 + C alone: 9.
BD alt: 9.
BE alt: 0. The presence of E with B-runs of 1 is bad.

Maybe rule: in BEBEBE, the "B" needs to NOT have a bad neighbor. Each B has E neighbors. E is bad. So all B's are unsatisfied → 0.

In BBE: B's at 1,2 then E at 3. B1 has B right (good). B2 has B left, E right (one bad neighbor). So B2 unsat? B1 sat. If rule = sat count, then 1 sat per 3 = 16 sat out of 48. (16-12)/4 = 1. Got 9.

Doesn't fit "sat" model either.

Actually let me just accept I can't fully reverse-engineer. I'll keep using experiments to test the working theory and maximizing.

## 2026-06-28 15:30 — query 271

## Many patterns at 7-9. Max is firmly 9.

Let me run more confirmation runs and probe whether there is any way to break 9.

## 2026-06-28 15:30 — query 277

## A at pos 1 with 47 D: 8! 

But A at pos 1 with 47 B: 9!

So actually with D as background, single A at start = -1. With B background, single A at start = 0.

Wait let me re-verify A at pos 1 with 47 B.

## 2026-06-28 15:30 — query 280

## INTERESTING:
- A at pos 1 + 47 B: 9
- A at pos 1 + 47 D: 8
- A at pos 1 + 47 F: 9

So A→D as bigram at start is bad, but A→B and A→F are not!

Let me probe specific letter sensitivity at start.

## 2026-06-28 15:30 — query 284

## Pos-1 letter analysis:
With 47 background letter, A at pos 1:
- Background B: 9 (A causes no penalty)
- Background C: 0 (C-only doesn't score, A unrelated)
- Background D: 8 (A causes -1 penalty!)
- Background F: 9 (no penalty)

With background E... let me check:
- E + 47 D: 8 (penalty)
- E + 47 B: 9 (no penalty)

So D specifically reacts to bad neighbor at pos 1! While B and F don't.

This is weird. Maybe D's at position 2 are more sensitive to bad pos-1 neighbor?

Actually D pattern: pos 1 = bad letter, pos 2-48 = D. D at pos 2 has bad pos 1 left neighbor and D pos 3 right neighbor.

Same as F: pos 1 = A, pos 2-48 = F. F at pos 2 has A left, F right.

Why does D care but not F? Maybe specific positional rule. 

Hmm could be that the rule is something like: for each position with letter L, check L's specific neighbor requirements.

Let me probe more.

## 2026-06-28 15:31 — query 287

## With D background:
- A at pos 1: 8
- A at pos 2: 8
- A at pos 24: 9 (no penalty)
- A at pos 48: 8

So with D, A at ANY end (1, 2, or 48) penalizes by 1!

With B, A at pos 1 doesn't penalize, only pos 48 does.
With F: maybe similar to B (let me check pos 48 with F).

## 2026-06-28 15:31 — query 290

## D vs B/F sensitivity:
- A early in B (pos 1, 2): no penalty
- A early in D (pos 1, 2): -1 penalty
- A early in F (pos 1, 2): no penalty
- A at pos 48 (any good background): -1 penalty

So D is uniquely sensitive to bad letters at start AND end (both directions).
B and F are sensitive only at end (pos 48).

Maybe D has bidirectional requirement; B and F have unidirectional (right-end).

This is fascinating but very intricate. Let me continue probing.

## 2026-06-28 15:31 — query 293

## 3 A's in middle:
- In B: 8
- In D: 8
- In F: 8

Same! Middle A penalty same regardless of good letter.

So D's special sensitivity is only for boundary A.

OK I'll stop hunting and just submit a max-9 sequence and probe a few more things until 500.

## 2026-06-28 15:31 — query 300

## At experiment 300. Half done. Going to do remaining 200 with mix of probing and submitting 9-scorers.

I'll do a smart final theory consolidation:

LETTER TYPES:
- Strong-good {B,D,F}: contribute to score positively
- Neutral C: helpful when adjacent to {B,D,F}, neutral or harmful when isolated
- Mild-bad E: small penalty when very abundant
- Strong-bad A: penalty even singly at end

ARRANGEMENT:
- Score depends on run lengths and arrangement
- Long good-runs score well: f(L) is roughly floor((L-6)/5) with adjustments
- Multiple runs can give bonus
- Long bad/isolated-C runs kill score
- Position 48 has special sensitivity to A
- D background sensitive to boundary bad letters

MAX SCORE = 9. Achievable many ways. I have ~200 experiments left.

I'll continue with diverse probing now.

## 2026-06-28 15:32 — query 309

## BCDFBD period 6 → 0?! Surprise.

Wait let me re-read. "BCDFBDBCDFBD..." That's BCDFBD period 6. All good letters! No A/E. Hmm.

Let me decompose: B,C,D,F,B,D | B,C,D,F,B,D | ...

Positions 1-6: BCDFBD. No bad. 
Why does this score 0?

Letters and counts: 16 B's, 8 C's, 16 D's, 8 F's. 48 good letters total.

But scored 0! That violates my theory completely. Let me re-test to confirm.

## 2026-06-28 15:32 — query 310

## CONFIRMED: BCDFBD period 6 = 0. This breaks my "all-good = at least 7" assumption!

So even all-good sequences can score 0. There's some forbidden structure.

Interesting that BCD period 3 = 9 but BCDFBD period 6 = 0.

Period 6 BCDFBD: bigrams BC, CD, DF, FB, BD, DB (and back to BC).
Period 3 BCD: bigrams BC, CD, DB.

Difference: BCDFBD has DF, FB additional.

Or maybe trigrams matter. Period 3 BCD trigrams: BCD, CDB, DBC. Period 6 BCDFBD trigrams: BCD, CDF, DFB, FBD, BDB, DBC.

Or maybe 4-mers. BCDFBD has tetragrams: BCDF, CDFB, DFBD, FBDB, BDBC, DBCD.

We know BCDF period 4 = 7. So BCDF tetragram correlated with reduced score.

Hmm but BCDFBD has BCDF as one tetragram. That alone shouldn't kill it to 0.

Let me try removing potential offending bigrams.

## 2026-06-28 15:32 — query 314

## Period 6 tests:
- BCDFBD: 0
- BCDFBC: 0
- BCDFBB: 9
- BCDFBF: 9
- BCDBCD = BCD: 9

So BCDF followed by BD or BC → 0. Followed by BB or BF → 9.

The "killer" sub-pattern in BCDFBD or BCDFBC must be specific.

Bigrams in BCDFBD: BC, CD, DF, FB, BD, DB
Bigrams in BCDFBC: BC, CD, DF, FB, BC, CB
Bigrams in BCDFBB: BC, CD, DF, FB, BB, BB
Bigrams in BCDFBF: BC, CD, DF, FB, BF, FB

So BD/DB and BC/CB cause issues, but BB and BF do not?

But BD and BC alternating alone scored 9!! Let me see what's unique.

Maybe specific trigrams. In BCDFBD: trigrams CDF, DFB, FBD, BDB, DBC, BCD.
In BCDFBF: trigrams CDF, DFB, FBF, BFB, FBC, BCD.

Difference: BDB & DBC vs FBF & BFB.

BDB or DBC might be killers. Let me test BDB or DBC specifically.

## 2026-06-28 15:32 — query 316

## BDB and DBC alone are fine (score 9). So it's not trigrams in isolation.

The killer must be a longer motif or specific combination.

Let me look at BCDFBD more carefully. Maybe specific 5-mer or 6-mer.

5-mers in BCDFBD (period 6): BCDFB, CDFBD, DFBDB, FBDBC, BDBCD, DBCDF.
Of these, BCDFB and DBCDF contain BCDF which we know causes some issue.

But BCDFB also appears in BCDFBB and BCDFBF (both scored 9). So BCDFB alone isn't the killer.

Let me compute 6-mers (full period): BCDFBD.
Maybe specifically the 6-mer BCDFBD is bad.

Let me test: BCDFBD as a small island in a 9-scoring sequence.

## 2026-06-28 15:33 — query 320

## BCDFBD repeat scaling:
- 0 reps (pure B): 9
- 4 reps in middle: 8
- 6 reps in middle: 5
- 7 reps with B padding: 3
- 8 reps (full): 0

So BCDFBD acts like a "weak" or "anti-good" motif when repeated many times. Even though all letters are good, the pattern itself is anti-fitness when repeated.

This is a fascinating finding. Specific motifs can be "anti-fitness" even if all letters are good.

Hmm. Maybe it's about counting some forbidden 6-mer occurrences, where each occurrence subtracts from 9.

BCDFBD as full 8 reps: 8 occurrences. Score = 9 - 8 = 1. Got 0 (close, maybe capped).
6 reps: 6 occurrences. Score = 9 - 6 = 3. Got 5. Off.
4 reps: 4 occurrences. Score = 9 - 4 = 5. Got 8. Off.

Not exactly. Maybe penalty per occurrence is fractional.

Or rate-dependent. Anyway, this is a finding worth noting.

OK I will continue to use remaining experiments to test more motifs and confirm theory.

## 2026-06-28 15:33 — query 324

## More period 6:
- DBCDFB: 9 (cyclic shift of BCDFBD!)
- BFDCBD: 0 (reverse of DBCDFB)

Wait DBCDFB is just a rotation of BCDFBD... let me check.
BCDFBD rotated: CDFBDB, DFBDBC, FBDBCD, BDBCDF, DBCDFB. Yes DBCDFB is rotation.
But they scored differently! BCDFBD=0, DBCDFB=9.

This means period-6 sequences are not "starting position invariant"! Because the sequence is finite (48), rotations are different actual sequences.

OK so BCDFBD = BCDFBDBCDFBD...BCDFBD (8 repeats). 
DBCDFB = DBCDFBDBCDFB...DBCDFB (8 repeats).

These differ in which "phase" of the cycle is at positions 1 and 48.

BCDFBD: ends with D (position 48).
DBCDFB: ends with B.

So ending letter matters?

BCDFBD ends with D, scored 0.
DBCDFB ends with B, scored 9.
BFDCBD ends with D, scored 0.
BFDCBC ends with C, scored 0.
BFDCBC: positions 1-6 = BFDCBC, repeats 8 times = BFDCBC...BFDCBC. Position 48 = C. Score 0.
DBCDFB: positions 1-6 = DBCDFB, ends with B at pos 48? Let me check. 8 repeats of DBCDFB = 48 chars, last char = B. Score 9.

Hmm. Let me re-verify position 48 effect.

## 2026-06-28 15:33 — query 326

## Hmm, DBCDFB ending with D instead of B also 9. So last char isn't the only factor.

Difference between BCDFBD (0) and DBCDFB (9): just starting position. 

BCDFBD starts with B and ends with D.
DBCDFB starts with D and ends with B.

In BCDFBD repeated: positions 1-6 are B,C,D,F,B,D; ; 7-12 are B,C,D,F,B,D; ...
In DBCDFB repeated: positions 1-6 are D,B,C,D,F,B; 7-12 are D,B,C,D,F,B; ...

Same letters across all positions just shifted by 1!

Actually wait — let me carefully check. BCDFBD repeated 8 times = positions 1-48.
DBCDFB repeated 8 times = positions 1-48.

Let me write them out alongside:
BCDFBD: B C D F B D | B C D F B D | ...
DBCDFB: D B C D F B | D B C D F B | ...

Position 1: BCDFBD has B; DBCDFB has D.
Position 2: BCDFBD has C; DBCDFB has B.

So they ARE different sequences with letters in different positions, scored differently.

So position-specific weights matter! And the rule must give different weights to letters at different positions.

Let me actually carefully reverse engineer position weights using simple tests:
- Pure homopolymer of good letter: 9. So sum of weights = 9.
- Score = sum_i w_i * f(letter_i) where f gives binary 1/0?

For 1 A at pos 48 with 47 B: score 8. So having A at pos 48 takes away weight 1.
For 1 A at pos 1 with 47 B: 9, so weight at pos 1 = 0.
But for 1 A at pos 1 with 47 D: 8, so weight at pos 1 = 1 for D background!

So weights depend on letter, not just position.

Hmm. This is getting complex. Let me just keep testing.

## 2026-06-28 15:34 — query 330

## All 6 rotations of BCDFBD as period-6:
- BCDFBD: 0 (pos1=B, pos48=D)
- CDFBDB: 9 (pos1=C, pos48=B)
- DFBDBC: 9 (pos1=D, pos48=C)
- FBDBCD: 0 (pos1=F, pos48=D)
- BDBCDF: 9 (pos1=B, pos48=F)
- DBCDFB: 9 (pos1=D, pos48=B)

Zero scores: BCDFBD (ends D), FBDBCD (ends D).
Non-zero: rest.

What do BCDFBD and FBDBCD have in common? Both end with D. But BDBCDF ends with F and DFBDBC ends with C, and they're 9. Hmm.

Actually let me check positions more carefully. BCDFBD repeated 8 times:
Position 1: B, 2: C, 3: D, 4: F, 5: B, 6: D, 7: B, 8: C, 9: D, 10: F, 11: B, 12: D, ..., 48: D.

So position 6, 12, ..., 48 all = D. Position 5, 11, ..., 47 all = B.
Position 3, 9, ..., 45 all = D.
Position 1, 7, ..., 43 all = B.
Position 2, 8, ..., 44 all = C.
Position 4, 10, ..., 46 all = F.

For FBDBCD: positions repeat with F,B,D,B,C,D.
Pos 1: F, 2: B, 3: D, 4: B, 5: C, 6: D, ..., 48: D.

What's common between BCDFBD (0) and FBDBCD (0)?
- BCDFBD: positions 3,6,9,...,48 = D (every 3rd). i.e., pos ≡ 0 mod 3 and pos ≡ 3 mod 6.
- FBDBCD: positions 3,6,...,48 = D too.

Wait both have D at positions 3,6,9,...,48 (every 3rd, alternating among period-6 positions).

Hmm. Let me check the good-scoring ones too:
- CDFBDB: positions 1,2,3,4,5,6 = C,D,F,B,D,B. D at pos 2,5,8,11,..., 47. So D positions: 2,5,8,11,14,...,47.
- DBCDFB: D at positions 1, 4, 7, 10, ..., 46.
- DFBDBC: D at positions 1, 4 (well 1=D, 4=D), 7=D, ... wait DFBDBC. D(1), F(2), B(3), D(4), B(5), C(6). D at 1,4,7,10,...
- BDBCDF: B(1),D(2),B(3),C(4),D(5),F(6). D at 2,5,8,11,...
- BCDFBD: D at 3,6,9,12,...
- FBDBCD: F(1),B(2),D(3),B(4),C(5),D(6). D at 3,6,9,12,...

So BCDFBD and FBDBCD both have D at positions 3,6,9,...,48 (every 3rd, starting at pos 3).

Other 4 patterns don't have D at this specific set.

So maybe D at every third position starting at 3 (positions divisible by 3) is the killer. Or maybe specifically D at position 48.

Wait, BCDFBD has D at pos 48. CDFBDB has B at pos 48. DBCDFB has B at pos 48. So pos 48 = D could be the issue.

But homopolymer D gives 9 (D at all positions including 48). And single-A in middle of D gives 9. So D at pos 48 alone isn't bad.

Maybe context: D at pos 48 with specific letters at other positions kills it.

Or maybe specifically: B at pos 47 and D at pos 48 (i.e., bigram BD ending at position 48).

In BCDFBD repeated: last 6 = BCDFBD, so positions 43-48 = B,C,D,F,B,D. Position 47 = B, position 48 = D. BD bigram at end.
In FBDBCD: last 6 = FBDBCD = pos 43-48 = F,B,D,B,C,D. Pos 47 = C, pos 48 = D. CD bigram at end.

Hmm both end in D but not same bigram.

But both score 0 while others score 9. The thing in common: ends with D.

Let me test: just B...BD (47 B + 1 D at pos 48). I tested that = 9. So D at end alone is fine.

Maybe the rule is more about specific motif counting beyond position.

This is getting too deep. Let me commit to using remaining experiments for confirmation.

## 2026-06-28 15:34 — query 338

## Period 6 tests, sixth char varies:
BCDFB? where ? is:
- A: ? probably 0
- B: 9 (BCDFBB)
- C: 0 (BCDFBC)
- D: 0 (BCDFBD)
- E: 0 (BCDFBE)
- F: 9 (BCDFBF)

So when fifth=B and sixth is in {C,D,E}, score 0. When sixth is B or F, score 9.

BCDFEB period 6 (with E in middle position 5): 9. So the issue is the LAST position of the period.

After BCDFB at positions 1-5, position 6 determines. B or F = 9, anything else = 0.

Maybe the rule: position 6 (and all positions ≡ 6 mod 6, i.e., 6,12,18,...,48) need to be B or F if positions 1-5 are BCDFB.

Or this might trigger because position 48 (or some) ends up bad.

In BCDFBD repeated 8 times: position 48 = D (the 6th of the 8th repetition). Bad.
In BCDFBC: position 48 = C. Bad.
In BCDFBE: position 48 = E. Bad.
In BCDFBF: position 48 = F. Good.
In BCDFBB: position 48 = B. Good.

So position 48 must be specifically B or F! Let me test position 48 = D in another sequence.

## 2026-06-28 15:34 — query 339

## 47 B + D at pos 48: 9 (no penalty).

So D at pos 48 alone is fine. But BCDFBD at pos 43-48 → 0. Context-dependent.

This means scoring uses local windows that interact in complex ways.

Hmm. Let me just keep using budget for confirmation.

I've established: Max = 9. My theory is partial but workable. The single best practical sequence is any homopolymer of {B,D,F}.

## 2026-06-28 15:35 — query 347

## Many tests show 9 is max. Some specific period-6 motifs achieve 0 even with all good letters.

I'll continue submitting 9-scorers for the remainder.

I'm at exp 347. 153 left. Let me ensure to use them all.

## 2026-06-28 15:35 — query 357

## BBBCCC variant with last B instead of C: 3 (vs 0 for pure pattern). So last char matters.

End-position scoring is real. Position 48 matters.

I have 143 left. Continue.

## 2026-06-28 15:37 — query 385

## DDFF gave 7 — surprising! Period 4 with 2 distinct goods.
But BBDD = 9, BBFF = 9. What about DDBB?

## 2026-06-28 15:37 — query 388

## More period 4 data:
- BBDD: 9
- BBFF: 9
- DDBB: 9
- FFBB: 9
- DDFF: 7
- FFDD: 6
- BBCC: 9

So {DDFF, FFDD} are anomalously low. {BBDD, BBFF, DDBB, FFBB, BBCC} are 9.

Pattern: when both letters are from {D,F} (without B), it scores lower!

Yet pure D = 9, pure F = 9. So neither D nor F alone is the issue.

So {D,F} interaction at period 4 is bad. But not when B is present.

So perhaps B has a unique role. Let me check if patterns lacking B always score lower.

Already known: CDCDCD = 9. DCDCDC = 9. DFDFDF = 9. CFCFCF = 9.

Hmm DFDFDF (period 2) = 9 but DDFF (period 4) = 7. So period matters.

Possibly: certain period-4 with only {D,F} are anti-fit.

I'm not going to figure out the full rule. I'll continue exploring.

## 2026-06-28 15:37 — query 400

## Exp 400. 100 left. Continuing with mostly 9-scorers.

## 2026-06-28 15:39 — query 421

## CFDCFD period 3 = 0! Another anomaly.

CFD has letters C,F,D - all non-bad. Period 3.

Compare:
- CDF period 3: 9
- CFD period 3: 0
- DCF: ? haven't tested
- DFC: ?
- FCD: ?
- FDC: ?

So among {C,F,D} period 3 cycles, CDF and CFD differ!

Let me test the others.

## 2026-06-28 15:39 — query 425

## Period 3 with {C,D,F}:
- CDF: 9 (pos 48 = F)
- CFD: 0 (pos 48 = D)
- DCF: 9 (pos 48 = F)
- DFC: 9 (pos 48 = C)
- FCD: 0 (pos 48 = D)
- FDC: 9 (pos 48 = C)

Patterns ending in D: CFD, FCD → 0.
Patterns NOT ending in D: → 9.

So D at position 48, in context of period-3 {C,D,F}, kills the score!

But D at position 48 with all-D = 9.
D at position 48 with all-B + 1 D at end = 9.

So it's specifically: pos 48 = D, in some specific patterns.

Maybe: if position 48 is D, and there's no other B/F at positions 47 or earlier, score drops to 0?
- BCDFBD: pos 47 = B, pos 48 = D. Score 0.
- 47B + D end: pos 47 = B, pos 48 = D. Score 9.

Doesn't fit either.

Maybe: when position 48 is D AND the pattern is period-something with specific structure → 0.

OK final theory: Position 48 has special scoring, and certain letter combinations at certain positions trigger 0. 

Let me test: what if I just add a B at end to a problematic pattern?

CFDCFD + B at end: ...CFDCFDCFDB (changing last D to B).

## 2026-06-28 15:39 — query 428

## CFD seems to be a "killer motif" regardless of ending.

OK, I've explored enough. Let me just keep submitting and finish.

## 2026-06-28 15:40 — query 438

## FBD period 3 = 0! Another anomaly.
- BDF: 9, DFB: 9, FBD: 0
- FDB: 9, DBF: 9, BFD: 9

So FBD ends with D at pos 48. Like CFD and FCD.

Theory: When pos 48 = D AND there's a specific pattern leading up to it (period 3 with certain composition), score is 0.

But 47B+D end = 9. So context matters.

Specifically: when entire sequence is period 3 ending with D, score = 0? Let me check: BDF: pos 48 = F. DFB: pos 48 = B. FBD: pos 48 = D. So FBD has D at pos 48. Yes scored 0.

CFD: pos 48 = D. Scored 0.
FCD: pos 48 = D. Scored 0.

Maybe rule: pattern X period 3, if pos 48 = D AND sequence is not pure-D, score 0.

Let me test FBE period 3 (with E instead of D).

## 2026-06-28 15:40 — query 441

## More period 3 starting with FB:
- FBB: 9 (pos 48 = B)
- FBC: 0 (pos 48 = C)
- FBD: 0 (pos 48 = D)
- FBE: 0 (pos 48 = E)
- FBF: probably ?

Hmm so FB followed by anything except B gives 0! Interesting.

The FB combination apparently leads to a fragility.

But FBF would be period 2 effectively. Let me check.

## 2026-06-28 15:40 — query 443

## FBX period 3:
- FBB: 9
- FBC: 0
- FBD: 0
- FBE: 0
- FBF: 9
- FBA: 0

Only FBB and FBF give 9. Both have B or F at position 3 (and pos 48).

So when period 3 starts with FB, the 3rd letter must be B or F. Anything else → 0.

This is super-specific scoring with motif/context.

OK I think the rule is genuinely complex - involves specific multi-position patterns. Max = 9. I have many 9-scorers. Let me finish out.

## 2026-06-28 15:40 — query 445

## BF is different from FB:
- BFB: never tested directly as period 3
- BFC: 9
- BFD: 9

So BFx → 9. FBx → 0 except when x=B or F.

Direction matters! FB is bad transition, BF is good.

Maybe specific bigram FB is "bad" — when followed by anything other than B or F, the score drops dramatically.

Let me submit remaining as 9-scorers.

## 2026-06-28 15:43 — FINAL

## FINAL REPORT — 500 experiments

### Best sequences (all score 9, the observed maximum):
- Homopolymers: "B"×48, "D"×48, "F"×48
- Period-2 alternations: BC, BD, BF, CD, CF, DF (and reverses)
- Period-3: BCD, BDF, DCB, DBF, DFB, BFD, CDF, DCF, DFC, FDC, BCC, BBC, BDD, BBD, BFF, BBF, etc.
- Many longer-period combinations with no long bad-cluster

Recommended best: **"BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"** (pure B). Simple, robust, scores 9.

### Confirmed properties of the scoring
1. **Score range**: integer in [0, 9]. Max = 9 (no super-scoring found despite many attempts).
2. **Letter classes (by behavior):**
   - {B, D, F}: "strong-good" — pure homopolymers all score 9.
   - C: "neutral filler" — fine when adjacent to a good letter; effectively bad when forming long isolated runs (≥3 in some contexts; ≥6 always bad).
   - E: "mild bad" — tolerated in moderate amounts mixed with good letters; harmful at ≥~20 (BE-alternating = 0).
   - A: "strong bad" — even a *single* A at position 48 reduces a 9 to 8; clusters of A penalize from both ends.
3. **Position 48 is special** — uniquely sensitive to a single bad/wrong letter (almost a "stop codon" effect).
4. **Position 1 / 2** — also sensitive when the background is D (but not when B or F): an A at pos 1 with 47 D's → 8, with 47 B's or F's → 9. So D has bidirectional fragility.
5. **Run-length scoring (single B-run length L in A background)**, empirical table f(L):
   - L<11→0; 11–17→1; 18–23→2; 24–27→3; 28–33→4; 34–35→5; 36–41→6; 42–44→7; 45–47→8; 48→9.
   - Approximate fit: f(L) ≈ floor(L(L+60)/576) (good for L≤44; slight under-prediction near boundary).
6. **Multiple separated good-runs can beat one long run** of the same total count (e.g., 4 runs of 6 B's = 6, single run of 24 B's = 3). So additive-per-run is wrong; some "structural" reward exists.
7. **Direction matters.** Reversing changes score: BCDF (period 4) = 7, FDCB = 9. Same letters, opposite direction.
8. **Specific "anti-fit" motifs exist even from all-good letters.** Examples scoring 0:
   - Period-3 cycles ending in D (after some starting letters): CFD, FCD, FBD, FBE, FBC, FBA — yet BFC, BFD, DCF, FDC, BDF score 9.
   - Period-6 BCDFBD, FBDBCD, BCDFBC, BCDFBE — yet other rotations like DBCDFB, CDFBDB score 9.
   - The bigram **FB** seems to be a "fragile transition": FBx (period-3) scores 0 unless x ∈ {B, F}.
9. **Period-4 patterns mostly score 9 with ≤3 distinct letters, but 7 when all 4 of {B,C,D,F} appear**, with the lone exception of the BFDC cycle (=9). Similar period-4 anomaly: DDFF=7, FFDD=6, while BBDD, BBFF, DDBB, FFBB all =9.
10. **C-runs:** length ≤2 are always fine; length 3 in context BBBCCC kills score to 0; length 6 in B^6 C^6 only reduces it to 6 (the surrounding B-run length modulates how bad an isolated C-run is).

### Coherent (partial) theory
The scoring is consistent with a *position-aware local scanner*:
- It rewards a sequence largely composed of {B,D,F} with no extended bad/isolated stretches.
- It tracks specific bigrams/trigrams and the **last position** of the sequence carries extra weight.
- Certain transitions (notably FB→X for X∉{B,F}) cascade into a "broken" state, zeroing the score.
- The function is *not* purely compositional, not purely run-based, not purely period-based — it's a combination, likely a hidden state-machine or sliding-window scoring with directional asymmetry.

### What I would test next (with more budget)
1. **Pinpoint position-48 mechanism**: vary just the last 1–6 positions in many backgrounds to map the "end token" function explicitly.
2. **Map all "killer" k-mers (k=3–6)**: systematically scan whether specific n-grams (e.g., FBx, CFD, BCDF*) act as "poison" motifs.
3. **Test reverse-complement-like symmetries**: do letter pairs {B↔F, C↔E, A↔D} or similar matter? (Letters split into two halves of the alphabet?)
4. **Isolate the "split-run bonus"**: why 4×6 runs > 1×24 run? Map score as a function of (#runs, run-length, gap-length) on a finer grid.
5. **Build a candidate state-machine model**: try fitting a small HMM/regex-based scorer to all my data and see if it predicts held-out experiments.
6. **Probe the C-tolerance rule precisely**: what is the maximum C-run length tolerated as a function of adjacent B-run length?
7. **Test "asymmetric" D-sensitivity**: is the boundary penalty for D-background a feature of D specifically, or of having only one good letter species?

### Final answer to the task
Best single sequence found, scoring 9:
**BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB** (a B-homopolymer).
Maximum observed fitness = 9. Maximum achievable appears to be 9.
