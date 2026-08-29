
## 2026-06-28 15:31 — query 0

## Initial Setup
- Alphabet: {A, B, C, D}, sequence length: 48, budget: 500 experiments
- No prior assumptions about biology
- Score is a single number, higher = better

## Initial Strategy
1. Test homogeneous sequences (all-A, all-B, all-C, all-D) to see baseline letter preferences
2. Test simple periodic patterns (AB, AC, AD, BC, BD, CD repeated) to detect pairwise interactions
3. Test position-dependence by varying single positions
4. Build up a model from there

## First experiment: all-A (48 A's) - baseline reference

## 2026-06-28 15:31 — query 4

## Homogeneous results
- AAAA...: 9
- BBBB...: 0
- CCCC...: 9
- DDDD...: 9

B is bad on its own. A, C, D all give 9. Need to test mixtures - perhaps diversity matters, or B is just a negative letter.

## Next: simple alternating patterns to test pairwise interactions

## 2026-06-28 15:32 — query 9

## Pairwise patterns
- AB...: 0  (B is poisonous)
- AC...: 9
- AD...: 9
- CD...: 9
- ABCD repeated: 6 (mixed)

Hypothesis: B is a "poison" letter that drops score, OR there's a stop codon-like pattern.
- All-B = 0, AB alternating = 0. AC, AD, CD all = 9.
- ABCD = 6 (still has B but interspersed, score is 6, not 0)

Wait - AB gave 0 but ABCD gave 6? Both contain B. Maybe particular adjacencies matter:
- In AB repeated, every adjacent pair is AB or BA
- In ABCD repeated, B is adjacent to A and C

Maybe BA is the killer pattern? Or AB? Let me test sequences with B in different contexts.

## Next: isolate where B is and what neighbors matter

## 2026-06-28 15:32 — query 11

## More pairwise
- BC alt: 0
- BD alt: 0
- AB alt: 0
- BB only: 0

So any sequence with lots of B gives 0. But ABCD repeated (with 12 B's) gave 6, not 0.

Maybe the rule is: if too many B's, score = 0. Threshold?
- All-B (48 B's): 0
- AB alt (24 B's): 0
- ABCD (12 B's): 6

So somewhere between 12 and 24 B's the score collapses. Or it's about B-runs / B-density.

Let me test fewer B's.

## 2026-06-28 15:32 — query 13

## B position tests
- AC...AB (B at pos 48): score 8 (was 9 without B)
- B at pos 1, rest AC...: score 9

Interesting - B at end cost 1 point. B at start cost 0. So position matters!

Or wait - maybe it's about what B is adjacent to. End B: ...CAB (neighbors are A). Start B: BAC... (neighbor is A). Both neighbor A.

Actually let me re-examine. In "ACACACACAB" (48 chars), position 48 is B. Sequence ends ...ACAB. Last 4: A,C,A,B. So B's only neighbor is A.

In "BACAC..." position 1 is B, neighbor is A.

Both single B's flanked by A. Different scores: 8 vs 9.

Maybe end-of-sequence matters specifically? Or maybe the AC pattern is so strong starting with A gives 9 even with a B at start?

Hmm, let me check if "ACAC..." starts with A and ends with C. 48 chars of AC: A at odd, C at even. Position 48 = C. So replacing last C with B (->...CACAB) cost 1 point but replacing first A with B (->BCAC...) might also cost a point - need to compare to actual AC baseline more carefully.

Wait AC alt baseline was 9. ACACAB (last) = 8. So -1. BACAC (start) = 9. So 0.

Let me see if there's a maximum (maybe 9 is just the cap and B at start happens to also yield max 9 in a noisy way).

## Try maximizing - test if anything exceeds 9

## 2026-06-28 15:32 — query 14

## Surprise!
- ACDACD... = 0! Wow.

So ACDACD repeated gives 0, but AC alone gives 9, AD alone gives 9, CD alone gives 9. Adding all three together = 0??

This breaks my "B is poison" theory. Something more complex going on.

Possibilities:
- Certain triplets are bad. ACD or CDA or DAC?
- Period-3 sequences are bad?
- Specific adjacency patterns

ACDACD has all adjacent pairs: AC, CD, DA, AC, CD, DA, ...
- AC = good (AC alt = 9)
- CD = good (CD alt = 9)
- DA = ? (this is AD reversed, AD alt = 9 but DA wasn't tested)

Or maybe the triplets: ACD, CDA, DAC are bad?

Let me test DA alternating to check.

## 2026-06-28 15:32 — query 17

## Direction tests
- DA=9, CA=9, DC=9. All pairwise alternations of {A,C,D} work fine in both directions.
- ACD repeated = 0. Three-letter cycle breaks it.

Hypothesis: maybe period-3 sequences are bad, or specific triplets.

Test more period-3 patterns and also test if certain triplets cause failure.

## 2026-06-28 15:32 — query 19

## Triplet exclusion test
Both ACDD and AACD give 0. Both contain A, C, AND D.

Hypothesis: presence of all three letters {A, C, D} simultaneously = score 0?

Wait but ABCD repeated gave 6, and that has A, C, D plus B. Let me reconsider.

ABCD repeated = 6. That has A, B, C, D (all four).
ACD-based = 0. Has only A, C, D.

Hmm. So adding B saves the sequence? Or maybe the rule is about specific triplets:
- ACD repeated has ACD, CDA, DAC triplets
- AACD repeated has AAC, ACD, CDA, DAA
- ABCD has ABC, BCD, CDA, DAB

Both ACD and AACD contain "ACD" substring. AABCD doesn't. Wait ABCD: A-B-C-D, no "ACD" adjacent.

Hypothesis: the substring "ACD" (or maybe "CDA", "DAC") is lethal.

Let me test.

## 2026-06-28 15:32 — query 20

## Single ACD test
ACAC...ACDA = 9. So a single ACD substring is not lethal.

Wait, does this sequence actually contain ACD? Let me trace 48 chars.
"ACACACACACACACACACACACACACACACACACACACACACACACDA" - that's 48 chars.
Position 1-46: AC alternating (46 chars), then "DA" at 47-48.
But wait, position 46 should be C (even index = C in 1-indexed AC pattern). Then 47=D, 48=A. So we have ...A,C,D,A at end. That gives substring "ACD" at positions 45-47 and "CDA" at 46-48. So yes ACD is present.

Score 9, so ACD substring isn't lethal alone.

Maybe it's about density / count, or about all three letters appearing many times.

Let me count letter usage in failures:
- ACD repeated (48): A=16, C=16, D=16, B=0. Score 0.
- AACD repeated (48): A=24, C=12, D=12. Score 0.
- ACDD repeated (48): A=12, C=12, D=24. Score 0.
- ABCD repeated: A=12, B=12, C=12, D=12. Score 6.

Hypothesis: A sequence with substantial amounts of A, C, AND D (all 3) fails, UNLESS rescued by B.

Or: the problem is needing exactly 2 distinct letters (no more) from {A,C,D}, but B is "neutral"?

Test: ACACACAC...ACD with some D's mixed in - 9 with 1 D. Try 2 D's, etc.

## 2026-06-28 15:33 — query 24

## Updated data
- ACAC...DD..ACAC (2 D's): 9
- ACDDDD pattern (16 D's, 16 A, 16 C): 7
- ACD x8 + B x24: 0  -- B doesn't rescue ACD!
- ABC repeated (16 each of A,B,C): 0

So ABCD repeated = 6, but ABC repeated = 0. And ACD = 0.

Maybe the rule: certain repeating motifs are bad. ABCD has period 4 which somehow works.

Or: about specific dimer transitions?
- ABCABC adjacencies: AB, BC, CA, AB, BC, CA. Has AB and BC, both gave 0 alone.
- ABCDABCD adjacencies: AB, BC, CD, DA. Has AB (0) and BC (0) but mixed with CD (9) and DA (9). Score 6.

Hmm. ACD repeated adjacencies: AC, CD, DA. All "good" individual pairs but combined give 0.

Maybe it's not about adjacent pairs but about distances or counts.

Wait — pure pairs (only 2 letters) all give 9 if neither is B. Three letters from {A,C,D} gives 0. So maybe: must use at most 2 letters from {A,C,D}?

Check: AC+DD partial (mostly AC, 8 D's): score 7. Still has 3 letters from {A,C,D}.
Check: 2 D's inserted: score 9. Has 3 letters from {A,C,D} but only 2 D's.

So it's not just letter presence - it's amount.

Maybe a count-based rule. Let me make a table:
- A=24,C=24,D=0: 9 (AC alt)
- A=24,C=0,D=24: 9 (AD alt)
- A=0,C=24,D=24: 9 (CD alt)
- A=16,C=16,D=16: 0 (ACD alt)
- A=23,C=23,D=2: 9 (AC + 2 D inserted) 
- A=16,C=16,D=16, but with B=0 still 0
- A=12,B=12,C=12,D=12: 6 (ABCD)
- A=20,C=20,D=8: 7 (ACDDDD pattern... wait that's 16/16/16)

Let me recount ACACACACDDDDACACACACDDDDACACACACDDDDACACACACDDDD:
Pattern "ACACACACDDDD" (12 chars) repeated 4 times = 48.
Per repeat: A=4, C=4, D=4. Total: A=16, C=16, D=16. Score 7.

Interesting - same letter counts as ACD repeated (16/16/16), but score 7 vs 0. So it IS about arrangement, not just counts.

Maybe: B is required to "break up" or maybe specific repeats are bad.

The clean pattern is: short repeated motifs containing all three of A,C,D simultaneously fail.

Let me test: longer ACD-containing stretches vs interspersed.

## 2026-06-28 15:33 — query 25

## Big insight!
- 16A then 16C then 16D (blocked) = 9!
- Same letter counts as ACDACD... but blocks instead of interspersed.

So it's about local arrangement. ACDACD has bad adjacency patterns somewhere.

Adjacencies in AAAA...CCCC...DDDD: AA (15x), AC (1x), CC (15x), CD (1x), DD (15x). 
So only ONE AC adjacency, ONE CD adjacency. Very low density of certain transitions.

Adjacencies in ACDACD: AC, CD, DA, AC, CD, DA, ... 16x AC, 16x CD, 15x DA.

Hypothesis: too many of certain transitions? Or specifically, having all of AC, CD, DA together is bad?

In AAAA...CCCC...DDDD we have AC=1, CD=1, DA=0. Only AC and CD.

Let me test mixing all three transitions but at lower density.

## 2026-06-28 15:33 — query 28

## More cyclic tests
- DAC repeat: 0
- ADC repeat: 0
- ACD repeat: 0

All triplet repetitions of {A,C,D} give 0.

What about doubling: AACCDD?

## 2026-06-28 15:33 — query 30

## Block size matters
- AACCDD repeated (blocks of 2): 0
- AAAACCCCDDDD repeated (blocks of 4): 7
- AAA...CCC...DDD (single blocks of 16): 9

So bigger blocks = better. Crossing all three letters with short period = 0.

This feels like there might be a "loop" / closure / topology rule. The cycle A→C→D→A creates a cyclic dependency.

Or there might be a global parity / counting rule about which letters border which.

Let me think more carefully about it. In AAA..CCC..DDD: A borders A,A,A,...,A,C. C borders A,C,...,C,D. D borders C,D,D,...,D. So:
- A is adjacent to: A (lots), C (1x)
- C is adjacent to: A (1x), C (lots), D (1x)
- D is adjacent to: C (1x), D (lots)

C has both A and D neighbors. Fine, score 9.

In ACDACD: A has C,D neighbors. C has A,D neighbors. D has A,C neighbors. EVERY letter borders both other letters multiple times.

In AAAACCCCDDDD repeated: A borders A,C. C borders A,C,D. D borders C,D,A (at boundary D→A). At the wrap... let me check: AAAACCCCDDDDAAAA... so D borders A. So D borders C and A. 
- A: A, C, D
- C: A, C, D  
- D: A, C, D

All three border all three. Score 7 (intermediate).

In AAA...CCC...DDD (single block): A borders only A,C. C borders A,C,D. D borders C,D. So only C touches all three. Score 9.

Hypothesis emerging: bad to have letters frequently adjacent to "diverse" neighbors? Or: having all three of A,C,D each adjacent to both of the others is bad.

This is interesting. Let me also note that BB-heavy = 0. B might be totally lethal. Maybe B is fine in low amounts.

Let me test:
1. low amount of B in good sequence
2. Test triplet idea: any sequence where ALL of {A,C,D} each have both other letters as neighbors → low score

## 2026-06-28 15:33 — query 34

## B effects in A background
- 0 B's: 9
- 1 B: 9
- 4 B's block: 7
- 8 B's block: 6
- 12 B's blocks: 7
- 24 B's (AB alt): 0
- 48 B's: 0

So B isn't pure poison; large amounts of B drop score, but moderate amounts are tolerated. Note 12 B's in blocks gave 7, 8 B's at end gave 6.

Now let me revisit ABCD = 6:
- A=12, B=12, C=12, D=12.
- ABCDABCD... adjacencies: AB, BC, CD, DA. 
- Score 6. Not 0!

Maybe B "neutralizes" the bad ACD cycle? In ABCD, the cycle A→B→C→D→A includes B which is "safe" somehow.

Let me explore the underlying rule more. Maybe B has a special role.

What if B is "blank" / "gap" and the rule is about the remaining structure?

Let me try sequences with B as spacer.

## 2026-06-28 15:34 — query 37

## Mixed observations
- ABCB rep (12A,24B,12C): 0 (high B count?)
- ABBCBB rep (8A,24B,8C, 0D): 0
- 16A+16B+16C blocks: 6 (lower than 16A+16C+16D which was 9)

So even blocks of A+B+C give 6, less than A+C+D = 9. B brings down score.

Score 0 cases (so far):
- All-B: 0
- AB, BC, BD alternating: 0
- ABC repeated: 0
- ABCB repeated: 0  
- ACD, AACD, ACDD, DAC, ADC, AACCDD: 0
- ACDB blend (24 B's, 8 ACDs): 0
- ABBCBB: 0

Common to many 0s: high B count (>= ~16 with intermixing) OR ACD interleaving.

Score 6+ cases:
- ABCD repeat (12 each): 6
- 16A+16B+16C blocks: 6
- 16A+16C+16D blocks: 9 (no B)
- AAAA...CCCC blocks of 4 with D: 7

Tentative theory: 
1. Need some structure (long blocks or 2-letter alternation)
2. B is somewhat tolerated but degrades score in proportion to count
3. Having all 3 of {A,C,D} in tight interleaving causes structural failure

Let me test pure A+B blocks at various ratios to map B's effect.

## 2026-06-28 15:34 — query 39

## A+B block ratio
- 48A,0B: 9
- 44A,4B: 7
- 40A,8B: 6
- 32A,16B: 4
- 24A,24B: 3
- 0A,48B: 0

Roughly linear: score ≈ 9 - 0.2*N_B? Actually rough fit shows B alone hurts.

But B mixed with A and C and D might be different. Need to think about B's role separately from interleaving.

Let me now reach for higher scores. So far max is 9. Maybe the cap is 9 or maybe sequences can reach higher. Let me try some specific patterns to see if anything scores >9.

## 2026-06-28 15:34 — query 42

## Search for >9
- 24A+24C blocks: 9
- 44A+4C: 9
- 47A+1C: 8 (!)
- 48A: 9

Interesting: 47A+1C dropped to 8, but 48A=9 and 44A+4C=9. So 47A+1C isn't as good as 48A or 44A+4C.

Maybe sequence "ends" need to differ? Or it's about runs?

Let me check what 47A+1C looks like: AAAAA...AAAAC (C at end). Vs 44A+4C: AAAAAAA...AAAACCCC. The single C at end creates a run length distribution {47 A's, 1 C}. 

Theory: maybe score relates to # of distinct "runs" or similar?
- 48A: 1 run, score 9
- 47A+1C: 2 runs (run of 47, run of 1), score 8
- 44A+4C: 2 runs (44, 4), score 9
- 24A+24C: 2 runs (24, 24), score 9

So having a run of length 1 hurts? Let me test.

## 2026-06-28 15:34 — query 43

## Surprising end-bias
- 47A+1C (C at end): 8
- 1C+47A (C at start): 9

Position dependent! Start vs end of sequence matter differently.

Re-examining earlier: ACAC...ACAB (B at end) = 8, BACAC... (B at start) = 9. Same pattern!

So: foreign letter at end of sequence drops score by 1, but at start doesn't. Could be that there's a "terminator" / "ribosome end" rule.

Let me look at 48-A vs others: end character matters.
- All-A ends in A: 9
- AC alt ends in C (position 48 is even): 9
- 47A+1C ends in C: 8
- 44A+4C ends in C: 9
- 24A+24C ends in C: 9

Hmm, multiple sequences ending in C give 9, but specifically 47A+1C ends in C and gives 8.

Maybe the rule is about the LAST RUN being short:
- 48A: last run = 48 A's = 9
- 47A+1C: last run = 1 C, short = 8
- 44A+4C: last run = 4 C's = 9
- 24A+24C: last run = 24 C's = 9

So last run of length 1 = score - 1. Test with last run of length 2 or 3.

## 2026-06-28 15:34 — query 45

## End-run length
- 48A (end run 48 of A): 9
- 47A+1C (end run 1): 8
- 46A+2C (end run 2): 8
- 45A+3C (end run 3): 9
- 44A+4C (end run 4): 9

So end run < 3 hurts. Specifically, end run >= 3 is fine, end run of 1 or 2 = -1.

OR: this is some other rule about "stop codons" - maybe the last 3 chars matter.

Let me check 45A+3C: last 3 chars are CCC. 46A+2C: last 3 chars are ACC.
44A+4C: last 3 chars CCC. 47A+1C: last 3 chars AAC.

Hypothesis: last 3 characters must be all same? Test by putting different end runs.

## 2026-06-28 15:34 — query 46

## End-3 not "all same"
- 45A+CDC: 9. So last 3 don't need to be same.

Hmm. Let me revisit:
- 47A+1C: 8 (ends with "AAC")
- 46A+2C: 8 (ends with "ACC")
- 45A+3C: 9 (ends with "CCC")
- 45A+CDC: 9 (ends with "CDC")
- 44A+4C: 9 (ends with "CCCC")

What's special about ACC vs CDC vs CCC? Wait — 46A+2C ends in "ACC", and 47A+1C ends in "AAC".

Looking at the last 3 positions:
- AAC: 8
- ACC: 8
- CCC: 9
- CDC: 9
- CCCC: 9

The pattern that gave 8: end with one or two C's after A's, i.e. exactly one "A→C" transition near the end.

What about CDC: it has C→D→C. Two transitions at end. 

Maybe what matters is the very end pair: position 47-48?
- last 2 = "AC" → 8 (47A+1C)
- last 2 = "CC" → 8 (46A+2C, but here pos 47 is A→C transition is at pos 46-47)
  - wait actually 46A+2C: positions are AAAAAA...A(46)C(47)C(48). So pos 46=A, 47=C, 48=C.
  - last 2 (pos 47-48) = CC
- last 2 = "CC" → 9 (45A+3C: pos 46=C, 47=C, 48=C)

So last 2 can't distinguish. But pos 46 differs: 46A+2C has pos 46=A; 45A+3C has pos 46=C.

Maybe the rule involves codons - position-mod-3 reading frame.
- Pos 1-3, 4-6, ..., 46-48: 16 codons.
- Last codon = positions 46-48.

In 47A+1C: last codon = pos 46,47,48 = A,A,C = "AAC"
In 46A+2C: last codon = "ACC"
In 45A+3C: last codon = "CCC"
In 45A+CDC: last codon = "CDC"

Maybe AAC and ACC are "bad codons" while CCC and CDC are "good codons"? Or this is a stop-codon rule!

Let me test reading frame hypothesis - change a middle codon.

## 2026-06-28 15:34 — query 48

## Codon hypothesis evidence
- AAC at end (position 46-48): 8
- AAC at start (position 1-3): 8
- ACC at end (pos 46-48): 8
- AAA + CCC inserted at codon-aligned 25-27: 9 (CCC codon is fine, AAA codons fine)

So "AAC" appearing as a codon (frame-aligned) costs 1 point.

Let me test if "ACC" also bad in middle, and explore more codons.

## 2026-06-28 15:35 — query 49

## ACC mid-codon
- ACC at codon 9 (pos 25-27): score 9! Not penalized.
- ACC at end (codon 16, pos 46-48): 8

So only the END codon penalty? Or maybe the start codon too.

Test ACC at start vs end vs middle:
- mid: 9
- end: 8

So end matters. Test AAC at middle.

## 2026-06-28 15:35 — query 50

## Mid AAC: 9
- AAC at codon 9: 9
- AAC at codon 16 (end): 8
- AAC at codon 1 (start): 8

So START and END codons matter, middle ones can be AAC freely.

Or, alternatively: the rule isn't about codons at all but about positions near edges.

Test single C at various positions to map.

## 2026-06-28 15:35 — query 51

Oops I sent the same sequence. Got 8 again, confirming AAC at start = 8. 

Test single C at pos 2 to see if it's the codon or just "C in pos 3".

## 2026-06-28 15:35 — query 53

## Single C position tests in all-A background
- pos 1 (codon "CAA"): 9
- pos 2 (codon "ACA"): 9
- pos 3 (codon "AAC"): 8
- pos 27 (codon "AAC" at codon 9): 9
- pos 48 (codon "AAC" at codon 16): 8

So AAC at codon 1 and codon 16 gives 8. AAC at middle codons gives 9.

Hmm, maybe the rule is: first codon and last codon work as start/stop signals. Some "good" first/last codons, some "bad" or "default" ones.

Let me think reverse:
- ALL-A (first AAA, last AAA): 9
- C at pos 3 (first AAC): 8
- C at pos 48 (last AAC): 8

So changing first codon AAA→AAC dropped score by 1.

So maybe AAA is good but AAC is suboptimal as first/last codon. Or specifically AAA is the "default" good codon.

What if score = 9 - (number of "bad" first/last codons)? Or something like:

If first codon = X and last codon = Y, score depends on (X, Y).

Test: change first codon to other things.

## 2026-06-28 15:35 — query 57

## More first-codon tests
- AAA: 9
- CCC: 9
- DDD: 9
- BBB: 8
- ABA (one B at pos 2): 9
- AAC (one C at pos 3): 8

This is odd. CCC, DDD fine, but BBB is bad as first codon. And AAC bad.

Maybe the rule isn't codon-based at all - maybe it's just about specific (position, letter) penalties.

Single C at pos 3: -1. Single C at pos 48: -1. Single C at pos 27: 0.

Single B at pos 2: 0. But BBB (3 B's at start): -1.

Hmm. Let me check single B at specific positions.

## 2026-06-28 15:35 — query 59

## Single B positions in all-A
- pos 1 (BAA): 9
- pos 2 (ABA): 9
- pos 3 (AAB): 8

So B at position 3 = -1 just like C at position 3 = -1.

This looks frame-related! Position 3 is end-of-first-codon. So having something other than A at the third position of the first codon hurts.

But wait — CCC at start gave 9 (positions 1,2,3 all C). Position 3 = C, yet score 9.
And DDD at start gave 9. Position 3 = D, yet 9.

So a single non-A at pos 3 hurts, but if all three positions are the same letter it doesn't?

Maybe rule: first codon must be a "homorepeat" (XXX) to avoid penalty?

Test "ACA" first codon — already did, single C at pos 2 in all-A = 9.

OK so what's the actual rule? Let me list first codons tested:
- AAA: 9 (all-A)
- CAA: 9 (single C pos 1)
- ACA: 9 (single C pos 2)
- AAC: 8 (single C pos 3) ← penalty
- AAB: 8 (single B pos 3) ← penalty
- BAA: 9 (single B pos 1)
- ABA: 9 (single B pos 2)
- BBB: 8 ← penalty
- CCC: 9
- DDD: 9

Penalty seems to fire when position 3 has a non-A letter UNLESS positions 1,2 also match (CCC, DDD ok). Hmm but BBB also has all 3 same but penalized!

Wait — BBB also penalized. So B is special.

Maybe rule about "homopolymer runs that are length-3 of B" OR "transitions at position 2-3"?

Actually let me reconsider. BBB has 3 B's. What if there's a global B-count penalty AND a position-3 penalty?

Single B anywhere = ? Single B at pos 1, 2 = 9 (no penalty). At pos 3 = 8. So position-3 hurts.

But BBB at start = 8 = same as single B at pos 3. So if there's a B-count penalty, it's <1 per B for small counts.

Try BB at start (positions 1-2).

## 2026-06-28 15:35 — query 60

## More patterns
- BB at pos 1-2 then A's: 9 (no penalty)
- BBB at pos 1-3: 8 (penalty)

So having 3 B's in a row OR something positional matters. Specifically pos 3 B's hurt.

Wait — BBA at pos 1-3 then A's: same as "BB at start": 9. Pos 3 = A.
BBB at pos 1-3: pos 3 = B. 8.

So the pattern is just: pos 3 must be A. Or: position 3 must match position 2? Let's see:
- CAA: pos 3 = A → 9
- ACA: pos 3 = A → 9
- AAC: pos 3 = C → 8 (mismatch)
- AAB: pos 3 = B → 8
- BAA: pos 3 = A → 9
- ABA: pos 3 = A → 9
- BBA: pos 3 = A → 9
- BBB: pos 3 = B → 8
- CCC: pos 3 = C → 9!
- DDD: pos 3 = D → 9!

So pos 3 isn't simply "must be A". CCC and DDD with pos 3 ≠ A give 9.

Maybe rule: position 3 letter must match position 1 letter (or maybe position 2)?
- CCC: pos1=C, pos3=C ✓ match → 9
- DDD: pos1=D, pos3=D ✓ match → 9  
- BBB: pos1=B, pos3=B ✓ match → 8 (DOESN'T fit!)
- AAC: pos1=A, pos3=C ✗ → 8
- AAB: pos1=A, pos3=B ✗ → 8

Hmm BBB is exception. Maybe B is just always penalized?

Test: AB-only sequences with B at various counts.

Or maybe rule: pos 1 and pos 3 must match, plus B is bad in general (small global penalty per B).

Let me test specific: BAB and BCB and BDB as start.

## 2026-06-28 15:35 — query 62

## First codon palindrome test
- BAB: 8
- CAC: 9
- AAA: 9
- CCC: 9
- DDD: 9

So pos1=pos3 with letter A,C,D: 9. With B: 8.

So B is intrinsically -1 (always). Or only at certain positions.

Hypothesis re-cast: The score has multiple components:
- A base score related to letter composition
- Position-3 letter and how it relates to context

Actually I wonder if I should test isolation: pure 47A + 1B at different positions.

## 2026-06-28 15:36 — query 64

Single B at pos 24, 25 both = 9. So a lone B in the middle of A's is fine. 

So B is NOT intrinsically penalized.

Let me revisit BBB at start: 8. AAB at start: 8. BB at start: 9.

Maybe the rule is: position 3 specifically. AAB has non-A at pos 3 → -1.
BBB has B at pos 3 → but matches pos 1.

Hmm. But CCC has C at pos 3 and no penalty. BBB has B at pos 3 and -1.

OH! Maybe a totally different angle: maybe the penalty for BBB comes from B count = 3 reaching some threshold via mass-action.

Test: 4 B's elsewhere (not at start).

## 2026-06-28 15:36 — query 65

4 B's in middle = 9. So 4 B's not enough to lower.

Earlier 4 B's at end (44A+4B at end) gave 7. Let me recheck — actually I tested 4 B's at end position 45-48: AAAA...AAAABBBB. Got 7.

So 4 B's at end: 7. 4 B's in middle: 9.

Hmm, the END is much more sensitive! 

Let me dig into the end-of-sequence rule more systematically.

## 2026-06-28 15:36 — query 69

## Single B at end positions
- pos 45 (codon 15 pos 3): 9
- pos 46 (codon 16 pos 1): 9
- pos 47 (codon 16 pos 2): 9
- pos 48 (codon 16 pos 3): 8

So only pos 48 hurts. Same as pos 3 for start (only pos 3 hurts).

For 4 B's at end (45-48): 7. That's pos 45,46,47,48. Pos 48 = -1, but score is 7 not 8. So the additional 3 B's at 45-47 also cost. Maybe they form a run.

Maybe rule about (positions 1-3) and (positions 46-48) being "framed" specifically.

Let me re-examine more carefully:
- 8 B's at positions 41-48: 6
- 4 B's at positions 45-48: 7
- single B at pos 48: 8

So as B-block extends inward from end, score drops.

Penultimate codon (44-46) and last codon (46-48 — wait, 46+47+48 is "last codon" if codons are 1-3, 4-6, ..., 46-48).

Let me test: last codon = ABB (pos 46=A, 47=B, 48=B).

## 2026-06-28 15:36 — query 71

## Last codon B tests
- BBB last codon (45 A's + BBB): 8 — wait that's 45 A's + 3 B's at pos 46-48. Score 8.
- BBBB at 45-48: 7
- Single B at pos 48: 8
- 4 B's at 45-48: 7

So pos 48 = -1 (regardless of pos 47, 46 if A). Adding pos 45 B → -2.

Hmm let me see: pos 45 is the LAST position of codon 15.
Pos 48 is last of codon 16.

Codon-3-position is special! Pos 3, pos 48 both are codon-position-3 of edge codons.

Hmm but pos 45 (a non-edge codon's pos 3) gave 9 with single B...
Wait single B at pos 45: 9. But BBBB at 45-48: 7.

Let me test BBBA (B at 45,46,47, A at 48).

## 2026-06-28 15:36 — query 72

## Refined end-codon
- BBBA (pos 45-48 = B,B,B,A): 9 — no penalty!
- BBBB (pos 45-48): 7 — penalty 2
- ABBB (pos 45-48 = A,B,B,B): 8 (this is the 45A+3B case)
- AAAB (pos 45-48 = A,A,A,B): 8

So as long as pos 48 = A, penalty is 0. Once pos 48 ≠ A, penalty depends on more.

Wait the position 3 of first codon: AAB, AAC, BBB all 8. CCC, DDD = 9.
And ABBB (last 4 chars) = 8, BBBB = 7.

For last codon (46,47,48):
- AAA: 9
- AAC: 8 (47A+1C; last codon "AAC")
- AAB: 8 (47A+1B; last codon "AAB")  
- BBB: 8 (45A+BBB)
- CCC: 9 (45A+3C ended in CCC)
- CDC: 9 (45A+CDC)
- ACC: 8 (46A+2C; last codon "ACC")

Pattern: last codon "AAA" = 9. Last codon ending in C/D/B but starting with A's = penalty. But CCC/CDC = no penalty.

Maybe the rule depends on "good last codon" set. Like: stop codons in our world.

Let me think of it as: what makes a sequence "valid"?

If sequence = mostly homo-A but last 1-2 chars different from A → penalty.
If sequence = AAA...AAA-CCC at end → no penalty (looks like a valid "stop").

Maybe analogous to start/stop codons!

Let me check: does the first codon also need to be one of {AAA, CCC, DDD}?
- AAA: 9
- CCC at start: 9
- DDD at start: 9
- BBB at start: 8

So maybe "start codons" allowed = {AAA, CCC, DDD} (homopolymer with non-B)?

For last codon: AAA, CCC, CDC = 9. Test more.

## 2026-06-28 15:36 — query 76

## Last codon tests
- AAA: 9
- AAC: 8
- ACC: 8
- AAB: 8
- BBB: 8
- CCC: 9
- DDD: 9
- CDC: 9
- CDA: 9
- CCD: 9
- CAA: 9

Pattern! Codons that score 8 all START with A (and don't equal "AAA"). 
Codons that score 9 either:
- start with non-A letter (C, D)
- or equal AAA

Wait CAA starts with C and ends in AA: 9. So "starts with C, D" + anything → 9.
AAB starts with A (not AAA) → 8.
AAC starts with A (not AAA) → 8.
ACC starts with A (not AAA) → 8.

So the rule for last codon (pos 46-48) seems to be:
- If starts with A: must be AAA (or score -1)
- If starts with C or D: no penalty
- Need to test B

Or simpler: position 46 specifically? If pos 46 = A, then pos 47-48 must also be A?

CDA: pos 46=C → 9 (irrelevant of rest)
CCD: pos 46=C → 9
CAA: pos 46=C → 9
AAC: pos 46=A, pos 47=A, pos 48=C → not all A → 8
ACC: pos 46=A, pos 47=C → not all A → 8
AAA: all A → 9
BBB: pos 46=B → ? (got 8)
AAB: pos 46=A, last not A → 8

So if pos 46 = A, last 3 must be AAA. Otherwise no penalty.

Test: pos 46 = B, rest A's.

## 2026-06-28 15:36 — query 77

BAA last codon: 9. So pos 46 = B, then A, A → 9.

Hmm so the rule may be even simpler: last 2 positions (47,48) must match position 46? OR: the score depends on transitions in last positions.

Let me check:
- AAA: pos46=A=pos47=pos48 → 9
- CAA: pos46=C, pos47=A=pos48=A → 9 (transition at 46-47)
- CDA: pos46=C, 47=D, 48=A → all different → 9
- BAA: pos46=B, 47=A=48=A → 9
- AAC: pos46=A=47=A, 48=C → 8
- ACC: pos46=A, 47=C=48=C → 8
- AAB: pos46=A=47=A, 48=B → 8

I notice: failures all have pos 46 = A AND pos 48 ≠ A. Successes either pos 46 ≠ A OR pos 48 = A.

Wait: 47-48: AA, AA, DA, AA, AC, CC, AB.
- AC: 8
- CC: 8 (after A at 46)
- AB: 8
- AA: 9 always

Maybe simpler: last 2 must be AA OR first letter (pos 46) must not be A?

Test: last 3 = ABA (pos 46=A, 47=B, 48=A).

## 2026-06-28 15:37 — query 78

ABA last codon: 9. Pos 48 = A. ✓ matches my hypothesis (pos 48 = A → ok).

Refined: penalty if pos 48 ≠ A AND pos 46 = A.
- AAC, ACC, AAB all match this. → 8
- BBB: pos 46=B (not A) → should be 9, but was 8!

Hmm BBB doesn't fit. Let me re-test BBB at end.

Wait, maybe the issue is the transition between pos 45 (A) and pos 46 (B). For all-A + BBB: pos 45=A, 46=47=48=B. Transition at 45-46.

For BAA: pos 45=A, 46=B, 47=A. Transitions at 45-46 and 46-47. Still 9.

For ABA: pos 45=A, 46=A, 47=B, 48=A. Transition at 46-47. 9.

Maybe it's about whether last position (48) equals first position of a "tail run"? 

Or maybe simpler: last position pos 48 = A → 9 OR if not, score = 8?

But CCC at end gave 9, with pos 48 = C!

So:
- pos 48 = C, last 3 CCC: 9
- pos 48 = C, last 3 AAC: 8
- pos 48 = C, last 3 ACC: 8
- pos 48 = C, last 3 CDC: 9
- pos 48 = D, last 3 DDD: 9
- pos 48 = D, last 3 CCD: 9
- pos 48 = A, last 3 BAA, ABA, AAA, CAA, BBA?: 9

It seems sometimes pos 48 = C is fine, sometimes not.

Maybe the rule is: position 46 must NOT be A unless the last 3 are AAA?

- AAA: AAA → 9 ✓
- BAA: 46=B (not A) → 9 ✓
- CAA: 46=C → 9 ✓
- CDA: 46=C → 9 ✓
- CCC: 46=C → 9 ✓
- DDD: 46=D → 9 ✓
- CDC: 46=C → 9 ✓
- CCD: 46=C → 9 ✓
- ABA: 46=A but last 3 = ABA, not AAA → should be 8, but was 9!

Wait ABA was 9. So my rule fails.

Hmm. Let me list all again with pos 46,47,48:
- (A,A,A): 9
- (A,A,B): 8 ← single B at end
- (A,A,C): 8
- (A,C,C): 8
- (A,B,A): 9
- (B,A,A): 9 ← BAA
- (C,A,A): 9
- (C,C,C): 9
- (C,D,A): 9
- (C,D,C): 9
- (C,C,D): 9
- (D,D,D): 9
- (B,B,B): 8

So 8 cases: AAB, AAC, ACC, BBB.
9 cases include: ABA, CAA, BAA, CCC, DDD, CDA, CDC, CCD, AAA.

What's common in the 8 cases?
- AAB: 47=A, 48=B
- AAC: 47=A, 48=C
- ACC: 47=C, 48=C  
- BBB: 47=B, 48=B

Common: 47=48 except AAB and AAC? No AAB has 47=A 48=B.

Actually let me look at (47, 48):
- AB → 8 (AAB)
- AC → 8 (AAC)
- CC → 8 (ACC) 
- BB → 8 (BBB)

(47, 48) for 9 cases:
- AA: 9 (AAA, BAA, CAA, ABA—wait ABA has 47=B, 48=A. Let me redo)

(47, 48) recheck:
- (A,A,A) → (47=A, 48=A)
- (A,A,B) → (A, B)
- (A,A,C) → (A, C)
- (A,C,C) → (C, C)
- (A,B,A) → (B, A)
- (B,A,A) → (A, A)
- (C,A,A) → (A, A)
- (C,C,C) → (C, C) — wait this gives 9 with same (C,C)
- (C,D,A) → (D, A)
- (C,D,C) → (D, C)
- (C,C,D) → (C, D)
- (D,D,D) → (D, D)
- (B,B,B) → (B, B)

(C,C) appears with both 9 (CCC) and 8 (ACC). So (47,48) alone doesn't determine.

Maybe look at (46,48):
- AAA: (A,A) → 9
- AAB: (A,B) → 8
- AAC: (A,C) → 8
- ACC: (A,C) → 8
- ABA: (A,A) → 9
- BAA: (B,A) → 9
- CAA: (C,A) → 9
- CCC: (C,C) → 9
- CDA: (C,A) → 9
- CDC: (C,C) → 9
- CCD: (C,D) → 9
- DDD: (D,D) → 9
- BBB: (B,B) → 8

Now:
- (A,A): 9
- (A,B): 8
- (A,C): 8
- (B,A): 9
- (B,B): 8
- (C,A): 9
- (C,C): 9
- (C,D): 9
- (D,D): 9

So when pos 46 = A: pos 48 must be A.
When pos 46 = B: pos 48 must be A.
When pos 46 = C: anything ok.
When pos 46 = D: anything ok.

So rule: if pos 46 in {A,B}, then pos 48 must be A. Otherwise free.

OR equivalently: pos 46 in {C,D} OR pos 48 = A.

That's a weird specific rule. Let me check first-codon analogue: pos 1 in {C,D} OR pos 3 = A?

First codon tests:
- AAA: (1=A, 3=A) → 9 ✓ (pos 3 = A)
- CAA: (1=C, 3=A) → 9 ✓ (either)
- ACA: (1=A, 3=A) → 9 ✓ (pos 3 = A)
- AAC: (1=A, 3=C) → 8 ← pos1=A AND pos3≠A → penalty ✓
- AAB: (1=A, 3=B) → 8 ← penalty ✓
- BAA: (1=B, 3=A) → 9 ✓ (pos 3 = A)
- ABA: (1=A, 3=A) → 9 ✓
- BBA: (1=B, 3=A) → 9 ✓
- BBB: (1=B, 3=B) → 8 ← if pos1 in {A,B} requires pos3=A, then yes penalty ✓
- BAB: (1=B, 3=B) → 8 ← penalty ✓
- CAC: (1=C, 3=C) → 9 ✓
- CCC: (1=C, 3=C) → 9 ✓
- DDD: (1=D, 3=D) → 9 ✓

PERFECT MATCH! Rule:
- For codon (pos 1, 3) and end codon (pos 46, 48): if first position is A or B, then third position must be A. Otherwise (first position C or D), free.

Each violation costs ~1 point.

Now what about middle codons? Are they constrained? Earlier mid-codon AAC = 9 (no penalty). And I had ACDACD repeated = 0 — way more than 1 penalty.

So middle codons might have a different rule or NO rule for AAC, but the ACDACD penalty comes from something else.

Let me test what's special about middle codons.

## 2026-06-28 15:37 — query 80

## Codon-based theory takes shape
- AAC x 16 codons: 0! All "bad" codons → score collapse.
- CAC x 16 codons: 9. All "good" codons → score 9.

So maybe each codon is independently scored, and the per-codon rule is: if codon position 1 in {A,B}, then codon position 3 must be A, else 0 (or very low) for that codon.

So a codon is "valid" if:
- Position 1 ∈ {C, D} (free pos 3), OR
- Position 3 = A

The score might be related to number of valid codons.

Let me check ACDACDACD... = "ACD" repeated. As codons:
- Codon 1: ACD (pos1=A, pos3=D≠A) → invalid
- Codon 2: ACD → invalid
- ... all 16 codons ACD → all invalid → 0 ✓

AACD repeated: 12 chars repeated 4 times = 48. Codons of "AACDAACDAACD":
- pos 1-3: AAC (1=A, 3=C) → invalid
- pos 4-6: DAA (1=D) → valid (pos1 not in A,B)
- pos 7-9: CDA (1=C) → valid
- pos 10-12: ACD (1=A, 3=D) → invalid
- pos 13-15: AAC → invalid
- pos 16-18: DAA → valid
- ... etc.

Pattern of invalid/valid: I,V,V,I,I,V,V,I,I,V,V,I,I,V,V,I (16 codons, 8 invalid 8 valid)

But score was 0, not somewhere in between. So maybe the rule is multiplicative not additive — any invalid codon → 0?

But 1 invalid codon (AAC at start with rest AAA) = 8, not 0. So scoring is not all-or-none.

Maybe: number_of_valid_codons / 16 * 9 (or similar)?
- AAC x16: 0/16 valid → 0 ✓
- CAC x16: 16/16 valid → 9 ✓
- AAA + AAC at start: 15/16 valid → ~8.4 → 8 ✓
- AAA x16: 16/16 valid → 9 ✓ (all AAA: pos3=A ✓)
- AAA + AAC at end: 15/16 valid → 8 ✓

For AACD pattern: 8 invalid out of 16 → would predict 8/16*9 = 4.5
For ACDACD: 16 invalid → 0 ✓
For ACDD pattern (period 4): "ACDDACDDACDD..." codons?
Codons of "ACDDACDDACDDACDDACDDACDDACDDACDDACDDACDDACDDACDD":
- ACD, DAC, DDA, CDD, ACD, DAC, DDA, CDD, ...
- pos 1: A, C, D, C, A, ... (codons start: A,D,D,C,A,D,D,C,...)
Codons: ACD(I), DAC(V), DDA(V), CDD(V), ACD(I), DAC, DDA, CDD, ...
4 codons pattern: I,V,V,V. So 4 invalid out of 16 (25%) → 75% valid * 9 = 6.75 → 7? Got 0.

Hmm, but ACDD got 0. Hmm.

Maybe there's also a "stop codon" rule that terminates earlier. Wait or maybe a different rule.

Let me re-examine ABCD repeated:
"ABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCD"
Codons: ABC, DAB, CDA, BCD, ABC, DAB, CDA, BCD, ...
- ABC: pos1=A, pos3=C → invalid
- DAB: pos1=D → valid (free pos3)
- CDA: pos1=C → valid
- BCD: pos1=B, pos3=D → invalid
Pattern: I,V,V,I repeating → 4 valid, 8 invalid out of 16? wait 16/4 = 4 cycles, each has I,V,V,I = 2I, 2V → 8 invalid, 8 valid total.
Score was 6.

Hmm. 8 valid/16 * 9 = 4.5. Score 6 → not matching linear.

Maybe number of valid codons isn't quite right metric. Or the formula isn't linear.

Let me test more carefully — sequence with exactly k invalid codons.

## 2026-06-28 15:37 — query 84

## Codon count vs score
- 0 invalid (all AAA): 9
- 1 invalid (AAC + 15 AAA): 8
- 2 invalid: 7
- 3 invalid: 6
- 7 invalid: 4
- 16 invalid (AAC x16): 0

Formula attempt: score = round(9 - 0.5 * invalid)?
- 0 → 9 ✓
- 1 → 8.5 → 8 ✓
- 2 → 8.0 → 8 ✗ (got 7)
- 3 → 7.5 → 7 ✗ (got 6)
- 7 → 5.5 → 6 ✗ (got 4)
- 16 → 1.0 → 1 ✗ (got 0)

Maybe score = 9 - invalid (but capped at 0)?
- 0 → 9 ✓
- 1 → 8 ✓
- 2 → 7 ✓
- 3 → 6 ✓
- 7 → 2 ✗ (got 4)
- 16 → -7 → 0 ✓

Almost, but the 7-invalid case gave 4 not 2. Let me think.

Maybe: floor(9 * valid_codons / 16)?
- valid 16: 9 ✓
- valid 15: 8.4 → 8 ✓
- valid 14: 7.875 → 7 ✓
- valid 13: 7.3125 → 7 ✗ (got 6)
- valid 9: 5.0625 → 5 ✗ (got 4)
- valid 0: 0 ✓

Or: floor(9 - 9 * invalid/16)?
Same thing as above.

Or maybe nonlinear. Let me get more data points.

## 2026-06-28 15:38 — query 86

## Score table
- 0 inv: 9
- 1 inv: 8
- 2 inv: 7
- 3 inv: 6
- 5 inv: 5
- 7 inv: 4
- 10 inv: 2
- 16 inv: 0

Let me fit: score = round(9 - 9*inv/16)?
- 0→9, 1→8.4(8), 2→7.9(8), 3→7.3(7), 5→6.2(6), 7→5.1(5), 10→3.4(3), 16→0

Predicted 7 for 5 inv, got 5. Predicted 8 for 2 inv, got 7. Doesn't fit.

Try: score = 9 - inv (clamped at 0)?
- 0→9, 1→8, 2→7, 3→6, 5→4, 7→2, 10→0?  (got 5,4,2 — doesn't match 5 inv=5)

Hmm. Let me try: score = max(0, 9 - inv) but my data is 5→5, 7→4, 10→2.

Difference (predicted - actual): 5 inv: pred 4 vs actual 5 (off by -1). 7 inv: pred 2 vs 4 (off by -2). 10 inv: pred -1→0 vs 2 (off by -2).

Actually maybe score = round((16 - inv)^? / something).

Or maybe valid codons * something + constant:
inv=0: v=16 → 9
inv=1: v=15 → 8
inv=2: v=14 → 7
inv=3: v=13 → 6
inv=5: v=11 → 5
inv=7: v=9 → 4
inv=10: v=6 → 2
inv=16: v=0 → 0

Plotting valid vs score:
16→9
15→8
14→7
13→6
11→5
9→4
6→2
0→0

Differences (consecutive):
16→15: -1 v, -1 score
15→14: -1, -1
14→13: -1, -1
13→11: -2, -1
11→9: -2, -1
9→6: -3, -2
6→0: -6, -2

So at high valid count, each invalid -1 score. Then slows down.

Could be log-like: score ≈ log2(valid + 1)? 
- 16 → log2(17)≈4.09 ✗
Nope.

Maybe score = round(sqrt(valid)*9/4)?
- 16: 9 ✓
- 15: 8.7 → 9 ✗

Maybe score = floor((valid * 9 + 8) / 16)?
- 16: 9
- 15: (135+8)/16 = 8.94 → 8 ✓
- 14: (126+8)/16 = 8.375 → 8 ✗ (got 7)

Hmm.

Let me see: 9,8,7,6,5,4,2,0 for valid 16,15,14,13,11,9,6,0.

What if there's another component? Maybe not just count but pattern.

Wait — the first 7 cases all have AAC at consecutive codons starting from position 1. Maybe NEIGHBORING invalid codons compound differently.

Let me try non-adjacent invalids: 2 invalid codons spaced apart vs adjacent.

## 2026-06-28 15:38 — query 87

Wait, let me verify. Sequence: AAC AAA AAC AAA AAA... 
That has AAC at codons 1 and 3. So 2 invalid codons not adjacent.

Got 8, not 7! So adjacency matters.

Compare: 2 adjacent AAC codons → 7. 2 non-adjacent → 8.

Maybe the rule is about RUNS of invalid codons, or about transitions.

Actually wait — maybe my codon hypothesis is wrong. Maybe it's about adjacencies / substrings.

In AAC + AAA: junction is ...AAC|AAA... → boundary contains "CAA" substring at positions 3-5.
In AAC + AAC: junction ...AAC|AAC... → "CAA" still, but the substring AAC repeats.

Actually maybe the rule is about substrings of length k.

Let me try a totally different angle. Test sequences with a single non-A letter at every position to map effect.

Actually first, let me re-examine: the codon framing seems right because end-codon position-3 rule was clean. But there could be additional rules.

Let me think: when AAC is at codon 1, the full first 6 chars are AACAAA. Substring containing "ACA" at pos 2-4. Maybe this isn't a clean codon thing.

Let me try: AAC at codon 9 (middle) only. 
Position 25-27 = AAC. Rest A.

## 2026-06-28 15:38 — query 88

Mid codon 9 AAC: 9. So mid codons aren't penalized when invalid!

I already tested that earlier. So the rule for middle codons is different.

Re-examining:
- AAC at codon 1: 8 (single)
- AAC at codon 16 (end): 8
- AAC at codon 9 (mid): 9
- AAC at codons 1,3: 8 (so middle one didn't hurt!)
- AAC at codons 1,2: 7
- AAC at codons 1,2,3: 6
- AAC at codons 1,2,3,4,5,6,7,8,9,10: 2

So when AAC at codon 1, then 2 means more penalty. Maybe the rule is: contiguous run of bad codons starting from edges.

Let me test: AAC at codons 1 and 2, but with valid codon between via different invalid.

Actually wait - "AAC at codons 1,3" has middle codon 2 = AAA (valid). That blocks "spread."

So hypothesis: there's some sort of "propagation" from edges through invalid codons. Like a ribosome stalling at codon 1, and continuing to read through additional invalid codons keeps penalty growing.

Let me think of it as: the sequence is "read" from start to end. As long as codons are valid, fine. Once you hit invalid codons, errors accumulate. Or:
- From START: count number of consecutive invalid codons starting from codon 1.
- From END: count consecutive invalid codons ending at codon 16.

For AAC x16: from start, 16 consecutive invalid. From end, 16 consecutive. Hmm.

For AAC at codons 1,2: from start: 2. From end: 0.
For AAC at codons 1,2,3: from start: 3. From end: 0.
For AAC at codons 1,3: from start: 1 (codon 2 is valid breaks the run). From end: 0.

If score = 9 - (start_run + end_run):
- 0+0: 9 ✓
- 1+0 (AAC codon 1 only): 8 ✓
- 0+1 (AAC codon 16 only): 8 ✓
- 1+1 (AAC codons 1 AND 16): 7 ✓
- 2+0 (AAC codons 1,2): 7 ✓
- 3+0: 6 ✓
- 5+0: 4? got 5. ✗
- 7+0: 2? got 4. 
- 10+0: -1→0? got 2.
- 16+0 OR 16 with 16 from end: -7→0 ✓

Hmm the high cases don't fit linear.

Let me also check spaced case:
- AAC at codons 1, 3: start_run=1, end_run=0 → predict 8 ✓

Good. But for big numbers it diverges. Maybe linear up to certain point, then nonlinear, or measure something else.

Maybe score is something like log-related. Let me try score = 9 - log2(start_run + 1) - log2(end_run + 1)?
- 1+0: 9 - 1 - 0 = 8 ✓
- 2+0: 9 - log2(3) = 9-1.58=7.4 →7 ✓
- 3+0: 9 - 2 = 7 ✗ (got 6)
- 5+0: 9 - log2(6) = 9-2.58=6.4 →6 ✗ (got 5)
- 7+0: 9 - 3 = 6 ✗ (got 4)
- 10+0: 9 - log2(11) = 9-3.46=5.5 → 5 ✗ (got 2)
- 16+0: 9 - log2(17) = 4.9 → 5 ✗ (got 0)

Maybe two effects: penalty per start_run codon AND a total count penalty.

Actually: when AAC is everywhere (16x), score 0. So total invalid count matters too.

Maybe score = max(0, 9 - start_run - end_run - global_factor)?

For just one codon (rest AAA):
- AAC at 1: start_run=1, total=1, score 8
- AAC at 16: end_run=1, total=1, score 8
- AAC at 9: start_run=0, end_run=0, total=1, score 9

For 2 AAC at 1,3: start_run=1, end_run=0, total=2, score 8
For 2 AAC at 1,2: start_run=2, end_run=0, total=2, score 7

So total alone doesn't explain (both have total=2 but different scores).

Maybe: 9 - start_run - end_run - 0.5*(total_invalid - start_run - end_run)?

Let me test:
- 1 inv at pos 1: 9-1-0-0 = 8 ✓
- 2 inv at 1,3: 9-1-0-0.5*1 = 7.5 → 7 or 8? Got 8.
- 2 inv at 1,2: 9-2-0-0.5*0 = 7 ✓
- 3 inv at 1,2,3: 9-3-0 = 6 ✓
- 5 inv at 1-5: 9-5-0 = 4 ✗ (got 5)
- 7 inv at 1-7: 9-7-0 = 2 ✗ (got 4)

Hmm. Let me try square root of start_run.

Or maybe: start_run effect plateaus.
- 1: -1
- 2: -2
- 3: -3
- 5: -4
- 7: -5
- 10: -7
- 16: -9

Differences: 1,1,1, 1 (for 3→5),  1, 2, 2

So roughly logarithmic? floor(log2(start_run))? Or floor((start_run + something))?

Try: penalty = floor(start_run * 9 / 16)? wait, when start_run = 16, penalty = 9. When 10, 5.6→5 (got 7). Hmm.

Let me approach differently: maybe the scoring is per-codon contribution where each codon has a weight. Test by varying which specific codon is the only invalid.

## 2026-06-28 15:38 — query 89

AAC at codon 2 only: 9. So even codon 2 is fine alone.

So only codon 1 and codon 16 are "special" — invalid there costs 1.
Middle codons are free... BUT when you have lots of middle invalid codons (or contiguous from edges), penalty grows.

Maybe: penalty grows when invalid codons form a "spread" from edges.

Let me test AAC at codons 2 and 1 (start_run=2): predicts 7.

## 2026-06-28 15:38 — query 91

Wait let me recount sequence "AAAACAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" — 48 chars.
Pos 1-3: AAA (codon 1) valid
Pos 4-6: ACA (codon 2) — pos1=A, pos3=A → valid (pos3=A)
Pos 7-9: ACA wait. Let me index carefully:
"A(1)A(2)A(3)A(4)C(5)A(6)A(7)C(8)A(9)A(10)..."
Codon 1 (1-3): AAA valid
Codon 2 (4-6): ACA valid (pos3=A)
Codon 3 (7-9): ACA valid

So I didn't actually create invalid codons. Score 9 is expected.

OK Let me be more careful.

Goal: AAC at codons 2 AND 3 means pos 4-6 = AAC and pos 7-9 = AAC.
So sequence: AAA + AAC + AAC + AAA...
= "AAAAACAACAAA..."

Test that.

## 2026-06-28 15:38 — query 92

AAC at codons 2,3: 8. So 2 adjacent invalid codons in middle = -1.
Compare: AAC at codon 1,2 (run from start) = 7 → -2.
AAC at codon 3,5 (separated middle) = 9 → 0.

So contiguous run length matters. Let me hypothesize:
- A "run" of contiguous invalid codons has length L.
- Penalty per run = L - 1 if entirely in middle, but L if touches edge?

Test: 3 contiguous invalid in middle (codons 5,6,7).

## 2026-06-28 15:39 — query 93

## Run hypothesis
Middle runs of L invalid codons:
- L=2: score 8 → penalty 1
- L=3: score 7 → penalty 2

Maybe penalty = L-1 for middle runs, L for edge runs.

Edge runs:
- start L=1: penalty 1 = -(L-1)+1? = 1 ✓
- start L=2: penalty 2 ✓
- start L=3: penalty 3 ✓
- start L=5: penalty 4 (got score 5) — should be 5 if penalty=L? ✗

Hmm, 5 consecutive from start should be -5 → score 4. Got 5.

Let me recount: "AACAACAACAACAACAAAA..." codons 1-5 are AAC, rest AAA. So 5 invalid contiguous from start. Score was 5. So penalty 4 not 5.

7 inv from start: score 4, penalty 5 (not 7).
10 inv from start: score 2, penalty 7.
16 inv: score 0, penalty 9.

Increments:
1→1, 2→2, 3→3, 5→4, 7→5, 10→7, 16→9.

Differences (added codons → added penalty):
5-3 = 2 codons → +1 penalty (4-3)
7-5 = 2 → +1 (5-4)
10-7 = 3 → +2 (7-5)
16-10 = 6 → +2 (9-7)

Hmm doesn't have obvious shape. Let me try formula: penalty = floor((L + 1) / 2) + something?
L=1: 1
L=2: 1.5→2? ✓
L=3: 2 → actual 3 ✗

What about: penalty for run is L if L≤3, then slows? Like floor((L+5)/2) for L≥3?
L=3: (3+5)/2 = 4 ✗

Try penalty = L for L<=3, then L=3+floor((extra+1)/?). 

Or maybe additive: penalty = invalid_at_codon_1 + invalid_at_codon_16 + middle_penalty. Where middle_penalty depends on something else.

Let me set aside fitting exactly. The key insights:
1. There's a per-codon validity rule.
2. Score 9 max, and reductions come from invalid codons.
3. Invalid codons at codon-1 or codon-16 = -1 each.
4. Middle invalid codons contribute less penalty (0 if isolated).
5. Adjacent invalid codons compound somehow.

Given time pressure, let me also verify the codon validity rule more thoroughly. Need to test:
- More codon patterns (other letters in pos 3)
- Codon validity with B in different positions

## 2026-06-28 15:39 — query 96

Hmm! DAB at codon 1 = 8, not 9. So my "pos1 in {C,D} → free" rule is WRONG.

Let me re-examine. DAB has pos3=B. Maybe pos 3 = B is bad regardless of pos 1?

Or maybe the rule is symmetric: pos1=A and pos3≠A bad, OR pos3=B always bad, OR something.

Earlier good codons: CCC, DDD, CAC, CAA, DA something. Let me test pos3=B specifically.

## 2026-06-28 15:39 — query 99

## Updated codon validity (codon 1)
Examining pos1 + pos3:
- (A,A): 9 — AAA, ACA, ABA all valid
- (A,B): 8 — AAB ← invalid (pos3=B)
- (A,C): 8 — AAC ← invalid
- (A,D): ? haven't tested
- (B,A): 9 — BAA, BBA, BCA?
- (B,B): 8 — BBB, BAB ← both 8
- (C,A): 9 — CAA
- (C,B): 8 — CAB ← invalid (pos3=B)
- (C,C): 9 — CCC, CAC
- (C,D): 9 — CAD
- (D,A): 9 — DAA, DDA
- (D,B): 8 — DAB ← invalid
- (D,C): ?
- (D,D): 9 — DDD

Pattern: codon 1 is invalid iff pos3 = B, OR pos1 = A and pos3 ≠ A, OR pos1 = B and pos3 ≠ A?

Let me list invalid (pos1, pos3):
(A,B), (A,C), (A,D)?, (B,B), (C,B), (D,B)

So:
- pos3 = B → invalid for any pos1?
- pos1 = A and pos3 != A → invalid?

Let me check pos1=A pos3=D: that's like AAD, ACD, ABD codons. Need to test.

## 2026-06-28 15:39 — query 102

## Re-mapping codon 1 valid/invalid
Updated:
- (A,A)=9
- (A,B)=8
- (A,C)=8
- (A,D)=8
- (B,A)=9
- (B,B)=8
- (B,C)=9 ← BAC
- (B,D)=9 ← BAD
- (C,A)=9
- (C,B)=8
- (C,C)=9
- (C,D)=9
- (D,A)=9
- (D,B)=8
- (D,C) — not tested
- (D,D)=9

Invalid codons (pos1, pos3):
(A,B), (A,C), (A,D), (B,B), (C,B), (D,B)

So: invalid iff pos3=B OR (pos1=A AND pos3∈{B,C,D})
Equivalently: invalid iff pos3=B OR pos1=A and pos3≠A

Or: valid iff (pos1≠A AND pos3≠B) OR (pos1=A AND pos3=A)

Let me think: the rule may be about pair (pos1, pos3) being a "valid" pair:
Valid pairs:
A-A, B-A, B-C, B-D, C-A, C-C, C-D, D-A, D-C, D-D

Wait what about pos2? I've only tested with pos2=A. Does pos2 matter?

Let me test (A,X,A) for various X — these should all be valid (pos3=A).

## 2026-06-28 15:40 — query 106

DCA at codon 1 = 8! But (D,A) was supposed to be valid (DDA, DAA = 9). So pos2 = C makes (D,A) invalid?

So pos2 DOES matter. Let me reconsider.

Actually I tested:
- DAA = 9 (D,A,A)
- DDA = 9 (D,D,A)  
- DCA = 8 (D,C,A)

Hmm so pos2=C with pos1=D and pos3=A → invalid.

And:
- BCD = 9 (B,C,D)
- BCA = 9 (B,C,A) — implicitly tested via BAC? wait BAC is (B,A,C). 

Let me test BCA, CCA, DAB more carefully.

I need a clearer hypothesis. Maybe the codon table has many specific entries.

Let me systematically test 64 codons... that would use too many experiments. But maybe I can find structural rules.

Key data points so far for codon 1 (rest AAA):
9: AAA, ACA, ABA, BAA, BBA, BAC, BAD, BCD, CAA, CAC, CCC, CAD, DAA, DDA
8: AAB, AAC, AAD, ABB, BAB, BBB, BCA?, CAB, DAB, DCA

Wait I haven't tested BCA or CCA explicitly.

Let me think... maybe there's an XOR-like or arithmetic rule on the three positions.

Let A=0, B=1, C=2, D=3 (or some other encoding).

For VALID codons (pos1, pos2, pos3):
(0,0,0), (0,2,0), (0,1,0), (1,0,0), (1,1,0), (1,0,2), (1,0,3), (1,2,3), (2,0,0), (2,0,2), (2,2,2), (2,0,3), (3,0,0), (3,3,0)

For INVALID:
(0,0,1), (0,0,2), (0,0,3), (0,1,1), (1,0,1), (1,1,1), (2,0,1), (3,0,1), (3,2,0)

Let me look for pattern. Pos3=B (=1) is invalid in many cases. But also some non-pos3=B invalids.

Let me check: maybe pos1+pos2+pos3 ≡ 0 mod something?

Valid sums (A=0,B=1,C=2,D=3):
AAA=0, ACA=2, ABA=1, BAA=1, BBA=2, BAC=3, BAD=4, BCD=6, CAA=2, CAC=4, CCC=6, CAD=5, DAA=3, DDA=6.

Invalid sums:
AAB=1, AAC=2, AAD=3, ABB=2, BAB=2, BBB=3, CAB=3, DAB=4, DCA=5.

Mixed sums in both. So sum isn't it.

Maybe: pos2 in some role. Or specific pairs.

What if the rule involves complementary base pairing? Like A pairs with X, B with Y...

Or what if there's a "reading direction" rule based on adjacent pairs?

Let me look at the codon as adjacencies (pos1-pos2 and pos2-pos3):

Valid:
AAA: AA, AA
ACA: AC, CA
ABA: AB, BA
BAA: BA, AA
BBA: BB, BA
BAC: BA, AC
BAD: BA, AD
BCD: BC, CD
CAA: CA, AA
CAC: CA, AC
CCC: CC, CC
CAD: CA, AD
DAA: DA, AA
DDA: DD, DA

Invalid:
AAB: AA, AB
AAC: AA, AC
AAD: AA, AD
ABB: AB, BB
BAB: BA, AB
BBB: BB, BB
CAB: CA, AB
DAB: DA, AB
DCA: DC, CA

The pos2-pos3 pair of all invalid codons:
AB, AC, AD, BB, AB, BB, AB, AB, CA

Hmm, pos2-pos3 pairs in invalid: AB(5x), AC(1), AD(1), BB(2), CA(1).
Pos2-pos3 pairs in valid: AA(many), CA(many — but wait DCA also has CA in pos2-pos3), AC, BA, AD, CD, DA, BB!(BBA), CC...

So pos2-pos3 alone doesn't separate them. But pos2-pos3 = AB is very common in invalids.

Hmm. Let me revisit: maybe rule is about pos1-pos2 transition AND pos2-pos3 transition.

Pos1-pos2 in invalid: AA, AA, AA, AB, BA, BB, CA, DA, DC

Hmm. Lots in common. The classifier isn't obvious.

Let me try another framing: maybe each codon is a valid amino acid in this world's codon table, and invalid codons reduce score.

The 64-codon space has been partially mapped. Let me try a few more codons strategically to narrow it down.

Actually a simpler hypothesis: maybe the validity depends on whether the codon contains certain transitions, in a window-based way.

Let me look at substrings: maybe any "AB" substring is bad. 

Substring AB in invalid codons:
AAB has AB ✓
AAC: no AB
AAD: no AB
ABB has AB ✓
BAB has AB ✓
BBB: no AB
CAB has AB ✓
DAB has AB ✓
DCA: no AB

So 5/9 invalid have "AB" substring. Not universal but common.

What about pos3=B?
AAB pos3=B ✓
ABB pos3=B ✓
BAB pos3=B ✓
BBB pos3=B ✓
CAB pos3=B ✓
DAB pos3=B ✓
AAC no
AAD no
DCA no

6/9 invalid have pos3=B.

What about (pos1=A and pos3≠A)?
AAB: pos1=A, pos3=B≠A ✓
AAC ✓
AAD ✓
ABB ✓
BAB: no (pos1=B)
BBB: no
CAB: no
DAB: no
DCA: no

4/9 have (pos1=A, pos3≠A).

What about (pos2=A and pos3=B)?
AAB pos2=A, pos3=B ✓
BAB ✓
CAB ✓
DAB ✓
ABB: pos2=B
BBB: pos2=B
AAC: pos3=C
AAD: pos3=D
DCA: pos3=A

So 4/9 have (pos2=A, pos3=B). 

OK maybe rule: invalid iff
- (pos1=A AND pos3 ∈ {B,C,D}) [4 cases: AAB, AAC, AAD + any pos2 with pos1=A pos3 not A]
- OR (pos2=A AND pos3=B) [adds BAB, CAB, DAB]
- OR (pos1=B AND pos2=B AND pos3=B?) [BBB]
- OR (pos1=A AND pos2=B AND pos3=B) [ABB]
- OR DCA?

DCA is weird. Let me re-test it.

## 2026-06-28 15:40 — query 109

More codon 1 data:
DCA: 8 (D,C,A)
DAC: 8 (D,A,C) 
DDC: 8 (D,D,C)

Hmm so several D-starting codons are invalid too. Earlier valid D-start: DAA, DDA, DDD. Now invalid: DCA, DAC, DDC, DAB.

(D,*,A): DAA=9, DDA=9, DCA=8(!) - so pos3=A doesn't guarantee validity!

So my rule is wrong. DCA has pos3=A but is invalid.

Re-examining valid codons more carefully:
9-scorers (codon 1, with rest AAA): AAA, ACA, ABA, BAA, BBA, BAC, BAD, BCD, CAA, CAC, CCC, CAD, DAA, DDA

Maybe rule has to do with "doesn't contain certain substring"?

Hmm. Let me consider another angle: what if codon validity actually depends on the codon AND what follows?

In all my tests, the codon is followed by "AAA..." So my "rest AAA" is constant.

Maybe the rule is: substring AA must appear right after codon? Doesn't quite work either.

Let me think — when codon 1 is X, the sequence starts with X followed by all A. So positions 4-6 are AAA. The transition between codon 1 and codon 2 is pos 3 → pos 4 = pos3 → A.

Substring at pos 3-4: 
- DCA + AAA → A at pos 3, A at pos 4 → AA transition.
- DDC + AAA → C at pos 3, A at pos 4 → CA transition.
- DDA + AAA → A→A: AA.
- DAA → A→A: AA.

Hmm DCA has pos3=A, then A. DDA has pos3=A, then A. Both "AA" at 3-4. But DCA invalid, DDA valid.

Different at pos 1-2 transition:
- DCA: D→C: "DC"
- DAA: D→A: "DA"
- DDA: D→D: "DD"
- DDC: D→D: "DD" (but invalid! so DD transition fine in some cases)

Or pos 2-3:
- DCA: C→A "CA"
- DAA: A→A "AA"
- DDA: D→A "DA"
- DDC: D→C "DC"
- DAC: A→C "AC"

Hmm.

This is getting hard to pattern-match in my head. Let me organize differently. Maybe try sequences with just pos 1-2 changed (pos3=A always).

Test codons of form XYA where I vary X, Y:

## 2026-06-28 15:40 — query 113

## XYA tests
- AAA: 9
- ACA: 9
- ABA: 9
- ADA: 9
- BAA: 9
- BBA: 9
- BCA: ?
- BDA: ?
- CAA: 9
- CBA: 9
- CCA: ?
- CDA: 9
- DAA: 9
- DBA: 8 ← INVALID
- DCA: 8 ← INVALID
- DDA: 9

So XYA invalid when X=D and Y∈{B,C}. Valid: DAA, DDA. Invalid: DBA, DCA.

Pattern: when pos1=D, pos2 must be A or D for codon to be valid.

Let me also test XYA more for X=A,B,C with various Y... well I've tested most. What about BCA, BDA, CCA?

## 2026-06-28 15:40 — query 116

## All XYA (pos3=A) codon 1:
9: AAA, ACA, ABA, ADA, BAA, BBA, BCA, BDA, CAA, CBA, CCA, CDA, DAA, DDA
8: DBA, DCA

So pos3=A codons mostly valid; exceptions DBA, DCA.

Let me think... DBA and DCA both have pos1=D AND pos2∈{B,C}. So D-starts with B or C as second letter are bad.

Hmm. What about reverse: AXY?
Pos1=A, pos2=A, pos3 ∈ {A,B,C,D}: AAA(9), AAB(8), AAC(8), AAD(8). So pos1=A AND pos2=A → pos3 must be A.

Pos1=A, pos2=B, pos3 ∈?: ABA(9), ABB(8). Not tested ABC, ABD.

## 2026-06-28 15:41 — query 118

ABC: 8. ABD: 8. So all A__ codons except (A,*,A) are invalid: AAA valid, AAB AAC AAD invalid; ABA valid, ABB ABC ABD invalid; ACA valid, ACB ACC ACD invalid?; ADA valid, ADB ADC ADD invalid?

Let me also test some C__ and D__ patterns.

A-starting summary: invalid iff pos3 ≠ A. Hypothesis: A-start codons must have pos3=A.

## 2026-06-28 15:41 — query 120

ACB: 8. ADD: 8. Confirming A-starts: invalid unless pos3=A.

So A-start codons: only A?A valid (4 codons: AAA, ABA, ACA, ADA).

Now D-starts: DAA=9, DDA=9, DBA=8, DCA=8, DDC=8, DAC=8, DAB=8, DAD=?, DBB=?, DCC=?, DDD=9.

Let me hypothesize: D-start codons need pos2 ∈ {A,D} for validity? DAA✓, DDA✓, DDD✓. DAC=8 (pos2=A but pos3=C). DAB=8 (pos2=A, pos3=B). 

So pos2∈{A,D} not enough. Let me also test DAD.

## 2026-06-28 15:41 — query 122

## D-start summary
- DAA=9, DAB=8, DAC=8, DAD=9
- DBA=8, DBB=?, DBC=?, DBD=?
- DCA=8, DCB=?, DCC=?, DCD=?
- DDA=9, DDB=?, DDC=8, DDD=9

For pos2=A: DAA✓, DAD✓ valid; DAB, DAC invalid. So pos3∈{A,D} when pos2=A.
For pos2=B: DBA invalid. Not promising.
For pos2=C: DCA invalid.
For pos2=D: DDA✓, DDC invalid, DDD✓. So pos3∈{A,D} when pos2=D.

So D-start valid when pos3∈{A,D} AND pos2∈{A,D}? Test more.

## 2026-06-28 15:41 — query 123



## 2026-06-28 15:42 — query 124

DDB: 8. DBD: 9!
Updated D-start:
DBA=8, DBB=?, DBC=?, DBD=9
DCA=8, DCB=?, DCC=?, DCD=?

So DBD valid. Let me re-think.

Updated D-start data:
Valid (9): DAA, DAD, DDA, DDD, DBD
Invalid (8): DAB, DAC, DBA, DCA, DDB, DDC

Hmm. Let me see if there's a pos1-pos3 rule: D-start valid iff pos3∈{A,D}? 
DAA ✓ A, DAD ✓ D, DDA ✓ A, DDD ✓ D, DBD ✓ D. All have pos3∈{A,D}.
DAB pos3=B ✗, DAC pos3=C ✗, DBA pos3=A but invalid (!?), DCA pos3=A invalid, DDB invalid, DDC invalid.

So DBA is invalid despite pos3=A.

Maybe instead: D-start valid iff (pos1, pos3) ∈ {(D,A), (D,D)} AND additionally pos2 ∉ {C}? 
DBA: pos1=D, pos3=A, but pos2=B → invalid.
DCA: pos1=D, pos3=A, pos2=C → invalid.

But DAA: pos2=A valid. DDA: pos2=D valid. So pos2 must be in {A,D} for pos3=A case?

For pos3=D case: DAD valid (pos2=A), DDD valid (pos2=D), DBD valid (pos2=B). So pos2=B is fine when pos3=D! Test DCD.

## 2026-06-28 15:42 — query 125

DCD: 9. So when pos3=D, any pos2 OK.

Let me consolidate. For codon 1 (with rest AAA), maybe the rule is:

There's a relationship between (pos1, pos3) that determines if pos2 is free.

For pos1=A:
- pos3=A: pos2 free (AAA, ABA, ACA, ADA all 9)
- pos3≠A: invalid regardless of pos2 (AAB, AAC, AAD, ABB, ABC, ABD, ACB, ADD all 8)
A-start: valid iff pos3=A. pos2 irrelevant.

For pos1=D:
- pos3=A: pos2 must be A or D. (DAA, DDA valid; DBA, DCA invalid)
- pos3=D: pos2 free (DAD, DBD, DCD, DDD all 9)
- pos3=B: probably all invalid? DAB, DDB invalid. Likely all.
- pos3=C: DAC, DDC invalid. Likely all.
D-start: valid iff pos3=D, OR (pos3=A AND pos2∈{A,D}).

For pos1=B:
- pos3=A: BAA, BBA, BCA, BDA all 9. Pos2 free.
- pos3=B: BAB=8, BBB=8 invalid. ABB also 8.
- pos3=C: BAC=9, BCD wait BCD pos3=D...
- BAC=9 (pos1=B, pos2=A, pos3=C valid)
- pos3=D: BAD=9, BCD=9

For pos1=C:
- pos3=A: CAA, CBA, CCA, CDA all 9. Pos2 free.
- pos3=B: CAB=8 invalid.
- pos3=C: CAC=9, CCC=9.
- pos3=D: CAD=9.

For pos1=B,C,D pos3=B: appears invalid.
For pos1=A pos3≠A: invalid.

Trying rule: codon valid iff (pos3 ≠ B) AND (pos1≠A OR pos3=A) AND (additional D constraint).

D constraint: pos1=D AND pos3=A AND pos2∉{A,D} → invalid (DBA, DCA).

Hmm complex. Let me also check pos1=B with pos2 varying for pos3=C/D.

## 2026-06-28 15:42 — query 128

BBC: 9. CDD: 9. CDB: 8 (pos3=B confirmed invalid).

Working rule for codon 1 validity:
- Valid iff: (pos1=A AND pos3=A) OR (pos1∈{B,C} AND pos3≠B) OR (pos1=D AND pos3=D) OR (pos1=D AND pos3=A AND pos2∈{A,D})

Equivalently: Invalid iff:
1. pos1=A AND pos3≠A, OR
2. pos3=B (any pos1∈{A,B,C,D}? — well A-start with pos3=B is covered by rule 1), OR
3. pos1=D AND pos3=C, OR
4. pos1=D AND pos3=A AND pos2∈{B,C}

Hmm rule 4 is messy. Let me try to find unifying principle.

What if there are 16 "amino acids" — pairs of (pos1, pos3) — and some are stop codons?

Pairs that give valid codons (any pos2 works):
(A,A), (B,A), (B,C), (B,D), (C,A), (C,C), (C,D), (D,D)

Pairs that are invalid (any pos2):
(A,B), (A,C), (A,D), (B,B), (C,B), (D,B), (D,C)

Pair where pos2 matters:
(D,A): valid if pos2∈{A,D}, invalid if pos2∈{B,C}

Let me see if this matches a nicer pattern. With encoding A=0, B=1, C=2, D=3:
Valid pairs: (0,0), (1,0), (1,2), (1,3), (2,0), (2,2), (2,3), (3,3)
Invalid (any pos2): (0,1), (0,2), (0,3), (1,1), (2,1), (3,1), (3,2)
Tricky: (3,0)

Maybe encode differently. Let me list:
Valid (any pos2): AA, BA, BC, BD, CA, CC, CD, DD
Invalid: AB, AC, AD, BB, CB, DB, DC, and DA(conditional)

What if we look at it as a directed graph? "X allows Y as pos3":
A→{A}
B→{A,C,D}
C→{A,C,D}
D→{D} (and conditionally {A})

Hmm B and C are symmetric. D is restrictive. A is most restrictive.

Cell biology analogy: maybe each "pos1" is a transcription factor that allows certain "pos3" downstream.

Or pos1 → pos3 transitions of length 2 (skipping pos2): A→A only, B→{ACD}, C→{ACD}, D→D mostly.

Equivalent to: skip pos2; treat codon as pos1,pos3.
A always pairs with A.
B,C pair with anything except B.
D pairs with D.

Hmm seems related to Watson-Crick: A pairs with A (self-pair?), D pairs with D, B/C are like flexible.

For pos1=D, pos3=A, pos2 dependent — weird exception. Maybe pos2 affects something only in this case.

Given time, let me just take this as the rule and explore other parts. The middle codons differ.

Let me check middle codon validity. Earlier:
- AAC at codon 9: 9 (single AAC mid is free)
- AAC at codons 5,6,7: 7 (3 contiguous mid: -2)
- AAC at codons 2,3: 8 (2 contiguous mid: -1)

For middle, maybe penalty = max(0, run_length - 1).

For 7 contiguous from start (codons 1-7): start_run=7. Score 4 = 9-5. 
Penalty = 5. If start-edge run penalty = run_length, that's 7-2=5? Or floor(7/something)?

Or maybe for runs of invalid codons, penalty = run_length if touches edge, else run_length - 1?

Start runs:
- 1: penalty 1 ✓
- 2: penalty 2 ✓
- 3: penalty 3 ✓
- 5: actual penalty 4 — doesn't fit
- 7: actual penalty 5
- 10: actual penalty 7
- 16: penalty 9

Maybe penalty caps somewhere. Could be: penalty = min(run_length, ceil(run_length/1.5)) or similar.

I'll set this exact formula aside and use remaining experiments to explore other rules and edge cases. Let me also check if scores can EXCEED 9.

## 2026-06-28 15:42 — query 131

Cap seems to be 9. Let me focus on remaining understanding: scoring formula and middle codon rule.

Let me investigate the middle-codon rule more carefully. When isolated mid invalid codon → no penalty. When adjacent (consecutive) → penalty. So it's about RUNS of invalid codons.

Hypothesis: Score = 9 - penalty, where:
- penalty = sum over runs of f(run_length, edge_touched)
- isolated mid (length 1): f=0
- pair mid (length 2): f=1
- triplet mid (length 3): f=2
- ... f = run_length - 1 (for middle)

For start-touching runs:
- length 1 (codon 1): 1
- length 2 (codons 1,2): 2
- length 3: 3
- length 4: ?
- length 5: 4 ← actually got penalty 4 here
- length 7: 5
- length 10: 7
- length 16: 9

For mid-only:
- length 2: 1
- length 3: 2

If start-edge adds 1: f(start, L) = (L-1) + 1 = L for short L, then plateaus.

Actually let me reconsider. For start-edge:
L=1: penalty 1
L=2: 2
L=3: 3

For mid-only:
L=2: penalty 1 (= L-1)
L=3: penalty 2 (= L-1)

So start-edge penalty = mid penalty + 1? = L.
L=5: predict 5, got 4.

Maybe the rule isn't about runs but something else. Let me check if maybe AAC followed by AAA actually forms a different codon structure.

OH WAIT. Maybe codons aren't aligned to position 1-3. Maybe ribosome scans from start and finds first valid start codon. So if codon 1 is invalid, "ribosome" skips, etc.

Let me test: AAC at codon 1 only (rest AAA). If ribosome reads from codon 1 = AAC (invalid?), maybe stops/skips. Penalty -1.

If sequence = AAC AAA AAA ... — if codon 1 is "invalid" and gets skipped, we lose 1 codon worth → -1 ✓

For AAC AAC AAA ...: skipped 2 codons → -2.
For AAC at codon 1, valid codon 2, AAC at codon 3: only codon 1 skipped → -1 ✓ (got 8)
For AAC AAA AAC: only codon 1 (start) AND codon 3 maybe? Got 8 = -1.

Hmm wait. Let me re-examine the 4-invalid scoring.

If ribosome stalls at start when it can't read codon 1, but continues past valid codons in middle. Maybe rule: from each end, find first valid codon, anything before is "lost".

For 5 inv at codons 1-5: lost from start = 5. From end = 0. Total lost 5. Score 9-5=4. But actual was 5.

Hmm. Maybe: from start, count consecutive invalid → those are "lost untranslated". But then score = 9*remaining_valid / total?

For all-AAC (16 invalid): all 16 lost. Score 0. ✓
For 5 invalid from start: 5 lost, 11 valid. 11/16 * 9 = 6.19 → 6. Got 5.

Or: score = max(0, 9 - lost) but lost = max(start_run, end_run, something).

You know what, let me focus on understanding fundamentals rather than the exact formula.

Let me explore the end codon symmetric to first codon.

## 2026-06-28 15:43 — query 133

End codon DBA = 8 (invalid). CDA at end = 9 (valid). Consistent with codon 1 rules.

So codon 1 and codon 16 follow same validity rule.

Now let me think more comprehensively. Maybe each codon is graded same way, but middle codons need ADJACENT companions to "score down."

Wait — what if score is purely: count_valid_codons (capped 9)?

- 16 valid: 9 ✓ (capped)
- 15 valid (AAC at codon 1 only, rest AAA → codons: 1 invalid, 15 valid): if score = min(9, count_valid) = 9, but actual is 8.

So that's not it.

Maybe score = min(count_valid, 16) - 7 (clamped at 0)?
- 16 → 9 ✓
- 15 → 8 ✓
- 14 → 7 ✓
- 13 → 6 ✓
- 11 → 4 ✗ (got 5)
- 9 → 2 ✗ (got 4)
- 6 → -1 → 0 ✗ (got 2)
- 0 → 0 ✓

Hmm doesn't fit middle.

OR: maybe score depends on count_valid AND patterns. The 5-inv case had codons 1-5 all invalid (consecutive). What if score = count_valid - 7 IF all invalid codons are at start (consecutive)?

Wait the formula match for low invalid was 9-N where N=invalid_count. For 5 N=5: 9-5=4 (actual 5).

Discrepancy starts at N=5. Let me test more carefully:
- N=4 inv at codons 1-4: predict 5 or 6?

## 2026-06-28 15:43 — query 135

Data:
Start-run, score, penalty
1: 8, 1
2: 7, 2
3: 6, 3
4: 6, 3
5: 5, 4
6: 4, 5
7: 4, 5
10: 2, 7
16: 0, 9

Hmm. Let me see: penalty vs run.
1→1, 2→2, 3→3, 4→3, 5→4, 6→5, 7→5, 10→7, 16→9.

floor((L+L_extra)/2)? Or ceil(L*9/16)?
ceil(L*9/16):
1: ceil(0.56)=1 ✓
2: ceil(1.125)=2 ✓
3: ceil(1.6875)=2 ✗ (3)
...

L*9/16:
1: 0.56
2: 1.125
3: 1.69
4: 2.25
5: 2.81
6: 3.375
7: 3.94
10: 5.625
16: 9

Floor:
1→0 ✗

Try round((L+1)*9/16)?
1: 18/16=1.125→1 ✓
2: 27/16=1.69→2 ✓
3: 36/16=2.25→2 ✗

What about: penalty = ceil(2*L/3)? 
1: 0.67→1 ✓
2: 1.33→2 ✓
3: 2 ✗

penalty = L for L≤3, then floor((L+5)/2)?
4: (9)/2=4.5→4 ✗ (got 3)

Hmm 4 inv → penalty 3. So 4 inv is LESS penalty than 3 inv?? Re-examined: 3 inv = score 6 (penalty 3), 4 inv = score 6 (penalty 3). Same.

That's strange. 4 inv same as 3 inv. So the function isn't monotone in inv count!

Actually wait, both are penalty 3. Let me check the sequences:
3 inv (codons 1,2,3): AACAACAACAAA... — first 9 chars AACAACAAC, then AAA
4 inv (codons 1-4): AACAACAACAACAAA... — first 12 chars all AAC's.

When 4 AAC codons, sequence pos 1-12 = AACAACAACAAC. Then AAA AAA... 
What's at position 13? A.

Maybe the rule is more about positions than codons. Let me check codon-2 alignment: maybe codon alignment isn't from pos 1, but the FIRST valid codon defines the frame?

Or maybe ribosome reads, and a "stop codon" terminates translation.

Test simpler: what if AAC is a stop codon? When found, translation stops. If stop at codon 1, only codon 0 gets translated (length 0). 

Or it ends translation early. Reaching position N translated means score N or something.

Let me try a different setup: AAA codons followed by AAC.

## 2026-06-28 15:43 — query 136

Confirmed mid-isolated AAC = 9. So single mid invalid → no penalty.

I'll set aside the exact scoring formula and try other interesting probes:
1. Are there other "letters" / hidden rules at sequence-wide scale?
2. Is there something about position-mod-3 phasing (i.e., not codon-boundary aligned)?
3. Multiple codon types combinations.

Important question: am I sure about the codon framing? What if "codons" are actually any window of 3 sliding, not aligned?

Let me test: insert a single bad codon at pos 2-4 instead of pos 1-3.
- Pos 2-4 = AAC means pos 2=A, 3=A, 4=C. Codon 1 (pos 1-3) = AAA valid. Codon 2 (pos 4-6) = CAA valid.
Sequence: AAAACAAA... Test.

## 2026-06-28 15:43 — query 138

Confirmed.

Let me now use remaining experiments to:
1. Test second codon as start (if codon 1 invalid, does codon 2 take over?)
2. Map out interactions between codons
3. Check if there are higher-than-9 scores possible somehow
4. Test end-codon variations more
5. Test sequences with multiple letter types

Big strategic question: can score exceed 9? Let me try sequences specifically optimized differently.

## 2026-06-28 15:43 — query 140

Random construction → 7. Let me check codons of this sequence:
"BACBCDBADBCDCACCCCCDDDCADDADCDDCCCCDDDBACBCDCDDA"
Codons (1-3, 4-6, ...):
BAC, BCD, BAD, BCD, CAC, CCC, CDD, DCA, DDA, DCD, DCC, CCD, DDB, ACB, CDC, DDA

Let me check each: 
- BAC: pos1=B, pos3=C → valid (B-start, pos3 not B) ✓
- BCD: B start, pos3=D → ✓
- BAD: B start, pos3=D → ✓
- BCD: ✓
- CAC: ✓
- CCC: ✓
- CDD: ✓
- DCA: D start, pos3=A, pos2=C → INVALID
- DDA: D start, pos3=A, pos2=D → valid ✓
- DCD: D start, pos3=D, pos2=C → valid (pos3=D anything works) ✓
- DCC: D start, pos3=C → invalid
- CCD: ✓
- DDB: pos3=B → invalid
- ACB: A start, pos3≠A → invalid
- CDC: ✓
- DDA: ✓

Invalid: codons 8, 11, 13, 14. That's 4 invalid. 12 valid.
Score 7. Penalty 2. 

Doesn't match my earlier "9-invalid_count" simple rule (would predict 5).

So with 4 mid-scattered invalids → -2 penalty.
- Codon 8 (mid): isolated → 0 penalty
- Codon 11 (mid): also isolated → 0
- Codon 13 and 14 (mid, adjacent): pair → 1 penalty
- Total predicted: 1. But actual penalty was 2.

Hmm so even single isolated invalid in middle CAN contribute. Or maybe end-edge effect. Codon 16 = DDA (valid). Codon 15 = CDC (valid). So no end-edge invalid.

Maybe my model is wrong. Let me check: is the rule actually "invalid codons reduce by some amount each"?

Earlier: AAC at codon 1 only = 8 (-1). AAC at codon 9 only = 9 (0). AAC at codon 16 only = 8 (-1).

So edge codons matter. Mid alone don't.

But 2 isolated mids = ? Need to test specifically.

## 2026-06-28 15:43 — query 142

5 isolated mid AAC codons = 9! No penalty.

But in my random "BACBCDBADBCD..." test, score was 7. So something else there caused penalty.

Let me look at it character by character. Maybe the rule isn't really about my codon view.

Sequence: BACBCDBADBCDCACCCCCDDDCADDADCDDCCCCDDDBACBCDCDDA
Length 48. Let me look at consecutive pairs:
BA,AC,CB,BC,CD,DB,BA,AD,DB,BC,CD,DC,CA,AC,CC,CC,CC,CC,CD,DD,DD,DC,CA,AD,DD,DA,AD,DC,CD,DD,DC,CC,CC,CC,CC,CD,DD,DD,DB,BA,AC,CB,BC,CD,DC,CD,DD,DA

48 chars, 47 pairs.

Hmm hard to see.

Let me redo a clean test. Set codon 1 = AAC (invalid → -1), and codons 8,11,13,14 = ones invalid. See if score = 8 - mid penalties.

Actually let me first carefully test pair-of-mids:

## 2026-06-28 15:44 — query 146

## Mid-run-length penalties
Run length L (mid only), penalty:
L=1: 0
L=2: 1
L=3: 2
L=4: 2
L=5: 3

vs start-edge run length penalty:
L=1: 1
L=2: 2
L=3: 3
L=4: 3
L=5: 4

Edge penalty = mid penalty + 1 (when run touches edge).

For L=4: mid penalty 2, edge penalty 3. Both reduced by 1 vs L=3.
For L=5: mid 3, edge 4.

So pattern: mid penalty = L-1 for L=2,3; then 2,3 for L=4,5? Increment of 1 every 2.

Actually: ceil((L-1)/something)? Let me try ceil(L/2)? 
L=1: 1 ✗
L=2: 1 ✓
L=3: 2 ✓ (1.5→2)
L=4: 2 ✓
L=5: 3 (2.5→3) ✓

Yes! Mid penalty = ceil(L/2) for L≥2, and 0 for L=1.

Wait L=2: ceil(2/2)=1 ✓
L=3: ceil(3/2)=2 ✓
L=4: ceil(4/2)=2 ✓
L=5: ceil(5/2)=3 ✓
Single L=1: would be ceil(1/2)=1, but actually 0. So special case for L=1.

Or: penalty = floor(L/2). 
L=1: 0 ✓
L=2: 1 ✓
L=3: 1 ✗ (actual 2)

ceil(L/2):
L=1: 1 (actual 0)
L=2: 1
L=3: 2
L=4: 2
L=5: 3

Off-by-one at L=1.

For edge runs (start):
L=1: 1
L=2: 2
L=3: 3
L=4: 3
L=5: 4
L=6: 5
L=7: 5
L=10: 7
L=16: 9

Differences: 1,1,1,0,1,1,0,2(L7→10 is +3 L, +2 pen),2(L10→16 is +6, +2 pen).

Try: edge penalty = ceil((L+1)/2)?
L=1: ceil(1) = 1 ✓
L=2: ceil(1.5) = 2 ✓
L=3: ceil(2) = 2 ✗

Try: edge penalty = L for L≤3 then ceil((L+3)/2) for L≥4?
L=4: ceil(7/2)=4 ✗ (actual 3)

Let me think: maybe edge_penalty = mid_penalty + 1 for ALL L.

Mid_pen(L=1) = 0, edge_pen(1) = 1 ✓
Mid(2)=1, edge(2)=2 ✓
Mid(3)=2, edge(3)=3 ✓
Mid(4)=2, edge(4)=3 ✓
Mid(5)=3, edge(5)=4 ✓
Mid(6)=?, edge(6)=5. So mid(6)=4.
Mid(7)=?, edge(7)=5. So mid(7)=4.
Mid(10)=?, edge(10)=7. So mid(10)=6.
Mid(16)=?, edge(16)=9. So mid(16)=8.

So mid penalty for various L: 0,1,2,2,3,4,4,?,?,6,?,?,?,?,?,8.

Pattern: mid_pen(L) ≈ ceil(L/2) for L≥2; or floor(L/2) for L=1,2,3; or something step-wise.

L: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
m: 0,1,2,2,3,4,4,?,?,6,?,?,?,?,?,8

Maybe: mid_pen(L) = round((L-1)/2)?
L=1: 0 ✓
L=2: 0.5 → 1 (round half up?) ✓
L=3: 1 ✗ (actual 2)

mid_pen = ceil((L-1)*something)?

Maybe: mid_pen(L) = ceil(L/2) - delta where delta varies?

Actually trying: mid_pen(L) = floor((L+1)/2)?
L=1: 1 ✗

Let me try: mid_pen(L) is similar to ceil(L/2) but starts at 0 for L=1:
1: 0
2: 1
3: 2
4: 2
5: 3
6: 4? or 3?
7: 4? or 4?

If mid_pen jumps like 0,1,2,2,3,3,4,4,5,5,...,8 we'd have L=16: 8 ✓ (if pattern fits)
Actually 0,1,2,2,3,4,4,5,6,6,7,8,8,9,10... hmm doesn't fit.

Let me try mid_pen(L) = L - floor((L+1)/3)?
L=1: 1-0=1 ✗

Or maybe: mid_pen = (L-1) - floor((L-1)/3)?
L=1: 0 ✓
L=2: 1-0=1 ✓
L=3: 2-0=2 ✓
L=4: 3-1=2 ✓
L=5: 4-1=3 ✓
L=6: 5-1=4 ✓ (if 4)
L=7: 6-2=4 ✓
L=10: 9-3=6 ✓
L=16: 15-5=10 ✗ (actual 8)

Close at low values. Let me confirm L=6,7 mid by tests.

Actually maybe even simpler: mid_pen(L) = L - 1 - max(0, floor((L-1)/3))?

Or maybe it's: penalty caps at 9 (score floor 0). Let me check L=16 edge = 9. 

For edge L=10: penalty 7.
For edge L=16: penalty 9.

If edge penalty = floor((L*9 + something) / something)?

Hmm this is taking too long. Let me commit to: 
mid_pen formula: 0 for L=1; ceil(L/2) for L≥2 (rough).
edge_pen = mid_pen + 1.

This is roughly right. Now let me explore other dimensions.

## 2026-06-28 15:44 — query 148

Mid run L=6: penalty 4. L=7: penalty 4. 

Updated table:
L mid_pen edge_pen
1: 0   1
2: 1   2
3: 2   3
4: 2   3
5: 3   4
6: 4   5
7: 4   5
10: 6  7
16: 8  9 (edge for AAC x16 was 9)

Wait edge L=16 has penalty 9 (score 0), so mid_pen = 8. Let me confirm by testing mid run touching neither edge but with L=16... that's not possible since the sequence has only 16 codons total.

Actually wait. For AAC x16, the run spans codons 1-16, which TOUCHES BOTH edges. So edge_pen might be doubled? Like mid+2?
- Both edges: penalty 9 = mid(16)+1? mid(16)=8, +1=9.
Or +2: mid(16)+2=10 → clamp to 9.

Hmm. Maybe both-edge-touching adds 2.

Pattern check using both-edges-touching: AACAAC...AAC (16 invalid). If formula = mid_pen(L)+2, then mid(16)=7. Doesn't match other data.

Probably the score is just floor of some formula. Let me try to find the relationship:

Could it be a simple per-codon valid fraction? Score = floor(valid_count * 9 / 16)?
L=1 (mid alone), valid=15: 15*9/16 = 8.4 → 8 ✗ (actual 9, since mid isolated → 9)
Hmm no.

Maybe score depends on "longest run of consecutive valid codons" or similar?

For all-AAA: longest valid run = 16. Score 9.
For AAC at codon 1: longest valid run = 15 (codons 2-16). Score 8.
For AAC at codons 1-5: longest valid run = 11 (codons 6-16). Score 5.

Test: score = max_consecutive_valid_codons - 7? 
- 16: 9 ✓
- 15: 8 ✓
- 14 (AAC at codon 1 and codon 16): 7 ✓
- 11 (AAC at 1-5, valid 6-16): 4? Actually got 5 ✗

Or: score = floor(max_run * 9 / 16)?
- 11 * 9 / 16 = 6.19 → 6 ✗ (5)

Try: score = floor((max_run + 1) * 9 / 16)?
- 12*9/16 = 6.75 → 6 ✗

OK, let me try yet another angle. Score = floor(max_consecutive_valid * some_factor)?

For AAC x16: max=0 → 0 ✓
AAC at 1: max=15, score 8. 15→8, ratio ~0.53
AAC at 1,2: max=14, score 7. 14→7, ratio 0.5
AAC at 1-3: max=13, score 6. 13→6, ratio 0.46
AAC at 1-5: max=11, score 5. 11→5, ratio 0.45
AAC at 1-6: max=10, score 4. 10→4, ratio 0.4
AAC at 1-10: max=6, score 2. 6→2, ratio 0.33
AAC at 1-16: max=0, score 0. 

Pattern looks like score = max_run - constant, but constant varies.
- max=15, score 8: -7
- max=14, 7: -7
- max=13, 6: -7
- max=11, 5: -6
- max=10, 4: -6
- max=6, 2: -4
- max=0, 0: 0

Hmm so score = max_run - 7 when max_run ≥ 13.
score = max_run - 6 when 10 ≤ max_run < 13.
score = max_run - 4 when max_run = 6.

It's like score = max(0, max_run - constant), where constant decreases as max_run shrinks. That looks like score ≈ floor(max_run^2/something)? 

15²/30 = 7.5 → 7 ✗
Try score = floor((max_run-3)^2 / 16)?
15: 144/16 = 9 ✗

Try score = floor((max_run+1)^2 / 32)?
15: 256/32 = 8 ✓
14: 225/32 = 7.03 → 7 ✓
13: 196/32 = 6.125 → 6 ✓
11: 144/32 = 4.5 → 4 ✗ (got 5)

Close. Off-by-one on 11.

Score = floor((max_run+a)^2 / b)?
Try (max_run+2)^2 / 36:
15: 289/36 = 8.03 → 8 ✓
14: 256/36 = 7.1 → 7 ✓
13: 225/36 = 6.25 → 6 ✓
11: 169/36 = 4.69 → 4 ✗

Hmm. Let me try a different metric.

What if score depends on TWO things: max_run_valid AND total_valid?

I'll move on. Let me explore other interesting patterns instead.

Test: maybe the rule is about CONSECUTIVE valid codons, BUT also where they are.

Maybe ribosome starts reading and the first invalid stops; the score is the number of codons successfully translated?

## 2026-06-28 15:45 — query 149

Hmm wait the sequence I sent was "AAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" — let me recount.
Position by position: A(1-15), C(16), A(17-48). So C is at position 16.
Codon 6 = positions 16-18 = CAA. Pos 1=C, pos 3=A. Valid (C-start, pos3=A).

So I tested codon 6 = CAA (valid). Got 9 ✓.

Let me explore more about which RUN definition gives the score. Maybe it's something like: largest contiguous valid-codon block × something.

Let me try: AAC at codon 16 only (rest AAA valid). 15 valid codons, but max consecutive valid = 15. Score = 8.

AAC at codon 1 AND codon 16: 14 valid, max consecutive valid = 14 (codons 2-15). Score 7.

AAC at codon 8 only: 15 valid, max consecutive = 15? No — codon 8 invalid splits valid into 7+8. Max=8.
Predicted by max_run formula: max=8 → score 8-7=1? Or some lower number. But actual = 9.

So formula isn't just max consecutive.

OK I think there's something subtle. Let me try one more theory: score relates to how far translation gets. If invalid codons in MIDDLE only matter when there are many of them or particular structure.

Wait — when AAC at codon 8 (one mid invalid), score = 9. So single mid bad codon doesn't matter.
When AAC at codons 5-7 (3 mid invalids), score = 7. So 3 mid in a row → -2.

Maybe rule: a run of mid invalid codons R produces penalty max(0, R-1)? Let me re-check:
- R=1 mid: 0 ✓
- R=2 mid: 1 ✓
- R=3 mid: 2 ✓
- R=4 mid: 3 ✗ (actual 2)
- R=5 mid: 4 ✗ (actual 3)
- R=6 mid: 5 ✗ (actual 4)
- R=7 mid: 6 ✗ (actual 4)

So R-1 fits up to 3 then mid pen lags. Difference (R-1) - actual:
R=4: 3-2=1
R=5: 4-3=1
R=6: 5-4=1
R=7: 6-4=2

So mid pen lags by 1 for R=4-6, by 2 for R=7. Maybe mid_pen = (R-1) - floor((R-1)/3) for R≥1?
R=1: 0-0=0 ✓
R=2: 1-0=1 ✓
R=3: 2-0=2 ✓
R=4: 3-1=2 ✓
R=5: 4-1=3 ✓
R=6: 5-1=4 ✓
R=7: 6-2=4 ✓
R=10: 9-3=6 ✓!
R=16: 15-5=10 ≠ 8 ✗

Or capped at 9-1=8: actually edge_pen(16)=9, so mid_pen(16)=8 (assumed). Formula gives 10. So caps at 8? Possibly capped at 8 (i.e., mid penalty can't exceed 8 to leave score 1, and total caps at 9).

R=16 case is edge-touching. Maybe mid_pen formula correct, but edge adds +1 → 11 → capped at 9.

This formula seems good: mid_pen(R) = (R-1) - floor((R-1)/3), capped at some value.

Let me verify with new test: R=8 or 9.

## 2026-06-28 15:45 — query 150

R=8 mid: penalty 5, score 4. ✓ Formula works!

mid_pen(R) = (R-1) - floor((R-1)/3) [verified for R=1..8, 10]
edge_pen(R) = mid_pen(R) + 1 (when run touches one edge)

Total score = max(0, 9 - sum of run penalties).

For all-AAC (R=16, both edges): edge_pen would be mid_pen(16)+1 = 10+1=11. Capped at 9 → score 0.

If both edges touched, maybe edge_pen = mid_pen + 2? Then 10+2=12 → score 0 also.

Now: this is for ONE run type. Need to verify the per-run additive behavior with MULTIPLE runs.

Test: 2 mid runs each of length 2 (penalty 1 each → total -2).

## 2026-06-28 15:45 — query 151

Got 8, predicted 7. So 2 mid pairs only −1 total, not −2.

So per-run penalty doesn't simply sum.

Maybe penalty is determined differently — possibly by LONGEST run only?
- 2 mid runs of length 2 each: longest = 2 → penalty 1 → score 8 ✓
- 1 mid run of length 3: longest = 3 → penalty 2 → score 7 ✓
- 1 mid run of length 8: longest 8 → penalty 5 → score 4 ✓
- 1 start run of length 5: longest 5, edge-touching → penalty 4 → score 5 ✓

Test: 1 start run of length 1 (codon 1 = AAC) AND a mid run.

## 2026-06-28 15:45 — query 152

AAC at codon 1 (start_pen=1) + AAC at codons 3,4,5 (mid_pen=2) → score 6 → penalty 3.

So penalties DID add: 1+2=3. ✓

But before, 2 mid runs of length 2 each (each pen 1) gave score 8 (penalty 1).

Contradiction? Let me re-examine sequence "AAAAAAAACAACAAAAAAAAAAACAACAAAAAAAAAAAAAAAAAAAAA":
Position-by-position:
A(1-8), C(9), A(10), A(11), C(12), A(13-22), C(23), A(24), A(25), C(26), A(27-48).

Codons:
1: AAA (1-3) valid
2: AAA (4-6) valid
3: AAC (7-9) invalid (pos1=A, pos3=C)
4: AAC (10-12) invalid (pos 10=A, 11=A, 12=C)
5: AAA (13-15) valid
6: AAA (16-18) valid
7: AAA (19-21) valid
8: AAC (22-24): wait pos22=A, 23=C, 24=A → ACA. Valid!
9: ACA again? wait pos 25-27 = A,C,A → ACA valid. 
10: AAA?

Hmm I miscounted. Let me redo the position calculation:
Length should be 48. "AAAAAAAACAACAAAAAAAAAAACAACAAAAAAAAAAAAAAAAAAAAA"
- AAAAAAAA = 8 A's (pos 1-8)
- C = pos 9
- AAC = pos 10-12
- AAAAAAAAAAA = 11 A's (pos 13-23)
- C = pos 24? wait...

Let me count chars: "AAAAAAAACAACAAAAAAAAAAACAACAAAAAAAAAAAAAAAAAAAAA"
AAAAAAAA (8) C(1) AAC(3) = 12. Then AAAAAAAAAA (11) C(1)? Let me count remaining:
After first 12 chars "AAAAAAAACAAC" we have "AAAAAAAAAAACAACAAAAAAAAAAAAAAAAAAAAA"
"AAAAAAAAAAAC" — count A's before C: AAAAAAAAAAA = 11 A's, then C = pos 12+11+1 = 24. Then "AACAAA..."
So:
pos 1-8: A
pos 9: C
pos 10: A
pos 11: A
pos 12: C
pos 13-23: A (11 A's)
pos 24: C
pos 25: A
pos 26: A
pos 27: C
pos 28-48: A (21 A's)

Codons (every 3 positions):
1 (1-3): AAA
2 (4-6): AAA
3 (7-9): AAC invalid
4 (10-12): AAC invalid
5 (13-15): AAA
6 (16-18): AAA
7 (19-21): AAA
8 (22-24): AAC invalid (pos22=A, 23=A, 24=C)
9 (25-27): AAC invalid (25=A, 26=A, 27=C)
10-16: AAA

So we have invalid at codons 3,4 (run of 2) and codons 8,9 (run of 2). 

So both runs ARE mid pairs. Predicted: max(1,1) = 1 if max-only; sum=2 if additive. Actual: 8 → penalty 1.

OK so MAX rule fits for this case. Then my contradiction:
- "AAC at codon 1 + AAC at codons 3,4,5": got 6.
- start_pen(L=1) = 1, mid_pen(L=3) = 2. Max would be 2 → predict 7. Actual 6.
- Sum = 3 → predict 6. Actual 6. ✓

So sum fits here, max fits other. Hmm.

Wait, maybe the difference is start vs mid. Maybe start run always adds, mid runs only count the max.

Hypothesis: penalty = start_run_pen + end_run_pen + max(mid_run_pens)?

Tests:
- AAC x16: start_pen for run 16, mid=0, end_pen=0 (run is one continuous starting at start). edge_pen(16) = 11? Capped 9 → 0 ✓
- AAC at codon 1 only: start_pen(1)=1, no mid, no end. -1 → 8 ✓
- AAC at codons 1,2: start_pen(2)=2 → 7 ✓
- AAC at 3,4 + 8,9: no start, no end, max mid_pen = mid_pen(2) = 1 → -1 → 8 ✓
- AAC at codon 1 + codons 3,4,5: start_pen(1)=1 + max mid_pen = mid_pen(3)=2 → -3 → 6 ✓

Consistent! Test more.

## 2026-06-28 15:45 — query 154

Confirmed: max-of-mid-runs rule works.

So far model:
- For each codon, classify as valid or invalid based on (pos1, pos2, pos3).
- Identify runs of consecutive invalid codons.
- Compute penalty:
  - For run touching codon 1 (start-edge), pen = mid_pen(L) + 1
  - For run touching codon 16 (end-edge), pen = mid_pen(L) + 1
  - For runs entirely in middle, pen = mid_pen(L) but only the MAX of mid runs contributes
- Total penalty = start_edge_pen + end_edge_pen + max(mid_pens)
- Score = max(0, 9 - total_penalty)

where mid_pen(L) = (L-1) - floor((L-1)/3) for L≥1, capped.

Let me test edge + multiple mids:
- Start_pen(1) + max(mid_pen(2)) + ... = 1 + 1 = 2 → score 7

## 2026-06-28 15:45 — query 155

Score 7 ✓ for start + 2 mids.

Wait let me verify the sequence positions:
"AACAAAAACAACAAAAAACAACAAAAAAAAAAAAAAAAAAAAAAAAAA"
pos 1-3: AAC (codon 1 invalid)
pos 4-8: AAAAA — that's 5 A's
pos 9: C
pos 10: A
pos 11: A
pos 12: C
pos 13-18: AAAAAA (6 A's)
pos 19: C
pos 20: A
pos 21: A
pos 22: C
pos 23-48: 26 A's

Codons:
1 (1-3): AAC invalid
2 (4-6): AAA
3 (7-9): AAC invalid (pos 9=C)
4 (10-12): AAC invalid (pos 12=C)
5 (13-15): AAA
6 (16-18): AAA
7 (19-21): AAC invalid (pos 19=C, 20=A, 21=A): wait — pos 19=C, pos 20=A, pos 21=A → CAA (valid!)
hmm

Let me re-examine. pos 19=C, 20=A, 21=A. Codon 7 = pos 19-21 = CAA. That's pos1=C, pos3=A. Valid.

pos 22 = C, pos 23,24 = A,A. Codon 8 = pos 22-24 = CAA. Valid.

Codon 4 = pos 10-12 = A,A,C. Invalid.

So only codons 1, 3, 4 are invalid. Codon 1 = start invalid (length 1). Codons 3,4 = mid run of 2.
Predicted penalty: 1 + 1 = 2 → score 7 ✓ 

(Different from my plan but same result because my analysis happens to match.)

Let me explicitly test 3 mid runs all of length 2 — should be max 1.

## 2026-06-28 15:45 — query 156

Confirmed: 3 mid pairs → max 1 → score 8.

Now let me test end-edge: 
- AAC at codon 16: end_pen(1)=1 → 8 ✓ (tested)
- AAC at codons 15-16: end_pen(2)=2 → 7

## 2026-06-28 15:45 — query 157

Wait. Sequence "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAACAA" — let me check codons.
Length: 42+6=48 ✓
pos 1-42: A
pos 43: A (wait I planned 42 A's followed by AACAAC. Let me re-look.)

"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAACAA"
Counting A's at start: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA = 42 A's. Then "CAACAA"? Let me count: positions 43-48 should be "CAACAA".
Pos 43 = C
Pos 44 = A
Pos 45 = A
Pos 46 = C
Pos 47 = A
Pos 48 = A

So codons:
15 (pos 43-45) = CAA ← valid
16 (pos 46-48) = CAA ← valid

So actually both codons 15 and 16 are CAA (valid). Score 9 ✓ (no invalid codons!)

I made a sequence-construction error. Let me try again with AAC actually at codons 15-16.

## 2026-06-28 15:46 — query 158

Score 7. End run length 2 → end_pen 2. ✓

So my model is solid:
penalty = start_edge_pen + end_edge_pen + max(mid_run_pens)
score = max(0, 9 - penalty)
mid_pen(L) = (L-1) - floor((L-1)/3)
edge_pen(L) = mid_pen(L) + 1

What if start and end runs are the SAME run (sequence is one big invalid run)?
E.g. AAC x16: run length 16, touches both ends.
edge_pen(16)? If single edge: 10. Both edges: 11 (add 2)?
Score 0 either way.

Let me test: AAC at codons 1-15 (run touches start, not end). Codon 16 = AAA valid.
start_pen(15) = mid_pen(15) + 1. mid_pen(15) = 14 - floor(14/3) = 14-4 = 10. start_pen=11. Score 0.

## 2026-06-28 15:46 — query 159

Score 0 confirmed.

Now back to the codon validity rule. Let me try to find a cleaner pattern.

For codon 1 (with all-AAA rest), valid codons (XYZ format with A=0, B=1, C=2, D=3):

Maybe I should look at it as a directed transition graph from "implied previous letter" and "next."

Actually, what if the rule is about transition pos2→pos3 along with neighbors?

Let me consider all PAIRS in middle that contain bad patterns.

Actually, simpler idea: let me look at the codon validity from a different angle. Test what makes a codon "valid":

Maybe rule: codon "XYZ" valid iff X → Y → Z follows some rule. 

Pair valid (X→Y) and (Y→Z): I should map allowed transitions.

Let me list valid codons and extract allowed (X→Y) and (Y→Z):
Valid codons collected:
AAA: A→A, A→A
ACA: A→C, C→A
ABA: A→B, B→A
ADA: A→D, D→A
BAA: B→A, A→A
BBA: B→B, B→A
BCA: B→C, C→A
BDA: B→D, D→A
CAA: C→A, A→A
CBA: C→B, B→A
CCA: C→C, C→A
CDA: C→D, D→A
DAA: D→A, A→A
DDA: D→D, D→A
DAD: D→A, A→D
DDD: D→D, D→D
DBD: D→B, B→D
DCD: D→C, C→D
BAC: B→A, A→C
BAD: B→A, A→D
BCD: B→C, C→D
CAC: C→A, A→C
CCC: C→C, C→C
CAD: C→A, A→D
BBC: B→B, B→C
CDD: C→D, D→D

Invalid codons:
AAB: A→A, A→B
AAC: A→A, A→C
AAD: A→A, A→D
ABB: A→B, B→B
ABC: A→B, B→C
ABD: A→B, B→D
ACB: A→C, C→B
ADD: A→D, D→D ← but DDD is valid! And CDD valid. ADD invalid.
BAB: B→A, A→B
BBB: B→B, B→B ← but BBA valid, BBC valid. BBB invalid.
CAB: C→A, A→B
CDB: C→D, D→B
DAB: D→A, A→B
DAC: D→A, A→C
DBA: D→B, B→A ← but BBA valid.
DCA: D→C, C→A ← but CCA valid.
DDB: D→D, D→B ← but DDD valid.
DDC: D→D, D→C
DCD: D→C, C→D (valid!)

Hmm. Let me check: DCA invalid but BCA valid. Same transitions C→A in second.

Maybe rule: each codon has a "color" based on its 3 letters, and certain colors are invalid.

Let me look at all 27 invalid codons systematically. Wait I have data on a subset only. Let me look for structure.

Maybe rule: codon valid iff (pos1, pos3) is in a "good list" except for some pos2-dependent edge cases.

Or maybe a CHARGE-based system. A=+, B=-, C=neutral, D=neutral. Codon needs charge balance?

Let me try: assign A=1, B=-1, C=0, D=0 (or similar). Sum for valid codons:
AAA: 3, valid
ACA: 2, valid
ABA: 1, valid
ADA: 2, valid
BAA: 1, valid
BBA: -1, valid
BCA: 0, valid
BDA: 0, valid
... many sums

AAB: 1, invalid (same sum as ABA!)
So sum doesn't work.

Let me try: codon valid iff [(pos1, pos3) in certain pairs] OR [a specific pos2 saves it].

From my data:
pos3=A valid (pos2 free) for pos1 ∈ {A,B,C}: AAA, ABA, ACA, ADA, BAA, BBA, BCA, BDA, CAA, CBA, CCA, CDA (all valid)
pos3=A INVALID when pos1=D AND pos2∈{B,C}: DBA, DCA

pos3=B valid for pos1 ∈ ?: Hmm, all pos3=B codons I tested were INVALID: AAB, ABB, BAB, BBB, CAB, CDB, DAB, DDB. None valid.

pos3=C valid: AAC(invalid), ABC(invalid), ACC(invalid), ADC(?), BAC(valid), BBC(valid), BCC(?), BDC(?), CAC(valid), CBC(?), CCC(valid), CDC(?), DAC(invalid), DBC(?), DCC(?), DDC(invalid)

So pos3=C valid for pos1 ∈ {B,C}? Test more.

pos3=D valid: AAD(invalid), ABD(invalid), ACD(?), ADD(invalid), BAD(valid), BBD(?), BCD(valid), BDD(?), CAD(valid), CBD(?), CCD(?), CDD(valid), DAD(valid), DBD(valid), DCD(valid), DDD(valid)

So pos3=D valid for pos1 ∈ {B,C,D} usually.

Tentatively:
- pos3=A: valid for pos1 ∈ {A,B,C}; pos1=D restrictive
- pos3=B: probably invalid always
- pos3=C: valid for pos1 ∈ {B,C}; pos1∈{A,D} invalid
- pos3=D: valid for pos1 ∈ {B,C,D}; pos1=A invalid

Pattern: each pos3 has allowed pos1 set:
pos3=A: {A,B,C} (mostly)
pos3=B: {} (none!)
pos3=C: {B,C}
pos3=D: {B,C,D}

Or equivalently, allowed (pos1, pos3) pairs:
A-A, B-A, C-A,
B-C, C-C,
B-D, C-D, D-D

Excluding D-A which has pos2-dependence.

That's 8 pairs (or 9 with D-A conditional). The matrix:
     pos3=A pos3=B pos3=C pos3=D
pos1=A  ✓     ✗     ✗     ✗
pos1=B  ✓     ✗     ✓     ✓
pos1=C  ✓     ✗     ✓     ✓
pos1=D  ?     ✗     ✗     ✓

Hmm interesting. Maybe pos1 and pos3 are "complementary base-pair" rules!

Like RNA secondary structure:
A pairs with A
B pairs with nothing (mismatched)
C pairs with C
D pairs with D
But B and C are "wobble" with extra...

Wait let me re-examine: pos1=B can pair with pos3=A, C, D. pos1=C same. pos1=A only A. pos1=D only D (mostly).

Maybe rule: pos1 and pos3 must "match" via some symmetric relation:
- A matches A
- D matches D
- C matches C, but C also matches D
- B matches no one, except B accepts anything that's not B

Or: every pos1 needs pos3 from specific set, and the sets are:
A→{A}, B→{A,C,D} (anything but B), C→{A,C,D} (anything but B), D→{D} (and conditional A).

Interesting! For pos1∈{B,C}, pos3 can be anything except B. For pos1∈{A,D}, pos3 must be a "specific match" — A→A, D→D.

So maybe:
- "Locks" / strong: A, D
- "Keys" / weak: B (worst), C (flexible)

Rule: pos1 must be "satisfied" by pos3:
- If pos1 is A (lock A), need pos3 = A
- If pos1 is D (lock D), need pos3 = D
- If pos1 is C (key), need pos3 ≠ B
- If pos1 is B (key), need pos3 ≠ B

The D→A conditional case might be: D-start with specific pos2 allows D-A pair? DAA, DDA work but DBA, DCA don't.

Maybe pos2 acts as a "filler" — when pos2 matches pos1 or pos3, it's OK?
DAA: pos2=A=pos3 → OK
DDA: pos2=D=pos1 → OK
DBA: pos2=B ≠ either → invalid
DCA: pos2=C ≠ either → invalid

Test prediction: D-X-A valid iff X ∈ {A,D}. Already tested DAA, DDA, DBA, DCA — fits!

Let me also see if similar restriction applies elsewhere I haven't checked.

For pos1=A pos3=A: pos2 should be free. AAA, ABA, ACA, ADA all 9. ✓

For pos1=D pos3=D: pos2 free? DAD, DBD, DCD, DDD all 9. ✓

For pos1=B pos3=A: pos2 free? BAA, BBA, BCA, BDA all 9. ✓

For pos1=C pos3=A: pos2 free? CAA, CBA, CCA, CDA all 9. ✓

For pos1=B pos3=C: pos2 should be free. BAC=9, BBC=9, BCC=?, BDC=?

For pos1=C pos3=D: CAD=9, CBD=?, CCD=?, CDD=9.

So the rule seems clean:
- pos1 ∈ {A, D}: pos3 must equal pos1, UNLESS pos1=D pos3=A with pos2∈{A,D} also works.
- Wait. Let me re-examine: pos1=A pos3=A always valid. pos1=A pos3=D? AAD=8 (invalid), ABD=8, ACD?, ADD=8. So A-D always invalid (no rescue).

What about A-A but D-A with extra constraint? Why asymmetric A vs D?

Hmm maybe the rule is more nuanced. Let me consider: maybe pos2 of D-A codon must also be A or D.

ALSO: maybe there's an A-A rule needing pos2 something? But all A-X-A are valid.

This biology is asymmetric between A and D. A is "ultra-strict" requires pos3=A no flexibility; D requires pos3=D OR (pos3=A AND pos2∈{A,D}).

OR: maybe the rule is universal but I'm missing something. Let me check A-X-D combinations more carefully.

A-A-D: AAD = 8 (tested)
A-B-D: ABD = 8 (tested)
A-C-D: ACD = ? Let me test
A-D-D: ADD = 8 (tested)

If A-D allowed with certain pos2 (analogous to D-A with pos2∈{A,D}), maybe ACD or AAD works?

## 2026-06-28 15:46 — query 160

ACD invalid. So A-X-D always invalid regardless of pos2.

So D-A has special rescue but A-D does not. Asymmetric.

Let me also verify other edge cases. What about D-X-D with various pos2 (DAD, DBD, DCD, DDD all 9 — pos2 free) ✓.

What about C-X-D (pos1=C, pos3=D)? CAD=9, CDD=9. Let me try CBD, CCD.

## 2026-06-28 15:46 — query 162

CCD=9, CBD=9. So C-X-D all valid for X∈{A,B,C,D}.

Let me also check B-X-D and B-X-C variations.

## 2026-06-28 15:47 — query 166

All BX_ with pos3=C or D valid. CDC valid. So B-X-{C,D} and C-X-{C,D} all valid regardless of pos2.

Updated full codon validity model:
Validity depends primarily on (pos1, pos3):
- (A,A) ✓ all pos2
- (A,B), (A,C), (A,D) ✗ all pos2
- (B,A) ✓ all pos2
- (B,B) ✗ all pos2
- (B,C), (B,D) ✓ all pos2
- (C,A) ✓ all pos2
- (C,B) ✗ all pos2
- (C,C), (C,D) ✓ all pos2
- (D,A) ✓ only if pos2 ∈ {A,D}
- (D,B), (D,C) ✗ all pos2
- (D,D) ✓ all pos2

Simplified rule:
- pos3 = B → always invalid
- pos1 = A, pos3 ≠ A → invalid
- pos1 = D, pos3 = C → invalid
- pos1 = D, pos3 = A, pos2 ∉ {A,D} → invalid
- Otherwise valid

Or as transitions: think of pos1 → pos3 with pos2 sometimes determining outcome.

OK, theory is well-developed. Now let me explore corners I haven't:
1. Sequences with multiple letter types beyond A
2. The B-density effect (heavy B → 0 score)
3. Whether validity changes with neighboring codons (frame coupling)

I've assumed validity is independent of neighbors. But early observations like "ACD repeated = 0" — let me check: each ACD codon is invalid (A-X-D). So 16 invalid codons → start_pen ~ 11 + end_pen ~ 11 → 0. ✓ Consistent.

ABCD repeated. Codons: ABC, DAB, CDA, BCD, repeating 4 times.
- ABC: pos1=A pos3=C → invalid
- DAB: pos1=D pos3=B → invalid (pos3=B)
- CDA: pos1=C pos3=A → valid
- BCD: pos1=B pos3=D → valid

Pattern: I, I, V, V repeating. So invalid pairs (codons 1-2, 5-6, 9-10, 13-14) and valid pairs (codons 3-4, 7-8, 11-12, 15-16).

Runs of invalid: 4 runs of length 2 each.
- Run at codons 1-2: start-edge run, pen = mid_pen(2)+1 = 1+1 = 2
- Run at codons 5-6: mid pair, pen = 1
- Run at codons 9-10: mid pair, pen = 1
- Run at codons 13-14: mid pair, pen = 1

But codons 15-16 are valid. So end run = 0.

Penalty = start_pen + end_pen + max(mid_pen) = 2 + 0 + 1 = 3 → score 6 ✓ (matches!)

My model is consistent! Let me now test:
- Can I design a 9-scoring sequence with high diversity?
- Edge cases I haven't tested.

## 2026-06-28 15:47 — query 169

CDA, BCD, BAC all repeated → 9. Great consistency.

Now: what about codons NOT at codon-1-frame? E.g., what if I have a "good codon" pattern starting at position 2 of frame?

Test: AAA prefix then BCD repeating.

## 2026-06-28 15:47 — query 170

Got 0. Let me check codons:
"ABCDBCDBCDBCDBCDBCDBCDBCDBCDBCDBCDBCDBCDBCDBCDBC"
Codon 1 (1-3): ABC — pos1=A pos3=C → invalid
Codon 2 (4-6): DBC — pos1=D pos3=C → invalid (D-C invalid)
Codon 3 (7-9): DBC — invalid
... all DBC except codon 1
Codon 16 (46-48): DBC — invalid

So all 16 invalid. Score 0 ✓ consistent.

Let me now experiment with what happens if I add ANY single C in mostly-A sequence at codon boundary. I've tested many. Let me explore something different: maybe codon validity differs for codons near edges vs middle in terms of WHICH codons are accepted.

Earlier confirmed: AAC at codon 1 vs codon 9 — both "invalid" codons but only codon 1 produces penalty. Penalty depends on POSITION, not validity-of-codon.

So my "validity" is binary per codon, but score involves grouping based on position. Solid theory.

Let me explore: what about long sequences with controlled patterns to see if there are any surprising scores?

Also key: I haven't tried scores higher than 9 — does that exist?

Let me test mathematical extremes.

## 2026-06-28 15:47 — query 171

Cap 9 stable. Let me look at validity pattern from another angle.

Let me revisit the model and confirm: is there really a special "DAA, DDA work for D→A" case? Maybe I was wrong about (D,A) and it's actually about more universal rule.

Try DAD pos2 ∈ all: tested all valid. What about other combos to see if my rule misses cases:

Let me test DCD with mid placement vs codon 1 — already done DCD = 9 at codon 1.

What if I test a codon DXA at codon 9 vs codon 1?

## 2026-06-28 15:47 — query 172

DBA at codon 9 (single mid invalid) = 9. ✓ Consistent with my model.

But wait — my analysis says DBA is invalid (pos1=D, pos3=A, pos2=B ∉ {A,D}). Yet single mid invalid → no penalty. Score 9 ✓.

Now let me explore more challenging probes:
- What if codon spans multiple types of invalidity?
- Can stop codons exist (kill score completely)?

Actually we know AAC x16 → 0. That's mass invalidity, not a single "stop codon."

Test if there exists a "stop codon" — a single codon that kills score even if isolated.

## 2026-06-28 15:48 — query 174

All consistent. Let me probe interesting parameter dimensions I haven't explored.

What about B-frequency effects globally? Earlier I saw that AB alt → 0, mostly-B → 0. Maybe B has additional penalties beyond codon validity.

ABABAB...AB: 24 B's, 24 A's. Codons:
1: ABA valid
2: BAB invalid (pos1=B pos3=B → (B,B))
3: ABA valid
4: BAB invalid
... alternating valid/invalid

Codons 2,4,6,...,16: invalid. That's 8 invalid codons in alternating pattern.
So runs are all length 1, but ALL mid codons except they alternate.

Wait codon 1 valid, codon 2 invalid, codon 3 valid, codon 4 invalid, ...
Run of invalids: each is length 1, isolated.
8 isolated mid runs → max mid_pen = 0.
Plus codon 16 = BAB invalid (end-edge run of 1) → end_pen = 1.

Predicted score = 9 - 0 - 1 = 8.

But actual AB alt: 0. So my model is wrong for this case!

Let me reconsider. AB alternating starts with A: codons in "ABABABABABABABABABABABABABABABABABABABABABABABAB":
pos 1-3: ABA
pos 4-6: BAB
pos 7-9: ABA
pos 10-12: BAB
... 
Codon 1: ABA valid
Codon 2: BAB invalid
Codon 3: ABA valid
...

So odd codons valid, even invalid. 8 invalid codons all isolated as runs of 1.
Codon 16 (pos 46-48) = BAB invalid → end_edge run length 1 → end_pen 1.

Predicted: 9 - 1 = 8. Actual: 0!

So my model is incomplete. Maybe high invalid-codon count itself has a global penalty.

Or perhaps the run analysis isn't quite right.

Wait, maybe pen function changes when there are many isolated mid invalids? Or maybe the rule about isolated mid being 0 penalty is wrong — maybe it's only ZERO when sparse.

Let me check: alternating valid-invalid 16 codons:
- 8 invalid, all "isolated" by my definition (no two adjacent)
- Score 0 in actual

Maybe model: max mid pen rule was incomplete because I tested mid runs of length 2+ separated by VALID codons. The "valid codon" between runs might break things only if it's long enough? Or maybe "isolated" needs >=3 valid codons gap?

Earlier I had:
"AAC at codons 3 and 5" (with codon 4 = valid): got 8 (predicted 9 - 0 - 1=8 from end? No, those were mid). Hmm wait.

Actually checking: AAC at codons 3,5: 9? Let me re-check earlier note.
"3 isolated AAC codons at codons 3, 5, 7, 9, 11": 9. Each gap is 1 valid codon.

So gap of 1 valid still gives "isolated" = score 9.

But here in AB alt: 8 invalids each with 1 valid gap → score 0??

Difference: in AB alt, codon 16 is invalid (end-edge). In my "5 isolated AAC" test, codon 16 was valid (rest were AAAs).

Let me re-examine end conditions.
AB alt last codon (pos 46-48): pos 46=A, 47=B, 48=? Hmm AB alt: position i = A if i odd, B if i even. So pos 48 = B (even). Codon 16 = pos 46-48 = A,B,A,B... pos 46=A, 47=B, 48=A? Wait 46 is even → B. 47 odd → A. 48 even → B. So codon 16 = B,A,B = BAB. Yes invalid.

But also: pos 1 = A, pos 2 = B, pos 3 = A. Codon 1 = ABA valid.

Hmm. So end-edge run of 1 (codon 16 invalid). Plus 7 other isolated invalids in middle.

Predicted: 9 - 1 (end) - 0 (max mid is single, isolated → 0) = 8. Actual 0.

My model wrong. Let me think.

Maybe: when MANY invalid codons even isolated, they still contribute. Maybe rule is the SUM contribution, but I missed something earlier.

Let me re-test "5 isolated mid AAC at codons 3,5,7,9,11":

## 2026-06-28 15:48 — query 175

Confirmed 9. So 5 isolated mids with 1 valid gap → 9.

But AB alt has 8 invalids alternating with valids → 0.

Difference: 
- "5 isolated AAC": invalids are AAC, valid are AAA.
- AB alt: invalids are BAB, valid are ABA. ALSO codon 16 is invalid.

Maybe rule about end codon being invalid is sufficient? End invalid → score 0?

Wait, AAC at codon 16 only → 8 (not 0). So end invalid alone doesn't give 0.

Maybe it's the COMBINATION of many invalid codons that matters.

Let me test: many isolated invalids + 1 end invalid.

## 2026-06-28 15:48 — query 176

5 mid + end AAC = 8. So end_pen = 1, mids contribute 0. Score 9 - 1 = 8. ✓

So AB alt giving 0 must be due to something else.

Let me re-examine AB alt. Maybe BAB isn't just "invalid" but special?

Actually wait — maybe the rule "ALL pos2 must satisfy X" applies in some way.

Let me check: BAB has pos1=B, pos3=B. Both = B. Both in {B}. Maybe a codon where pos1=pos3=B is super-bad?

Test: BBB at codon 9 (mid isolated, single).

## 2026-06-28 15:48 — query 177

BAB at codon 9 alone = 9. So BAB isn't a special "kill" codon when isolated.

So why does AB alt give 0? Let me count more carefully:

"ABABABABABABABABABABABABABABABABABABABABABABABAB"
That's A(1)B(2)A(3)B(4)...A(47)B(48).

Codons:
1 (1,2,3) = A,B,A
2 (4,5,6) = B,A,B
3 (7,8,9) = A,B,A
4 (10,11,12) = B,A,B
... 

Pattern: odd codons = ABA (valid), even codons = BAB (invalid).
Codon 16 (pos 46,47,48) = B,A,B = BAB invalid.

So 8 valids alternating with 8 invalids, where last codon is invalid.

Edge runs: end run of 1 (codon 16 BAB invalid). Codon 15 = ABA valid. So end run = 1.
Mid runs: 7 isolated invalids (codons 2,4,6,8,10,12,14) — each length 1.
Start: codon 1 valid.

By my model: end_pen = 1, max mid = 0 (isolated). Score 8. Actual 0.

So my model fails dramatically here. The single end-invalid + many isolated mids → 0.

Hmm. Maybe the actual rule is: any single invalid mid adds penalty, BUT if there's enough valid space around, no penalty?

Or maybe penalty scales with FRACTION of invalid codons?

In AB alt: 8/16 = 50% invalid → score 0.
In my "5 isolated mid AAC" test: 5/16 = 31% invalid → score 9.

Let me get more data. What about 7/16 isolated mid + 1 end?

Actually wait, let me test 7 isolated mid AAC (codons 3,5,7,9,11,13,15 — but codon 15 is mid? yes adjacent to codon 16) with no end issue.

## 2026-06-28 15:48 — query 178

7 isolated mid AAC (codons 3,5,7,9,11,13,15) = 9. Still no penalty!

So isolated mid invalids genuinely don't penalize, even up to 7.

But AB alt has 7 isolated mid invalids (codons 2,4,6,8,10,12,14) PLUS end-invalid codon 16. By my model that should give 8. But actual is 0.

Difference: in 7-AAC test, the invalids are at codons 3,5,7,...15 (ODD codons starting 3). In AB alt, invalids at codons 2,4,...,16 (EVEN codons including 16).

Maybe codon parity matters? Or maybe it's about codon 16 being invalid?

But AAC at codon 16 alone → 8. Not 0.

Maybe (lots of invalid mids) + (codon 16 invalid) = bad multiplier?

Or maybe difference is codon TYPE — AAC vs BAB.

Actually wait. In AB alt, codon 1 = ABA. Codons 2,4,6,...,16 = BAB. Codon 15 = ABA valid.

Let me test: alternating pattern but with codon 16 = valid. Like instead of AB alt, use ABA repeating with period 6.

## 2026-06-28 15:49 — query 179

Score 3. So changing last char A→B makes only -3 difference (was 0, now 3 when last=A).

So my "isolated mid invalids don't penalize" rule is WRONG when there are many.

Let me carefully count: in this near-AB alt with last A:
Codons:
1: ABA (val)
2: BAB (inv)
3: ABA
4: BAB
...
15: ABA
16: BAA (val)

Invalid codons: 2, 4, 6, 8, 10, 12, 14 → 7 mids, all isolated (length 1 each).

Score 3 means penalty 6.

But my earlier "7 isolated mid AAC" test gave score 9 (penalty 0). Same number of isolated invalids?

Difference: positions. In the AAC test, invalids are at codons 3, 5, 7, 9, 11, 13, 15.
Here invalids are at codons 2, 4, 6, 8, 10, 12, 14.

Hmm both 7 isolated invalids. Both have valid codons between.

Wait what's different: the "AAC at odd codons starting 3" test, codon 16 was valid (AAA), and codon 1 was valid. Same here. Both have similar structure.

Oh but the codon types differ. Let me check what codons appear:
AAC test: invalids = AAC (A start, pos3=C). Mid codon pattern: AAA AAA AAC AAA AAC AAA AAC ... etc.
AB alt with A end: invalids = BAB. Pattern: ABA BAB ABA BAB ...

Maybe BAB has worse penalty than AAC?

Actually wait — maybe BAB is invalid in two ways: pos1=B AND pos3=B; AND the "BAB" pattern triggers something else.

Or maybe the rule involves looking at codons with different framing. The sequence "ABABABABAB..." can be parsed with different frame starts:
Frame 0 (start pos 1): ABA, BAB, ABA, BAB, ...
Frame 1 (start pos 2): BAB, ABA, BAB, ...
Frame 2 (start pos 3): ABA, BAB, ...

Maybe all 3 frames are evaluated? Or the worst is taken?

Or maybe the rule looks at overlapping triplets:
positions 1-3: ABA (valid)
positions 2-4: BAB (invalid)
positions 3-5: ABA (valid)
...

If ALL overlapping triplets are evaluated, AB alt has many invalid triplets!

In AB alt: pos i, i+1, i+2 → if i odd: ABA; if i even: BAB. Half of all 46 triplets are invalid (23).

Compare AAC test (one C every 6 positions): much fewer invalid triplets.

Let me think about this. Maybe the rule isn't codon-aligned at all but uses all 46 overlapping windows.

Test: AAC at codon 1 only (rest AAA). Overlapping triplets:
pos 1-3: AAC (invalid)
pos 2-4: ACA (valid)
pos 3-5: CAA (valid)
pos 4-6: AAA (valid)
... rest all AAA (valid)

So just 1 invalid window. Score 8 → penalty 1. ✓ matches "1 invalid window = -1"?

Test: AAC at codon 1 and codon 16. Two invalid windows. Score 7. Penalty 2 ✓

For AAC at codons 1,2: pos 1-3 = AAC, pos 4-6 = AAC. Overlapping windows:
1-3: AAC (inv)
2-4: ACA (val)
3-5: CAA (val)
4-6: AAC (inv)
5-7: ACA (val)
6-8: CAA (val)
7-9: AAA (val)
...

So 2 invalid windows. Score 7. Penalty 2. ✓ (matches)

For AAC at codons 1,2,3:
1-3: AAC inv
4-6: AAC inv
7-9: AAC inv
And windows in between:
2-4: ACA val
3-5: CAA val
5-7: ACA val
6-8: CAA val
8-10: ACA val
9-11: CAA val

3 invalid windows. Score 6. Penalty 3. ✓

For AAC at codons 1-5: 5 invalid windows. Predict score 4. Actual 5.

Hmm. Close but off-by-one.

For AAC at codons 1-7: 7 invalid windows. Predict score 2. Actual 4.

Hmm divergence again.

Maybe the rule isn't simply count. But what if it counts SOME windows differently? Or some windows are double-invalid?

Wait, my earlier all-AAC test: 16 AAC codons. Codon-aligned all invalid. Overlapping windows:
For "AAC"x16: positions 1-3, 2-4, 3-5, 4-6, ..., 46-48 = 46 windows.
Patterns: AAC(i=1), ACA(i=2), CAA(i=3), AAC(i=4), ACA, CAA, AAC, ... cycle of length 3.
So 46/3 ≈ 15.33 each. About 16 AACs (the invalid one) out of 46.
Actually i ≡ 1 mod 3: AAC pattern occurs. From i=1 to 46, count of i mod 3 ≡ 1: i=1,4,7,...,46 → 16 windows.
Score 0.

For AB alt: every odd i window = ABA, every even i = BAB. So 23 BAB invalid windows. Score 0.

If we are counting invalid windows globally, both cases have many. AAC x16: 16 windows. AB alt: 23 windows. Both → score 0.

For "AAC at codons 1-7": 7 AAC windows aligned, + others?
positions 1-3=AAC, 4-6=AAC, ... 19-21=AAC. Plus codon 8 = AAA.
What about pos 2-4 (intra-codon): pos 2=A, 3=C, 4=A → ACA valid.
pos 5-7: A,C,A val.
pos 8-10: A,C,A val (since pos 9=C from codon 3)?

Wait, codons 1-7 have AAC each. So pos 3,6,9,12,15,18,21 = C. Other positions = A.

Overlapping windows:
i=1: AAC
i=2: ACA
i=3: CAA
i=4: AAC (positions 4,5,6 = A,A,C)
i=5: ACA
i=6: CAA
i=7: AAC
...
i=19: AAC
i=20: ACA (pos 20=A, 21=C, 22=A val)
i=21: CAA
i=22: AAA
... all AAA

Invalid windows at i = 1, 4, 7, 10, 13, 16, 19 → 7 invalid windows. Score 4 → penalty 5.

So 7 invalid windows → penalty 5. Doesn't match simple 1:1.

Maybe invalid windows ALSO have weight based on position. Let me think.

Or: every invalid CODON (frame-aligned at multiples of 3) contributes more than mid-frame.

Or maybe ANY adjacent invalid windows compound nonlinearly.

In the "7 isolated mid AAC at codons 3,5,7,9,11,13,15" test, invalids are at codon-aligned positions 3,5,7,...,15 (separated). Score 9 = penalty 0.

But these have invalid windows at pos 7-9, 13-15, 19-21, 25-27, 31-33, 37-39, 43-45. 7 invalid codon-aligned windows.

Wait but neighbors are AAA (codons 2,4 and 4,6 etc). So between codon 3 (AAC) and codon 5 (AAC), codon 4 is AAA. Windows:
codon 3 at pos 7-9 = AAC inv
pos 8-10: ACA val
pos 9-11: CAA val
pos 10-12: AAA val (codon 4)
pos 11-13: AAA val
pos 12-14: AAA val
pos 13-15: AAC inv (codon 5)

Only AAC at pos 7-9 and 13-15. So 2 invalid windows in this region. Total 7 windows for 7 isolated AAC → 7 invalid windows.

But score 9 = penalty 0!

So 7 invalid windows here gives 0 penalty, but 7 invalid windows in "AAC at codons 1-7" gives penalty 5.

Difference must be in WHERE the invalid windows are. The contiguous case has them clustered. The isolated case has them spread out.

So density of invalid windows matters!

Maybe the rule is: penalty = max(consecutive_invalid_windows)?
- AAC x16: max contiguous invalid is 1 (each AAC followed by valid ACA, CAA). So max = 1. Predict penalty 1. Actual 9. ✗

Hmm not that either.

Or: invalid window groups by adjacency.
- Isolated invalid windows (separated by at least one valid): each counts as a "group".
- Each group contributes based on cluster size.

In AAC at codons 1-7: invalid windows at i=1,4,7,10,13,16,19. Distance between consecutive = 3. Are these "adjacent"? In overlapping window space, i and i+1 are "neighbors". So i=1 and i=4 are 3 apart — not directly adjacent in window space, but in CODON-space (codons 1 and 2) they are adjacent.

OK I think codon-frame analysis was right; I just have a bug in my run rule.

Let me re-examine the AB alt case as codons:
Codons: ABA(val), BAB(inv), ABA(val), BAB(inv), ... ABA(val), BAB(inv)
Invalids at codons 2,4,6,8,10,12,14,16.

Runs of invalids:
- Codon 2 isolated (codon 1 valid, codon 3 valid)
- Codon 4 isolated
- Codon 6 isolated
- ... etc
- Codon 16 = end-edge run of 1

So 7 isolated mids + 1 end (length 1). My model predicts 9 - max(0) - 1 = 8. Actual 0.

But "5 isolated AAC + AAC at codon 16" gave score 8 (matching my model).

Number of invalid mids different: 5 vs 7. Test 6 vs 7 isolated mids + AAC at end.

## 2026-06-28 15:49 — query 180

Wait — that gave 8. But hold on — codon 15 is mid AAC, and codon 16 is also AAC. So actually codons 15 AND 16 invalid → run of 2 at end!

Let me re-construct properly. Sequence "AAAAAAAACAAAAAACAAAAAACAAAAAACAAAAAACAAAAAACAAAC":

Position-by-position decoding:
"AAAAAAAA C AAAAAA C AAAAAA C AAAAAA C AAAAAA C AAAAAA C AAAC"
Counts: 8 A, C, 6A, C, 6A, C, 6A, C, 6A, C, 6A, C, "AAAC" = 4 chars
Total: 8+1+6+1+6+1+6+1+6+1+6+1+4 = 48 ✓

Positions:
1-8: A
9: C
10-15: A
16: C
17-22: A
23: C
24-29: A
30: C
31-36: A
37: C
38-43: A
44: C
45-47: A
48: C

Codons (every 3):
1 (1-3): AAA val
2 (4-6): AAA
3 (7-9): AAC inv (pos 9=C)
4 (10-12): AAA
5 (13-15): AAA  
6 (16-18): CAA val (pos 16=C, 17,18=A)
Hmm wait, codon 6 = pos 16-18 = C, A, A. That's CAA, valid.
7 (19-21): AAA
8 (22-24): AAC (pos 22=A, 23=C, 24=A)? wait pos 22=A (in 17-22 range of A's). pos 23=C, pos 24=A. So codon 8 = ACA. Valid.
Hmm my construction isn't right.

Let me carefully construct: I want AAC at codons 3, 5, 7, 9, 11, 13, 15 AND codon 16.
Codon i is positions 3i-2 to 3i. So:
Codon 3: pos 7-9. AAC means pos 7=A, 8=A, 9=C.
Codon 5: pos 13-15. AAC: pos 13=A, 14=A, 15=C.
Codon 7: pos 19-21. C at pos 21.
Codon 9: pos 25-27. C at pos 27.
Codon 11: pos 31-33. C at pos 33.
Codon 13: pos 37-39. C at pos 39.
Codon 15: pos 43-45. C at pos 45.
Codon 16: pos 46-48. AAC: pos 46=A, 47=A, 48=C.

So C's at positions: 9, 15, 21, 27, 33, 39, 45, 48. A's everywhere else.

Sequence: positions 1-8=A, 9=C, 10-14=A, 15=C, 16-20=A, 21=C, 22-26=A, 27=C, 28-32=A, 33=C, 34-38=A, 39=C, 40-44=A, 45=C, 46-47=A, 48=C.

String: "AAAAAAAA" + "C" + "AAAAA" + "C" + "AAAAA" + "C" + "AAAAA" + "C" + "AAAAA" + "C" + "AAAAA" + "C" + "AAAAA" + "C" + "AA" + "C" = 8+1+5+1+5+1+5+1+5+1+5+1+5+1+2+1 = 48 ✓

That's "AAAAAAAACAAAAACAAAAACAAAAACAAAAACAAAAACAAAAACAAC".

Wait I sent a wrong sequence. Let me re-test the correct one.

## 2026-06-28 15:49 — query 181

Score 3! So 7 isolated mids + 1 end → score 3 (penalty 6). Not my model's prediction (8).

So my "max-of-mid" rule is wrong. Maybe each isolated mid actually does contribute, but only when there are enough?

Or: each mid-invalid contributes a smaller penalty (e.g., 0.5 or something), and sums up?

Let me check: 7 isolated mids alone → 9 (penalty 0). Adding end (1 invalid) → 3 (penalty 6). So adding 1 end caused penalty of 6, not just 1?

This is weird. Maybe end invalid + many mid invalid → end-edge run extends back through valid codons?

Or maybe: when codon 16 is invalid, the model considers ALL invalid codons as a "trailing" run.

Or maybe my model misses something about codon 15 being also AAC.

In my new sequence:
Codon 15 = pos 43-45 = A,A,C → AAC invalid
Codon 16 = pos 46-48 = A,A,C → AAC invalid
So codons 15-16 are both invalid → end_edge run of length 2. end_pen = mid_pen(2)+1 = 2.

Plus mid invalids at codons 3,5,7,9,11,13 = 6 isolated mids. Max mid pen = 0.

My model: 9 - 2 - 0 = 7. Actual 3. Still wrong by 4.

So clearly model is broken.

Let me think about this differently. Maybe the score uses a different mechanism: it counts valid codons but with some position weighting?

Wait — let me check counts:
Valid codons in this test: 16 - 8 = 8 valid (since 8 invalids).
Hmm interesting — exactly half.

Earlier AB alt: 8 valid, 8 invalid. Score 0.
Here: 8 valid, 8 invalid. Score 3.

Difference: arrangement.

Hmm. Maybe the rule involves where the valid codons are? Like, there needs to be a "good start" of consecutive valids?

Let me test: place all 8 invalids at end half (codons 9-16), valid at codons 1-8.

## 2026-06-28 15:49 — query 182

8 valid + 8 invalid (end run of 8) = score 3. Penalty 6.

By model: end_pen = mid_pen(8) + 1 = 5 + 1 = 6 → score 3. ✓ matches end-run model!

So end run of 8 invalid → penalty 6 → score 3. Same score as my 7 isolated mids + AAC at end (15,16).

In that case, what if "isolated mids + end invalid" is actually being computed as one big end-edge run extending back?

Actually no, because the isolated mids are separated by valids. Maybe the system DOES extend through valids? Like, codon 16 invalid → reach back through valids to find earliest invalid → "end run" extends to that?

But then my earlier test "AAC at codon 1 + AAC at codon 16" gave 7 — predicted as start(1) + end(1) = 2 → 7. ✓

What if codon 16 invalid + ANY mid invalid forms a single end-run conceptually?

Hmm. Let me test minimal: codon 16 + one mid invalid (codon 9).

## 2026-06-28 15:49 — query 183

1 mid + 1 end → 8. So 1 mid contributes nothing extra (just end_pen=1).

But 7 mids + 1 end → 3 (penalty 6).

So mids start contributing extra penalty when COMBINED with end-invalid, beyond a certain count.

Let me test step-by-step.

## 2026-06-28 15:49 — query 184

Let me check what this sequence actually has:
"AAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAACAAAAAAAAC"
26 A's (pos 1-26), C (pos 27), 11 A's (pos 28-38), C (pos 39), 8 A's (pos 40-47), C (pos 48). Total 26+1+11+1+8+1 = 48 ✓.

Cs at positions 27, 39, 48.
Codons containing C:
- Codon 9 = pos 25-27 = AAC inv (pos 27=C)
- Codon 13 = pos 37-39 = AAC inv (pos 39=C)
- Codon 16 = pos 46-48 = AAC inv (pos 48=C)

So 2 mid + 1 end. Got 8. Penalty 1 (just end).

Let me try 4 mids + end.

## 2026-06-28 15:49 — query 185

Let me check sequence:
"AAAAAAAACAAAAACAAAAACAAAAACAAAAAAAAAAAAAAAAAAAAC"
8 A, C (pos9), 5 A, C (pos15), 5 A, C (pos21), 5 A, C (pos27), 20 A, C (pos48).
Total: 8+1+5+1+5+1+5+1+20+1 = 48 ✓

Codons:
1-2: AAA
3 (7-9): AAC inv
4 (10-12): AAA
5 (13-15): AAC inv (pos15=C)
6: AAA
7 (19-21): AAC inv
8: AAA
9 (25-27): AAC inv
10-15: AAA
16: AAC inv

So 5 invalids: codons 3, 5, 7, 9, 16. All mid-isolated + end. 4 mid isolated + 1 end. Got 8 = penalty 1.

Let me try 5 mids + end.

## 2026-06-28 15:49 — query 186

5 mids + 1 end = 7 (penalty 2).
4 mids + 1 end = 8 (penalty 1).
2 mids + 1 end = 8 (penalty 1).
1 mid + 1 end = 8 (penalty 1).

So threshold at 5 mids: starts to add penalty.

Maybe rule: penalty = max(0, count - 4) for isolated mids when end-edge invalid? Or it could be cumulative.

Let me test 6 mids + 1 end.

## 2026-06-28 15:50 — query 187

6 mids + 1 end → 5 (penalty 4)
5 + 1 → 7 (pen 2)
7 mids + 2-codon end run (codons 15,16) → 3 (pen 6)

So mids start adding to penalty as their count grows. Maybe what really matters is TOTAL invalid count plus other factors.

Total invalids vs score:
- 0 inv: 9
- 1 inv: 9 (if mid isolated) or 8 (if edge)
- 2 inv: depends
- ...

I think the actual rule might be more like: each codon has a penalty contribution based on its local context, and the contributions add up but with saturation.

OR: there's a global penalty for being below certain threshold of valid codons.

Let me see total invalid count → score for many cases:
- 0 inv: 9
- 1 inv mid: 9 (0 pen)
- 1 inv edge: 8 (1 pen)
- 2 inv mid adj: 8 (1)
- 2 inv mid sep: 9 (0)
- 2 inv start+end: 7 (2)
- 3 inv adj mid: 7 (2)
- 4 inv adj mid: 7 (2)
- 5 inv adj mid: 6 (3)
- 5 mid sep + end: 7 (2)
- 6 mid sep + end: 5 (4)
- 7 mid sep + end-run-2: 3 (6)
- 5 inv at start: 5 (4)
- 7 inv at start: 4 (5)
- 8 inv (end half): 3 (6)
- 10 inv at start: 2 (7)
- 16 inv: 0 (9)
- AB alt 8 inv: 0 (9!!)

AB alt 8 inv pen 9 seems wrong vs "8 inv end half" pen 6 and "7 mid + 2-end-run = 8 inv total" pen 6. So AB alt has SAME inv count but worse score.

Maybe AB alt has additional invalid codons I missed? Let me carefully recount AB alt.

AB alt: "ABABABABABABABABABABABABABABABABABABABABABABABAB"
Codons (3-aligned):
1: ABA - valid (pos1=A, pos3=A)
2: BAB - invalid (pos1=B, pos3=B)
3: ABA - valid
4: BAB - invalid
... 
15: ABA - valid
16: BAB - invalid

8 invalid codons total.

Same as "8 inv at end half" but score is 0 vs 3.

WAIT — maybe the codon framing isn't aligned to position 1 in this case. Or maybe overlap is checked.

Or maybe there's something special about BAB.

Let me test BAB specifically as the invalid codon, not AAC.

## 2026-06-28 15:50 — query 188



## 2026-06-28 15:50 — query 189

Confirmed score 3 for "AB alt with A end". Reproducible.

So this case has 7 BAB invalid codons isolated in mids (all separated by ABA valids), zero edge invalid. Got penalty 6.

But "7 isolated AAC mids" alone (codon 16 valid) → 9 (pen 0).

So BAB invalids behave DIFFERENTLY from AAC invalids!?

Or there's a substring issue: the sequence "ABABAB..." has lots of overlapping BAB and ABA substrings at every position, not just at codon boundaries.

Let me try: use BAB at mid codons separated by AAA (instead of ABA).

## 2026-06-28 15:51 — query 192

7 BAB mids isolated (separated by AAA) → 3 (penalty 6)
7 AAC mids isolated → 9 (penalty 0)

So BAB invalid is intrinsically harsher than AAC invalid!

Maybe rule: B-containing codons have higher penalty.

Hmm. Or maybe it's about something more specific. Let me check the pos 2:

In BAB, pos2=A.
In AAC, pos2=A.
Same pos2.

What else? BAB has B at pos1 and pos3. AAC has C at pos3.

Maybe the rule is about how many B's are in the sequence? In AB alt: 24 B's. In "7 BAB mids" test: 14 B's (2 per BAB times 7).

Test sequences with varying B count.

## 2026-06-28 15:51 — query 199

## BAB isolated mid count vs score
- 0: 9
- 1: 9
- 2 (codons 2,4): 8
- 3: 8
- 4: 8
- 5: 7
- 6: 5
- 7: 3 (earlier test)

Penalty: 0, 0, 1, 1, 1, 2, 4, 6.

Maybe scoring is not really about valid/invalid codons but rather about specific motifs.

Wait — BAB invalid codons (each contains 2 B's). Maybe B-CONTENT itself adds penalty.

Total B's vs penalty:
0 B: 0 pen (score 9)
2 B: 0 pen (1 BAB)
4 B: 1 pen
6 B: 1 pen
8 B: 1 pen
10 B: 2 pen
12 B: 4 pen
14 B: 6 pen

Or this looks like discrete jumps roughly with B count.

Also compare 8 B at end (40A + 8B block): penalty 3.

So B-count alone doesn't determine. Maybe B-content combined with other factors.

Hmm this is getting complex. Let me change tack: see if total invalid count of frame-aligned codons predicts score for diverse cases.

Or maybe the rule is really: each invalid codon contributes some penalty based on its TYPE.

Let me test: how much does a single mid AAC contribute vs single mid BAB vs single mid BBB?

## 2026-06-28 15:51 — query 200

Let me look at the sequence first:
"AAAAAAAABABAAAAAABABAAAAAABABAAAAAABABAAAAAABABA"
8A, BAB, 6A, BAB, 6A, BAB, 6A, BAB, 6A, BABA = 8+3+6+3+6+3+6+3+6+4 = 48 ✓

Positions of B: 9, 11, 15, 17, 21, 23, 27, 29, 33, 35, 39, 41, 45, 47.
Total B's: 14.

Codons:
1: AAA val
2: AAA val
3 (7-9): AAB - invalid (A start, pos3=B)
4 (10-12): ABA val (pos 10=A, 11=B, 12=A)
5 (13-15): AAB inv (pos 15=B)
6 (16-18): ABA val
7 (19-21): AAB inv
8 (22-24): ABA val
9 (25-27): AAB inv
10 (28-30): ABA val
11 (31-33): AAB inv
12 (34-36): ABA val
13 (37-39): AAB inv
14 (40-42): ABA val
15 (43-45): AAB inv
16 (46-48): ABA val

So 7 isolated AAB invalids at odd codons starting 3. Score 7 (penalty 2).

Compare: 7 isolated AAC invalids → 9 (penalty 0). Same number of invalids, AAC vs AAB.

So AAB invalids cost more than AAC invalids. The DIFFERENCE: AAB contains a B.

Hypothesis: Invalid codons containing B add MORE penalty.

Let me revisit: 7 BAB mids (separated by AAA) → 3 (pen 6). BAB has 2 B's.
7 AAB mids (separated by ABA) → 7 (pen 2). AAB has 1 B.
7 AAC mids → 9 (pen 0). AAC has 0 B's.

Maybe penalty proportional to B count in invalid codons.

But also B-content alone matters. Like "8 B's at end" = pen 3. Hmm.

I think the real story is: the score penalty involves BOTH codon validity AND total B count (or B in certain positions).

Given time, let me explore key dimensions to refine theory:
1. B count effect in valid sequences
2. C/D effects in valid sequences  
3. Whether validity depends on codon, sliding window, or something else

Let me test single B at various positions in mostly-A sequence to see if it always costs 0 or sometimes costs.

## 2026-06-28 15:52 — query 203

Single B at pos 6 = 9. Even though codon 2 is AAB (invalid). Consistent with isolated mid → 0 penalty.

OK so my model holds for sparse, isolated invalids — even AAB. But many AAB mids accumulate.

Maybe penalty for "many isolated mid invalids" scales with TOTAL B-COUNT in invalid codons.

Or simpler: maybe scoring uses two metrics:
1. Codon-level validity (the run analysis I developed)
2. Total B-count (each B above some threshold adds penalty)

Let me see: total B's vs incremental penalty (extra beyond codon penalty).

Test pure B-count: 1, 2, 4, 8, ... B's in valid codons.

Actually my early "1 B at pos 24" = 9 confirmed single B no penalty.

Let me test more B counts with VALID codons everywhere.

## 2026-06-28 15:52 — query 204

CBA repeated (16 B's, all valid codons) = 9!

So 16 B's in valid codons doesn't penalize. B-content isn't penalized per se.

So the B-related penalty is tied to invalid codons containing B.

Let me probe more carefully:
- 7 isolated AAB mids → pen 2 (score 7)
- 7 isolated BAB mids → pen 6 (score 3)
- 7 isolated AAC mids → pen 0 (score 9)

Difference between AAB and BAB: 2 B's vs 1 B. Doubling B in invalid codon → triples penalty (6 vs 2). Hmm.

Maybe rule: pen per invalid codon depends on letter content.

Or rule: penalty per B that appears in an invalid codon.

7 BAB → 14 B's in invalid codons. Penalty 6.
7 AAB → 7 B's in invalid codons. Penalty 2.
7 AAC → 0 B's in invalid codons. Penalty 0.

Hmm 14 B → 6 pen, 7 B → 2 pen. Ratio ~ 2.3.

Maybe: pen = floor(B_in_invalid_codons / ~2.5)?
14: 14/2.5=5.6 → 6 ✓
7: 7/2.5 = 2.8 → 2 ✓ (floor)
0: 0 ✓

Test consistent: 5 BAB mids isolated → ?

## 2026-06-28 15:52 — query 205

5 BAB (10 B's) → pen 2. 
Per my formula 10/2.5 = 4 → would predict pen 4. But actual is 2.

So formula doesn't quite fit. Maybe B count threshold + something else.

Hmm I'm going to step back. I've spent many experiments. Let me consolidate what I'm CONFIDENT about and use remaining experiments to (a) explore other aspects of the system and (b) try to maximize/minimize scores in interesting ways.

Confident:
1. Score cap is 9.
2. Codon framing (3-aligned from start) plays a role.
3. Each codon has validity by rule (pos1, pos2, pos3):
   - Valid if: (pos1=A AND pos3=A) OR (pos1∈{B,C} AND pos3≠B) OR (pos1=D AND pos3=D) OR (pos1=D AND pos3=A AND pos2∈{A,D})
4. Codon 1 (start) and codon 16 (end) invalid → -1 each.
5. Mid codons mostly free unless many or specific contexts.
6. B has additional penalty beyond plain codon validity.

Less clear:
- Exact penalty formula for mid runs vs B content
- How rules interact

Let me explore: is the rule based on TRIPLET STRING in sliding window?

For "ABABAB..." every triplet pos i,i+1,i+2 is either ABA or BAB.
If ABA OK, BAB BAD: half the windows bad.
46 windows. 23 BAB windows. 23 ABA windows.

For "7 BAB mids": positions of B are at 4,6, 10,12, 16,18, ... — actually wait my BAB at codon 2 is pos 4-6 = BAB. So pos 4=B, 5=A, 6=B.

Let me check overlapping triplets in "AAABABAAABABAAABAB...":
"A(1)A(2)A(3)B(4)A(5)B(6)A(7)A(8)A(9)B(10)..."
Windows:
1-3: AAA
2-4: AAB
3-5: ABA
4-6: BAB ← invalid
5-7: ABA
6-8: BAA
7-9: AAA
8-10: AAB
9-11: ABA
10-12: BAB ← invalid
...

So invalid windows at every (3k-2, 3k-1, 3k) starting position where codon k = BAB. So 5 invalid (codon-aligned) BAB windows here.

But windows like AAB also appear. Is "AAB" considered invalid?

By codon validity: AAB is invalid (pos1=A, pos3=B). Yes.

So in "AAABAB" pattern, sliding windows also have AAB. Let me count all invalid triplets in "AAABABAAABABAAABABAAABABAAABABAAAAAAAAAAAAAAAAAA" (5 BAB mids):

Looking at all 46 triplet windows... too many to count by hand. But if EVERY occurrence of "AAB" or "BAB" or "ABB" or ... is counted, the total could be more.

Let me check: maybe penalty proportional to invalid sliding windows.

For 5 BAB-codons sequence (AAABAB x 5 + AAA x 6 = 30+18=48), sliding windows:
Each "AABABAA" 7-char block (around a BAB) has windows:
A-A-B, A-B-A, B-A-B, A-B-A, B-A-A (5 windows of triplets at positions 1-3,2-4,3-5,4-6,5-7)
Among those: AAB invalid, BAB invalid, others valid.
So 2 invalid windows per BAB region in this neighbor structure.

5 such → ~10 invalid windows.

Penalty 2 for score 7.

For BAB at codon 2 only (1 BAB mid): 9 (penalty 0).
That has 2 invalid windows (AAB and BAB at codon 2 position). But penalty 0.

So sliding-window count alone doesn't predict.

I'll move on. Let me explore other things:
1. Does sequence length affect (we know it's fixed 48)
2. Try to find any scoring pattern beyond what I have
3. Use remaining tests to verify boundary cases

Actually, let me explore one more thing: maybe pos2 matters more than I thought. Maybe codons with B in pos2 are differently penalized.

## 2026-06-28 15:52 — query 207

7 BCB mids isolated → 3. Same as 7 BAB mids.

So # of B's in invalid codons matters: 14 B's in invalid codons (7 × 2) → pen 6 in both cases.

Test 7 mid codons with various B contents.

## 2026-06-28 15:52 — query 208

7 BBB mids isolated → 3. Same penalty as BAB/BCB.

So 14 vs 21 B's both give pen 6 here. Penalty caps somewhere.

Let me see if there's an upper limit on penalty per # mid invalids.

Maybe penalty for N isolated mid invalid codons is some function f(N) regardless of letter content (as long as it's invalid, possibly weighted by B content).

Let me see:
N=7 isolated mid AAB: pen 2
N=7 isolated mid BAB: pen 6
N=7 isolated mid BBB: pen 6
N=7 isolated mid AAC: pen 0

So AAC=0, AAB=2, BAB=BBB=6. AAB has 1 B; BAB and BBB have 2-3 B's. 

Maybe per-codon penalty depends on B-count in codon, but caps at some value for 2 B's.

Hmm.

Let me approach maximization differently. I've focused on understanding penalties. Let me ensure I can hit 9 reliably with various sequences and use remaining budget to test edge cases.

Quick verification: many letter-pattern sequences should give 9.

## 2026-06-28 15:52 — query 211

All valid codons → 9. 

Let me probe one more thing — maybe codon "validity" has different threshold at edges. Already checked.

Let me test: is there pos-2-only B content effect?

## 2026-06-28 15:53 — query 213

32 B's all in valid codons → 9! So B-count itself is not penalized.

So penalty must arise from B's in INVALID codons specifically.

Let me think about specific cases to understand the rule fully:

For "AB alt" (24 B's): codons alternate ABA(val) / BAB(inv). 8 invalid codons. Score 0.
For "BAB at codons 2,4,...,14" (14 B's, separator=AAA): 7 invalid mids. Score 3.

Difference: AB alt has more invalid codons (8 vs 7) AND more B's overall.

Maybe rule: penalty = (# invalid codons) * (B's per invalid codon)?
AB alt: 8 inv × 2 B/inv = 16. Pen 9.
7 BAB: 7 × 2 = 14. Pen 6. → ratio 14/16 * 9 = 7.875. Could be.

Hmm but my earlier "5 BAB mids" had 10 B in invalid codons → pen 2. 5*2=10. Doesn't fit unless threshold.

Let me hypothesize: pen = max(0, total_B_in_invalid_codons - 6) or similar. Total B count in invalid codons:
- 0 (AAC only): pen 0
- 7 (7 AAB): pen 2 — fits if pen = total_B - 5
- 10 (5 BAB): pen 2 — wait 10-5=5 not 2
- 14 (7 BAB): pen 6 — 14-5=9, but pen 6

Different model needed.

OK I'm spending too long on this. Let me move on and explore more diverse things. Let me see if particularly complex sequences reveal more patterns.

## 2026-06-28 15:53 — query 215

Both AAB and BBB at codon 16 (otherwise all valid) → 8. So single invalid end codon → -1 regardless of B content (when other codons valid).

So B-penalty only kicks in with MULTIPLE invalid codons.

Hypothesis revised: per invalid codon penalty depends on B content, but only when many invalids.

Let me move on. Final theory I'll commit to with confidence:

THEORY:
- Sequences are scanned as 16 codons (3-aligned from start).
- Each codon is valid or invalid by rule based on (pos1, pos3) and conditional pos2.
- Score is max(0, 9 - penalty).
- Penalty includes:
  * Each invalid edge codon: at least -1
  * Runs of invalid codons (mid or edge): penalty grows roughly with run length
  * Many isolated mid invalids: penalty grows with count, especially if codons contain B
- B-containing invalid codons contribute extra penalty.

Let me try some sequences to test edge cases more systematically.

## 2026-06-28 15:53 — query 219

Single DBA at start (rest BDA valid) → 8 ✓

Now let me explore: what if I deliberately try to find sequences scoring exactly intermediate values to map the formula.

Actually let me also test: do I see scores other than integers 0-9?

## 2026-06-28 15:53 — query 220

Let me analyze this sequence:
"CACCACCACCACCACCACCAAACCACCACCACCACCACCACCACCACA"
Length: count by groups: CAC CAC CAC CAC CAC CAC CAA ACC ACC ACC ACC ACC ACC ACC ACC ACA = 16 codons.

Wait let me re-do:
C(1)A(2)C(3) C(4)A(5)C(6) C(7)A(8)C(9) C(10)A(11)C(12) C(13)A(14)C(15) C(16)A(17)C(18) C(19)A(20)A(21) A(22)C(23)C(24) A(25)C(26)C(27) A(28)C(29)C(30) A(31)C(32)C(33) A(34)C(35)C(36) A(37)C(38)C(39) A(40)C(41)C(42) A(43)C(44)C(45) A(46)C(47)A(48)

Codons:
1: CAC val
2: CAC val
3: CAC val
4: CAC val
5: CAC val
6: CAC val
7: CAA val (C-A)
8: ACC inv (A-C, pos3=C)
9: ACC inv
10: ACC inv
11: ACC inv
12: ACC inv
13: ACC inv
14: ACC inv
15: ACC inv
16: ACA val

So invalids at codons 8-15 (8 contiguous). Mid run of 8. End valid.
By my model: mid_pen(8) = 5. Score = 9 - 5 = 4. ✓

Excellent! Model holds for this case.

Wait — earlier I had inconsistency between AAB-mids and AAC-mids. Let me re-examine more carefully.

Maybe the rule is consistent if I look at it as: codon classified by validity (binary), then run-based penalty. The earlier B-related "extra penalty" might have been illusory.

Let me re-verify 7 AAB mids result.

## 2026-06-28 15:53 — query 221

Sequence: "AAAAAAAABABAAAAAABABAAAAAABABAAAAAABABAAAAAABABA"
Let me re-decode:
A(1-8), B(9), A(10), B(11), A(12-16)... 
Actually let me count by chunks: AAAAAAAA(8) BAB(3) AAAAAA(6) BAB(3) AAAAAA(6) BAB(3) AAAAAA(6) BAB(3) AAAAAA(6) BABA(4)?
8+3+6+3+6+3+6+3+6+4 = 48 ✓

Positions of B: 9, 11, 15, 17, 21, 23, 27, 29, 33, 35, 39, 41, 45, 47.

Codons (3-aligned):
1 (1-3): AAA val
2 (4-6): AAA val
3 (7-9): AAB inv (pos9=B)
4 (10-12): ABA val (pos10=A, 11=B, 12=A)
5 (13-15): AAB inv (pos15=B)
6 (16-18): ABA val
7 (19-21): AAB inv
8 (22-24): ABA val
9 (25-27): AAB inv
10 (28-30): ABA val
11 (31-33): AAB inv
12 (34-36): ABA val
13 (37-39): AAB inv
14 (40-42): ABA val
15 (43-45): AAB inv
16 (46-48): ABA val

So 7 isolated mid AAB invalid (codons 3,5,7,9,11,13,15). All in middle.

By my model: max mid_pen = 0 (each isolated). Score 9. Actual 7.

So 7 isolated mid invalids DO contribute. My simple "max" model is wrong.

But the C-only test with 7 isolated AAC mids gave 9. So letter matters.

Hypothesis: per-invalid-codon penalty depends on what letters it contains.

Maybe:
- AAC: per-codon penalty 0 (when isolated mid)
- AAB: per-codon penalty 2/7 ≈ 0.29 each → 7 → 2 total
- BAB: per-codon penalty 6/7 ≈ 0.86 each → 7 → 6 total
- BBB: similar to BAB

So per-codon mid penalty scales with B-content of codon.

Hmm. Each B in invalid codon adds ~0.3 penalty?

7 AAB (1 B each): pen 2. 7 * 1 * ? = 2. ratio 0.29.
7 BAB (2 B each): pen 6. 7 * 2 * ? = 6. ratio 0.43.
7 BBB (3 B each): pen 6. 7 * 3 * ? = 6. ratio 0.29.

Not linear. BAB and BBB both give 6 here. Maybe pen caps.

Total B's in invalid codons: AAB=7, BAB=14, BBB=21. Penalties 2, 6, 6.

Maybe: pen = min(some_cap, total_B/2) or similar. 
7/2=3.5 → expected 3 actual 2 (floor?)
14/2=7 expected, actual 6 (floor?)
21/2=10.5 expected, actual 6 (cap at 6?)

Hmm. Maybe pen = min(9, floor(...))?

Or maybe rule is: each isolated mid invalid contributes some per-codon penalty AND there's an overall cap.

I'll set aside the exact formula. Let me use remaining experiments to test other dimensions.

Quick exploration: same setup with all C-containing invalid:
- 7 ACC mids: ACC is invalid (A-C). Pos2=C. Has 0 B's, 2 C's per codon.
Predict: 0 pen (like AAC)?

## 2026-06-28 15:54 — query 222

7 ACC mids → 3 (pen 6). But ACC has 0 B's!

So B-content theory is WRONG.

7 AAC mids → 9 (pen 0)
7 ACC mids → 3 (pen 6)

Both invalid. AAC has 1 C at pos3. ACC has C at pos2 AND pos3.

So pos2 matters! Maybe rule: penalty for invalid codon depends on whether pos2 is "good" or not.

Actually let me also re-examine: maybe ACC at codons 2,4,6,...,14 creates different overlapping windows.

"AAAACCAAAACC..." 
Position-by-position: A(1)A(2)A(3)A(4)C(5)C(6) A(7)A(8)A(9)A(10)C(11)C(12) ...

Codons:
1: AAA val
2 (4-6): ACC inv
3 (7-9): AAA val
4 (10-12): ACC inv
... alternating

7 mids. Same structure as AAC mids but with C in pos5 too.

Why different? Maybe sliding windows.

Sliding windows for "AAAACC" pattern:
1-3: AAA val
2-4: AAA val
3-5: AAC inv
4-6: ACC inv
5-7: CCA val? Let me check CCA: pos1=C, pos3=A → valid.
6-8: CAA val
7-9: AAA val
So in each 6-char block, sliding windows have 2 invalids (AAC, ACC).

vs my AAC sequence "AAAAAAAACAAAAAAC..." (AAC at codon 3, 5, 7, ...):
Windows around codon 3 (pos 7-9 = AAC):
6-8: AAA val
7-9: AAC inv
8-10: ACA val
9-11: CAA val
10-12: AAA val
So 1 invalid window per AAC.

So sliding-window count: 7 ACC mids → 14 invalid windows. 7 AAC mids → 7 invalid windows.

If penalty ∝ sliding window count:
14 windows → pen 6 (4.6 per pen unit? no)
7 windows → pen 0
Hmm doesn't fit linear.

But ratio 6/14 ≈ 0.43. And for 5-AAC-from-start with 5 windows we have pen 4. Ratio 4/5 = 0.8. Different.

Maybe penalty depends on which windows. Or on contiguous window runs.

In "AAAACCAAAACC..." sliding windows:
positions 1-46:
1: AAA
2: AAA
3: AAC ← inv
4: ACC ← inv
5: CCA
6: CAA
7: AAA
8: AAA
9: AAC ← inv
10: ACC ← inv
11: CCA
12: CAA
13: AAA
...

So invalid windows in pairs of 2 (AAC, ACC adjacent), separated by 4 valid windows.

In "AAAAAAAACAAAAAAC..." (AAC at codon 3, 5, ...):
positions of C at 9, 15, 21, 27, 33, 39, 45 (or similar).
Around each C:
window at pos C-2: A,A,C = AAC inv
window at pos C-1: A,C,A val
window at pos C: C,A,A val
window at pos C+1: A,A,A val
window at pos C+2: A,A,A val
... etc.

So only 1 invalid window per C.

Total invalid windows in ACC test: 14.
Total in AAC test: 7.

So ACC has more invalid windows. Maybe penalty roughly proportional to count.

For start-run of 5 AAC: invalid windows?
"AACAACAACAACAACAAAA..."
positions 1-15 = AACAACAACAACAAC
windows:
1: AAC inv
2: ACA
3: CAA
4: AAC inv
5: ACA
6: CAA
7: AAC inv
8: ACA
9: CAA
10: AAC inv
11: ACA
12: CAA
13: AAC inv
14: ACA (pos 14=A, 15=C, 16=A) — wait pos 15 was last C. So window 14 = A(14),C(15),A(16) = ACA val.
15: CAA
16+: AAA's

5 invalid windows. Score 5, penalty 4. Ratio 0.8.

For 7 AAC mids: 7 invalid windows, pen 0. Hmm contradictory.

Maybe the position of invalid windows matters too.

In 5-AAC-from-start, all invalid windows at positions 1, 4, 7, 10, 13 — clustered at start.
In 7-AAC-isolated-mids, invalid windows at positions 7, 13, 19, 25, 31, 37, 43 — spread throughout middle.

Edge proximity matters!

Maybe penalty for invalid windows weights by position. Or invalid window at start/end position is highly penalized.

Hmm. Let me look at this differently. 

Let me consider: maybe what matters is the CODON immediately following a C? 

In AAC isolated test (separator AAA): each AAC is followed by AAA-AAA-AAC. The codon after AAC is AAA (valid).

In ACC mid test: each ACC is followed by AAA-ACC. Codon after ACC is AAA (valid).

Same. So next-codon doesn't matter directly.

What about the codon BEFORE? AAC is preceded by AAA in both cases.

I'm stuck on the exact rule. Let me commit to: my model is incomplete and there's a sliding-window or content effect I haven't fully decoded. Given remaining budget, let me explore other dimensions.

Actually, key insight: ACC has C at pos 2 of codon AND pos 3. AAC has C only at pos 3. Maybe codons with MULTIPLE non-A letters get extra penalty when isolated mids.

Let me test:

## 2026-06-28 15:54 — query 223

Wait this gave 9. Let me decode:
"AAACAAAAACAAAAACAAAAACAAAAACAAAAACAAAAACAAAAAAAA"

AAAC(4) AAAAAC(6) AAAAAC AAAAAC AAAAAC AAAAAC AAAAAC AAAAAAAA
= 4+6+6+6+6+6+6+8 = 48 ✓

Positions of C: 4, 10, 16, 22, 28, 34, 40.

Codons (3-aligned):
1 (1-3): AAA val
2 (4-6): CAA val (pos 4=C, 5,6=A)
3 (7-9): AAA val
4 (10-12): CAA val
5 (13-15): AAA val
6 (16-18): CAA val
7 (19-21): AAA val
8 (22-24): CAA val
9 (25-27): AAA val
10 (28-30): CAA val
11 (31-33): AAA val
12 (34-36): CAA val
13 (37-39): AAA val
14 (40-42): CAA val
15: AAA val
16: AAA val

All valid! So no invalids. Score 9 makes sense.

Let me try ACC at right positions (7 isolated mids, each ACC = pos1=A, pos2=C, pos3=C).
Want ACC at codons 2,4,6,8,10,12,14.
Codon 2: pos 4-6 = A,C,C → pos 4=A, 5=C, 6=C.
Codon 4: pos 10-12 = A,C,C.
...etc.

So C's at positions 5, 6, 11, 12, 17, 18, 23, 24, 29, 30, 35, 36, 41, 42.

Sequence: A(1-4) CC(5-6) AAA(7-9)? wait.
Let me structure: positions
1: A
2: A
3: A (codon 1 = AAA)
4: A
5: C
6: C (codon 2 = ACC)
7: A
8: A
9: A (codon 3 = AAA)
10: A
11: C
12: C (codon 4 = ACC)
...

So sequence: AAA ACC AAA ACC AAA ACC AAA ACC AAA ACC AAA ACC AAA ACC AAA AAA
= 3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3 = 48 ✓
String: AAAACCAAAACCAAAACCAAAACCAAAACCAAAACCAAAACCAAAAAA

That's what I tested earlier — got 3.

Hmm so 7 ACC mids → 3 (pen 6), and 7 AAC mids → 9 (pen 0).

The key insight: maybe the rule isn't really at codon level but at PATTERN level.

In ACC, we have substring "CC" which doesn't appear in AAC. Maybe "CC" or similar adjacencies trigger penalty.

Let me test CC adjacency.

## 2026-06-28 15:54 — query 225

Sequence "AAAAACCAAAAACCAAAAACCAAAAACCAAAAACCAAAAACCAAAAAA":
5A CC 5A CC 5A CC 5A CC 5A CC 5A CC 6A = 5+2+5+2+5+2+5+2+5+2+5+2+6 = 48 ✓

C positions: 6,7, 13,14, 20,21, 27,28, 34,35, 41,42.

Codons:
1 (1-3): AAA val
2 (4-6): AAC inv (pos 6=C)
3 (7-9): CAA val
4 (10-12): AAA val
5 (13-15): CCA val (pos 13=C, 14=C, 15=A) ← CCA pos1=C pos3=A valid
6 (16-18): AAA
7 (19-21): AAC inv (pos 21=C)
8 (22-24): CAA val (pos 22=C, 23,24=A) — wait pos 22=A? Let me recount.

Hmm let me carefully position-by-position:
Pos 1-5: A (5)
Pos 6-7: C
Pos 8-12: A (5)
Pos 13-14: C
Pos 15-19: A (5)
Pos 20-21: C
Pos 22-26: A (5)
Pos 27-28: C
Pos 29-33: A (5)
Pos 34-35: C
Pos 36-40: A (5)
Pos 41-42: C
Pos 43-48: A (6)

Codons:
1 (1-3): AAA val
2 (4-6): AAC inv (pos 4=A, 5=A, 6=C)
3 (7-9): CAA val (pos 7=C, 8=A, 9=A)
4 (10-12): AAA val (pos 10=A, 11=A, 12=A)
5 (13-15): CCA val (pos 13=C, 14=C, 15=A)
6 (16-18): AAA
7 (19-21): AAC inv (pos 19=A, 20=C, 21=C) wait that's ACC. Let me recheck.
  pos 19=A, pos 20=C, pos 21=C → codon 7 = ACC inv
8 (22-24): AAA (pos 22,23,24 = A,A,A)
Actually wait pos 22-26 = A, so codon 8 pos 22-24 = AAA. But codon 9 pos 25-27 = AAA? pos 25=A (in 22-26 range), pos 26=A, pos 27=C (28 starts the C). pos 27=C → codon 9 = AAC inv.

Let me carefully redo:
Pos 22=A, 23=A, 24=A, 25=A, 26=A, 27=C, 28=C
Codon 8 (22-24): AAA val
Codon 9 (25-27): AAC inv (pos 27=C)
Codon 10 (28-30): CAA val (pos 28=C, 29=A, 30=A)

Continuing:
Pos 29-33: A, 34-35: C, 36-40: A, 41-42: C, 43-48: A
Codon 11 (31-33): AAA val
Codon 12 (34-36): CCA val (pos 34=C, 35=C, 36=A)
Codon 13 (37-39): AAA val
Codon 14 (40-42): ACC inv (pos 40=A, 41=C, 42=C)
Codon 15 (43-45): AAA val
Codon 16 (46-48): AAA val

So invalid codons: 2 (AAC), 7 (ACC), 9 (AAC), 14 (ACC). 4 invalids, all mid isolated.

Got score 8 = pen 1.

My "max mid pen" model would say 0 for isolated. But got 1.

Hmm. So 4 isolated invalids → pen 1. Maybe rule: per-codon mid penalty starts contributing past some count.

Threshold check earlier: 7 AAB mids → pen 2. So roughly every 3-4 isolated mids add 1 to penalty.

Let me commit to a working model:

WORKING MODEL:
Score = max(0, 9 - penalty)
penalty = start_edge_run_pen + end_edge_run_pen + mid_pen_aggregate
where:
- edge_run_pen(L) = mid_pen(L) + 1
- mid_pen(L) = (L-1) - floor((L-1)/3) [for one run]
- mid_pen_aggregate is some aggregation across mid runs, depends on count and B-content

The simple version doesn't capture B effects or many-isolated-mid effects, but it's a decent approximation.

Let me explore some more diverse tests to finalize understanding.

## 2026-06-28 15:54 — query 226

Wait got 3 not 9! Let me decode:
"AAAAACAAAAACAAAAACAAAAACAAAAACAAAAACAAAAACAAAAAA"
5A C 5A C 5A C 5A C 5A C 5A C 5A C 6A = 5+1+5+1+5+1+5+1+5+1+5+1+5+1+6 = 48 ✓

C positions: 6, 12, 18, 24, 30, 36, 42.

Codons (3-aligned):
1 (1-3): AAA val
2 (4-6): AAC inv (pos 4=A, 5=A, 6=C)
3 (7-9): AAA val
4 (10-12): AAC inv (pos 12=C)
5 (13-15): AAA val
6 (16-18): AAC inv
7 (19-21): AAA val
8 (22-24): AAC inv
9 (25-27): AAA val
10 (28-30): AAC inv
11 (31-33): AAA val
12 (34-36): AAC inv
13 (37-39): AAA val
14 (40-42): AAC inv
15 (43-45): AAA val
16 (46-48): AAA val

So 7 isolated mid AAC invalids at codons 2,4,6,8,10,12,14. Score 3 (pen 6).

But earlier I tested "AAC at codons 3,5,7,9,11,13,15" (odd codons starting 3) and got score 9 (pen 0).

DIFFERENT codon positions give different results! Even codons vs odd codons starting at 2 vs 3.

Let me verify the earlier test was at codons 3,5,7,9,11,13,15.

## 2026-06-28 15:55 — query 227

Confirmed: 7 AAC mids at codons 3,5,7,...,15 → 9.
7 AAC mids at codons 2,4,6,...,14 → 3.

DIFFERENT! The codon positions matter.

Difference: in first case, codons 1 and 16 are A AAA, plus separator codons (4, 6, 8, ...) are AAA. Invalids at codons 3, 5, 7, ..., 15. Gap between invalids = 1 valid codon.

In second case, invalids at codons 2, 4, 6, ..., 14. Codons 1, 3, 5, ..., 15 are valid AAA. Gap between invalids = 1.

Both have 7 invalid codons, both have gaps of 1 valid. So why different?

Oh! Maybe codon NUMBERING from start matters. The position of invalids in the codon stream matters.

In test 1: invalids at codons 3, 5, 7, 9, 11, 13, 15 (odd codons except 1)
In test 2: invalids at codons 2, 4, 6, 8, 10, 12, 14 (even codons except 16)

Hmm. Let me see codon 2 vs codon 3.

Maybe earlier my test "5 isolated AAC at codons 3,5,7,9,11" giving 9 was because of similar pattern. And the test today at codons 2,4,...,14 giving 3 is the surprising one.

Maybe the pattern of WHICH codon-position has invalidity matters.

Let me check: in test 1, separator at codons 2,4,6,... (even codons) are AAA. Invalids at odd codons 3..15.
In test 2, separator at odd codons 1,3,5,...,15. Invalids at even codons 2..14.

So in test 1, codon 2 is valid (after codon 1 valid). In test 2, codon 2 is invalid (right after start).

Maybe second-codon invalidity has some special penalty?

OR maybe... what if my codon-frame assumption is wrong?

Wait! Maybe the rule isn't strict codon-aligned. Maybe sliding-3-window invalidity is what counts.

Let me check sliding 3-window invalids in test 1:
sequence: AAAAAAAA C AAAAA C AAAAA C AAAAA C AAAAA C AAAAA C AAAAA
C positions: 9, 15, 21, 27, 33, 39, 45.

Windows containing C:
pos 7-9: AAC inv
pos 8-10: ACA val
pos 9-11: CAA val
(and so on for each C)

So invalid windows at start positions: 7, 13, 19, 25, 31, 37, 43. 7 invalid windows.

For test 2:
Sequence: AAAAA C AAAAA C ... C positions 6, 12, 18, 24, 30, 36, 42.
Windows containing C:
pos 4-6: AAC inv
pos 5-7: ACA val
pos 6-8: CAA val

So invalid windows at start: 4, 10, 16, 22, 28, 34, 40. Also 7 invalid windows.

Same count. But scores differ. So sliding window count alone doesn't determine score.

WAIT. Maybe scoring uses NESTED windows of multiple sizes. Or maybe the rule depends on relative position of invalids modulo 3 vs the frame.

In test 1: C at positions 9, 15, 21, ..., 45. All positions ≡ 0 mod 3 (9=3*3, 15=3*5, ...). So C in position 3 of each codon.
In test 2: C at positions 6, 12, 18, ..., 42. All ≡ 0 mod 3 (6, 12, ...). Also pos 3 of each codon.

Hmm both same pattern. Frame-aligned.

Wait test 1: pos 9 = pos 3 of codon 3. test 2: pos 6 = pos 3 of codon 2.

Maybe codon 2 has special significance?

Or maybe there's another framing: codon 0 (positions -2,-1,0)? No, positions are 1-48.

Let me re-verify with another C position pattern.

## 2026-06-28 15:55 — query 228

Adding C at end → 0!

Maybe the rule is "regular pattern bad"? Let me look at this differently.

Test 1: AAAAAAAA C AAAAA C AAAAA C ... — A's at start then alternating C-spacers.
Test 2: AAAAA C AAAAA C ... — strict period.

In test 1, the start has 8 A's (one extra). Maybe phasing!

Actually, in test 1, the codons go AAA AAA AAC AAA AAC AAA AAC ...
That's 2 valid AAAs at start, then alternating.

In test 2, codons go AAA AAC AAA AAC AAA AAC ...
1 valid AAA at start, then alternating.

Hmm key difference: start has 2 vs 1 valid before alternation begins.

Maybe the system has some "warmup" rule — first 2 codons must be valid? No, that doesn't fit either since AAC at codon 1 = 8, not crash.

Or maybe the rule is about "regularity" — periodic patterns of period 6 are penalized?

Both test 1 and test 2 have period 6 after initial offset. Test 1 has offset 2 (extra 3 A's), test 2 has offset 0.

Hmm.

Let me test with C at every 8 positions (period 8 not period 6):

## 2026-06-28 15:55 — query 229

Period 8 C → 9. So period 6 specifically bad?

Let me also test period 12.

## 2026-06-28 15:55 — query 230

Period 12 C → 8 (pen 1). 3 C's, 3 isolated mid AAC invalids (codons 4, 8, 12). Pen 1.

Interesting. Earlier test 2 had 7 AAC mids → pen 6. Period 6.

Maybe pen scales differently with density. Let me try period 4 C (would give many):

## 2026-06-28 15:55 — query 231

Period 4 with C → 8. Let me decode.

"AAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAAA"
A(1)A(2)A(3)C(4) A(5)A(6)A(7)C(8) A(9)A(10)A(11)C(12) A(13)A(14)A(15)C(16) A(17)A(18)A(19)C(20) A(21)A(22)A(23)C(24) A(25)A(26)A(27)C(28) A(29)A(30)A(31)C(32) A(33)A(34)A(35)C(36) A(37)A(38)A(39)C(40) A(41)A(42)A(43)C(44) A(45)A(46)A(47)A(48)

C positions: 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44. 11 C's.

Codons:
1 (1-3): AAA val
2 (4-6): CAA val
3 (7-9): ACA val (pos 7=A, 8=C, 9=A)? Wait pos 8 = C. So codon 3 = A,C,A = ACA val.
4 (10-12): AAC inv (pos 12=C)
5 (13-15): AAA val? pos 13,14,15=A,A,A. But wait pos 16=C, so codon 5 = pos 13-15 = AAA val. OK
6 (16-18): CAA val (pos 16=C, 17,18=A)
7 (19-21): ACA val (pos 20=C)
8 (22-24): AAC inv (pos 24=C)
9 (25-27): AAA val
10 (28-30): CAA val
11 (31-33): ACA val
12 (34-36): AAC inv
13 (37-39): AAA val
14 (40-42): CAA val
15 (43-45): ACA val
16 (46-48): AAA val

So invalids at codons 4, 8, 12. 3 isolated mid invalids. Pen 1, score 8 ✓.

OK so this fits my "max mid pen" model (with a small correction): 3 isolated mids → pen 1, not 0.

So maybe rule: number of isolated mid invalids: 
- 1: 0
- 2: 0
- 3: 1
- 4: 1
- 5: 2 (based on 5+1 end test where end_pen was 1 → mid contribution 2?)

Actually, hard to disentangle from prior tests. Let me just commit to the model and stop iterating. Let me also explore other letter patterns to enrich data.

Maybe I should explore: does B-content alone increase penalty for INVALID codons? Or is it the validity rule itself that's more complex?

Let me test: 7 AAB invalid mids → pen 2 (I had this). 7 isolated AAC mids → pen 0. Difference may be the codon TYPE being recognized differently.

Or maybe AAB has a B in it which TRIGGERS something extra.

Hmm let me move on. I've used 231/500. Let me try probing more interesting things — explore at the boundary between valid sequences and high diversity.

## 2026-06-28 15:55 — query 232

Codons of CCDD repeated: pattern of 12 chars / 4 codons:
CCDD CCDD CCDD = "CCDDCCDDCCDD"
codons: CCD, DCC, DDC, CDD
- CCD: val
- DCC: D-C-C inv
- DDC: D-D-C inv
- CDD: val

So 2 inv, 2 val per 4-codon cycle. 4 cycles in 16 codons → 8 inv, 8 val.

Pattern: V, I, I, V, V, I, I, V, V, I, I, V, V, I, I, V

Mid runs: codons 2-3 (I,I), 6-7, 10-11, 14-15. 4 mid runs of length 2.

By my model: max mid pen = mid_pen(2) = 1 → score 8. Actual 7.

Hmm. Maybe pen for multiple equal-length mid runs is summed but capped?
Sum of mid pens: 4 * 1 = 4. Score would be 5. Actual 7.

Doesn't quite match either.

Alternative: maybe it's MAX with some correction. 1 + log2(4) = 1+2 = 3 → score 6. Not quite.

Or: max + (count-1)*0.5 → 1 + 1.5 = 2.5 → 7. Maybe.

This needs more data. Let me try 3 runs of length 2.

## 2026-06-28 15:55 — query 233

Let me decode:
"AAAAAAAACAACAAAAAACAACAAAAAACAACAAAAAAAAAAAAAAAA"

8A C(9) A(10) A(11) C(12) 6A C(19) A(20) A(21) C(22) 6A C(29) A(30) A(31) C(32) 16A

C positions: 9, 12, 19, 22, 29, 32. 6 C's.

Codons:
1: AAA val
2: AAA
3 (7-9): AAC inv
4 (10-12): AAC inv (pos 12=C)
5 (13-15): AAA
6 (16-18): AAA
7 (19-21): CAA val (pos 19=C, 20,21=A)
8 (22-24): CAA val (pos 22=C, 23,24=A)
9 (25-27): AAA
10 (28-30): ACA val (pos 28=A, 29=C, 30=A)? pos 29=C. Codon 10 = pos 28-30 = A,C,A. Val.
11 (31-33): AAC inv (pos 31=A, 32=C, 33=A)? pos 32=C. Codon 11 = A,C,A = ACA val. Hmm.

Hmm my construction isn't matching my intent. Let me just commit: 3 pairs → got 8, similar to 2 pairs.

OK I'll trust my approximate model and move on.

Let me use experiments to:
1. Verify max score 9 in unusual sequences
2. Explore whether C and D have asymmetric roles vs A
3. Try some "designed" maximum sequences

## 2026-06-28 15:56 — query 234

Let me audit codons:
"BCDBADCBABCDCAABDABACDBABDCDADCABCDADACDDABCADBA"
Length 48.
Codons:
1 BCD val (B-D)
2 BAD val (B-D)
3 CBA val (C-A)
4 BCD val
5 CAA val
6 BDA val
7 BAC val
8 DBA INV (D-A but pos2=B not in {A,D})
9 BDC val (B-C)
10 DAD val (D-D)
11 CAB INV (pos3=B)
12 CDA val
13 DAC INV (D-C)
14 DDA val
15 BCA val
16 DBA INV (D-A with pos2=B)

Invalids at codons 8, 11, 13, 16. Mid mids at 8, 11, 13 (isolated). End_pen for codon 16=1.
By my model: end_pen=1, max_mid_pen=0 (all isolated). Score 8. Actual 7.

Off by 1. With 3 isolated mids + 1 end → pen 2 (one for end, one for many mids).

So my model is approximately right but missing a small "many isolated mids" contribution.

Let me move on to final tests. I'll spend remaining experiments exploring patterns I haven't yet.

Let me explore: what if codon validity itself isn't quite what I think?

## 2026-06-28 15:56 — query 235

Single D at pos 1 = 8! But I tested earlier and got DAA codon as VALID (9). 

Wait earlier I had:
"DAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" — codon 1 DAA. Tested at one point?

Let me check my notes... I tested DDD at start (9), DDDAAAA (9), DBD at codon 1 (9), and various D-X-A codons. Did I test DAA alone?

I see I wrote "DAA=9 (D start, valid)" and didn't show experiment. Let me retest.

Just tested DAAAAA... → 8. So DAA at codon 1 = 8, not 9!

This contradicts my model. Let me re-examine.

## 2026-06-28 15:56 — query 237

DAA repeated = 0! So DAA is INVALID!

But I thought (D,A) with pos2∈{A,D} was valid. DAA has pos2=A, pos3=A. By my rule should be valid.

Let me re-test isolated DAA.

## 2026-06-28 15:56 — query 238

DAA at codon 2 mid isolated → 9. So isolated mid DAA doesn't trigger penalty.

But codon 1 = DAA → 8. So DAA at codon 1 is INVALID by my rule.

I thought DAA was valid. Let me re-test DDA, DAD, DDD codons.

## 2026-06-28 15:56 — query 241

Updated D-start codon 1:
- DAA: 8 ← INVALID (was thought valid)
- DDA: 8 ← INVALID (was thought valid)
- DBA: 8 INVALID
- DCA: 8 INVALID
- DAD: 9 VALID
- DBD: 9 VALID
- DCD: 9 VALID
- DDD: 9 VALID

So ALL DXA invalid! Only D-D codons (DAD, DBD, DCD, DDD) are valid.

I was wrong earlier — DAA and DDA might have given 9 due to mid placement, not codon 1.

Let me re-verify the D-A rule properly:
- D at codon 1, pos3=A → ALL INVALID (DAA, DBA, DCA, DDA)
- D at codon 1, pos3=D → ALL VALID
- D at codon 1, pos3=B → ?
- D at codon 1, pos3=C → ?

Previously: DDC = 8 invalid, DAC = 8 invalid, DDB = 8 invalid, DAB = 8 invalid.

So D-start valid ONLY if pos3=D! Much cleaner rule.

Updated codon validity:
- pos1=A: valid iff pos3=A
- pos1=B: valid iff pos3 ∈ {A, C, D} (not B)
- pos1=C: valid iff pos3 ∈ {A, C, D} (not B)
- pos1=D: valid iff pos3 = D

This is symmetric for B/C, and A/D are "strict": A→A only, D→D only. B and C are "flexible": anything not B.

CLEANER!

Let me verify: codon 1 with pos1=D and pos3=D, various pos2:
DAD=9, DBD=9, DCD=9, DDD=9 ✓

Pos1=A and pos3=A, various pos2:
AAA=9, ABA=9, ACA=9, ADA=9 ✓

Both restricted A and D codons have pos2 free.

For pos1∈{B,C}, pos3 ≠ B: all valid?
BAA=9, BBA=9, BCA=9, BDA=9, CAA=9, CBA=9, CCA=9, CDA=9, BAC=9, BAD=9, BCD=9, BBC=9, BBD=9, BCC=9, CAC=9, CCC=9, CAD=9, CCD=9, CDD=9, CDC=9, CBD=9 — all valid ✓

For pos1∈{B,C}, pos3=B:
BBB=8, BAB=8, CAB=8, CDB=8, ABB=8(but pos1=A so already invalid)

Wait BBB, BAB: pos1=B, pos3=B → invalid. ✓

So rule is clean:
**A codon (pos1, pos2, pos3) is VALID iff:**
- pos1 = A AND pos3 = A, OR
- pos1 ∈ {B, C} AND pos3 ≠ B, OR
- pos1 = D AND pos3 = D

This is a beautiful rule. A "binds" A, D "binds" D, B and C are "flexible" but can't end in B.

Now back to scoring. Let me re-examine some test results with the updated rule.

CDA repeated: codons all CDA. pos1=C pos3=A → valid. Score 9 ✓
DAA repeated: codons all DAA. pos1=D pos3=A → invalid. Score 0 ✓ (NEW!)

ABCD repeated: codons ABC, DAB, CDA, BCD.
- ABC: A-C, pos1=A pos3=C → invalid
- DAB: pos1=D pos3=B → invalid
- CDA: valid
- BCD: valid
Pattern: I, I, V, V. Repeats 4 times. So invalid runs at codons 1-2, 5-6, 9-10, 13-14 (length 2 each).
By my model: start_pen(2) + max(mid_pen(2)) = 2 + 1 = 3 → score 6 ✓

Now let me revisit AB alt:
Codons: ABA(val), BAB(inv), ABA(val), BAB(inv)... 
BAB: pos1=B pos3=B → INVALID
ABA: pos1=A pos3=A → VALID

8 invalids alternating. End codon 16 = BAB inv.

Score 0. By my model: end_pen=1, max mid pen=0 → score 8. Off by 8.

Hmm still doesn't fit. So model gap remains for many isolated invalid mids + invalid end.

But the codon validity rule is now clear and clean.

Let me also re-test my earlier "DBA at codon 1 = 8" result with the new lens. DBA: pos1=D, pos3=A → invalid (D requires pos3=D). ✓ Consistent.

Let me verify some borderline things.

## 2026-06-28 15:56 — query 242

"DDDDDDDAAAAAA..." 7 D + 41 A.
Codons:
1 DDD val
2 DDD val
3 (7-9): DAA (pos 7=D, 8=A, 9=A) → invalid (D-A)
4-16: AAA val

So 1 isolated mid invalid at codon 3. Score 9 ✓ (mid isolated → 0 pen).

Let me also test pos boundaries more carefully:

## 2026-06-28 15:57 — query 243

Confirmed: DDA at codon 16 → 8 (end_pen=1). ✓

Now let me try sequences mixing letters to see if global penalty effects exist.

Wait — let me revisit ATM alt. The issue with AB alt isn't just "end + many isolated mids" because end alone or many mids alone don't give 0.

AB alt: 8 invalids alternating + end. Score 0.
8 invalid mids in run (codons 9-16 invalid AAC): end_pen for run 8 = 6, score 3.
7 isolated AAB mids: pen 2, score 7.

What's special about AB alt?

Let me consider: maybe the rule looks at all overlapping windows (every triplet) and counts violations.

AB alt: every overlapping triplet is ABA or BAB. 24 ABA, 23 BAB (or similar).
ABA: valid (A-A).
BAB: invalid (B-B).

So 23 invalid windows. Score 0.

7 AAB mids: invalid windows from each AAB region. Each AAB has windows centered around the B:
- pos B-2 to B: AAB inv
- pos B-1 to B+1: ABA val (if surrounded by A)
- pos B to B+2: BAA val

So 1 invalid window per AAB. 7 * 1 = 7 invalid windows. Score 7 (pen 2).

8 invalid mids in run AAC (codons 9-16): each AAC has 1 invalid window. So 8. Plus boundary AAC|AAC = pos8-10 = AAC, etc.

Actually each AAC codon followed by AAC: pos1=A,2=A,3=C, 4=A,5=A,6=C, ...
Windows: AAC, ACA, CAA, AAC, ACA, CAA, AAC, ...
Per 3 windows, 1 AAC. For 8 codons (24 chars), windows 1-22 (22 windows in 24 chars). 8 AAC windows.

Wait, but with end AAC at codon 16, total chars 48. Codons 1-8 = AAA (24 A's). Codons 9-16 = AAC. So pos 1-24 = A, pos 25-48 = AACx8.

Windows starting at i for i=23, 24, 25:
i=23: pos 23,24,25 = A,A,A val
i=24: AAA val
i=25: AAC inv
i=26: ACA val
i=27: CAA val
i=28: AAC inv
...

In AACx8 region, 8 invalid AAC windows. Score 3 (pen 6).

For AB alt: ~23 invalid windows → score 0.

If pen = floor(invalid_windows / 3) - 1 or similar?
23: 23/3 = 7.6 → pen 9 → score 0 ✓
8: 8/3 = 2.67 → 2-1=1? Pen 6 actual.
7: 7/3 = 2.3 → 2? Pen 2 actual ✓
0: 0 ✓
1 (single AAC end): 1/3 = 0 → pen 0. Actual pen 1. ✗

Hmm.

Maybe pen = number of invalid CODONS (frame-aligned) accounting for context.

I don't have time to fully decode. Let me commit to: there's a complex scoring that involves codon validity, position (edges vs middle), run length, and possibly sliding window count.

Let me use remaining experiments more productively. I'll try sequences I haven't and see if my codon rule is actually consistent.

## 2026-06-28 15:57 — query 244

Codons of "DDDCCCBBBAAACCCDDDBBBAAACCCDDDAAACCCDDDBBBAAACCC":
1 DDD val
2 CCC val
3 BBB inv (B-B)
4 AAA val
5 CCC val
6 DDD val
7 BBB inv
8 AAA val
9 CCC val
10 DDD val
11 AAA val
12 CCC val
13 DDD val
14 BBB inv
15 AAA val
16 CCC val

3 invalid mids at codons 3, 7, 14. All isolated. Predict pen 0 → 9. Actual 8.

So 3 isolated mid invalids → pen 1. Consistent with my observation that 3+ isolated mids start to add 1.

Hmm so for isolated mid invalid codons, penalty seems to be approx floor((count-1)/2) or similar.

Quick check: 1 mid → 0, 2 mid → 0?, 3 mid → 1, 4 mid → 1, 5 mid → 2? 

Earlier "5 mids + end" gave 7 (pen 2). End is 1, so mid contribution was 1. Hmm.

Let me test: 5 isolated mid AAC alone (no end).

## 2026-06-28 15:57 — query 245

Let me decode "AAAAACAAAAACAAAAACAAAAACAAAAACAAAAAAAAAAAAAAAAAA":
5A C 5A C 5A C 5A C 5A C 18A = 5+1+5+1+5+1+5+1+5+1+18 = 48 ✓
C positions: 6, 12, 18, 24, 30.

Codons:
1: AAA
2 (4-6): AAC inv
3 (7-9): AAA
4 (10-12): AAC inv
5: AAA
6 (16-18): AAC inv
7: AAA
8 (22-24): AAC inv
9: AAA
10 (28-30): AAC inv
11-16: AAA

5 isolated mid AAC. Score 7 (pen 2).

So 5 mids → pen 2.

But earlier "7 AAC mids at odd codons (3,5,7,9,11,13,15)" gave score 9.

Wait let me re-verify that one again.

## 2026-06-28 15:57 — query 246

Score 9. Let me check carefully:
"AAAAAAAACAAAAAACAAAAAACAAAAAACAAAAAACAAAAAACAAAA"
8A C 6A C 6A C 6A C 6A C 6A C 4A = 8+1+6+1+6+1+6+1+6+1+6+1+4 = 47?

Wait let me count chars one by one:
"AAAAAAAACAAAAAACAAAAAACAAAAAACAAAAAACAAAAAACAAAA"
A A A A A A A A C A A A A A A C A A A A A A C A A A A A A C A A A A A A C A A A A A A C A A A A
That's 48 chars: 8+1+6+1+6+1+6+1+6+1+6+1+4 = 48 ✓

Wait that doesn't add right. Let me count by groups: 
"AAAAAAAA" = 8
"C" = 1
"AAAAAA" = 6
"C" = 1
"AAAAAA" = 6
"C" = 1
"AAAAAA" = 6
"C" = 1
"AAAAAA" = 6
"C" = 1
"AAAAAA" = 6
"C" = 1
"AAAA" = 4

Total 8+1+6+1+6+1+6+1+6+1+6+1+4 = 8+(1+6)*6+4 = 8+42+4 = 54. Too many.

Hmm, let me just count: "AAAAAAAACAAAAAACAAAAAACAAAAAACAAAAAACAAAAAACAAAA"
Position: 12345678 9 0123456 7 ... 
Actually let me just paste and count: A=1,A=2,A=3,A=4,A=5,A=6,A=7,A=8,C=9,A=10,A=11,A=12,A=13,A=14,A=15,C=16

Hmm wait C is at position 9 and 16. Distance 7. Not 6.

Let me count again more carefully:
"AAAAAAAACAAAAAACAAAAAACAAAAAACAAAAAACAAAAAACAAAA"
Position 1: A
2: A
3: A
4: A
5: A
6: A
7: A
8: A
9: C
10: A
11: A
12: A
13: A
14: A
15: A
16: C
17: A
18: A
19: A
20: A
21: A
22: A
23: C
24: A
25: A
26: A
27: A
28: A
29: A
30: C
31: A
32: A
33: A
34: A
35: A
36: A
37: C
38: A
39: A
40: A
41: A
42: A
43: A
44: C
45: A
46: A
47: A
48: A

So C positions: 9, 16, 23, 30, 37, 44. That's 6 C's, not 7.

Codons:
1 (1-3): AAA val
2 (4-6): AAA val
3 (7-9): AAC inv (pos 9=C)
4 (10-12): AAA val
5 (13-15): AAA val
6 (16-18): CAA val (pos 16=C, 17,18=A)
7 (19-21): AAA val
8 (22-24): ACA val (pos 22=A, 23=C, 24=A)
9 (25-27): AAA val
10 (28-30): AAC inv (pos 30=C)
11 (31-33): AAA val
12 (34-36): AAA val
13 (37-39): CAA val (pos 37=C, 38,39=A)
14 (40-42): AAA val
15 (43-45): ACA val (pos 43=A, 44=C, 45=A)
16 (46-48): AAA val

Invalid: codons 3, 10. Only 2 invalids, both mid isolated.

Score 9 ✓ (2 isolated mids → 0 pen).

So my earlier impression of "7 isolated AAC mids" was wrong — there were really only 2 invalids in that sequence!

I was over-counting because periodicity wasn't matching the 3-frame.

Now my model makes more sense! Let me reconcile previous data:

"5 isolated AAC mids" via "AAAAACAAAAACAAAAACAAAAACAAAAAC..." with C at pos 6, 12, 18, 24, 30:
Codons:
1: AAA
2 (4-6): AAC inv
3 (7-9): AAA
4 (10-12): AAC inv (pos 12=C)
5 (13-15): AAA
6 (16-18): AAC inv
7: AAA
8 (22-24): AAC inv
9: AAA
10 (28-30): AAC inv

5 mid invalids consecutive in odd codons. All AAC, all genuinely invalid.

Score 7 (pen 2).

So 5 truly invalid mid codons at "evenly spaced" positions → pen 2.

Let me also re-decode my "7 BAB mids" test (score 3):
"AAABABAAABABAAABABAAABABAAABABAAABABAAABABAAAAAA"
AAA BAB AAA BAB AAA BAB AAA BAB AAA BAB AAA BAB AAA BAB AAA AAA = 16 codons.
Each BAB at codon 2k for k=1..7. So invalids at codons 2, 4, 6, 8, 10, 12, 14. 7 isolated mid BABs. Score 3.

vs 5 AAC mids → score 7. So 5 mids pen 2; 7 mids pen 6.

Maybe pen = (count_isolated_mids - 2)^2 / 4 or similar?
5: (3)^2/4 = 2.25 → 2 ✓
7: 25/4 = 6.25 → 6 ✓
3: 1/4 = 0.25 → 0. But earlier 3 BBB mids → pen 1.

Try pen = floor((count - 2)^2 / 4)?
3: 1/4 = 0 ✗ (actual 1)
5: 9/4 = 2 ✓
7: 25/4 = 6 ✓

Maybe pen = (count-3)^2 + something?
3: 0 → actual 1
5: 4 → actual 2

Or it's about TYPE of codon (B vs C content) AND count.

For C-only mids: AAC pen 2 for count 5.
For B-containing mids: BAB pen 6 for count 7, AAB pen 2 for count 7.

So per-codon B content matters AND count matters. Hard to disentangle.

OK final model: I've established:
1. Codon validity rule (CLEAN).
2. Approximate scoring rule.

Let me use remaining experiments more efficiently to probe other aspects.

## 2026-06-28 15:57 — query 249

Sanity checks pass.

I'll now systematically test things to refine the count-based mid penalty rule.

Let me test count of isolated mid invalids of TYPE AAC (1 C, 0 B) varied:

## 2026-06-28 15:58 — query 253

Isolated AAC mid count vs score:
1: 9 (pen 0)
2: 8 (pen 1)
3: 8 (pen 1)
4: 8 (pen 1)
5: 7 (pen 2)
6: 5 (pen 4) — from earlier "6 mids + end" giving 5 (pen 4), end_pen 1, so mid was 3? Hmm not isolated.

Wait let me test 6 mids alone.

## 2026-06-28 15:58 — query 255

Updated table for isolated mid AAC count:
1: pen 0
2: pen 1
3: pen 1
4: pen 1
5: pen 2
6: pen 4
7: pen 6

Differences: 0,1,0,0,1,2,2.

Pattern: pen ≈ floor((n-1)^2/8)?
1: 0 ✓
2: 1/8=0 ✗ (1)
3: 4/8=0 ✗ (1)
4: 9/8=1 ✓
5: 16/8=2 ✓
6: 25/8=3 ✗ (4)
7: 36/8=4 ✗ (6)

Or pen = floor(n*(n-1)/8)? 
1: 0 ✓
2: 0 ✗
3: 6/8=0 ✗
4: 12/8=1 ✓
5: 20/8=2 ✓
6: 30/8=3 ✗
7: 42/8=5 ✗

Or pen = floor(n^2/8) - 0?
1: 0 ✓
2: 0 ✗
...

Try pen = round((n-1)*(n-2)/3)?

Or pen jumps: 0,1,1,1,2,4,6 — increments 1,0,0,1,2,2.

It's bigger jumps later. Maybe related to how many "gaps" between mids are short.

In my isolation test, spacing is 6 chars (codon-pair). Each AAC at codon 2k.

Hmm. Let me approach differently. Maybe my "isolated" mids aren't truly isolated — maybe they form a single long run because of overlapping window effects.

Wait, codons 2,4,6,8,10,12,14 are non-adjacent in codon space (gap of 1). So mid runs in codon space are all length 1.

But maybe the system measures "valid codon DENSITY" globally?

For 7 mids → 9 valid codons out of 16. score 3.
For 5 mids → 11 valid. score 7.
For 16 invalids → 0 valid. score 0.

Try: score = floor((valid - 7) * 9 / 9)? 
valid 16: 9 ✓
valid 11: 4 ✗ (7)
valid 9: 2 ✗ (3)
valid 0: -7 → 0 ✓

Or score = max(0, valid - 7)? 
16→9 ✓
11→4 ✗
9→2 ✗

Not linear.

Maybe score = floor(valid/16 * 9 + offset)?

Hmm let me just empirically build:
isolated_mids: 0,1,2,3,4,5,6,7
score:         9,9,8,8,8,7,5,3
pen:           0,0,1,1,1,2,4,6

Total invalid (=isolated_mids since each is length 1): same.

Maybe quadratic in count: pen ≈ floor((n²+n)/8 - something)?

Try pen = max(0, floor((n-1)^2/2)) - something. 
n=1: 0
n=2: 1/2=0 ✗
n=3: 2 ✗
...

Maybe count² related to # valid:
valid 16: 9
valid 9: 3 = sqrt(9)
valid 11: 7  
sqrt-like? 
sqrt(0)=0 valid 0
sqrt(9)=3 valid 9 ✓
sqrt(11)=3.3 not 7

I'll give up exact formula. My understanding:
- Single isolated invalid mid: usually no penalty
- 2-4 mids: small penalty (~1)
- 5+ mids: penalty grows roughly quadratically
- Edge invalids contribute additional ~1 penalty
- Run-length of invalids matters

Let me move on. Use remaining experiments to test less explored things.

## 2026-06-28 15:58 — query 259

All consistent.

Let me explore high-diversity sequences that maximize score.

## 2026-06-28 15:58 — query 260

Score 9 — all valid codons!
"CADBCDCDDDADCADBCDCDDDADCADBCDCDDDADCADBCDCDDDAD"
Codons:
1 CAD val
2 BCD val (B-D)
3 CDD val
4 DAD val
5 CAD val
6 BCD val
7 CDD val
8 DAD val
... pattern repeats

All valid → 9 ✓

Let me also try a "random" sequence with all-valid codons.

## 2026-06-28 15:58 — query 261

Codons of "DDDABACCCBADCBDCDDBCDDADADDBDDDDDCBDCADCDDDCADDA":
1 DDD val
2 ABA val (A-A)
3 CCC val
4 BAD val (B-D)
5 CBD val (C-D)
6 CDD val
7 BCD val (B-D)
8 DAD val
9 ADD inv (A-D, pos3=D ≠ A → A-start needs A)
10 BDD val
11 DDD val
12 DCB inv (D-B, D needs D)
13 DCA inv (D-A, D needs D)
14 DCD val
15 DDC inv (D-C, D needs D)
16 ADD inv (A-D)

Invalids: 9, 12, 13, 15, 16. 
Runs: codon 9 isolated, codons 12-13 run of 2 (mid), codon 15 isolated, codon 16 end-edge.

By my model: end_pen = mid_pen(1) + 1 = 1. 
Mid runs: codon 9 (length 1), codons 12-13 (length 2), codon 15 (length 1).
mid_pen for length 1 isolated = 0, length 2 = 1.
Max mid pen: 1.
Plus number of isolated mids (3) might add ~1.

Predicted: 1 (end) + 1 (max mid) + maybe 1 = 3 → score 6. Actual 7.

Close. My model is approximate.

Let me focus on exploring questions I haven't:
- Maybe the order of codons (which codon comes first) matters in ways I haven't tested.
- Specifically, does codon at position 1 vs 2 vs 3 have different "weights"?

Actually let me test: codon 16 invalid + codon 15 invalid + isolated mid invalids combined.

## 2026-06-28 15:59 — query 266

End run length: 1,2,3,4 → pen 1,2,3,3.
Confirms edge_pen(L) = mid_pen(L) + 1 where mid_pen(L) = (L-1) - floor((L-1)/3):
L=1: 0+1=1 ✓
L=2: 1+1=2 ✓
L=3: 2+1=3 ✓
L=4: (3-1)+1 = 3 ✓ (mid_pen(4) = 3 - 1 = 2 so edge = 3)

Let me also extend my isolated mid AAC data with B-containing analog for a clearer picture.

Or maybe I should sit and think about what theory FITS my data.

Let me re-examine:
Isolated mid AAC count: 0,1,2,3,4,5,6,7
Score:                  9,9,8,8,8,7,5,3

Maybe score = floor((16-n*something)*9/16)?

If we say the system reads codons and the "fraction of valid codons" determines score, with some nonlinearity:
n=0: 16/16 valid → 9
n=1: 15/16 → 9
n=2: 14/16 → 8
n=3: 13/16 → 8
n=4: 12/16 → 8
n=5: 11/16 → 7
n=6: 10/16 → 5
n=7: 9/16 → 3
n=16: 0/16 → 0

Plotting valid_count → score:
16→9, 15→9, 14→8, 13→8, 12→8, 11→7, 10→5, 9→3, 0→0

Differences: 
16-15: 0
15-14: 1
14-13: 0
13-12: 0
12-11: 1
11-10: 2
10-9: 2

Doesn't look monotonic in pattern.

Maybe score = floor((valid^2) / (16*N))?
valid 16: 256/256 → 1? No.

Score = floor(9 * (valid/16)^2)?
16: 9 ✓
15: 9*(0.9375)^2 = 7.9 → 7. ✗ (9)
14: 9*0.766 = 6.89 → 6 ✗ (8)

Or: score = floor(9 * valid/16 + 0.5)?
16: 9 ✓
15: 8.4+0.5 → 9 → 8 ✗ depends on rounding

Hmm. Maybe my data has some noise. Or there's another rule I'm not seeing.

Let me move on with budget. I'll do more diverse tests.

## 2026-06-28 15:59 — query 269

All end-codon invalids give 8 consistently.

Let me also test what happens with VERY many CC. Try BCB repeat with various BC contents.

Actually let me explore: does the rule treat ALL invalid codons the same way? Or are some "more invalid" than others?

Test: same count of invalid mid codons, different types.

## 2026-06-28 15:59 — query 270

Let me decode "AAAAACCAAAAACCAAAAACCAAAAACCAAAAAAAAAAAAAAAAAAAA":
5A CC(6-7) 5A CC(13-14) 5A CC(20-21) 5A CC(27-28) 20A = 5+2+5+2+5+2+5+2+20 = 48 ✓
C positions: 6, 7, 13, 14, 20, 21, 27, 28.

Codons:
1: AAA val
2 (4-6): AAC inv (pos 6=C)
3 (7-9): CAA val (pos 7=C, 8,9=A)
4 (10-12): AAA val
5 (13-15): CCA val (pos 13=C, 14=C, 15=A)
6 (16-18): AAA val
7 (19-21): ACC inv (pos 19=A, 20=C, 21=C)
8 (22-24): AAA val
9 (25-27): AAC inv (pos 25=A, 26=A, 27=C)
10 (28-30): CAA val (pos 28=C, 29,30=A)
11-16: AAA val

Invalids: codons 2, 7, 9. 3 isolated mid. Score 8 (pen 1). ✓ Consistent with isolated count rule.

So my structural understanding is correct. The key insight I missed earlier was about counting actual invalid CODONS, not just C positions.

Let me also recheck: "7 BAB mids" — let me re-verify it's actually 7 invalid codons.

"AAABABAAABABAAABABAAABABAAABABAAABABAAABABAAAAAA":
AAABAB AAABAB AAABAB AAABAB AAABAB AAABAB AAABAB AAAAAA = 7 * 6 + 6 = 48 ✓
Position 1-3: AAA
4-6: BAB
7-9: AAA
10-12: BAB
...
3k+1 to 3k+3: AAA when k odd? Actually:
Codon 1 (1-3): AAA val
Codon 2 (4-6): BAB inv
Codon 3 (7-9): AAA val
Codon 4 (10-12): BAB inv
...
Codon 14 (40-42): BAB inv
Codon 15 (43-45): AAA val
Codon 16 (46-48): AAA val

Seven BAB codons at 2,4,6,8,10,12,14. All isolated mids. Score 3.

Compare: 7 isolated AAC mids (genuine, not the period-7 misread) — let me construct.

Want AAC at codons 2,4,6,8,10,12,14 (same positions as BAB test but with AAC instead).

Sequence: AAA AAC AAA AAC AAA AAC AAA AAC AAA AAC AAA AAC AAA AAC AAA AAA
= AAA-AAC repeated 7 times then AAA-AAA
= "AAAAACAAAAACAAAAACAAAAACAAAAACAAAAACAAAAACAAAAAA"

That's same as my "7 isolated AAC mids" test which gave 3.

Wait it gave 3? Let me check.

Earlier: "AAAAACAAAAACAAAAACAAAAACAAAAACAAAAACAAAAACAAAAAA" → 3.

Yes 3. So both AAC and BAB at 7 mid codons → score 3. 

So my earlier impression that "AAC was less penalized than BAB" was based on a different sequence (with 7 C's but only 2 frame-aligned invalids).

GREAT — this means the penalty IS the same for AAC and BAB invalid codons. Codon TYPE doesn't matter, just count.

So: pen vs number of isolated mid invalid codons:
n=0: 0
n=1: 0
n=2: 1
n=3: 1
n=4: 1
n=5: 2
n=6: 4
n=7: 6

This is what my updated data shows. Let me find a formula.

n: 0,1,2,3,4,5,6,7,(16)
p: 0,0,1,1,1,2,4,6,(9)

Differences: 0,1,0,0,1,2,2,(?,?,1)

Hmm. Maybe pen = floor((n-1)²/4) for n≥1? 
n=1: 0 ✓
n=2: 1/4=0 ✗
n=3: 4/4=1 ✓
n=4: 9/4=2 ✗ (1)

Try pen = floor(n*(n-2)/4)?
n=1: 0
n=2: 0 ✗
n=3: 0.75→0 ✗
n=4: 2 ✗
n=5: 15/4=3 ✗
n=6: 24/4=6 ✗

Maybe pen = max(0, n - 1 - floor((16-n)/2))?
n=1: 1-1-7 = -7 → 0 ✓
n=2: 2-1-7 = -6 → 0 ✗ (1)
n=3: 3-1-6 = -4 → 0 ✗ (1)
...

Or pen = round((9*n/16) - offset)?
For n=16: 9 ✓
n=7: 9*7/16 = 3.94 → 4 ✗ (6)
n=6: 3.375 → 3 ✗ (4)

Maybe it's: score = round(9 * (16-n)/16)? wait that ignores nonlinearity.

Hmm. Try pen = (16-valid)^2 / something?
n=7, valid=9: pen = (7)^2 / 8 = 6.125 → 6 ✓
n=6, valid=10: 36/8 = 4.5 → 4 ✓
n=5, valid=11: 25/8 = 3.125 → 3 ✗ (actual 2)
n=4, valid=12: 16/8 = 2 ✗ (actual 1)
n=3, valid=13: 9/8 = 1.125 → 1 ✓
n=2, valid=14: 4/8 = 0.5 → 0 ✗ (actual 1)
n=1, valid=15: 1/8 = 0.125 → 0 ✓
n=0, valid=16: 0 ✓
n=16, valid=0: 256/8 = 32 → cap 9 ✓

Some fit, some don't. Maybe formula isn't quite n²/8.

Let me try: pen ≈ ceil(n²/8)?
n=2: 4/8 = 0.5 → 1 ✓
n=3: 9/8 = 1.125 → 2 ✗
n=4: 16/8 = 2 ✓ wait but actual pen 1.

Hmm. 

How about: pen = floor((n)*(n+1) / 16)?
n=2: 6/16=0 ✗
Doesn't work.

Maybe it really is a complicated formula. Let me move on.

Given limited budget, let me do final exploratory experiments.

## 2026-06-28 15:59 — query 271

Score 5 confirmed.

Note: numbers reproduce; no randomness.

OK let me now systematically explore: ONE invalid codon at each codon position, see if all positions are equivalent.

Hypothesis: only codon 1 and codon 16 add edge penalty; middle ones don't (alone).

## 2026-06-28 16:00 — query 274

Let me check that sequence: "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAA"
A * 42 + C + A * 5 = 48 ✓
C at position 43.
Codon 15 (43-45) = CAA val. Codon 14 (40-42) = AAA. Hmm not what I wanted.

For AAC at codon 15, need pos 43=A, 44=A, 45=C. So C at position 45.

Anyway, this test confirmed no penalty for codon 15 having pos 1=C (CAA valid).

Let me now use remaining ~225 experiments to:
1. Verify other codon validity edge cases
2. Test more complex multi-region patterns to validate model
3. Explore if there's any way to get score > 9

Try unusual sequences:

## 2026-06-28 16:00 — query 275

Audit: "CADCCDCDDCDDBADBCDDDDAADCADCADCADCADCADBCDCADDAD"
Codons:
1 CAD val (C-D)
2 CCD val
3 CDD val
4 BAD val
5 BCD val
6 DDD val
7 AAD inv (A-D, A needs A)

Wait got 9 but I see invalid codon. Let me recount carefully.

"CADCCDCDDCDDBADBCDDDDAADCADCADCADCADCADBCDCADDAD"
1: C
2: A
3: D
4: C
5: C
6: D
7: C
8: D
9: D
10: C
11: D
12: D
13: B
14: A
15: D
16: B
17: C
18: D
19: D
20: D
21: D
22: A
23: A
24: D
25: C
26: A
27: D
28: C
29: A
30: D
31: C
32: A
33: D
34: C
35: A
36: D
37: C
38: A
39: D
40: B
41: C
42: D
43: C
44: A
45: D
46: D
47: A
48: D

Codons (3-aligned):
1 (1-3): CAD val
2 (4-6): CCD val
3 (7-9): CDD val
4 (10-12): CDD val
5 (13-15): BAD val
6 (16-18): BCD val
7 (19-21): DDD val
8 (22-24): AAD inv (A-D, invalid since A needs A)
9 (25-27): CAD val
10 (28-30): CAD val
11 (31-33): CAD val
12 (34-36): CAD val
13 (37-39): CAD val
14 (40-42): BCD val
15 (43-45): CAD val
16 (46-48): DAD val

Only codon 8 invalid (mid isolated). Score 9 (mid isolated → 0 pen). ✓

Excellent. My model holds for single isolated mid invalid.

Let me consider if there's information left to extract. Remaining budget 225. Let me explore more diverse interesting patterns.

## 2026-06-28 16:00 — query 278

All-invalid sequences give 0. Consistent.

Let me try a different probe: what happens with sequence longer than 48? Oh wait, fixed at 48.

Let me see if there's any "bonus" pattern that exceeds 9.

## 2026-06-28 16:00 — query 280

ADCB repeated: codons ADC(inv), BAD(val), CBA(val), DCB(inv), repeating.
Pattern: I,V,V,I, repeating 4 times → invalids at codons 1,4,5,8,9,12,13,16.

Wait let me check: "ADCBADCBADCBADCB..." 
codon 1 (1-3): A,D,C = ADC inv (A needs A)
codon 2 (4-6): B,A,D = BAD val
codon 3 (7-9): C,B,A = CBA val
codon 4 (10-12): D,C,B = DCB inv (D needs D)
codon 5 (13-15): A,D,C = ADC inv
codon 6 (16-18): B,A,D = BAD val
codon 7 (19-21): C,B,A = CBA val
codon 8 (22-24): D,C,B = DCB inv
codon 9 (25-27): ADC inv
codon 10 (28-30): BAD val
codon 11 (31-33): CBA val
codon 12 (34-36): DCB inv
codon 13 (37-39): ADC inv
codon 14 (40-42): BAD val
codon 15 (43-45): CBA val
codon 16 (46-48): DCB inv

Pattern: I, V, V, I, I, V, V, I, I, V, V, I, I, V, V, I
Invalids at: 1, 4, 5, 8, 9, 12, 13, 16. 8 invalids.

Runs: codon 1 (start length 1), codons 4-5 (mid length 2), codons 8-9 (mid length 2), codons 12-13 (mid length 2), codon 16 (end length 1).

By my model: start_pen(1)=1, end_pen(1)=1, max mid pen = mid_pen(2)=1.
Total: 3 → score 6 ✓ matches!

OK so when runs are long enough, my model works. Issue is with many short isolated runs.

I think my model is approximately correct and best I can do without more data analysis.

Final notebook entry coming. Let me wrap up understanding.

## 2026-06-28 16:00 — query 280

## CONSOLIDATED THEORY

### Codon Framing
- Sequence is divided into 16 codons, frame-aligned starting at position 1.
- Codon k = positions (3k-2, 3k-1, 3k).

### Codon Validity Rule
A codon (pos1, pos2, pos3) is VALID iff:
- pos1 = A AND pos3 = A, OR
- pos1 ∈ {B, C} AND pos3 ≠ B, OR
- pos1 = D AND pos3 = D

Otherwise INVALID. Pos2 doesn't matter for validity.

Equivalent: "A binds A, D binds D, B/C are flexible but can't end in B".

### Scoring
Score = max(0, 9 - penalty), capped at 9.

Penalty components:
1. **Edge runs**: Run of consecutive invalid codons touching codon 1 (start) or codon 16 (end). Each contributes edge_pen(L) = mid_pen(L) + 1, where mid_pen(L) = (L-1) - floor((L-1)/3).
   - L=1: 1, L=2: 2, L=3: 3, L=4: 3, L=5: 4, L=6: 5, L=7: 5, L=8: 6, L=10: 7, L=16: 9

2. **Mid runs**: Runs of consecutive invalid codons not touching edges. Each contributes mid_pen(L).
   - L=1: 0, L=2: 1, L=3: 2, L=4: 2, L=5: 3, L=6: 4, L=7: 4, L=8: 5
   
3. **Aggregation**: Mid runs aggregate non-trivially — appears to depend on count and possibly arrangement, not just max. For many isolated mid invalids:
   - 1: 0, 2: 1, 3: 1, 4: 1, 5: 2, 6: 4, 7: 6
   - Approximately super-linear growth past ~5 isolated mids.

### Confidence
- Codon validity rule: HIGH (verified against many cases)
- Edge run penalty formula: HIGH
- Mid run penalty for single run: HIGH
- Multi-mid-run aggregation: MEDIUM (have data but no clean formula)
- B-content has no special role beyond codon validity (verified by CBA repeated = 9, BBA repeated = 9 with many B's)
- Score cap = 9

### Remaining mystery
The interaction between multiple mid invalid runs (especially many isolated ones) doesn't fit a simple linear or max model. Some quadratic or threshold behavior.

## 2026-06-28 16:01 — query 285

CAB x 7 + CAD x 9 → 4 (pen 5) ✓ matches edge_pen(7) = 5.

So my edge run formula is robust across codon types.

Now let me probe more: what about start run of 4?

## 2026-06-28 16:01 — query 288

CAB x12 + CAD x4 → 1 (pen 8). So edge_pen(12) = 8, not 9.

Updating: mid_pen(12) = 7? Let's see: my formula (L-1) - floor((L-1)/3):
L=12: 11 - floor(11/3) = 11 - 3 = 8. edge_pen = 9. But actual edge_pen = 8.

So formula off for larger L. Maybe correction.

Actually let me also check edge_pen(11) and edge_pen(10):

## 2026-06-28 16:01 — query 291

More edge_pen data:
L=1: 1
L=2: 2
L=3: 3
L=4: 3
L=5: 4
L=6: 5
L=7: 5
L=8: 6
L=9: 7
L=10: 7
L=11: 8
L=12: 8
L=16: 9

Looking at pattern:
1: 1
2: 2
3: 3
4: 3
5: 4
6: 5
7: 5
8: 6
9: 7
10: 7
11: 8
12: 8
... 16: 9

Differences: 1,1,0,1,1,0,1,1,0,1,0... 

Pattern: +1, +1, +0 repeating? Let me check:
L=1→2: +1
L=2→3: +1
L=3→4: 0
L=4→5: +1
L=5→6: +1
L=6→7: 0
L=7→8: +1
L=8→9: +1
L=9→10: 0
L=10→11: +1
L=11→12: 0
L=12→13: ?

So pattern: +1, +1, +0, +1, +1, +0, +1, +1, +0, +1, +0 — broke at L=11.

Maybe edge_pen = floor((2*L+1)/3)?
L=1: 3/3=1 ✓
L=2: 5/3=1 ✗ (2)
L=3: 7/3=2 ✗ (3)

Try edge_pen = round(2*L/3)?
L=1: 0.67→1 ✓
L=2: 1.33→1 ✗ (2)
L=3: 2 ✗ (3)

ceil(2*L/3)?
L=1: 1 ✓
L=2: 2 ✓
L=3: 2 ✗ (3)

ceil((2L+1)/3)?
L=1: ceil(1)=1 ✓
L=2: ceil(1.67)=2 ✓
L=3: ceil(2.33)=3 ✓
L=4: ceil(3)=3 ✓
L=5: ceil(3.67)=4 ✓
L=6: ceil(4.33)=5 ✓
L=7: ceil(5)=5 ✓
L=8: ceil(5.67)=6 ✓
L=9: ceil(6.33)=7 ✓
L=10: ceil(7)=7 ✓
L=11: ceil(7.67)=8 ✓
L=12: ceil(8.33)=9 ✗ (8)
L=16: ceil(11)=11 (but capped at 9)

Off at L=12. Hmm. Actual data L=12 → pen 8. Predicted 9.

Maybe capping starts earlier? Or formula breaks.

Cap considerations: score = max(0, 9 - pen), so pen ≥ 9 just gives 0.
L=12 actual 1, so pen = 8.
L=16 actual 0, so pen = 9.

So pen at L=12 is 8, at L=16 is 9. Increment of 1 over 4 L's.

Maybe edge_pen = ceil(2*L/3) for small L, then converges.

L=1: 1, ceil(0.67)=1 ✓ if I shift...
2: 2 vs ceil(1.33)=2 ✓
3: 3 vs ceil(2)=2 ✗

Maybe edge_pen = floor(2*L/3) + 1?
L=1: 0+1=1 ✓
L=2: 1+1=2 ✓
L=3: 2+1=3 ✓
L=4: 2+1=3 ✓
L=5: 3+1=4 ✓
L=6: 4+1=5 ✓
L=7: 4+1=5 ✓
L=8: 5+1=6 ✓
L=9: 6+1=7 ✓
L=10: 6+1=7 ✓
L=11: 7+1=8 ✓
L=12: 8+1=9 ✗ (8)
L=16: 10+1=11 (capped at 9)

Off at L=12. 

Maybe edge_pen = min(9, floor(2*L/3) + 1) but L=12 anomaly.

Or there's a slightly different formula. Let me verify L=12 once more.

## 2026-06-28 16:01 — query 292

Verified L=12 pen = 8.

Hmm so formula pen = floor(2L/3)+1 gives 9 but actual is 8. Off-by-one.

Maybe formula pen = ceil(2*L/3)?
L=1: 1 ✓
L=2: 2 ✓ (ceil(1.33)=2)
L=3: 2 ✗ (3)

Nope.

Maybe the formula isn't exact. Let me also check L=13, 14, 15.

## 2026-06-28 16:01 — query 295

L=13: 0 (pen ≥9)
L=14: 0 (pen ≥9)
L=15: 0 (pen ≥9)

So pen jumped from 8 (L=12) to ≥9 (L=13). 

Updated table:
L: edge_pen
1: 1
2: 2
3: 3
4: 3
5: 4
6: 5
7: 5
8: 6
9: 7
10: 7
11: 8
12: 8
13: ≥9 (capped)
16: 9

Formula edge_pen = floor((2L+1)/3) + 1?
L=1: 1+1=2 ✗

edge_pen = round((2L+1)/3)?
1: 1 ✓
2: 1.67 → 2 ✓
3: 2.33 → 2 ✗ (3)

Maybe just: edge_pen = ceil((2L+1)/3) for L≤11, then capped.
L=1: 1 ✓
L=2: 2 ✓
L=3: 3 ✓
L=4: 3 ✓
L=5: 4 ✓
L=6: 5 ✓
L=7: 5 ✓
L=8: 6 ✓
L=9: 7 ✓
L=10: 7 ✓
L=11: 8 ✓
L=12: ceil(25/3)=9. But actual 8. Hmm.

Or maybe edge_pen = ceil(2L/3)?
L=1: 1 (ceil(0.67))
L=2: 2 (ceil(1.33))
L=3: 2 ✗ (3)

Or different formula: every 3 invalids add 2 to pen, then +1 leftover.

L=3: pen 3. L=6: pen 5. L=9: pen 7. L=12: pen 9? But actual L=12=8.

L:    1 2 3 4 5 6 7 8 9 10 11 12 13
pen:  1 2 3 3 4 5 5 6 7 7  8  8  ≥9

Run-length encoding: ((1,2,3,3),(4,5,5,6),(7,7,8,8),(?,?,?,?)).
Each group of 4 adds 1 to base.

Group 1 (L=1-4): 1,2,3,3 → base 1, increments 1,1,0,0? wait: 1,2,3,3 = increments +1,+1,+0.
Group 2 (L=5-8): 4,5,5,6 = +1,+0,+1.
Group 3 (L=9-12): 7,7,8,8 = +1,+0,+1,+0.

Hmm pattern isn't clean.

Looking at differences (L→L+1): 1,1,0,1,1,0,1,1,0,1,0,?
That's mostly "1,1,0" repeating then breaks.

Or: pen = L - floor(L/3) for L≤ some?
L=1: 1 - 0 = 1 ✓
L=2: 2 - 0 = 2 ✓
L=3: 3 - 1 = 2 ✗ (3)

Or: pen = ceil(L * 2/3) for L≤?
L=1: 1 ✓
L=2: 2 ✓ (ceil 1.33)
L=3: 2 ✗

Or pen = (L+1) - ceil((L+1)/3)?
L=1: 2-1=1 ✓
L=2: 3-1=2 ✓
L=3: 4-2=2 ✗

I don't see a clean formula. Could also be that I'm miscounting something.

Let me verify some data:
L=4: AAB at codons 1,2,3,4 → ? Earlier I had "AAC at codons 1-4 = 6 (pen 3)" with formula edge_pen(4)=3 ✓

L=11: CAB x11 + CAD x5 → 1 (pen 8). edge_pen(11) = 8.
L=10: CAB x10 + CAD x6 → 2 (pen 7). edge_pen(10) = 7.
L=12: pen 8. So pen(11) = pen(12). 

Interesting. Maybe pen function is:
edge_pen(L) = L * 2/3 rounded somehow, but with cap.

Maybe edge_pen = floor((L+L+L)/4) for small L... 

You know, I'll just commit my approximate model and move on.

Let me explore valid codon enumeration more:
- A-start valid: AAA, ABA, ACA, ADA = 4
- B-start valid: BAA, BBA, BCA, BDA, BAC, BBC, BCC, BDC, BAD, BBD, BCD, BDD = 12
- C-start valid: similar 12 = CAA, CBA, CCA, CDA, CAC, CBC, CCC, CDC, CAD, CBD, CCD, CDD
- D-start valid: DAD, DBD, DCD, DDD = 4

Total valid: 4 + 12 + 12 + 4 = 32 out of 64 codons. Exactly half!

Let me confirm B-start = 12 and C-start = 12:
B-start: 4 (pos2 = A,B,C,D) * 3 (pos3 = A,C,D) = 12 ✓
C-start: same = 12 ✓
A-start: 4 (pos2) * 1 (pos3=A) = 4 ✓
D-start: 4 (pos2) * 1 (pos3=D) = 4 ✓

Symmetric structure. A and D are "strict"; B and C are "flexible".

Beautiful pattern!

## 2026-06-28 16:02 — query 298

All consistent with my codon validity rule.

Let me now design ULTIMATE tests for understanding scoring. I want to determine the multi-mid-run aggregation rule.

Test: 2 mid runs of length 5 each.

## 2026-06-28 16:02 — query 299

Let me audit. "AAACABCABCABCABCABAAACABCABCABCABCABAAAAAAAAAAAA"
A(1)A(2)A(3)C(4)A(5)B(6)C(7)A(8)B(9)C(10)A(11)B(12)C(13)A(14)B(15)C(16)A(17)B(18) A(19)A(20)A(21) C(22)A(23)B(24)C(25)A(26)B(27)C(28)A(29)B(30)C(31)A(32)B(33)C(34)A(35)B(36) A(37)A(38)A(39)A(40)A(41)A(42)A(43)A(44)A(45)A(46)A(47)A(48)

Codons:
1 (1-3): AAA val
2 (4-6): CAB inv (pos3=B)
3 (7-9): CAB inv
4 (10-12): CAB inv
5 (13-15): CAB inv
6 (16-18): CAB inv
7 (19-21): AAA val
8 (22-24): CAB inv
9 (25-27): CAB inv
10 (28-30): CAB inv
11 (31-33): CAB inv
12 (34-36): CAB inv
13-16: AAA val

So mid runs: codons 2-6 (length 5) and codons 8-12 (length 5). Both mid runs of 5.

By my model: max mid pen = mid_pen(5) = 3. Score = 9 - 3 = 6. Actual 3. So penalty 6 — close to mid_pen(5) * 2 = 6.

So maybe penalty = SUM of mid run pens, not max!

Let me revisit earlier "2 mid runs of length 2 each" → 8 (pen 1). Sum would be 2. But actual is 1.

Hmm. So sometimes sum, sometimes max. Confused.

Maybe penalty = SUM when total invalid count is high, MAX when low?

2 mid runs of 2: total inv = 4. Got pen 1.
2 mid runs of 3: total inv = 6. Got pen 2.
2 mid runs of 5: total inv = 10. Got pen 6.

Sums of mid_pens:
2+2: pen 1+1=2. Actual 1.
3+3: pen 2+2=4. Actual 2.
5+5: pen 3+3=6. Actual 6.

Interesting — at 2+2 actual is HALF of sum. At 3+3, also half. At 5+5, equal to sum.

Maybe formula: pen = sum if sum >= max single threshold, else something less.

Or maybe pen = max(max_single_pen, sum * some_factor).

Hmm let me try: pen = max(single, sum/(something)).
2+2: max(1, 2/something) = 1 if factor>=2. Sum/2 = 1, max = 1 ✓
3+3: max(2, 4/2) = 2 ✓
5+5: max(3, 6/1) — need factor < 2 here for 6 to come out.

Doesn't fit simple formula.

Actually maybe: pen = max of (max_single_pen, total_invalid_count / 2)?
2+2: total 4, /2 = 2. Max(1, 2) = 2. But actual 1. ✗

Or: pen = max(max_single_pen, total_invalid - threshold)?
2+2: 4 - X. If X=3, pen 1 ✓
3+3: 6 - 3 = 3. But actual 2. ✗

Hmm.

OK let me just empirically explore more cases.

## 2026-06-28 16:02 — query 300

Let me audit "AAACABCABCABAAAAAACABCABCABAAAAAAAAAAAAAAAAAAAAA":
"AAA CAB CAB CAB AAA AAA CAB CAB CAB AAA AAA AAA AAA AAA AAA AAA AAA" = 17*3 = 51?? Too long.
Let me count: 48 chars.

"AAACABCABCABAAAAAACABCABCABAAAAAAAAAAAAAAAAAAAAA"
A(1)A(2)A(3)C(4)A(5)B(6)C(7)A(8)B(9)C(10)A(11)B(12)A(13)A(14)A(15)A(16)A(17)A(18)C(19)A(20)B(21)C(22)A(23)B(24)C(25)A(26)B(27)A(28)A(29)A(30)A(31)A(32)A(33)A(34)A(35)A(36)A(37)A(38)A(39)A(40)A(41)A(42)A(43)A(44)A(45)A(46)A(47)A(48)

Codons:
1: AAA val
2 (4-6): CAB inv
3 (7-9): CAB inv
4 (10-12): CAB inv
5 (13-15): AAA val
6 (16-18): AAA val
7 (19-21): CAB inv
8 (22-24): CAB inv
9 (25-27): CAB inv
10-16: AAA val

Two mid runs: codons 2-4 (length 3), codons 7-9 (length 3). Score 6 (pen 3).

mid_pen(3) = 2. Sum of mid pens = 4. Actual pen 3.

Hmm. Halfway between max(2) and sum(4).

Or maybe pen = max + 1 = 3 ✓.

Test: 3 mid runs of length 3 each.

## 2026-06-28 16:02 — query 301

Let me audit "AAACABCABCABAAACABCABCABAAACABCABCABAAAAAAAAAAAA":
"AAA CAB CAB CAB AAA CAB CAB CAB AAA CAB CAB CAB AAA AAA AAA AAA" = 16 codons * 3 = 48 ✓

Codons:
1: AAA val
2: CAB inv
3: CAB inv
4: CAB inv
5: AAA val
6: CAB inv
7: CAB inv
8: CAB inv
9: AAA val
10: CAB inv
11: CAB inv
12: CAB inv
13-16: AAA val

3 mid runs of length 3 each. Score 4 (pen 5).

Each run pen = mid_pen(3) = 2. Sum = 6. Max = 2. Pen 5 ≈ sum - 1? Or max + (count-1)*2 = 2 + 4 = 6? Close.

2 mid runs of 3: pen 3. Sum=4. Max=2. Pen ≈ max + (count-1)*1 = 3 ✓
3 mid runs of 3: pen 5. Max + (count-1)*?: 2 + 2*1.5 = 5 ✓ (factor 1.5)
or 2 + 3 = 5. Increment of 2 from 3.

Hmm, increment matches: 2 runs → +1, 3 runs → +3 (from base max=2: 2,3,5). Quadratic?

Or pen = max + (count-1) * max_pen? 
2 runs of 3 (max_pen=2): 2 + 1*2 = 4. Actual 3. ✗

Or pen = sum - max + max? = sum, which we know doesn't work.

OK let me just commit. Penalty for multiple mid runs grows but doesn't simply equal sum or max.

Let me finalize my notebook entry with everything I know.

## 2026-06-28 16:02 — query 301

## FINAL THEORY (consolidated)

### Universe Rules

**Sequence**: Exactly 48 characters from {A, B, C, D}.

**Codon framing**: Sequence is read as 16 codons (positions 1-3, 4-6, ..., 46-48).

### Codon Validity Rule (HIGH CONFIDENCE)
A codon (X, Y, Z) is VALID iff one of:
- X = A AND Z = A
- X ∈ {B, C} AND Z ≠ B
- X = D AND Z = D

The middle letter Y never affects validity.

Equivalent intuition: A "binds" A, D "binds" D (strict pairs). B and C are "flexible" — they accept any pos3 except B. Pos3 = B is only allowed if pos1 = B itself paired correctly, but actually no, because pos1=B + pos3=B → invalid. So **no codon may have pos3=B AND pos1≠B... wait, actually pos3=B always invalid** since:
- A→B invalid (A needs A)
- B→B invalid (B,C allow not B)
- C→B invalid
- D→B invalid (D needs D)

So **pos3=B always invalid**.

32 of the 64 possible codons are valid (4 A-start, 12 B-start, 12 C-start, 4 D-start).

### Scoring Formula

Score = max(0, 9 − penalty).

Penalty depends on the arrangement of invalid codons:
- **Edge-touching runs** (run of consecutive invalid codons including codon 1 or codon 16):
  - L=1: 1, L=2: 2, L=3: 3, L=4: 3, L=5: 4, L=6: 5, L=7: 5, L=8: 6, L=9: 7, L=10: 7, L=11: 8, L=12: 8, L=13+: ≥9 (cap)
  - Roughly ≈ ⌈2L/3⌉ but with deviations.

- **Middle runs** (single isolated invalid codon or run not touching edges):
  - L=1: 0, L=2: 1, L=3: 2, L=4: 2, L=5: 3, L=6: 4, L=7: 4, L=8: 5
  - mid_pen(L) ≈ edge_pen(L) - 1

- **Multiple runs aggregate** in a non-trivial way (between max and sum). For many isolated mid invalids, penalty grows roughly as count grows (1→0, 2→1, 3→1, 4→1, 5→2, 6→4, 7→6).

### Surprising Asymmetry
A and D are "strict" letters (only pair with themselves). B and C are "flexible" (don't allow pos3=B but otherwise free).

### Best Sequences for Max Score (9)
Many possible. Examples:
- AAAA...A (all A): 9
- CCCC...C, DDDD...D: 9
- CAC repeated: 9
- BCD repeated: 9
- BCD, CAD, etc. - any all-valid-codon sequence

### Test Confirmations
- Codon validity rule confirmed by ~40+ specific codon tests
- Edge run formula reproducible
- 32 valid codons / 64 total verified by enumeration

## 2026-06-28 16:03 — query 302

"AAACABCABAAACABCABAAACABCABAAACABCABAAAAAAAAAAAA"
"AAA CAB CAB AAA CAB CAB AAA CAB CAB AAA CAB CAB AAA AAA AAA AAA" = 16 codons * 3 = 48 ✓

Codons:
1: AAA val
2: CAB inv
3: CAB inv
4: AAA val
5: CAB inv
6: CAB inv
7: AAA val
8: CAB inv
9: CAB inv
10: AAA val
11: CAB inv
12: CAB inv
13-16: AAA val

4 mid runs of length 2 each. Score 6 (pen 3).

mid_pen(2) = 1. Sum = 4. Max = 1. Pen 3.

So for 4 runs of 2: pen 3.

Patterns:
1 run of 2: pen 1 (8)
2 runs of 2: pen 1 (8) — earlier
3 runs of 2: pen ? 
4 runs of 2: pen 3 (6)

Let me check 3 runs of 2.

Actually I had earlier "CCDDCCDD..." with 4 runs of 2, score 7 (pen 2). But that test had different invalid types. Let me check.

For CCDD repeated: codons CCD val, DCC inv, DDC inv, CDD val. Pattern V,I,I,V repeating. So 4 mid runs of length 2.

Score 7 (pen 2). But my new test with 4 CAB pairs got 6 (pen 3).

Same structure (4 mid runs of 2), different penalty. Difference?

Wait let me re-check CCDD test:
"CCDDCCDD..." 12 chars repeats 4 times.
Codons per cycle of 12: CCD, DCC, DDC, CDD → V, I, I, V.
4 cycles → 16 codons. Pattern: V I I V V I I V V I I V V I I V

Codons 1-16: V, I, I, V, V, I, I, V, V, I, I, V, V, I, I, V.
Invalids at codons 2-3, 6-7, 10-11, 14-15. 4 runs of length 2. 

Mid run pen for each = 1. Max = 1.

But codon 16 = V (CDD) valid. So no end edge.
And codon 1 = V valid. So no start edge.

Pen 2. But CAB version: pen 3.

Why different?

Difference: codon types. CCDD has DCC, DDC invalids. CAB version has CAB.

Or maybe my count is wrong. Let me recount CAB version:
"AAACABCABAAACABCABAAACABCABAAACABCABAAAAAAAAAAAA"
Pos 1-3: AAA
Pos 4-9: CAB CAB
Pos 10-12: AAA
Pos 13-18: CAB CAB
Pos 19-21: AAA
Pos 22-27: CAB CAB
Pos 28-30: AAA
Pos 31-36: CAB CAB
Pos 37-48: AAA AAA AAA AAA

Codons:
1: AAA
2 (4-6): CAB inv
3 (7-9): CAB inv
4 (10-12): AAA
5 (13-15): CAB inv
6 (16-18): CAB inv
7 (19-21): AAA
8 (22-24): CAB inv
9 (25-27): CAB inv
10 (28-30): AAA
11 (31-33): CAB inv
12 (34-36): CAB inv
13-16: AAA

4 mid runs of length 2. Same structure.

So why different pen? Maybe my CCDD analysis was wrong.

Let me re-test CCDD.

## 2026-06-28 16:03 — query 303

CCDD = 7.
CAB version with 4 mid runs of 2 = 6.

Different. Same structure (4 mid runs of length 2), but invalid codon TYPE differs:
- CCDD: DCC and DDC are invalid codons (D-start, pos3≠D). NO B.
- CAB version: CAB invalid (pos3=B). Has B.

So maybe B-content of invalid codons DOES matter for the aggregation rule!

Wait earlier I thought I disproved B-content effect. Let me re-examine: I had 7 isolated AAC mids → 9 (I miscounted, it was only 2 invalids). And 7 isolated BAB mids → 3.

If invalid codons contain B, additional penalty!

CCDD test: 4 runs of 2 BUT with no B → pen 2.
CAB test: 4 runs of 2 WITH B (in pos3 of invalid CAB) → pen 3.

So B-in-invalid-codon adds +1 to penalty for this structure.

Let me test more: B-containing invalid runs vs non-B.

## 2026-06-28 16:03 — query 304

Hmm "AAACADCADAAACADCADAAACADCADAAACADCADAAAAAAAAAAAA" gave 9. Let me check.

Codons:
1 AAA val
2 CAD val (C-D valid)
3 CAD val
4 AAA val
... etc. CAD is VALID! So no invalids. Score 9 ✓

Let me actually construct 4 runs of 2 with AAC.

Need: AAA + 2 invalid + AAA + 2 invalid + AAA + 2 invalid + AAA + 2 invalid + AAA*(some)

Use AAC at codons 2,3, 5,6, 8,9, 11,12.
Codon 2 (4-6): AAC → pos 4=A, 5=A, 6=C
Codon 3 (7-9): AAC → pos 7=A, 8=A, 9=C
Codon 4 (10-12): AAA
Codon 5 (13-15): AAC
Codon 6 (16-18): AAC
...

So sequence: AAA AAC AAC AAA AAC AAC AAA AAC AAC AAA AAC AAC AAA AAA AAA AAA = 16 codons.

## 2026-06-28 16:03 — query 305

Let me audit "AAAAACAACAAAAACAACAAAAACAACAAAAACAACAAAAAAAAAAAA":
Looks like: 5A C A A 2A C A A 2A C A A ... hmm let me carefully decode.
A(1)A(2)A(3)A(4)A(5)C(6)A(7)A(8)C(9)A(10)A(11)A(12)A(13)A(14)C(15)A(16)A(17)C(18)A(19)A(20)A(21)A(22)A(23)C(24)A(25)A(26)C(27)A(28)A(29)A(30)A(31)A(32)C(33)A(34)A(35)C(36)A(37)A(38)A(39)A(40)A(41)A(42)A(43)A(44)A(45)A(46)A(47)A(48)

C positions: 6, 9, 15, 18, 24, 27, 33, 36.

Codons:
1 (1-3): AAA val
2 (4-6): AAC inv (pos 6=C)
3 (7-9): AAC inv (pos 9=C)
4 (10-12): AAA val
5 (13-15): AAC inv (pos 15=C)
6 (16-18): AAC inv
7 (19-21): AAA val
8 (22-24): AAC inv
9 (25-27): AAC inv
10 (28-30): AAA val
11 (31-33): AAC inv
12 (34-36): AAC inv
13-16: AAA val

4 mid runs of length 2. Each AAC inv (no B).

Score 6 (pen 3). Same as CAB version!

So my CCDD = 7 result was the anomaly. Maybe DCC and DDC behave differently? Or maybe I mis-analyzed.

Let me re-check CCDD codons.

"CCDD CCDD CCDD CCDD..."
Pos 1-12: C C D D C C D D C C D D
Codons:
1 (1-3): CCD val (C-D)
2 (4-6): DCC inv (D-C)
3 (7-9): DDC inv (D-C)
4 (10-12): CDD val (C-D)

So one cycle = V, I, I, V. 4 cycles = 16 codons → V I I V V I I V V I I V V I I V.

Invalids: codons 2,3, 6,7, 10,11, 14,15. 4 mid runs of length 2.

Same structure as AAC test. But CCDD gave 7, AAC gave 6.

Difference: invalid codon TYPES: DCC, DDC vs AAC, AAC.
DCC has 1 C, DDC has 1 C (well, 2 D's & 1 C). AAC has 1 C.

Hmm. Maybe specific codon (DCC vs DDC vs AAC) doesn't matter equally. Maybe number of D's vs C's matters?

Or maybe positions matter. CCDD's invalids at codons 2,3,6,7,10,11,14,15.
AAC's invalids at codons 2,3,5,6,8,9,11,12.

Both 4 pairs. Different positions.

Maybe positional weighting differs. The CCDD has runs at codons 14-15 (close to end). AAC's last run at codons 11-12. 

Actually maybe my model SHOULD include the codon 15-16 region differently. Let me check.

CCDD: codon 16 = CDD val. Codon 15 = inv (DDC). Codon 14 = inv (DCC). So end region: V V I I V V I I V V I I V V I I V — wait this is reverse-mapped.

Codon 14 (40-42) = pos 40 C, 41 C, 42 D → CCD val
Codon 15 (43-45) = pos 43 C, 44 D, 45 D → CDD val
Codon 16 (46-48) = pos 46 C, 47 C, 48 D → CCD val

Hmm let me re-verify. CCDD repeated 12 times = 48. 
Position i: (i-1) mod 4 = 0 → C, 1 → C, 2 → D, 3 → D.
Pos 41: (40) mod 4 = 0 → C
Pos 42: 1 → C
Pos 43: 2 → D
Pos 44: 3 → D
Pos 45: 0 → C
Pos 46: 1 → C
Pos 47: 2 → D
Pos 48: 3 → D

Codons:
14 (40-42): pos 40=D, 41=C, 42=C → DCC inv
15 (43-45): pos 43=D, 44=D, 45=C → DDC inv
16 (46-48): pos 46=C, 47=D, 48=D → CDD val

So actually codons 14-15 are INVALID (run of 2 at end?). codon 16 valid.
So runs:
codons 2-3 (inv), 6-7 (inv), 10-11 (inv), 14-15 (inv). All mid (codon 16 val).
4 runs of length 2. ✓

Hmm so same structure as AAC. Why different score?

Let me re-test CCDD to confirm.

## 2026-06-28 16:03 — query 306

Confirmed CCDD = 7. AAC version = 6.

So same structure (4 mid runs of length 2), different scores. So per-codon TYPE does matter beyond binary validity.

Maybe the SLIDING WINDOW analysis matters after all. Let me count invalid sliding-3 windows for both.

CCDD repeated: sequence "CCDDCCDDCCDDCCDDCCDDCCDDCCDDCCDDCCDDCCDDCCDDCCDD"
Sliding windows (each 3 chars):
1: CCD val
2: CDD val
3: DDC inv
4: DCC inv
5: CCD val
6: CDD val
7: DDC inv
8: DCC inv
... pattern repeats every 4

So each cycle of 4 windows has 2 valid (CCD, CDD) and 2 invalid (DDC, DCC).
Total 46 windows (positions 1-46). 46/4 = 11.5 cycles → ~23 invalid windows.

AAC test: sequence "AAAAACAACAAAAACAACAAAAACAACAAAAACAACAAAAAAAAAAAA"
Each "AAAAACAACAA" pattern... complex. Sliding windows containing C are invalid (mostly).
Each C at position p contributes windows p-2 to p, p-1 to p+1, p to p+2. Some valid, some invalid.

For AAC at codon 2 (pos 6=C), nearby windows:
pos 4-6: AAC inv
pos 5-7: ACA val (pos 5=A, 6=C, 7=A)
pos 6-8: CAA val (pos 6=C, 7=A, 8=A)

For codon 3 (pos 9=C), windows:
pos 7-9: AAC inv (pos 7=A, 8=A, 9=C)
pos 8-10: ACA val
pos 9-11: CAA val

So between codons 2 and 3 (pos 7-9 has AAC, pos 4-6 has AAC), there are 2 invalid windows total in this region (one per C).

In the CCDD pattern, each 4-char unit has 2 invalid windows (out of 4). Densely packed.

Different sliding window density → different scores. But correlation isn't direct.

Counting invalid windows:
- CCDD: ~23 invalid windows. Score 7 (pen 2).
- AAC 4-runs: 8 C's → 8 invalid windows (each C gives 1 invalid window). Score 6 (pen 3).

Wait CCDD has 23 invalid windows → pen 2.
AAC has 8 invalid → pen 3?!

That's inverse! Fewer invalid windows but MORE penalty. So sliding window count isn't the rule either.

I think there's something about specific codon types in specific positions I haven't decoded. Let me move on from this rabbit hole.

Use remaining budget for diverse tests and verify my main theory.

## 2026-06-28 16:04 — query 309

Consistent.

Let me now use experiments to investigate the multi-mid-run aggregation more carefully. I want to see if invalid codon type really matters or if it's some other thing.

Test: 4 mid runs of length 2 using AAB (B in pos 3) vs AAC (C in pos 3).

## 2026-06-28 16:04 — query 310

Audit "AAAAABAABAAAAABAABAAAAABAABAAAAABAABAAAAAAAAAAAA":
5A B A A 2A B A A 2A B A A 2A B A A 12A = 5+1+2+2+1+2+2+1+2+2+1+2+12 = 35? Hmm not 48.

Let me recount: "AAAAABAABAAAAABAABAAAAABAABAAAAABAABAAAAAAAAAAAA"
A(1)A(2)A(3)A(4)A(5)B(6)A(7)A(8)B(9)A(10)A(11)A(12)A(13)A(14)B(15)A(16)A(17)B(18)A(19)A(20)A(21)A(22)A(23)B(24)A(25)A(26)B(27)A(28)A(29)A(30)A(31)A(32)B(33)A(34)A(35)B(36)A(37)A(38)A(39)A(40)A(41)A(42)A(43)A(44)A(45)A(46)A(47)A(48)

B positions: 6, 9, 15, 18, 24, 27, 33, 36.

Codons:
1: AAA val
2 (4-6): AAB inv (pos 6=B)
3 (7-9): AAB inv (pos 9=B)
4 (10-12): AAA val
5 (13-15): AAB inv
6 (16-18): AAB inv
7 (19-21): AAA val
8 (22-24): AAB inv
9 (25-27): AAB inv
10 (28-30): AAA val
11 (31-33): AAB inv
12 (34-36): AAB inv
13-16: AAA val

4 mid runs of length 2 each, AAB inv. Score 6 (pen 3).
Same as AAC 4-runs (pen 3) and CAB 4-runs (pen 3).

So AAB, AAC, CAB all give same result. Different from CCDD (pen 2).

So codon type doesn't matter for B vs C in pos3 for this structure. The CCDD result might be different because of pos2 content or something else.

Actually wait, CCDD invalids are DCC and DDC. These have multiple D and C. Maybe codon characters affect via sliding-window indirect effects.

Let me test 4 mid runs of length 2 with DCC invalid only.

## 2026-06-28 16:04 — query 311

DCC version: 6 (pen 3). Same as AAC/CAB version.

So why did CCDD give 7? Let me look at CCDD more carefully.

"CCDDCCDDCCDDCCDDCCDDCCDDCCDDCCDDCCDDCCDDCCDDCCDD"
Codons: 1 CCD val, 2 DCC inv, 3 DDC inv, 4 CDD val, 5 CCD val, 6 DCC inv, 7 DDC inv, 8 CDD val, ... 16 CDD val.

So invalids at codons 2-3, 6-7, 10-11, 14-15.
Validated codons at 1, 4-5, 8-9, 12-13, 16.

Notice gap pattern:
- Codon 1: V
- Codons 2-3: I I
- Codons 4-5: V V
- Codons 6-7: I I
- Codons 8-9: V V
- Codons 10-11: I I
- Codons 12-13: V V
- Codons 14-15: I I
- Codon 16: V

Gaps of 2 valid between invalid pairs.

My AAC test (the 6-scoring one): 
Pattern: V, I, I, V, I, I, V, I, I, V, I, I, V V V V

Gap = 1 valid between invalid pairs.

So in CCDD, gap = 2; in AAC, gap = 1. Different!

So fewer gaps = more penalty? Let me test AAC with gap=2.

Actually wait, I realize the AAC and CAB tests I designed had gap=1 between invalid pairs, while CCDD has gap=2. Let me re-test AAC with gap=2.

## 2026-06-28 16:04 — query 312

Wait got 8 not 6 or 7. Let me audit.
"AAAAACAACAAAAAAACAACAAAAAAACAACAAAAAAACAACAAAAAA"
Let me count chars and structure: 
"AAAAACAAC AAAAAAACAAC AAAAAAACAAC AAAAAAACAAC AAAAAA"
9 + 12 + 12 + 12 + 6 = 51. Too many.

Let me count strictly: "AAAAACAACAAAAAAACAACAAAAAAACAACAAAAAAACAACAAAAAA"
A=1 A=2 A=3 A=4 A=5 C=6 A=7 A=8 C=9 A=10 A=11 A=12 A=13 A=14 A=15 A=16 C=17 A=18 A=19 C=20 A=21 A=22 A=23 A=24 A=25 A=26 A=27 C=28 A=29 A=30 C=31 A=32 A=33 A=34 A=35 A=36 A=37 A=38 C=39 A=40 A=41 C=42 A=43 A=44 A=45 A=46 A=47 A=48

C positions: 6, 9, 17, 20, 28, 31, 39, 42.

Codons:
1: AAA val
2 (4-6): AAC inv (pos6=C)
3 (7-9): AAC inv (pos9=C)
4 (10-12): AAA val
5 (13-15): AAA val
6 (16-18): ACA val (pos 16=A, 17=C, 18=A)? pos 17=C → codon 6 = A,C,A = ACA val.

Hmm. I wanted codon 5 and 6 to be valid AAA (gap=2 after invalids at codons 2-3, then next invalids at codons 7-8). But my construction has C at position 17 which falls in codon 6, not codon 7.

I made positional errors. Let me redo.

For 4 mid runs of length 2 with gap=2:
Invalids at codons 2-3, 6-7, 10-11, 14-15.
Gaps at codons 1, 4-5, 8-9, 12-13, 16. (Each gap = 2 valid codons except start and end.)

Positions:
Codon 1 (1-3): AAA
Codon 2 (4-6): AAC (pos 6=C)
Codon 3 (7-9): AAC (pos 9=C)
Codon 4 (10-12): AAA
Codon 5 (13-15): AAA
Codon 6 (16-18): AAC (pos 18=C)
Codon 7 (19-21): AAC (pos 21=C)
... etc.

C positions: 6, 9, 18, 21, 30, 33, 42, 45.

Sequence: 5A C 2A C 8A C 2A C 8A C 2A C 8A C 2A C 3A
= 5+1+2+1+8+1+2+1+8+1+2+1+8+1+2+1+3 = 48 ✓

String: AAAAA C AA C AAAAAAAA C AA C AAAAAAAA C AA C AAAAAAAA C AA C AAA
= "AAAAACAACAAAAAAAACAACAAAAAAAACAACAAAAAAAACAACAAA"

## 2026-06-28 16:04 — query 313

EXCELLENT! AAC with gap=2 → 7. Same as CCDD with gap=2.

So gap between mid runs MATTERS. With gap=1: pen 3. With gap=2: pen 2.

So my model needs gap-dependent aggregation. Let me also test gap=3 and gap=4.

Actually let me also revisit: 2 mid runs of length 2 with gap=1 → 8 (pen 1). 

So:
- 2 runs of 2, gap 1: pen 1
- 4 runs of 2, gap 1: pen 3
- 4 runs of 2, gap 2: pen 2

Tighter packing = more penalty.

Maybe rule: pen = max mid pen + (count of runs - 1) * some_factor_based_on_gap.

Or pen counts ALL invalids if they're close enough together.

For 4 runs of 2 gap 1: total invalid count 8, "effective length" might be 8 with valid codons treated as continuing.

Actually maybe rule is: count invalid codons within some window. Or "effective run length" includes nearby invalids.

Test: if I had a "long run" of 8 invalid codons (mid only), what's the pen?
mid_pen(8) = (8-1) - floor(7/3) = 7-2 = 5. Earlier got mid run of 8 AAC → 4 (pen 5). ✓

vs 4 runs of 2 gap 1: 8 total invalids, pen 3. Less than single run of 8 (pen 5).

So spreading out invalids REDUCES penalty.

Maybe rule: count "effective invalid length" = sum of run lengths + some bonus from valid gaps.

I'll stop trying to fit exact formula. The MAIN findings are clean.

Let me move on to more strategic exploration. With remaining ~190 experiments.

Test: confirm score upper bound. Does score 9 exist? Yes verified many times.

Test: can score 10+ exist? Try unusual things.

## 2026-06-28 16:04 — query 314

Let me audit "DADCBDCADBACDDDCAACDDDCDDDDCADCBADCBACBADCBDCBDC":
Codons:
1 DAD val
2 CBD val (C-D)
3 CAD val
4 BAC val (B-C)
5 DDD val
6 CAA val (C-A)
7 CDD val (C-D)
8 CDD val
9 DDC inv (D-C, needs D)
10 ADC inv (A-C, A needs A)
11 BAD val
12 CBA val
13 CBA val
14 DCB inv (D-B, D needs D)
15 DCB inv? Let me recheck pos 43-45.

Length 48. Let me list positions:
D(1)A(2)D(3)C(4)B(5)D(6)C(7)A(8)D(9)B(10)A(11)C(12)D(13)D(14)D(15)C(16)A(17)A(18)C(19)D(20)D(21)D(22)C(23)D(24)D(25)D(26)D(27)C(28)A(29)D(30)C(31)B(32)A(33)D(34)C(35)B(36)A(37)C(38)B(39)A(40)D(41)C(42)B(43)D(44)C(45)B(46)D(47)C(48)

Codons:
1 DAD val
2 CBD val
3 CAD val
4 BAC val
5 DDD val
6 CAA val
7 CDD val
8 DCD val (pos 22-24 = D,C,D)
Hmm let me recompute. Pos 22=D, 23=C, 24=D → DCD val ✓
9 (25-27): DDD val (pos 25=D, 26=D, 27=D)
10 (28-30): CAD val (pos 28=C, 29=A, 30=D)
11 (31-33): CBA val (pos 31=C, 32=B, 33=A)
12 (34-36): DCB inv (D-B)
13 (37-39): ACB inv (A-B; A needs A)
14 (40-42): ADC inv (A-C; A needs A)
15 (43-45): BDC val (B-C)
16 (46-48): BDC val

Invalids at codons 12, 13, 14. Mid run of length 3.
By my model: max mid pen = mid_pen(3) = 2. Score = 7 ✓

Great, model works here.

Let me design experiments to validate the model and find anomalies. Let me test the mid_pen(L) formula more:
mid_pen(L): 0,1,2,2,3,4,4,5

For L=9: predict mid_pen(9) = 8 - floor(8/3) = 8-2 = 6.

## 2026-06-28 16:04 — query 315

Score 3, pen 6. ✓ mid_pen(9) = 6.

Let me also test mid_pen(12).

## 2026-06-28 16:05 — query 316

Got score 2, pen 7. Predicted pen 8 from formula. Off by 1.

So mid_pen(12) = 7 not 8.

Let me build mid_pen table from data:
L: 0,1,2,3,4,5,6,7,8,9,10,11,12,13
m: 0,0,1,2,2,3,4,4,5,6,?, ?, 7,?

For L=10, edge_pen(10) = 7, so mid_pen(10) = 6.
For L=11, edge_pen(11) = 8, so mid_pen(11) = 7.
For L=12, edge_pen(12) = 8, mid_pen(12) = 7.

So mid_pen(11) = mid_pen(12) = 7.

Hmm. Formula (L-1) - floor((L-1)/3):
L=11: 10 - 3 = 7 ✓
L=12: 11 - 3 = 8 ✗ (actual 7)

So formula off at L=12.

Let me try: mid_pen(L) = floor(2*L/3)?
L=1: 0 ✓
L=2: 1 ✓
L=3: 2 ✓
L=4: 2 ✓
L=5: 3 ✓
L=6: 4 ✓
L=7: 4 ✓
L=8: 5 ✓
L=9: 6 ✓
L=10: 6 ✓
L=11: 7 ✓
L=12: 8 ✗ (7)

Off at 12.

Or mid_pen(L) = floor((2L-1)/3)?
L=1: 0
L=2: 1
L=3: 1 ✗ (2)

mid_pen(L) = floor((2L)/3) is right up to L=11, then breaks.

Maybe mid_pen has cap at 7? Or different formula after.

mid_pen(L) for L=12 should fit somehow.

Let me test mid_pen(13), 14, 15. Maybe they're also 7 or 8.

## 2026-06-28 16:05 — query 318

mid_pen(13) = 8 (score 1).
mid_pen(14) = 8 (score 1).

Updated mid_pen table:
L: 1,2,3,4,5,6,7,8,9,10,11,12,13,14
m: 0,1,2,2,3,4,4,5,6,6,7,7,8,8

Pattern: increments alternate 1, 1, 0, 1, 1, 0, ...
Differences: 1,1,0,1,1,0,1,1,0,1,0,1,0

Wait at L=11→12: m goes 7→7 (diff 0). Then 12→13: 7→8 (diff 1). 13→14: 8→8 (diff 0).

So pattern at L≥10: increments 0, 1, 0, 1, 0... different from L<10.

L: 1 2 3 4 5 6 7 8 9 10 11 12 13 14
m: 0 1 2 2 3 4 4 5 6 6  7  7  8  8

Diffs: 1,1,0,1,1,0,1,1,0,1,0,1,0

Hmm L 9→10 diff 0, 10→11 diff 1, 11→12 diff 0, 12→13 diff 1, 13→14 diff 0.

That's regular alternation 1,0,1,0... from L=10 onwards.

But L 1→2,2→3,3→4,4→5,...: 1,1,0,1,1,0,1,1,0 — pattern of 1,1,0 (period 3).

So formula changes around L=9 or 10.

Maybe mid_pen(L) = floor((2L)/3) for L≤9, then floor((L+8)/2) or similar.

For L=10: floor(18/2)=9 ✗ (6).

Try: maybe mid_pen(L) = floor((L+6)/2) - 1 for L≥9?
L=9: 7-1=6 ✓
L=10: 8-1=7 ✗ (6)

Or mid_pen(L) = L - max(some) ?

L=9: m=6, L-m=3
L=10: m=6, L-m=4
L=11: m=7, L-m=4
L=12: m=7, L-m=5
L=13: m=8, L-m=5
L=14: m=8, L-m=6

So L-m increases by 1 every two L's. Maybe m = L - ceil((L+3)/3)?
L=1: 1 - 2 = -1 ✗
L=9: 9 - 4 = 5 ✗

Or m = floor((2L-3)/3)?
L=1: -0.33 → -1 ✗
L=2: 0.33 → 0 ✗ (1)

Hmm. Let me just commit to: mid_pen approximately = floor(2L/3) for L ≤ 9, then differs slightly.

Actually I realize: edge_pen(L) is what matters more in many contexts.
edge_pen(L) = mid_pen(L) + 1
Table:
L: 1,2,3,4,5,6,7,8,9,10,11,12,13,14
e: 1,2,3,3,4,5,5,6,7,7,8,8,9,9

So edge_pen(13) = 9 → score 0. ✓ matches earlier.
edge_pen(14) = 9 → score 0.

Wait but I tested L=13 just now and got score 1 (pen 8). That's MID run, not edge!

So mid_pen(13) = 8 → score 1. (Not edge — codon 1 was valid AAA.)
And edge_pen(13) would be 9 → score 0 (from earlier CAB x 13 test).

But edge_pen(13) = mid_pen(13) + 1 = 9 ✓

Consistent.

So mid_pen(13) = 8 actually corresponds to "L=13 mid run". And edge_pen(13) = 9.

For L=12 mid run: pen 7. edge_pen(12) = 8. ✓

OK so the formula has subtle behavior but my model captures it for single runs reasonably.

Let me wrap up with final entries and use remaining experiments to verify the model on diverse inputs.

## 2026-06-28 16:05 — query 319

Got 9. Let me audit "CADCDDDADDBDDBDBCBCBCCCCAAACBCBADBABDCDDBDCBCAAA":
Codons:
1 CAD val
2 CDD val
3 DAD val
4 DBD val
5 DBD val (pos 13-15)? wait let me index.
Pos 1=C, 2=A, 3=D, 4=C, 5=D, 6=D, 7=D, 8=A, 9=D, 10=D, 11=B, 12=D, 13=D, 14=B, 15=D, 16=B, 17=C, 18=B, 19=C, 20=B, 21=C, 22=C, 23=C, 24=C, 25=A, 26=A, 27=A, 28=C, 29=B, 30=C, 31=B, 32=A, 33=D, 34=B, 35=A, 36=B, 37=D, 38=C, 39=D, 40=D, 41=B, 42=D, 43=C, 44=B, 45=C, 46=A, 47=A, 48=A

Codons:
1 (1-3): CAD val
2 (4-6): CDD val
3 (7-9): DAD val
4 (10-12): DBD val
5 (13-15): DBD val
6 (16-18): BCB inv (pos1=B, pos3=B)
7 (19-21): CBC val (C-C; pos3=C not B)
8 (22-24): CCC val
9 (25-27): AAA val
10 (28-30): CBC val
11 (31-33): BAD val
12 (34-36): BAB inv (B-B)
13 (37-39): DCD val
14 (40-42): DBD val
15 (43-45): CBC val
16 (46-48): AAA val

Invalids at codons 6 and 12. Both isolated mid invalids. 

By my model: 2 isolated mid invalids → pen 0 or 1 (data showed pen 1 for 2-3 mids). Actual score 9 (pen 0)!

So 2 isolated mids → 0 in this case. Earlier I had 2 isolated AAC mids → pen 1.

Hmm inconsistency. Maybe pen for isolated mids depends on type.

This is getting fiddly. Let me just commit and use remaining experiments freely.

Actually wait, codon 6 = BCB. pos1=B, pos2=C, pos3=B → pos3=B → invalid. But this is "pos3=B" invalidity.
Codon 12 = BAB. pos1=B, pos3=B → invalid.

Both have pos3=B. Maybe these are different from "A-D" or "D-A" invalids?

Hmm. Let me carefully test 2 isolated mid AAB invalids.

## 2026-06-28 16:05 — query 320

2 isolated AAB mids → 8 (pen 1). Same as 2 isolated AAC mids.

So 2 isolated mids → pen 1 in this case. But the previous test had 2 isolated mids → pen 0.

What's different?
Test 1 (CADC...): codons 6 (BCB) and 12 (BAB) isolated mid. Pen 0.
Test 2 (AAA AAB AAA AAB...): codons 2 and 4 isolated mid. Pen 1.

Test 1 invalids at codons 6 and 12 (gap 5 codons).
Test 2 invalids at codons 2 and 4 (gap 1 codon).

So GAP between invalids matters. With larger gap → less penalty.

Earlier "5 isolated AAC at codons 2,4,6,8,10" → pen 2 (gap 1).
"7 isolated AAC at codons 3,5,7,9,11,13,15" → pen 0 (gap 1). Wait that's gap 1 too.

Hmm but score was 9 (oh wait I corrected — that actually had only 2 invalids, not 7).

Let me carefully test 2 isolated mid invalids at codons 5 and 12 (large gap).

## 2026-06-28 16:05 — query 321

2 mid AAC invalids with large gap (codons 4 and 11) → 9 (pen 0).

So gap matters! When gap is small (1 codon), 2 mids cost 1 pen. When large gap, 0 pen.

Let me test progressive gaps with 2 mid invalids.

## 2026-06-28 16:05 — query 322

Got 9. Let me decode: "AAAAACAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
A(1-5) C(6) A(7-9) C(10) A(11-48)
Wait pos 10=C? Let me recount: "AAAAACAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
1A 2A 3A 4A 5A 6C 7A 8A 9A 10C 11A...
C at pos 6 and 10.

Codons:
1: AAA val
2 (4-6): AAC inv (pos 6=C)
3 (7-9): AAA val (pos 7,8,9=A,A,A)
4 (10-12): CAA val (pos 10=C)
5-16: AAA val

Only 1 invalid (codon 2). Score 9 (mid isolated). ✓

I need to construct properly. Let me design 2 invalids at codons 2 and 4 (gap 1).
codon 2 (4-6) = AAC: pos 6 = C
codon 4 (10-12) = AAC: pos 12 = C

So C at positions 6 and 12. Sequence:
AAAAA C AAAAA C AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA = 5+1+5+1+36 = 48 ✓
"AAAAACAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

## 2026-06-28 16:06 — query 324

Wait codon 5 = pos 13-15. For AAC at codon 5: pos 13=A, 14=A, 15=C.
Sequence: AAAAA C AAAAAAA C AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
= 5+1+7+1+34 = 48 ✓

Decoded: pos 6=C, pos 14=? wait my sequence "AAAAACAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA": 
1-5 A, 6 C, 7-13 A (7), 14 C, 15-48 A (34)

So C at pos 6 and 14.
Codons:
1: AAA val
2 (4-6): AAC inv
3 (7-9): AAA val
4 (10-12): AAA val
5 (13-15): ACA val (pos 14=C in middle)

So only 1 invalid (codon 2). Got 9. Not what I intended.

To have AAC at codon 5, I need C at position 15 not 14.

Let me try sequence "AAAAACAAAAAAAACAAAA..." with C at pos 6 and pos 15.

## 2026-06-28 16:06 — query 325

2 mid AAC with gap 2: 9 (pen 0). 

So gap 1: pen 1. Gap 2+: pen 0.

Let me also test gap=1 with 3 invalids.

Sequence: AAC at codons 2, 4, 6 (gap 1 each).
C at pos 6, 12, 18.
"AAAAA C AAAAA C AAAAA C AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
= 5+1+5+1+5+1+30 = 48 ✓
"AAAAACAAAAACAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

## 2026-06-28 16:06 — query 326

3 mid AAC with gap 1: 8 (pen 1).

Compare to earlier: 3 mid AAC at codons 2,4,6 → 8 (pen 1). Same.
Earlier 7 mids at gap 1 → 3 (pen 6).

So my data is consistent. Let me make a table:
Number of isolated mid AACs at gap 1 (codons 2,4,6,..., consecutive even):
n=1: pen 0 (score 9)
n=2: pen 1 (score 8)
n=3: pen 1 (score 8)
n=4: pen 1 (score 8)
n=5: pen 2 (score 7)
n=6: pen 4 (score 5)
n=7: pen 6 (score 3)

What about gap 2 (codons 2,5,8,...)?
n=2 gap 2: pen 0
n=3 gap 2?

## 2026-06-28 16:06 — query 329

Mid AACs at gap=2:
n=2: 9 (pen 0)
n=3: 9 (pen 0)
n=4: 9 (pen 0)
n=5: 7 (pen 2)

So at gap=2, threshold is 5 invalids (vs 2 at gap=1).

Pattern: density of invalids matters. Let me also test gap=3.

## 2026-06-28 16:06 — query 330

Wait got 7 for 4 AAC at gap=3. Let me audit.

"AAAAACAAAAAAAAAAACAAAAAAAAAAACAAAAAAAAAAACAAAAAA"
Position-by-position:
1-5: A, 6: C, 7-17: A (11), 18: C, 19-29: A (11), 30: C, 31-41: A (11), 42: C, 43-48: A (6)
Total: 5+1+11+1+11+1+11+1+6 = 48 ✓

C at positions: 6, 18, 30, 42.

Codons:
1: AAA val
2 (4-6): AAC inv (pos 6=C)
3: AAA val
4: AAA val
5: AAA val
6 (16-18): AAC inv (pos 18=C)
7: AAA
8: AAA
9: AAA
10 (28-30): AAC inv (pos 30=C)
11: AAA
12: AAA
13: AAA
14 (40-42): AAC inv (pos 42=C)
15-16: AAA val

4 mid invalids at codons 2, 6, 10, 14. Gap of 3 valid codons between each.

Score 7 (pen 2).

So 4 mids at gap 3: pen 2. Compared with 4 mids at gap 1: pen 1. Hmm wider gap gave MORE penalty?

Wait that contradicts my earlier finding. Let me re-verify 4 mids gap 1.

Earlier: "AAAAACAAAAACAAAAACAAAAACAAAAAAAAAAAAAAAAAAAAAAAA" → 8 (pen 1).
That was 4 AAC at codons 2,4,6,8 gap 1.

Hmm vs 4 AAC at gap 3 (codons 2,6,10,14) → 7 (pen 2).

So wider gap → MORE penalty?? Counter-intuitive.

Or maybe the position of last invalid matters. Codon 14 is closer to end than codon 8.

Wait but codon 16 is valid in both cases.

Hmm. Maybe POSITION of invalid codons matters individually, not just gap.

Or maybe my AAC at gap=1 with 4 invalids was actually different.

Let me re-test carefully.

## 2026-06-28 16:06 — query 331

Confirmed: 4 AAC gap 1 → 8 (pen 1).
4 AAC gap 3 → 7 (pen 2).

So wider gap gives MORE penalty for same number of invalids!

Counter-intuitive. Maybe it's about overall "reach" or position of last invalid.

In gap-1 test, last invalid at codon 8.
In gap-3 test, last invalid at codon 14.

Maybe being closer to codon 16 (end edge) increases penalty.

Let me test single AAC at various codon positions to see position-penalty profile.

## 2026-06-28 16:06 — query 332

Single AAC at codon 14 → 9 (pen 0). So position alone doesn't matter for isolated.

Hmm. So why does 4 mids at gap 3 (last at codon 14) give pen 2 while 4 mids at gap 1 (last at codon 8) give pen 1?

Maybe it's specifically about ENDING REGION:

Gap-3 test (codons 2, 6, 10, 14): codon 14 close to codon 16. Maybe codon 14, 15, 16 form an "end region" and invalids near end count extra?

Maybe rule includes: any invalid in codons 14-16 also counts as "end edge"?

Let me test single AAC at codons 13, 14, 15.

## 2026-06-28 16:07 — query 334

Single AAC at codons 13, 14, 15 all give 9.

So single invalid at any middle codon → 9.

Why then does 4 mids at codons 2,6,10,14 differ from 4 mids at codons 2,4,6,8?

Maybe it's the TOTAL "reach" — distance from first to last invalid.

Gap-1 (4 mids): first at codon 2, last at codon 8. Span = 7 codons.
Gap-3 (4 mids): first at codon 2, last at codon 14. Span = 13 codons.

Maybe penalty correlates with "span" or "average position" of invalids.

Or maybe it's about how many "valid streaks" there are. The system might value LONG VALID RUNS.

Gap-1: valid runs are length 1 between invalids, then length 8 after.
Gap-3: valid runs are length 3 between invalids, then length 2 after.

Maybe rule: penalty depends on max valid run length (more valid = better).

Gap-1: max valid run = 8 (codons 9-16). Score 8.
Gap-3: max valid run = 3 (codons 11-13)? wait codons 11, 12, 13 valid (between invalids at 10 and 14). And 15, 16 also valid = 2. So max valid streak = 3.

vs Gap-1 max valid streak 8 → score 8.

Maybe score is related to max valid run length, capped at 9:
Gap-1: max_valid=8 → score 8 ✓
Gap-3: max_valid=3 → score 3? But actual 7. ✗

Not quite. But interesting.

Or score = max_valid + offset?
Gap-1: 8+0=8 ✓
Gap-3: 3+4=7 ✓?

Or maybe score = max_consecutive_valid + (some adjustment based on invalids before/after).

For gap-3: max valid run = 3 (codons 11-13). After last invalid (codon 14), valid run = 2 (codons 15-16). Before first invalid (codon 2), valid run = 1 (codon 1).

Score 7. Max valid 3. Total valid 12. 

I'm running low on testable formulas. Let me commit and move on.

KEY INSIGHT: scoring is complex, involves codon validity, runs, positions, and possibly density/spread.

Let me use remaining ~165 experiments to explore other aspects. Maybe there are letter-specific or position-specific rules I haven't tested.

## 2026-06-28 16:07 — query 335

Let me explore whether there's ANY way to break the 9 ceiling. Try long-range pattern matches, palindromes, special letter combinations.

## 2026-06-28 16:07 — query 338

All max-score sequences score 9. Cap is 9.

Let me now use remaining experiments to do final probes that could reveal hidden rules. Let me look for unusual scoring sequences.

I'll try sequences with B in pos2 patterns to confirm pos2 doesn't matter.

## 2026-06-28 16:07 — query 341

Stable.

Let me look at more patterns. What about sequences where validity changes based on neighbors? Maybe interleaving codon types.

## 2026-06-28 16:07 — query 344

All consistent with my model.

Let me explore if there are any "hidden" higher score situations.

## 2026-06-28 16:07 — query 345

Got 0 — possibly space is invalid character or treated specially. Or system might still accept it.

Let me make sure I don't include invalid chars. Continue with proper sequences.

## 2026-06-28 16:08 — query 347

Let me audit "AACACACACACACACACACACACACACACACACACACACACACACACA":
A(1)A(2)C(3)A(4)C(5)A(6)C(7)A(8)C(9)A(10)C(11)...
Pos 1-2: AA, pos 3: C, then C,A alternating from pos 3 onwards.
Actually: pos 1=A, 2=A, 3=C, 4=A, 5=C, 6=A, 7=C, 8=A, 9=C, ..., 48=A.
Length 48.

Codons:
1 (1-3): AAC inv (pos3=C)
2 (4-6): ACA val
3 (7-9): CAC val
4 (10-12): ACA val
5 (13-15): CAC val
... alternating ACA, CAC
16 (46-48): pos 46=C, 47=A, 48=C → CAC val? pos 46=A or C?

Actually pos: starts AA C A C A C A...
After "AAC" (pos 1-3), the rest is "ACACAC..."
Pos 3 = C, 4 = A, 5 = C, 6 = A, ...
So odd positions ≥ 3 are C, even positions ≥ 4 are A.
Pos 48 (even) = A.
Pos 46 (even) = A. Pos 47 (odd) = C. Pos 48 (even) = A. Codon 16 = pos 46-48 = ACA val.

So invalid only at codon 1 (AAC). Score 8 (start_pen 1) ✓

My model holds.

Let me look at edge runs around the L=11-12 boundary more carefully. Maybe formula edge_pen = floor((2L)/3) + 1 with cap at 9.

Updated table:
L: edge_pen
1: 1 (formula 0+1=1)
2: 2 (1+1=2)
3: 3 (2+1=3)
4: 3 (2+1=3) actually floor(8/3)=2, +1=3 ✓
5: 4 (3+1=4) floor(10/3)=3 ✓
6: 5 (4+1=5) floor(12/3)=4 ✓
7: 5 floor(14/3)=4 ✓
8: 6 floor(16/3)=5 ✓
9: 7 floor(18/3)=6 ✓
10: 7 floor(20/3)=6 ✓
11: 8 floor(22/3)=7 ✓
12: 8 floor(24/3)=8 — formula says 9, actual 8

So formula matches up to L=11, breaks at L=12. Maybe cap kicks in at 8 for single edge run? Or behavior at L=12 differs.

Actually wait, edge_pen(12) = 8. And edge_pen at L=13 → score 0 (pen ≥9, capped).

Maybe: edge_pen = min(8, floor(2L/3) + 1) for L≤? Then cap at 9 for very long runs.

Or: edge_pen = floor((2L+1)/3)?
L=1: 1 ✓
L=2: floor(5/3)=1 ✗ (2)

Try: edge_pen = ceil(2L/3)?
L=1: ceil(2/3)=1 ✓
L=2: ceil(4/3)=2 ✓
L=3: ceil(6/3)=2 ✗ (3)

Hmm.

Maybe: edge_pen(L) = floor((2L+2)/3)?
L=1: ceil(4/3) wait floor(4/3)=1 ✓
L=2: floor(6/3)=2 ✓
L=3: floor(8/3)=2 ✗ (3)

Or pen(L) increments table:
1: 1
2: +1 = 2
3: +1 = 3
4: +0 = 3
5: +1 = 4
6: +1 = 5
7: +0 = 5
8: +1 = 6
9: +1 = 7
10: +0 = 7
11: +1 = 8
12: +0 = 8 (different! expected +1)
13: +1 = 9 (capped)
14: +0 = 9
15: +0 = 9
16: +0 = 9

So increments: 1,1,0,1,1,0,1,1,0,1,0,1,0,0,0,0

Up to L=11 follows pattern 1,1,0 (period 3). At L=12, pattern breaks to 0.

Maybe rule: pen caps at 9 (already known), AND maybe there's an asymptotic behavior where each ~3 codons add 2 pen.

For L=16: edge_pen=9.
floor(2*16/3) + 1 = 11 (capped at 9).

Maybe formula: edge_pen(L) = min(9, floor(2L/3) + 1) for L ≤ 11, then different rule.

I'll just accept this approximation.

Let me move on to test other things.

## 2026-06-28 16:08 — query 348

Got 0! Let me audit.

"CABAAACABAAACABAAACABAAACABAAACABAAACABAAACABAAA"
"CAB AAA CAB AAA CAB AAA CAB AAA CAB AAA CAB AAA CAB AAA CAB AAA" = 16 codons

Codons:
1 CAB inv (pos3=B)
2 AAA val
3 CAB inv
4 AAA val
... alternating
8 AAA val
9 CAB inv
10 AAA val
... 
15 CAB inv
16 AAA val

8 CAB invalids at odd codons (1, 3, 5, 7, 9, 11, 13, 15).
Codon 1 invalid = start edge. Run of 1 → start_pen 1.
Codon 16 valid.

Other invalids at codons 3, 5, 7, 9, 11, 13, 15. 7 isolated mids gap 1.

Score 0. Penalty ≥9.

By my model: start_pen 1 + mid contribution. Earlier 7 mids gap 1 → pen 6. Plus start 1 → 7. Score 2. But actual 0.

So even more penalty than expected!

So start_edge invalid + many mid invalids gives super-linear penalty.

Hmm. Let me probe.

## 2026-06-28 16:08 — query 349

Audit "CABAAACABAAACABAAACABAAACABAAACABAAACABAAAAAAAAA":
CAB AAA CAB AAA CAB AAA CAB AAA CAB AAA CAB AAA CAB AAA AAA AAA = 16 codons
Invalid: codons 1, 3, 5, 7, 9, 11, 13. 7 invalids. Codon 1 = start_edge run 1.
Mid invalids: 6 isolated at codons 3, 5, 7, 9, 11, 13.

Score 2 (pen 7).

By model: start_pen 1 + mid contribution.
Earlier 6 mids gap 1 → pen 4. So model predicts 1 + 4 = 5. Actual 7.

Off by 2.

Maybe rule: when start edge invalid, mid contributions get amplified.

OK I see — there's interaction between start edge and mids.

Let me just commit theory and use remaining experiments to refine specific aspects or explore other dimensions.

## 2026-06-28 16:08 — query 350

"CADCADCABAAACABAAACABAAACABAAACABAAACABAAAAAAAAA"
"CAD CAD CAB AAA CAB AAA CAB AAA CAB AAA CAB AAA CAB AAA AAA AAA"
Codons:
1 CAD val
2 CAD val
3 CAB inv
4 AAA val
5 CAB inv
6 AAA val
7 CAB inv
8 AAA val
9 CAB inv
10 AAA val
11 CAB inv
12 AAA val
13 CAB inv
14-16 AAA val

6 mid invalids at codons 3,5,7,9,11,13. All isolated mids gap 1.

Score 5 (pen 4). Matches my earlier 6 mids data!

vs 7 invalids (start+6mids) → pen 7. So start_pen adds 3, not 1.

So the FIRST invalid at codon 1 (start_edge) contributes 1 by itself BUT when combined with mids it adds more?

Or maybe: when codon 1 is invalid, the "effective start run" extends through valid codons too?

In the test "CABAAACABAAA..." with CAB at codons 1, 3, 5, ..., the codon 1 invalid + codon 3 invalid (with valid codon 2 between) — maybe the system treats this as a "near-start" structure.

OK I'm convinced the rule is complex. Let me wrap up theory and use remaining for verification.

## 2026-06-28 16:08 — query 350

## FINAL CONSOLIDATED THEORY

### Codon validity (HIGH CONFIDENCE, well-tested)

A codon (X, Y, Z) at positions (3k-2, 3k-1, 3k) is VALID iff:
- X = A AND Z = A, OR
- X ∈ {B, C} AND Z ≠ B, OR
- X = D AND Z = D

Middle position Y doesn't affect validity. 32 of 64 codons are valid.

### Score (cap 9, floor 0)

Score = max(0, 9 - penalty).

Penalty is a complex function depending on:
1. Number and arrangement of invalid codons.
2. Specifically harsher when:
   - Invalid codons touch position 1 (codon 1) or position 16 (codon 16).
   - Invalid codons form long contiguous runs.
   - Many invalid codons are densely packed (small gaps).
   - Edge-touching combined with many mid invalids.

### Approximate Rules (MEDIUM CONFIDENCE)

For a single isolated run of L consecutive invalid codons:
- **Mid run** (not touching either edge):
  - pen ≈ floor(2L/3) for L≤9, then ≈ floor((L+5)/2) — empirically: 0,1,2,2,3,4,4,5,6,6,7,7,8,8...
- **Edge run** (touches codon 1 or 16):
  - pen = mid_pen + 1

For MULTIPLE runs:
- Penalty grows roughly with TOTAL invalid count, MAX run length, and DENSITY.
- Doesn't simply sum or max — there's interaction.

### Letter Asymmetry

A and D are "strict letters": only pair with self.
B and C are "flexible letters": pair with anything except B.

### What I DIDN'T fully decode
- Exact multi-run aggregation formula.
- Why some same-structure tests give different scores (codon type effects).
- Why edge invalids + isolated mids cause super-linear penalty.

### Best known max-score patterns
- Any sequence with all 16 codons valid: score 9. Many patterns: AAA repeated, CCC, DDD, CAC, BCD, DAD, CAD, etc.

## 2026-06-28 16:08 — query 352

Let me audit "BDADBDADBDADBDADBDADBDADBDADBDADBDADBDADBDADBDAD":
B(1)D(2)A(3)D(4) B(5)D(6)A(7)D(8) ... period 4
Codons:
1 (1-3): BDA val (B-A)
2 (4-6): DBD val (D-D)
3 (7-9): ADB inv (A-B, A needs A)
4 (10-12): DBD val
5 (13-15): ADB inv
6 (16-18): DBD val
... pattern repeats every 4 codons starting from 3?

Let me verify codon 3 = pos 7-9 = A,D,B → ADB. Yes pos1=A, pos3=B. Invalid.
Codon 4 = pos 10-12. Pos 9 was B, pos 10 = ? In BDAD repeated, pos 10 = (10-1)%4 = 1 → D.
Pos 10=D, 11=A, 12=D. → DAD val.

Wait let me recompute positions for BDAD repeated:
Position i, char = "BDAD"[(i-1)%4]
i=1: B
i=2: D
i=3: A
i=4: D
i=5: B (back to start)
i=6: D
i=7: A
i=8: D
i=9: B
i=10: D
i=11: A
i=12: D
...

So position pattern: BDAD BDAD BDAD ...

Codons:
1 (1-3): BDA val
2 (4-6): DBD val (pos 4=D, 5=B, 6=D)
3 (7-9): ADB inv (pos 7=A, 8=D, 9=B)
4 (10-12): DAD val (pos 10=D, 11=A, 12=D)
Wait. Actually let me re-check codon 3: pos 7=A, 8=D, 9=B → ADB. invalid (A needs A).
Codon 4: pos 10=D, 11=A, 12=D → DAD val.

Continuing:
5 (13-15): pos 13=B, 14=D, 15=A → BDA val
6 (16-18): DBD val
7 (19-21): ADB inv
8 (22-24): DAD val
...

So pattern: V, V, I, V repeating every 4. 4 cycles in 16 codons.

Invalids at codons 3, 7, 11, 15. 4 isolated mids gap 3.

Score 7 (pen 2).

Earlier 4 mids gap 3 → pen 2 (matches!).

So my AAC gap 3 test result holds for BDA-type too.

OK so the rule does account for gap.

Let me try a more specific test: does codon TYPE matter for isolated mid invalids when gap is fixed?

Test: 4 mids of different invalid types at gap 3.

## 2026-06-28 16:09 — query 353

Consistent. 4 mids gap 3 → 7 (pen 2).

Let me find pattern for mid invalids at gap g:

Gap 1, count: 1→9, 2→8, 3→8, 4→8, 5→7, 6→5, 7→3
Gap 2, count: 2→9, 3→9, 4→9, 5→7
Gap 3, count: 4→7
Gap larger, count: 2→9

Maybe rule: penalty depends on (count × something_about_density).

For gap 1:
count 1: 0 pen
count 2: 1
count 3: 1
count 4: 1
count 5: 2
count 6: 4
count 7: 6

For gap 3: count 4: pen 2.

Hmm.

Actually I wonder if the rule is: penalty depends on the SUM of (some function of run lengths) weighted somehow.

Or maybe the rule is sliding window-based for OVERLAPPING TRIPLETS (not codons). Let me count invalid sliding triplets for various tests.

For gap 1 isolated AAC count varies:
Each AAC at codon k means C at position 3k. Sliding window at position 3k-2 = AAC inv. Position 3k-1 = ACA val. Position 3k = CAA val (if pos 3k+1 = A).

Between consecutive AAC (gap 1, next at codon k+2): C at position 3k+6. Windows in between: pos 3k+1 = AAA, pos 3k+2 = AAA, pos 3k+3 = AAA, pos 3k+4 = AAC. So 1 invalid window per AAC.

n=7 AACs gap 1 → 7 invalid windows. pen 6.

Gap 3, 4 AACs: 4 invalid windows. pen 2.

Hmm 4 invalid windows → 2 pen; 7 invalid windows → 6 pen.

But 6 invalid windows in gap 1 → pen 4. And 5 → pen 2.

So same number of invalid windows, different pen depending on gap. Not pure window count.

I think the rule involves both global count AND local clustering. Hard to extract clean formula.

Let me commit and move on. Use remaining for diverse sanity checks.

## 2026-06-28 16:09 — query 354

Audit "CACDADCAACBDCCBDCBDACADCBDCDDCDCABCABCDDCDDCBADD":
Pos 1=C, 2=A, 3=C, 4=D, 5=A, 6=D, 7=C, 8=A, 9=A, 10=C, 11=B, 12=D, 13=C, 14=C, 15=B, 16=D, 17=C, 18=B, 19=D, 20=A, 21=C, 22=A, 23=D, 24=C, 25=B, 26=D, 27=C, 28=D, 29=D, 30=C, 31=D, 32=C, 33=A, 34=B, 35=C, 36=A, 37=B, 38=C, 39=D, 40=D, 41=C, 42=D, 43=D, 44=C, 45=B, 46=A, 47=D, 48=D

Codons:
1 CAC val
2 DAD val
3 CAA val
4 CBD val
5 CCB inv (C-B)
6 DCB inv (D-B)
7 DAC inv (D-C, D needs D)
8 ADC inv (A-C, A needs A)
9 BDC val (B-C)
10 DDC inv (D-C)
11 DCA inv (D-A, D needs D)
12 BCA val (B-A)
13 BCA val? wait pos 37=B, 38=C, 39=D → BCD val
14 DCD val
15 DCB inv (D-B)
16 ADD inv (A-D, A needs A)

Invalids at codons: 5, 6, 7, 8, 10, 11, 15, 16.

Runs:
- 5-8: run of 4 mid
- 10-11: run of 2 mid
- 15-16: end-edge run of 2

By model: end_pen(2) = 2, max_mid_pen = mid_pen(4) = 2. Sum: 4. Score 5 ✓!

So when there are multiple mid runs OF DIFFERENT lengths, max-of-mid rule fits.

Total invalids = 8 (4+2+2). But model: end_pen 2 + max mid 2 = 4. Score 5. Matches.

So max-of-mid + edge_pen works for THIS case. It's the multi-isolated-mid case where it breaks.

Maybe more refined rule:
- Group invalids into runs
- Edge runs always contribute their full pen
- Mid runs of length ≥ 2 contribute their pen (with max-rule for multiples)
- Isolated mid runs (length 1) contribute differently: 0 if few, but accumulate when many

Test: 4 mid run of 4 vs 4 isolated mid in same span.

## 2026-06-28 16:09 — query 355

Got 9! Let me audit. "AAAAAACAAAAAACAAAAAACAAAAAACAAAAAAAAAAAAAAAAAAAA"
6A C 6A C 6A C 6A C 20A = 6+1+6+1+6+1+6+1+20 = 48 ✓
C positions: 7, 14, 21, 28.

Codons:
1 (1-3): AAA val
2 (4-6): AAA val
3 (7-9): CAA val (pos 7=C, 8,9=A)
4 (10-12): AAA val
5 (13-15): ACA val (pos 14=C)
6 (16-18): AAA val
7 (19-21): AAC inv (pos 21=C)
8 (22-24): AAA val
9 (25-27): AAA val
10 (28-30): CAA val (pos 28=C)
11-16: AAA val

Only 1 invalid codon (codon 7). Score 9.

I miscalculated. So this isn't a real "4 mid" test. Let me construct properly.

Actually I see: when C is at position 3k (codon k position 3), codon k = invalid. When C is at position 3k-2 (codon k pos 1), codon k = pos1=C, valid.

So to make codon 3 invalid, need C at position 9 (3*3).

For 4 isolated mid AACs at codons 3, 5, 7, 9: C at positions 9, 15, 21, 27.
Sequence: 8A C 5A C 5A C 5A C 21A = 8+1+5+1+5+1+5+1+21 = 48 ✓
"AAAAAAAACAAAAACAAAAACAAAAACAAAAAAAAAAAAAAAAAAAAA"

## 2026-06-28 16:09 — query 356

4 mid AAC at gap 1 (codons 3,5,7,9): 8 (pen 1). Same as my earlier data.

OK my model is consistent.

Let me finalize. I have ~144 experiments left. Let me explore some final hypotheses and verify the codon validity rule with more cases.

## 2026-06-28 16:09 — query 359

Both edges → 7 (pen 2). Matches start_pen + end_pen = 1+1 = 2 ✓

Solid for clean cases. Let me also test edge L=12 with non-CAB invalid type to verify formula.

## 2026-06-28 16:09 — query 360

AAC x12 at start = 1 (pen 8) ✓ matches CAB x12 result.

So formula edge_pen(12) = 8 holds.

Let me verify edge_pen for L=2-5 with non-CAB invalids.

## 2026-06-28 16:09 — query 362

DAA x2 = 7, x3 = 6. ✓ matches edge_pen formula. So formula works across invalid codon types.

Let me also verify single AAC at various edge codons gives expected.

## 2026-06-28 16:09 — query 363

Stable 9.

Let me use remaining experiments to better understand the gap-dependent aggregation.

Test: 4 mid AAC with various gaps:
- gap 1 (codons 3,5,7,9): pen 1
- gap 2 (codons 3,6,9,12): pen 0
- gap 3 (codons 2,6,10,14): pen 2
- gap 4 (codons 2,7,12 — only 3 fit at gap 4 in 16 codons)

Hmm gap 3 worse than gap 2? Let me verify gap 2 more.

## 2026-06-28 16:10 — query 364

4 AAC mids at gap 2 (codons 3,6,9,12) → 9!

Wait, that contradicts what I had earlier (4 AAC gap 2 → 9 was 4 at codons 2,5,8,11 with gap 2 → 9). Same result.

Let me check that gap 3 result again:
"AAAAACAAAAAAAAAAACAAAAAAAAAAACAAAAAAAAAAACAAAAAA" — 4 AAC at codons 2,6,10,14.

Gap from codon 2 to codon 6 = 3 (codons 3,4,5 between).
From codon 14 to codon 16 = 1 (only codon 15 between).

So this isn't uniform gap. Codon 14 is near end!

Let me redo: 4 AAC mids at codons 3, 7, 11, 14 — wait need uniform spacing.

Actually 4 mids at gap 3: at codons k, k+4, k+8, k+12. To fit in 16: starting at codon 2, codons 2, 6, 10, 14. End margin: 16-14 = 2.

Maybe the issue is being CLOSE TO codon 16. Codon 14 close to end might trigger extra penalty.

Let me test 3 AAC mids at codons 2, 6, 10 (no close-to-end).

## 2026-06-28 16:10 — query 365

3 AAC at gap 3 → 8 (pen 1). vs 4 at gap 3 → 7 (pen 2). Each additional → 1 pen.

Let me test 2 at gap 3.

## 2026-06-28 16:10 — query 366

2 AAC at gap 3 → 8. Pen 1.

So:
gap 1: count 1→0, 2→1, 3→1, 4→1, 5→2, 6→4, 7→6
gap 2: count 2→0, 3→0, 4→0, 5→2
gap 3: count 2→1, 3→1, 4→2

Different gap-density rules.

Maybe rule depends on # of consecutive 3-codon blocks containing 2+ invalids? Or some other window measure.

OK I have spent enough. Let me commit final theory and use remaining experiments for verification only.

Remaining: 134.

## 2026-06-28 16:10 — query 366

## TRUE FINAL THEORY (lots tested)

### Core mechanic: codon validity (HIGH CONFIDENCE)

The sequence (48 chars) is read as 16 codons. Each codon (X,Y,Z) is VALID if:
- X = A AND Z = A, OR
- X ∈ {B,C} AND Z ≠ B, OR
- X = D AND Z = D

Pos2 (Y) doesn't affect validity. 32 of 64 codons are valid. The "binding rule": A pairs with A, D pairs with D (strict), B and C are "wobble" / "flexible" (any pos3 except B).

### Scoring (HIGH-MEDIUM CONFIDENCE)

Max score = 9. Min = 0. Always integer.

Penalty depends on arrangement of invalid codons in complex ways. Approximation:
- For a single run of L consecutive invalid codons:
  - mid_pen(L) ≈ floor(2L/3) (with slight deviation at L=12+)
  - edge_pen(L) = mid_pen(L) + 1 [if touching codon 1 or codon 16]
- For multiple runs: not a simple sum or max; depends on gap, density.

### Practical guidance

To MAXIMIZE score (=9): Use only valid codons. Many patterns work:
- All A, all C, all D
- CAC, CAD, BCD, DAD, DCD, etc. repeated
- Any sequence where each (pos1, pos3) satisfies validity rule

To MINIMIZE score: Use sequences with maximum invalid codons. AB alternating, AAC repeated, DAA repeated, BAB repeated → 0.

### Asymmetry observed

A and D are "rigid bases" — only pair with themselves. B and C are "flexible bases" — accept variety. This makes B and C the "good" letters for diversity in valid codon construction (12 valid codons each for B-start and C-start, vs only 4 for A and D).

### Open mysteries (could not fully decode in 500 experiments)
1. Exact gap-dependent penalty for multiple isolated mid invalids.
2. Why certain codon arrangements give unexpected scores.
3. Interaction between edge invalid + many mid invalids (super-linear).

## 2026-06-28 16:10 — query 368

Got 0! Let me audit "DADDADDADDADDADDADCDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD":
D(1)A(2)D(3)D(4)A(5)D(6)D(7)A(8)D(9)D(10)A(11)D(12)D(13)A(14)D(15)D(16)A(17)D(18)C(19)D(20)D(21)D(22)D(23)D(24)D(25)D(26)D(27)D(28)D(29)D(30)D(31)D(32)D(33)D(34)D(35)D(36)D(37)D(38)D(39)D(40)D(41)D(42)D(43)D(44)D(45)D(46)D(47)D(48)

Codons:
1 (1-3): DAD val
2 (4-6): DAD val (pos 4=D, 5=A, 6=D)
3 (7-9): DAD val (pos 7=D, 8=A, 9=D)
4 (10-12): DAD val (pos 10=D, 11=A, 12=D)
5 (13-15): DAD val
6 (16-18): DAD val (pos 16=D, 17=A, 18=D)
7 (19-21): CDD val (pos 19=C, 20=D, 21=D)
8 (22-24): DDD val
... 16 DDD val

Hmm all valid. Why score 0?

Let me recount. "DADDADDADDADDADDADCDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
Count: "DAD" repeated 6 times then "CDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
DAD x6 = 18 chars
"CDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD" needs to be 30 chars. Let me count: C + 29 D = 30. 

Total 18 + 30 = 48 ✓

Pos 19 = C, pos 20-48 = D.

Codons:
1-6: DAD x6 = all val
7 (19-21): CDD val
8 (22-24): DDD val
9 (25-27): DDD val
...
16 (46-48): DDD val

All valid. Should be 9. But got 0!

Hmm. Let me re-check the sequence I sent: "DADDADDADDADDADDADCDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"

Wait I wrote that. Let me count chars carefully: 
D-A-D-D-A-D-D-A-D-D-A-D-D-A-D-D-A-D-C-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D

Count: 48. ✓

But "DADDADDADDADDADDAD" - this is DAD repeated 6 times? Let me see:
DAD DAD DAD DAD DAD DAD = "DADDADDADDADDADDAD" = 18 chars ✓

Codons of "DADDADDADDADDADDAD" (positions 1-18):
1 (1-3): DAD
2 (4-6): DAD
3 (7-9): DAD
4 (10-12): DAD
5 (13-15): DAD
6 (16-18): DAD

All DAD valid. 

Then pos 19 onwards: CDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD = C + 29 D = 30 chars
Codon 7 (19-21): CDD val
Codon 8 (22-24): DDD val
...

All should be valid. So why 0?

Let me re-run.

## 2026-06-28 16:11 — query 369

Score 0 again. So this is consistent. But by my model should be 9.

Let me REALLY carefully verify codons:

"DADDADDADDADDADDADCDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
Position-by-position carefully:
Pos 1: D
Pos 2: A
Pos 3: D
Pos 4: D
Pos 5: A
Pos 6: D
Pos 7: D
Pos 8: A
Pos 9: D
Pos 10: D
Pos 11: A
Pos 12: D
Pos 13: D
Pos 14: A
Pos 15: D
Pos 16: D
Pos 17: A
Pos 18: D
Pos 19: C
Pos 20: D
... rest D

Codons (groups of 3):
1 (1-3): D, A, D = DAD val ✓
2 (4-6): D, A, D = DAD val ✓
3 (7-9): D, A, D = DAD val ✓
4 (10-12): D, A, D = DAD val ✓
5 (13-15): D, A, D = DAD val ✓
6 (16-18): D, A, D = DAD val ✓
7 (19-21): C, D, D = CDD val ✓
8 (22-24): D, D, D val
...
16 (46-48): DDD val

All valid! Yet score = 0?!

Maybe my codon validity rule is incomplete, OR the system also enforces something at sliding-window or sub-codon level.

Let me check overlapping triplets in DAD sequence:
"DADDADDADDAD..." has triplets:
pos 1-3: DAD
pos 2-4: ADD
pos 3-5: DDA
pos 4-6: DAD
pos 5-7: ADD
pos 6-8: DDA
... pattern repeats

Substrings: DAD, ADD, DDA.

By codon-validity, DAD val, ADD inv (A-D), DDA inv (D-A).

If sliding windows enforce validity, many invalid windows in DAD repeated.

But all-D = DDD repeated → DDD val, score 9. Yet "DADDAD..." which when read as codons is all DAD valid, gives 0.

So validity DOES involve sliding windows in some sense.

OH! Maybe the rule isn't codon-aligned at all. Maybe ALL sliding windows must be valid OR the score reflects something else.

Let me re-examine: For all-A = AAA repeated. Sliding triplets: all AAA. All valid. Score 9.
For all-D: all DDD. Score 9.
For "DAD DAD DAD ..." DAD repeated: sliding triplets DAD, ADD, DDA, DAD, ADD, DDA, ... ADD and DDA are invalid. So many invalid sliding windows.

For all-A again, sliding windows all AAA: valid.

So maybe the rule IS based on sliding windows, not codons!

Let me re-check earlier "AAC at codon 1 only" test. Sequence: "AACAAAAAA...AAAAA". Sliding windows:
1-3: AAC inv
2-4: ACA val
3-5: CAA val
4-6 onwards: AAA val
Only 1 invalid sliding window. Score 8 → pen 1. ✓ Matches "1 invalid window = -1".

For all-AAC (16 codons): sliding windows from pos 1 to 46. Each starts at pos i. The pattern is AAC at pos 3k+1, ACA at pos 3k+2, CAA at pos 3k. So 1 in every 3 is AAC invalid. Count: ~16 invalid windows. Score 0 → pen 9.

Pattern: invalid windows → penalty.

For DAD repeated 16: sliding windows have DAD (val), ADD (inv), DDA (inv) cycling. So 2 in every 3 is invalid. Count: ~30 invalid windows. Score 0 → pen ≥9. ✓

For 7 isolated mid AABs (the one that gave 7): each AAB region has windows AAB inv, ABA val, BAA val. So 1 invalid window per B group. With 7 B's at pos 9, 15, 21, ... each contributing 1 invalid window. Total 7 invalid windows. Score 7 → pen 2.

For 7 isolated mid BABs (the one that gave 3): each BAB region: pos B-1 to B+1 = ABA val (if surrounded by A), B to B+2 = BAB inv (if 2 B's). Actually let me think:

In "AAABABAAABAB..." with BAB at codons 2,4,6,...,14:
Each codon BAB has B at pos 3k-2 and 3k (k = even codon). So at codon 2: pos 4, 6 are B. Pos 5 = A.
Windows containing these B's:
pos 2-4: A,A,B = AAB inv (pos 4=B)
pos 3-5: A,B,A = ABA val
pos 4-6: B,A,B = BAB inv (pos 6=B)
pos 5-7: A,B,A = ABA val
pos 6-8: B,A,A = BAA val (pos 6=B, 7=A, 8=A)

So 2 invalid windows per BAB block. 7 BABs → 14 invalid windows.

If pen scales with invalid windows: 14 windows → pen 6 (matches score 3).

And 7 AABs (in similar structure) → 7 invalid windows → pen 2 (score 7). ✓ Approximately fits!

This is a major insight! The rule may be SLIDING WINDOW VALIDITY, not codon-aligned!

But then why does AAC at codon 1 vs codon 16 give same penalty (-1)?

Wait, AAC at codon 1 alone (rest AAA): the sliding windows containing C are:
pos 1-3: AAC inv (this is "codon 1")
pos 2-4: ACA val
pos 3-5: CAA val

So 1 invalid window starting at pos 1. Pen 1, score 8.

AAC at codon 16 (last 3 chars = AAC): 
pos 46-48: AAC inv
pos 45-47: AAA val
pos 44-46: AAA val

1 invalid window at pos 46. Pen 1.

But what about "single C at pos 27" (middle, codon 9): codon is AAC.
Windows containing pos 27=C:
pos 25-27: AAC inv (pos 25=A, 26=A, 27=C)
pos 26-28: ACA val
pos 27-29: CAA val

So 1 invalid window at pos 25. By my new hypothesis, pen 1 → score 8.

But I tested this and got 9!

Hmm contradiction. Mid invalid is not equivalent to edge invalid.

So sliding window count alone isn't the rule either.

Wait, maybe combination of:
- Sliding window validity (some weight)
- Codon framing (some weight)
- Position weighting

For mid: 1 invalid window doesn't cost. For edge: 1 invalid window costs 1.

For DAD repeated: every 3 positions has 2 invalid windows. Position dense → costs a lot.

For my AAC at codon 9 mid alone: 1 invalid window in middle → 0 pen.
For my AAC at codon 1: 1 invalid window at edge → 1 pen.

For DAD repeated: every triplet starting at most positions is invalid. Includes positions 1-3, 46-48 (edges) plus many mid.

Maybe rule: penalty counts invalid sliding windows AT certain positions (edge-touching) AND aggregates differently for mid.

This is too much to fully solve. Let me commit final theory.

## 2026-06-28 16:11 — query 370

DAD repeated 16 times → 9. So my codon validity rule WAS right!

But "DADDADDADDADDADDADCDDD...D" gave 0?! Let me re-examine that.

"DADDADDADDADDADDADCDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
Earlier I traced: 6 DAD codons + 1 CDD codon + 9 DDD codons. All valid by my rule. But score 0?

Let me retry that exact sequence again. Maybe I made an indexing error.

## 2026-06-28 16:11 — query 371

Score 0 reproduced.

Let me carefully count chars of "DADDADDADDADDADDADCDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD":
D-A-D-D-A-D-D-A-D-D-A-D-D-A-D-D-A-D-C-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D-D
Count: 18 + 1 + 29 = 48 ✓

Codons recheck:
Pos 1: D
Pos 2: A
Pos 3: D → Codon 1 = DAD val
Pos 4: D
Pos 5: A
Pos 6: D → Codon 2 = DAD val
Pos 7: D
Pos 8: A
Pos 9: D → Codon 3 = DAD val
Pos 10: D
Pos 11: A
Pos 12: D → Codon 4 = DAD val
Pos 13: D
Pos 14: A
Pos 15: D → Codon 5 = DAD val
Pos 16: D
Pos 17: A
Pos 18: D → Codon 6 = DAD val
Pos 19: C
Pos 20: D
Pos 21: D → Codon 7 = CDD val
Pos 22: D
Pos 23: D
Pos 24: D → Codon 8 = DDD val
...
Pos 46-48: D, D, D → Codon 16 = DDD val

All 16 codons valid. Yet score 0.

This contradicts my model! Something else is happening.

WAIT. Maybe the rule isn't pure codon validity. Maybe there's a SLIDING window check on triplets that I missed.

Let me check sliding windows of this sequence:
pos 1-3: DAD val
pos 2-4: ADD inv
pos 3-5: DDA inv
pos 4-6: DAD val
pos 5-7: ADD inv
pos 6-8: DDA inv
pos 7-9: DAD val
pos 8-10: ADD inv
pos 9-11: DDA inv
pos 10-12: DAD val
pos 11-13: ADD inv
pos 12-14: DDA inv
pos 13-15: DAD val
pos 14-16: ADD inv
pos 15-17: DDA inv
pos 16-18: DAD val
pos 17-19: ADC inv (A-C, A needs A)
pos 18-20: DCD val
pos 19-21: CDD val
pos 20-22: DDD val
pos 21-23: DDD val
... all DDD val

Invalid sliding windows: many in the DAD section + ADC at junction.

So sliding-window count is high.

Compare to DAD x16 (all DAD codon-aligned):
"DADDADDAD..." (DAD x16 = 48 chars)
pos 1-3: DAD val
pos 2-4: ADD inv
pos 3-5: DDA inv
... same pattern throughout.

That gave 9! So DAD x16 has many invalid sliding windows but score 9.

vs "DAD x6 + CDD + DDD x9" has many invalid sliding windows + score 0.

DAD x16 has ~30 invalid sliding windows. Score 9.
DAD x6 + ... has fewer invalid sliding windows (only in DAD region + 1 at junction). Score 0.

So sliding window count alone clearly doesn't determine.

Maybe specific letters / patterns matter. The junction between DAD section and DDD section creates "...DADCDD..." with substring "ADC" or "DCD" or specific.

Actually: position 19 = C in the middle of D's. Maybe a SINGLE C in mostly-D sequence is highly punished?

Let me test: 47 D + 1 C in middle.

## 2026-06-28 16:11 — query 372

Score 0!! Single C in middle of D's → 0.

Let me audit: "DDDDDDDDDDDDDDDDDDDCDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
19 D + C + 28 D = 48
Pos 20 = C.

Codons:
1-6 (1-18): DDD val (6 codons)
7 (19-21): DCD val (D-D, pos2=C) ← valid!
8-16: DDD val

All valid. Yet score 0!

So my codon validity rule is WRONG!

Maybe single C in mostly-D is catastrophically bad due to some other rule.

Let me test C earlier:

## 2026-06-28 16:11 — query 375

Hmm:
- C at pos 2 (DCD codon): 9
- C at pos 3 (DDC inv codon): 8
- C at pos 4 (CDD val codon): 9
- C at pos 20 (DCD val codon): 0!

So C at pos 2 (codon 1 = DCD val) gives 9.
C at pos 20 (codon 7 = DCD val) gives 0.

Both make codon DCD val. But scores differ wildly!

What's special about pos 20 vs pos 2?

Pos 20 = codon 7 position 2. Pos 2 = codon 1 position 2.

Hmm, codon position-2 differs?

Let me test C at pos 5, 8, 11, 14, 17 (codon position 2 for various codons).

## 2026-06-28 16:12 — query 381

Score 9!! Different from earlier. Maybe I sent a different sequence then.

Let me compare:
- "DDDDDDDDDDDDDDDDDDDCDDDDDDDDDDDDDDDDDDDDDDDDDDDDD" (my prior test, claimed 0): let me count.
That was "47 D + 1 C in middle." But the sequence is 19+1+28 = 48. Pos 20 = C.

Just sent: same length and pos 20 = C. Got 9.

Either I had a sequence error before, or non-determinism (didn't observe before).

Let me re-count my earlier "Score 0" sequence:
"DDDDDDDDDDDDDDDDDDDCDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"

count D's before C: D D D D D D D D D D D D D D D D D D D = 19 D's, then C, then 28 D's. Total 48.

vs my new test "DDDDDDDDDDDDDDDDDDDCDDDDDDDDDDDDDDDDDDDDDDDDDDDD" — let me count.

Old: "DDDDDDDDDDDDDDDDDDDCDDDDDDDDDDDDDDDDDDDDDDDDDDDDD" — count chars: 
D x 19, C, D x 29 = 49. NOT 48! ⚠️

So the earlier "Score 0" had 49 characters which probably defaulted to an error.

New test: 48 chars. Score 9 (correct).

Same with "DADDADDADDADDADDADCDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD" — let me count that:
"DADDADDADDADDADDAD" = 18 chars (DAD x6)
"CDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD" = let me count: C + 30 D = 31 chars.
Total 18 + 31 = 49. NOT 48! ⚠️

Same error. Both "anomalies" were 49-char sequences, not 48.

So when sequence is wrong length, score is 0. Good — confirms length=48 strict.

My theory is preserved. Phew.

Let me also test 49-char sequence explicitly.

## 2026-06-28 16:12 — query 382

49 chars → 0. So wrong-length sequences silently scored 0. Important note!

My codon validity theory is preserved. Now let me re-examine some earlier "weird" results — they may have been character-count errors.

Actually my model is correct. Good. Let me ensure my final entry is right.

Use remaining experiments to verify diverse things, including some predictions.

## 2026-06-28 16:12 — query 383

27 chars → 0. Confirmed: wrong length → 0.

Let me think about whether earlier "unexpected" results might have been miscounts. The 7-mid-isolated-AAC giving 3 was reproduced; the AB alt giving 0 was reproduced. So those are real.

Final theory stands. Let me do a focused final round of experiments to test my best understanding.

Best max-score predictions to verify:

## 2026-06-28 16:12 — query 384

Audit "BCDBCABDDCABACADCBDCDABDCAACBBABDDCDCADBAABCDDAA":
Pos 1=B, 2=C, 3=D, 4=B, 5=C, 6=A, 7=B, 8=D, 9=D, 10=C, 11=A, 12=B, 13=A, 14=C, 15=A, 16=D, 17=C, 18=B, 19=D, 20=C, 21=D, 22=A, 23=B, 24=D, 25=C, 26=A, 27=A, 28=C, 29=B, 30=B, 31=A, 32=B, 33=D, 34=D, 35=C, 36=D, 37=C, 38=A, 39=D, 40=B, 41=A, 42=A, 43=B, 44=C, 45=D, 46=D, 47=A, 48=A

Codons:
1 BCD val
2 BCA val
3 BDD val
4 CAB inv (pos3=B)
5 ACA val (A-A)
6 DCB inv (D-B)
7 DCD val
8 ABD inv (A-D)
9 CAA val
10 CBB inv? wait pos 28=C, 29=B, 30=B → CBB. pos1=C pos3=B → invalid.
11 ABD inv? pos 31=A, 32=B, 33=D → ABD inv (A-D).
12 DCD val
13 CAD val
14 BAA val
15 BCD val
16 DAA inv (D-A)

Invalids at codons: 4, 6, 8, 10, 11, 16.
Runs:
- 4 isolated mid
- 6 isolated mid
- 8 isolated mid
- 10-11 mid run length 2
- 16 end edge run length 1

By model: end_pen(1) = 1, max mid run pen = mid_pen(2) = 1, plus isolated mids 3 of them.

If only max-mid + edge: 1 + 1 = 2 → score 7. Actual 6.

Extra penalty 1 from isolated mids (3 of them).

OK my model isn't precise enough.

Let me commit final and call it done with my best understanding.

## 2026-06-28 16:12 — query 385

ABC repeated = 0 (consistent with earlier).

Let me explore strange edge case: what about ALL char = X for various X. Already established A,C,D → 9, B → 0. Let me also try mixed.

## 2026-06-28 16:12 — query 387

8 isolated invalid mid (alternating with valid) ending at codon 16 invalid → 0.

Hmm same as AB alt case.

Maybe rule: when codon 16 is invalid AND there are many other invalids, score collapses?

Let me test: AAC at codon 16 + 7 isolated mid AABs (rest valid).

## 2026-06-28 16:12 — query 388

7 mid AAB + end AAC → 0. Massive penalty.

vs 7 mid AAB alone → 7 (pen 2). Adding end_pen 1 should give pen 3 → score 6.

But actual = 0! So pen jumped from 2 (no end) to 9+ (with end).

So having codon 16 invalid + many mid invalids is catastrophic.

Maybe the rule is: when codon 16 invalid, ALL mid invalids count as part of an "end-extending run" that uses sliding-codon logic.

Or simply: if codon 16 is invalid AND total invalid count is high, score crashes.

Let me test: 5 mid AAB + end AAC. Total 6 invalids.

## 2026-06-28 16:13 — query 389

Let me audit "AAABABAAABABAAABABAAABABAAABABAAAAAAAAAAAAAAAAAC":
AAA BAB AAA BAB AAA BAB AAA BAB AAA BAB AAA AAA AAA AAA AAA AAC
= 16 codons.

Wait, that has BAB not AAB. Let me check.

Hmm. Position 4=B, 5=A, 6=B → BAB. Codon 2 = BAB inv. 5 BABs at codons 2,4,6,8,10. AAC at codon 16.

So 5 mid BAB invalid + 1 end AAC invalid.

By my earlier data: 5 mid BAB alone → pen 6 (score 3). Add end → would predict 4? Actual 4.

Hmm so maybe pen = mid_pen_aggregate + end_pen, additive here?

But for 7 BAB + end: pen would be 6 + 1 = 7 → score 2. Actual 0!

So additive not quite. Let me see for 7 AAB + end AAC: actual 0.
By my earlier: 7 AAB mids alone → pen 2 (score 7). Add end: 2+1 = 3 → predict 6. Actual 0.

Big discrepancy! With more mids, end-invalid interaction blows up.

7 mid AAB: pen 2.
7 mid AAB + 1 end AAC: pen 9 (score 0). +7.

So 1 end invalid added 7 to penalty when combined with 7 mids.

For 5 mid BAB: pen 6. + 1 end: pen 5 (score 4). Penalty went DOWN from 6 to 5?

Wait let me re-check.

Actually 5 mid BAB → my data said score 7 (pen 2). Re-checking:
"AAABABAAABABAAABABAAABABAAABABAAAAAAAAAAAAAAAAAA" had BAB at codons 2,4,6,8,10 (5 mid). Score 7.

But the sequence I just sent "AAABABAAABABAAABABAAABABAAABABAAAAAAAAAAAAAAAAAC" has BAB at same 5 codons + AAC at codon 16. Score 4.

So 5 mid BAB + 1 end AAC: pen 5.
5 mid BAB alone: pen 2.
Difference: end adds 3.

7 mid AAB + 1 end AAC: pen 9.
7 mid AAB alone: pen 2.
Difference: end adds 7.

So end invalid's contribution grows with mid count.

Hmm.

OK let me commit and stop. I have the main insights.

## 2026-06-28 16:13 — query 389

## TRUE FINAL THEORY (after 389 experiments)

### Codon Validity Rule (VERY HIGH CONFIDENCE)

A sequence is read as 16 codons (3-aligned). Codon (X,Y,Z) is VALID iff:
- X=A AND Z=A, OR  
- X∈{B,C} AND Z≠B, OR
- X=D AND Z=D

(Y is irrelevant for validity. 32 of 64 codons valid.)

### Score (cap 9)

Score = max(0, 9 - penalty). 

Penalty is complex, depending on:
- Number of invalid codons
- Their positions (edge effects from codons 1 & 16)
- Run lengths (longer = more pen)
- Density / gaps
- Especially: invalid codon at END combined with many mid invalids causes catastrophic penalty

### Approximate component formulas

- Single edge run length L: edge_pen(L) = mid_pen(L) + 1
- Single mid run length L: mid_pen(L) ≈ floor(2L/3), exact table:
  L:  1 2 3 4 5 6 7 8 9 10 11 12 13 14 ...
  mp: 0 1 2 2 3 4 4 5 6 6  7  7  8  8  → eventually capped at 8

- Multiple runs aggregate non-trivially (between max and sum).
- Edge invalid + many mid invalids causes super-linear penalty.

### Asymmetries

- A and D are "strict" letters (only self-pair).
- B and C are "flexible" letters (any pos3 except B).
- Pos3=B is universally invalid (no codon with Z=B is valid).

### Strategy for max score

Use sequences where every codon (positions 1-3, 4-6, ..., 46-48) is valid by the rule. Easiest patterns:
- All A's, all C's, or all D's
- CAC, CAD, CDD, DAD, DCD, DDD, BAA, BCD, BAD repeated
- Any combo of valid codons

### Note on length

Sequence must be exactly 48 characters. Wrong length → score 0.

## 2026-06-28 16:13 — query 392

Many valid sequence patterns confirmed at 9.

Let me explore one more angle: the "1 isolated mid invalid → 0 pen" rule, but with various invalid types.

## 2026-06-28 16:13 — query 394

Single mid invalid → 9 across various codon types.

Let me explore: what if codon 1 is REALLY weird? Like all-B at codon 1.

## 2026-06-28 16:13 — query 396

Both → 8. Confirms edge single invalid = -1.

Let me also confirm: codon 1 invalid AND codon 16 invalid (both edges, all else valid).

## 2026-06-28 16:13 — query 397

7 ✓ (1+1=2 pen).

Let me test: 2 mids in middle (separated) + 2 edge invalids.

## 2026-06-28 16:13 — query 398

Let me audit "BBBCCCCCCCCCBBBCCCCCCCCCBBBCCCCCCCCCCCCCCCCCCBBB":
BBB(1-3) + 9C(4-12) + BBB(13-15) + 9C(16-24) + BBB(25-27) + 18C(28-45) + BBB(46-48)
Length: 3+9+3+9+3+18+3 = 48 ✓

Codons:
1: BBB inv
2 (4-6): CCC val
3 (7-9): CCC val
4 (10-12): CCC val
5 (13-15): BBB inv
6 (16-18): CCC val
7 (19-21): CCC val
8 (22-24): CCC val
9 (25-27): BBB inv
10-15 (28-45): CCC val (6 codons)
16: BBB inv

Invalids at codons 1, 5, 9, 16. 4 isolated invalids.
- Codon 1 = start edge (run 1)
- Codon 5 = mid isolated
- Codon 9 = mid isolated
- Codon 16 = end edge (run 1)

By model: start_pen 1 + end_pen 1 + max_mid 0 = 2 → score 7 ✓

Matches! Even with 2 isolated mid invalids, no extra pen.

So 2 isolated mid invalids by themselves → 0 pen. But "AAB at codons 2 and 4" (2 isolated mid AAB) gave pen 1.

Difference: in this test, isolated mids at codons 5 and 9 (separated by 3 valid codons). In AAB test, codons 2 and 4 (separated by 1 valid codon).

So distance between mid invalids matters! Close = penalty, far = no penalty.

This confirms my "gap matters" finding.

## 2026-06-28 16:13 — query 399

2 mid BBB invalids gap 1 with CCC separator → 8 (pen 1).

Same as AAB version. So pen 1 for gap=1 with 2 mids, regardless of separator type.

OK I've confirmed my main findings. Let me use remaining ~100 experiments to do final exploration.

Actually let me just verify the codon validity rule one more time with surprising codons.

## 2026-06-28 16:14 — query 402

All consistent.

Let me now consolidate and finalize. I'm confident in my codon validity rule. The scoring formula details remain partially mysterious but I've documented what I know.

Use remaining for diverse verifications.

## 2026-06-28 16:14 — query 405

All consistent. Let me also test pen formulas more rigorously.

mid_pen(L) for various single mid runs of L (with end and start codons valid):

## 2026-06-28 16:14 — query 407

Pattern V,I,V,I repeating with codon 16 = DAC inv (end edge).

8 invalid codons alternating with 8 valid. Similar to AB alt — score 0.

Confirming: many alternating invalids + invalid end → 0.

Let me check Pattern V,I,V,I but ending with V.

## 2026-06-28 16:14 — query 408

Start invalid + 7 mid invalids alternating = 0.

So both "start invalid + many alternating mids" and "end invalid + many alternating mids" give 0.

Pattern: when edge invalid + ~7 mid invalids → catastrophic.

Now let me figure out: with edge invalid + N mid invalids, what's the penalty progression?

Already have:
- start invalid + 6 mid invalids gap 1 = 2 (pen 7) — CABAAACABAAA...AAAAAA (CAB at codons 1,3,5,7,9,11,13)
- start invalid + 7 mid alternating = 0

Let me test 1, 2, 3 mids with edge.

## 2026-06-28 16:15 — query 413

Start invalid + N isolated mid invalids (gap 1):
N=0: 8 (pen 1)
N=1: 8 (pen 1)
N=2: 7 (pen 2)
N=3: 7 (pen 2)
N=4: 6 (pen 3)
N=5: 4 (pen 5)
N=6: 2 (pen 7)
N=7: 0 (pen 9+)

Mid only (no start):
N=1: 9 (pen 0)
N=2: 8 (pen 1)
N=3: 8 (pen 1)
N=4: 8 (pen 1)
N=5: 7 (pen 2)
N=6: 5 (pen 4)
N=7: 3 (pen 6)

Difference (with start - without start):
N=0: 1
N=1: 1
N=2: 1
N=3: 1
N=4: 2
N=5: 3
N=6: 3
N=7: ≥3

So start_pen 'effective contribution' grows from 1 to 3+ as mids increase.

Hmm. Maybe when start_pen = 1 and mids exist, total is like merged "near-start cluster".

I think the model is: edge invalid extends through codons treating valid codons between as "still in cluster" if total cluster is short.

OK final final commit.

## 2026-06-28 16:15 — query 413

## ULTIMATE FINAL THEORY

### Codon Validity (HIGH CONFIDENCE)
Sequence read as 16 codons (3-aligned from position 1).
Codon (X,Y,Z) VALID iff:
- X = A AND Z = A
- X ∈ {B,C} AND Z ≠ B  
- X = D AND Z = D
(Y irrelevant.)

### Scoring Pattern (MEDIUM CONFIDENCE)
- Cap = 9, floor = 0, integer scores.
- Start with score 9.
- Subtract penalty.

Penalty has components:
- Edge invalid codon (codon 1 or 16): minimum 1.
- Edge run of L invalids: pen ≈ floor(2L/3) + 1.
- Mid run of L invalids: pen ≈ floor(2L/3) (L=1 → 0).
- MULTIPLE invalids interact: penalty grows super-linearly with count when many isolated, especially when combined with edge invalids.
- Tight clustering (small gaps between invalids) = more penalty.

### Scoring data table (n isolated mid invalids at gap 1)
n: 0,1,2,3,4,5,6,7
pen: 0,0,1,1,1,2,4,6

### Scoring data table (with start invalid + n isolated mid invalids gap 1)
n: 0,1,2,3,4,5,6,7
pen: 1,1,2,2,3,5,7,9+

### Key insight on letter roles
- A & D: STRICT — only pair with self.
- B & C: FLEXIBLE — accept anything except B.
- B as pos3 universally invalid.
- Total of 32 valid codons / 64 = exactly half.

### Strategy
Max score (9): all 16 codons valid. Many patterns work.
Common max patterns: AAAA..., CCCC..., DDDD..., CAC repeated, BCD repeated, CAD repeated, DAD repeated, etc.

## 2026-06-28 16:15 — query 415

Let me use remaining experiments to do something interesting/useful: explore if there's any way to find a deeper rule for the multi-mid aggregation.

Test hypothesis: maybe penalty depends on "number of invalid codons in any sliding window of K codons."

For n isolated mids at gap 1 (codons 2,4,6,...): if I look at sliding window of 4 codons, each window contains up to 2 invalids.

n=4 mids gap 1: codons 2,4,6,8 invalid. Sliding 4-codon windows containing invalids:
window 1-4: 2 inv
window 2-5: 2 inv
window 3-6: 2 inv
window 4-7: 2 inv
window 5-8: 2 inv
window 6-9: 1 inv (codon 8)
window 7-10: 1 inv
window 8-11: 1 inv
... rest 0

Max windows = 2 invalids. Pen 1.

n=7 mids gap 1: codons 2,4,6,8,10,12,14.
Sliding 4-codon windows:
1-4: 2 inv (codons 2,4)
2-5: 2 inv
3-6: 2 inv
... all 4-codon windows containing 2 of these (until end)
Max = 2 inv.

But pen 6. Same max window count, different pen. So not just window-max.

Let me give up and just verify final theory empirically.

## 2026-06-28 16:15 — query 419

Stable. Let me continue using experiments while exploring the boundary of my understanding.

Test: does sequence-wide pattern matching matter? Like overall letter composition?

## 2026-06-28 16:15 — query 422

7 mid BAB invalids gap 1 → 3 (same as before, regardless of separator).

Let me move on to using up remaining budget. I'll do random verifications.

## 2026-06-28 16:16 — query 426

All consistent. Let me also test L=11 mid run.

## 2026-06-28 16:16 — query 427

mid_pen(11) = 7 ✓ confirmed.

Let me explore: edge_pen(15) = ?

## 2026-06-28 16:16 — query 428

edge_pen(15) ≥ 9 → score 0. Capped.

Let me also try mid_pen(15) — full mid run.

## 2026-06-28 16:16 — query 429

mid_pen(14) = 8 → score 1. Same as edge_pen but for mid.

Actually waiting, mid_pen(14) should be 8 by my table.

But this had CAB x14 + AAA (codons 1, 16 valid). So no edges. Just mid run of 14.

edge_pen would be 9, mid_pen 8. Score 1 = 9 - 8 ✓

So formula works.

Let me also test extreme: mid run of 16 (impossible since edges defining mid). Edge run of 16 → already 0.

Now I've thoroughly verified my model. Let me use remaining experiments to explore creative things.

## 2026-06-28 16:16 — query 432

All valid → 9. Good.

Let me probe some edge cases:

## 2026-06-28 16:16 — query 433

Audit "CACCABCAACABCCDCDDCAACAACADCCDCABDCBCDCDCABCABCC":
Pos 1-3: C,A,C → CAC val
Pos 4-6: C,A,B → CAB inv
Pos 7-9: C,A,A → CAA val
Pos 10-12: C,A,B → CAB inv
Pos 13-15: C,C,D → CCD val
Pos 16-18: C,D,D → CDD val
Pos 19-21: C,A,A → CAA val
Pos 22-24: C,A,A → CAA val
Pos 25-27: C,A,D → CAD val
Pos 28-30: C,C,D → CCD val
Pos 31-33: C,A,B → CAB inv
Pos 34-36: D,C,B → DCB inv
Pos 37-39: C,D,C → CDC val
Pos 40-42: D,C,A → DCA inv
Pos 43-45: B,C,A → BCA val
Pos 46-48: B,C,C → BCC val

Invalids: codons 2, 4, 11, 12, 14. 
Runs:
- 2 (isolated mid)
- 4 (isolated mid)
- 11-12 (mid run length 2)
- 14 (isolated mid)

By model: max mid pen = mid_pen(2) = 1. Score = 9 - 1 - extra = ?

If 3 isolated mids contribute +1 (based on count): 1+1=2 → score 7.
If isolated mids contribute 0 with one cluster: 1 → score 8.

Actual 8. So my model holds here.

OK let me use last ~65 experiments to test more.

## 2026-06-28 16:16 — query 435

Audit "DBABCADBABCADBABCADBABCADBABCADBABCADBABCADBABCA":
"DBABCA" repeated 8 times = 48 chars.
Codons (every 3):
1 DBA inv (D-A, pos2=B not in {A,D})
2 BCA val (B-A)
3 DBA inv
4 BCA val
... 16 BCA val.

8 isolated mid invalids (DBA at codons 1,3,5,7,9,11,13,15). Plus codon 1 is start_edge.
Codon 16 = BCA val.

By model: start_pen 1 + many mid → at gap 1 with 8 total: would be heavy. Pen 9+ → 0.

Score 0. Consistent with my "start + many mids = collapse" finding.

Let me confirm by reducing.

## 2026-06-28 16:16 — query 436

Audit "DBABCADBABCADBABCADBABCABCABCABCABCABCABCABCABCA":
"DBABCA" x4 + "BCA" x8 = 24+24=48 ✓
Codons:
1 DBA inv
2 BCA val
3 DBA inv (in second DBABCA)
4 BCA val
5 DBA inv
6 BCA val
7 DBA inv
8 BCA val
9-16: BCA val

Invalids at codons 1, 3, 5, 7. 4 invalids: codon 1 = start edge, codons 3, 5, 7 = 3 mid isolated.

Score 7 (pen 2). 

By my model: start_pen 1 + mid contribution. 3 isolated mids → pen 1 (from my table). Total 2 → score 7 ✓

Good, model holds for start_edge + few mids.

Final summary: my model is good for small invalid counts but breaks down for many.

Remaining 64 experiments. Let me finish strong with various verifications.

## 2026-06-28 16:17 — query 439

All consistent with my model.

Let me also probe some specific codon validity tests.

## 2026-06-28 16:17 — query 443

All consistent with codon validity rule:
- DBC, DAC at codon 1: invalid (D-C). → 8.
- DCD, DAD at codon 1: valid (D-D). → 9.

Rule holds.

Let me explore edge case I haven't: D at pos 1, pos2 = various, pos3 = D. All should be valid:
DAD, DBD, DCD, DDD all val.

What about pos1=D, pos3=D mid (not codon 1)? Should still be valid.

## 2026-06-28 16:17 — query 445

All consistent. My codon validity is solid.

Let me explore: anomalies with B in pos 2.

## 2026-06-28 16:17 — query 448

All invalid → 0. ✓

Let me probe one more thing: are pen formulas affected when starts and ends interact through long mid runs?

## 2026-06-28 16:17 — query 451

Got 6 (pen 3). Predicted 5 (pen 4). Off by 1.

Maybe start and end edge runs interact (subtractively)?

Or maybe my edge_pen(2) isn't quite 2.

Re-checking: CAB x2 at start alone gave 7 (pen 2). So start edge run 2 = pen 2 confirmed.
CAB x2 at end (if I tested): would be pen 2 → score 7.

With both edges: 2+2=4 pen → score 5. Actual 6. Off by 1.

So perhaps when both edges have invalids, total is slightly less. Or there's another small effect.

Or maybe my model of edge_pen needs refinement for combined edge cases.

Let me test start L=3 + end L=3.

## 2026-06-28 16:18 — query 454

Score 4. Let me audit: "CABCABCABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACABCABC"
9+30+? Actually count: C-A-B-C-A-B-C-A-B + A x N + C-A-B-C-A-B-C = 9 + N + 7 = 48 → N = 32.
So CAB x3 + AAA-stuff-32 + CABCABC (=7) wait that's CAB CAB C, not 9.

Let me carefully count "CABCABCABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACABCABC":
CABCABCAB = 9
Then "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" — count A: 32 A's
Then "CABCABC" = 7
Total 9+32+7 = 48 ✓

Codons:
1: CAB inv
2: CAB inv
3: CAB inv
4 (10-12): AAA val
5-14: AAA val (codons 5-14 are pos 13-42 = AAA)
Pos 41-48: A(41) C(42) A(43) B(44) C(45) A(46) B(47) C(48)
Codon 14 (40-42): AAC inv (pos 40=A, 41=A, 42=C)
Wait that's not what I expected.

Let me re-check positions:
After CAB x3 (pos 1-9), then 32 A's (pos 10-41), then "CABCABC" (pos 42-48).
Pos 42 = C, 43 = A, 44 = B, 45 = C, 46 = A, 47 = B, 48 = C.

Codon 14 (40-42): pos 40=A, 41=A, 42=C → AAC inv
Codon 15 (43-45): pos 43=A, 44=B, 45=C → ABC inv (A-C)
Codon 16 (46-48): pos 46=A, 47=B, 48=C → ABC inv

So invalids: codons 1-3 (start run 3), codons 14-16 (end run 3).

By model: start_pen(3) + end_pen(3) = 3 + 3 = 6 → score 3.
Actual 4 (pen 5).

So start+end both length 3 gives pen 5 not 6. Off by 1.

Hmm. Maybe edge interaction reduces by 1.

Or maybe individual edge_pen is slightly different.

Let me commit and stop fine-tuning.

## 2026-06-28 16:18 — query 455

Let me use last 45 experiments to test some more interesting predictions and verify my codon validity rule on edge cases I haven't.

Test all 16 possible (pos1, pos3) combinations at codon 1 with pos2=A to ensure I have the rule right.

pos1=A:
- AAA: 9 ✓ (val)
- AAB: 8 ✓ (inv)
- AAC: 8 ✓ (inv)
- AAD: 8 ✓ (inv)

pos1=B:
- BAA: 9 ✓
- BAB: 8 ✓ (inv, pos3=B)
- BAC: 9 ✓
- BAD: 9 ✓

pos1=C:
- CAA: 9 ✓
- CAB: 8 ✓ (inv)
- CAC: 9 ✓
- CAD: 9 ✓

pos1=D:
- DAA: 8 ✓ (inv, D needs D)
- DAB: 8 ✓ (inv)
- DAC: 8 ✓ (inv)
- DAD: 9 ✓ (val)

All 16 codon 1 tests with pos2=A have been verified. My rule is correct.

Now let me also verify pos2=D for the D-start case:
- DDA: 8 (inv)
- DDB: 8 (inv)
- DDC: 8 (inv)
- DDD: 9 (val)

I think I tested most of these already. Let me check.

## 2026-06-28 16:18 — query 457

All consistent. My rule (X=D, Z must be D) is verified.

Let me also check: what if pos2 = various for D-D and A-A?

## 2026-06-28 16:18 — query 459

DCD and ABA both 9. Pos2 doesn't affect validity. Confirmed.

I have solid understanding. Let me use remaining experiments for diverse interest, maybe trying to break my model in interesting ways.

## 2026-06-28 16:18 — query 462

All consistent.

Let me try a few more sequences to verify multi-mid scoring rule for n=3 with various spacings.

## 2026-06-28 16:18 — query 463

Got 9! Let me audit "AAAAACAAACAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA":
5A C 3A C 3A C A...A
Positions of C: 6, 10, 14.

Codons:
1: AAA val
2 (4-6): AAC inv (pos6=C)
3 (7-9): AAA val (pos7,8,9=A)
4 (10-12): CAA val (pos10=C)
5 (13-15): ACA val (pos13=A, 14=C, 15=A)
6-16: AAA val

Only 1 invalid (codon 2). Score 9 (isolated mid). ✓

I miscounted again. Let me try to construct 3 consecutive AAC mids.

For codons 2, 3, 4 = AAC each:
codon 2 (4-6) AAC: pos 6=C
codon 3 (7-9) AAC: pos 9=C
codon 4 (10-12) AAC: pos 12=C

C at positions 6, 9, 12.

Sequence: A(1-5) C(6) A(7-8) C(9) A(10-11) C(12) A(13-48)
"AAAAACAACAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" = 5+1+2+1+2+1+36 = 48 ✓

## 2026-06-28 16:19 — query 464

3 consecutive mid AAC → 7 (pen 2). matches mid_pen(3) = 2. ✓

OK model holds. Let me use last experiments.

## 2026-06-28 16:19 — query 468

All consistent. My theory is robust.

Last final entries.

## 2026-06-28 16:19 — query 468

## Theory complete!

After 468 experiments, I have determined:

### CODON VALIDITY (PRIMARY RULE)
- Sequence of 48 chars divided into 16 codons (3-aligned).
- Each codon (X,Y,Z) is VALID iff:
  * X=A and Z=A, OR
  * X in {B,C} and Z != B, OR
  * X=D and Z=D
- Middle letter Y doesn't affect validity.
- 32 of 64 codons are valid.

### LETTER ROLES
- A & D: "strict" — only self-pair
- B & C: "flexible" — accept any non-B in pos3
- B as pos3: always invalid
- B as pos2 or alone: fine

### SCORING (CAP 9)
- Penalty starts at 0; score = max(0, 9 - penalty)
- Each invalid codon contributes to penalty based on:
  1. Position (edge codons 1 & 16 = +1 minimum)
  2. Run length (longer runs = more penalty)
  3. Multiplicity (more runs = more, but not simply additive)
  4. Interactions (edge + many mid = catastrophic)

### Key empirical tables
For single mid run length L: mid_pen ≈ floor(2L/3): 0,1,2,2,3,4,4,5,6,6,7,7,8,8
For edge run length L: edge_pen = mid_pen + 1
For multiple mid runs: tends toward max(mid_pens) but increases with count
For edge invalid + many mids: super-linear penalty growth

### Strategy
Max (9): use all valid codons. Easy patterns work.
Min (0): use all invalid or many invalid + edge.

### Length requirement
Sequence MUST be exactly 48 characters. Otherwise score = 0.

## 2026-06-28 16:19 — query 474

All max-score sequences score 9. Cap confirmed.

Let me also explore: BCB val? Tested. CBC val? Tested. Other unusual codons.

## 2026-06-28 16:20 — query 477

All D-start codons with non-D pos3 are invalid. Confirmed.

Let me try a few more diversity tests with last 23 exps.

## 2026-06-28 16:20 — query 479

Audit "BCDBADCABBCDBADCABBCDBADCABBCDBADCABBCDBADCABCAD":
Codons (every 3):
1 BCD val
2 BAD val
3 CAB inv (pos3=B)
4 BCD val
5 BAD val
6 CAB inv
7 BCD val
8 BAD val
9 CAB inv
10 BCD val
11 BAD val
12 CAB inv
13 BCD val
14 BAD val
15 CAB inv
16 CAD val

5 mid invalids at codons 3, 6, 9, 12, 15 — all isolated mids with gap 2.

By my model: 5 mids at gap 2 → pen 2 (score 7) ✓

Matches perfectly!

Let me now use final ~20 experiments to test edge case mid run lengths I haven't and verify final formula.

## 2026-06-28 16:20 — query 482

All matching mid_pen formula. ✓

Final theory confirmed. Last few experiments:

## 2026-06-28 16:21 — query 496

Audit "CDDDCDDDCDDDCDDDCDDDCDDDCDDDCDDDCDDDCDDDCDDDCDDD":
Codons:
1 (1-3): CDD val
2 (4-6): DCD val (pos 4=D, 5=C, 6=D? Wait CDDD has C at pos 1, D at 2,3,4 — let me recompute.

Position i, char = "CDDD"[(i-1)%4]
i=1: C
i=2: D
i=3: D
i=4: D
i=5: C
i=6: D
i=7: D
i=8: D
i=9: C
...

Codons:
1 (1-3): CDD val
2 (4-6): DCD val (pos 4=D, 5=C, 6=D)
3 (7-9): DDC inv (pos 7=D, 8=D, 9=C) — wait pos 9 (i=9, (9-1)%4=0) = C. So pos 9=C. Codon 3 = D,D,C = DDC inv.
4 (10-12): DDD val (pos 10=D, 11=D, 12=D)
5 (13-15): CDD val (pos 13=C, 14=D, 15=D)
6 (16-18): DCD val
7 (19-21): DDC inv
8 (22-24): DDD val
9 (25-27): CDD val
10 (28-30): DCD val
11 (31-33): DDC inv
12 (34-36): DDD val
13 (37-39): CDD val
14 (40-42): DCD val
15 (43-45): DDC inv
16 (46-48): DDD val

Invalids: codons 3, 7, 11, 15. 4 isolated mid invalids at gap 3.

By my model (gap 3 with 4 invalids): pen 2 → score 7 ✓

CONFIRMED.

I have 4 experiments left. Let me do final verifications.

## 2026-06-28 16:21 — FINAL

## FINAL REPORT — Biology of this New World (500 experiments used)

### THE ORGANISM'S BIOLOGY

**Sequence frame**: Sequences are exactly 48 characters from {A, B, C, D}. They are read as **16 codons**, frame-aligned starting at position 1 (codons span positions 1–3, 4–6, …, 46–48). Wrong-length sequences score 0.

**Codon validity rule** (HIGH CONFIDENCE — verified by ~60+ targeted codon tests covering all 16 (pos1, pos3) pairs and many pos2 variations):

A codon (X, Y, Z) is VALID iff one of:
- X = A  AND  Z = A
- X ∈ {B, C}  AND  Z ≠ B
- X = D  AND  Z = D

The middle position Y never affects codon validity.

Equivalently: **A binds A, D binds D** (strict bases). **B and C are flexible** — they accept any pos3 except B. **Position 3 = B is universally invalid** in this world (no codon ending in B is ever valid). Exactly 32 of the 64 possible codons are valid (4 A-start, 12 B-start, 12 C-start, 4 D-start) — a beautifully symmetric pattern with A & D as "strict letters" and B & C as "flexible letters."

**Scoring**: Score = max(0, 9 − penalty). Cap = 9, floor = 0, always integer.

Penalty is determined by the arrangement of invalid codons:

1. **Single edge-touching run** (run of L consecutive invalid codons including codon 1 or 16):
   edge_pen(L) ≈ floor(2L/3) + 1
   Table: L=1→1, 2→2, 3→3, 4→3, 5→4, 6→5, 7→5, 8→6, 9→7, 10→7, 11→8, 12→8, ≥13→9 (capped).

2. **Single mid run** (length L, not touching either edge):
   mid_pen(L) = edge_pen(L) − 1
   Table: 0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8, 8 …

3. **Multiple runs aggregate non-trivially** — generally close to max(mid_pens) + edge_pen for sparse arrangements, but grows super-linearly when:
   - Many isolated mid invalids are densely packed (small gaps).
   - Edge invalid combined with many mid invalids (catastrophic — score collapses to 0).
   Empirically, n isolated mid invalids at gap-1 → pen 0, 0, 1, 1, 1, 2, 4, 6 for n=1..7.

### BEST SEQUENCE FOUND
Score 9 (the cap) is achieved by any sequence whose 16 frame-aligned codons are all valid. Example chosen:

**`CADCADCADCADCADCADCADCADCADCADCADCADCADCADCADCAD`**  →  fitness **9**

Many other "all-valid-codons" sequences also reach 9: all-A, all-C, all-D, CAC repeated, BCD repeated, DAD repeated, DCD repeated, ADAD…, BACBAC…, CDDCDD…, etc. I could find no way to exceed 9.

### WHAT I WOULD TEST NEXT (with more budget)

1. **Pin down the exact multi-run / density formula.** Systematically vary (number of isolated mid invalids, gap between them, identity of invalid codon) to derive a clean closed-form penalty function. My best guess is that the system "weights" each invalid codon by some local-density kernel.

2. **Edge × mid interaction.** Why does codon-1-invalid + 7 alternating mid invalids → score 0, while either alone gives a small penalty? Likely the system extends an "effective edge run" through valid spacers when many invalids are near the edge. Test by varying spacer length between edge invalid and first mid invalid.

3. **Search for sub-codon / sliding-window effects.** Some apparent "anomalies" (CCDD vs AAC giving different penalties for the same codon-run structure) hint that overlapping triplets may contribute. A clean test would compare codon-aligned vs frame-shifted versions of the same invalid pattern.

4. **Verify the model in extreme regimes.** Try carefully designed sequences predicted to give each integer score 0–9, to confirm my formulas across the whole range.

5. **Probe asymmetry of A vs D more deeply.** They look symmetric (both "strict"), but earlier tests hinted at subtle differences (DAA's apparent validity in some mid contexts vs DAD as the only valid D-start in codon-1). A deliberate sweep of all D-start codons in all 16 positions would clarify whether there are position-dependent exceptions.

6. **Sequence-length sensitivity.** Confirmed that ≠48 chars → 0. But are there other "hard fails" (e.g., specific killer triplets that drop score to 0 instantly even with everything else valid)? Worth a sweep.

### REFLECTION
The most satisfying finding is the **codon-validity rule** — it has a clean biological flavor reminiscent of base pairing (A↔A, D↔D being strict like complementary pairs; B and C being "wobble" bases). The scoring layer on top of validity remained partially mysterious within the 500-experiment budget, but the qualitative picture (edges matter more than middles; clustering hurts; B in pos3 is always poison) is solid.
