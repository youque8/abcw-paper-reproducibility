# v1.2.0 — Complex Systems submission reproducibility candidate

Release date: 2026-09-11

This candidate extends v1.1.0 without changing the ABCW model, the archived 692-coloring, or the exact minimum result.

## Added
- `experiments/05_anchor_structure_analysis/` with the analyses used by the revised manuscript.
- Independent verification of the winner-row conflict criterion on 10,094 co-observed within-anchor field-pair/action comparisons (0 mismatches).
- Exact maximum-clique witnesses for all 50 difficult anchor graphs; all 50 satisfy `omega = chi` in this finite instance, with distribution 39/8/2/1 for chi=2/3/4/7.
- `paper/complex_systems_v0.5.1/` as the manuscript candidate corresponding to these claims.
- Updated paper-to-artifact and reproducibility documentation.

## Verification
`sh scripts/verify_clean.sh` is the intended release audit. It now includes the v1.2 anchor-structure checks after regenerating the dataset and exact-partition artifacts.

## Scope
The observed `omega = chi` property is an instance-specific exact computational result. Release 1.2.0 does not assert that arbitrary ABCW anchor graphs are perfect or that the numerical value 692 is universal.
