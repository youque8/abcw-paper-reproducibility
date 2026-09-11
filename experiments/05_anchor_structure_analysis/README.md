# Anchor-structure analysis (new; baseline code unchanged)

This directory is additive. No files in experiments/01--04, `src`, or `scripts` are modified.

## Main findings

The anchor action is the unanimous action `(-1,-1,-1,-1,-1)`. All agents lose under this action, so each off-diagonal weight is updated by `w' = max(0,w-1)`. Consequently, coordinates with anchor-future absolute weight zero are non-injective: current weights 0 and 1 collapse to the same future value. In Delta-W coordinates these are exactly negative (`-1`) anchor-future entries.

For two current fields in the same anchor fiber, another action reveals a hidden 0/1 distinction exactly when the corresponding source-agent row belongs to a winning agent. `verify_winner_row_mechanism.py` checks this criterion on every co-observed within-anchor field pair/action combination in the archived dataset: 10,094 comparisons, 0 mismatches.

This explains why negative-dominated anchor futures are enriched among difficult groups. The earlier low-asymmetry association is partly confounded by the number of negative entries: across all 625 anchors, negative-entry count and the simple asymmetry measure are negatively correlated (r about -0.52). Therefore low asymmetry should not yet be treated as a causal explanation.

The unique chi=7 group is the extreme case: future_id 0 has all 20 off-diagonal Delta-W entries equal to -1 (absolute future field zero), is perfectly symmetric, contains 44 reachable current fields, and has 224 internal conflict edges. All 30 non-unanimous actions generate conflicts; the two unanimous actions do not.

## v0.3 — high-clipping easy vs difficult

Run:

```bash
python experiments/05_anchor_structure_analysis/analyze_easy_vs_difficult.py
```

Outputs include `all_anchor_reachability_features.csv`, `high_clipping_easy_vs_difficult.csv`, `high_clipping_summary.csv`, and `easy_vs_difficult_interpretation.md`.

The analysis leaves all pre-existing repository code and archived results unchanged.

## v0.4: chromatic mechanism

`analyze_chromatic_mechanism.py` computes clique numbers and explicit maximum-clique witnesses for all 50 difficult anchor fibers. In the analyzed instance, every difficult fiber satisfies `chi = omega`: 39 K2-forced fibers, 8 K3-forced fibers, 2 K4-forced fibers, and one K7-forced fiber. Pairwise witness actions are exported for each selected maximum clique. This is an instance-level exact result; it is not asserted as a general perfect-graph theorem.
