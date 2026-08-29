# 023 — K562 spaced (min 500bp gap)

K562 selection with greedy by |lfc| but min 500bp gap. Skipped 5890 entries for proximity; effective threshold dropped from |lfc|≥1.69 to ≥1.40.

**Result:** mean_r = 0.0033 (down from 015's 0.0045).
- K562 = 0.0007 (DROPPED hard from 015's 0.0024)
- HepG2 = 0.0026 (down from 0.0044 — strange, didn't expect)
- SKNSH = 0.0066 (matches 015)

**Interpretation:** K562 clustering is NOT noise — clustered top-|lfc| sites carry usable information. Forcing dispersion drops top-|lfc| threshold from 1.69 to 1.40 (i.e., we replace 5890 high-|lfc| clustered sites with weaker dispersed sites), and K562 r tanks. HepG2 also drops, possibly because the K562 "fill quality" interacts with HepG2 prediction in a way I don't understand (or seed/sampling noise).

**Lesson:** Don't enforce spacing on K562. The top-|lfc| ranking — clustering and all — is the best operating point. Probably superenhancers (closely-spaced active elements) genuinely cluster on chr19/chr1.

**Next (024):** Investigate eval-set structure. Multiple evals appear correlated (eval_01==eval_14, eval_02==eval_05==eval_11, etc.) — suggests cell-type-specific evals duplicated. eval_13 consistently outperforms. Test if HepG2 cell-type-specific fine-tuning matters: try H6-strict ultra-tight (|lfc|≥4.5) replicated 2x = 12k slots, K22, S16. Sacrifices SKNSH r (currently strongest) to push HepG2 further.
