# 012 — HepG2-weighted budget (K562=15k, HepG2=25k, SKNSH=10k)

Tested the hypothesis that HepG2 signal was sequence-count-limited in 011. Shifted budget toward HepG2.

**Result:** mean_r = 0.0024 (DOWN from 011's 0.0036).
- K562 avg = 0.0017 (down from 0.0024)
- HepG2 avg = 0.0007 (basically unchanged — 0.0009 in 011)
- SKNSH avg = 0.0050 (down from 0.0075)

**Hypothesis falsified:** HepG2 is NOT count-limited. Tripling HepG2 budget did not move HepG2 avg r. But shrinking K562/SKNSH budgets hurt them proportionally.

eval_13 HepG2 = 0.0123 (best HepG2 yet), suggesting the marginal HepG2 sequences DO contain real signal for one eval — but it averages out across all evals.

**Lesson:** Per-cell signal seems to saturate around 16k for HepG2 (no improvement) and K562 (slight degradation when reduced). SKNSH degrades cleanly with fewer sequences. So 011-style even split was near-optimal for total budget allocation.

**Next (013):** Test the opposite — reduce HepG2 budget to test if its marginal sequences are NEUTRAL (dropping them with no effect) or ACTIVELY HURTING. K562=20k, HepG2=10k, SKNSH=20k.
