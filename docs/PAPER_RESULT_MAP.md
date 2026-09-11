# Paper-to-Artifact Map / 論文結果とアーティファクトの対応

## English / 日本語
- **56,536 transitions; 2,562 fields; 11,202 `(a, field)` states** — `experiments/01_dataset/generate_transitions.py`; regenerated directly from the ABCW rules. / ABCW更新則から直接再生成。
- **Field-only determinism 1,390 / 2,562** and **out-strength 11,084 / 11,142** — printed by the historical minimum-partition pipeline and derivable from the regenerated transitions. / 再生成遷移から導出可能。
- **511 natural feature combinations** — `experiments/02_natural_features/run_511_features.py`; archived reference table `results/true_compression_all_511.csv`. / 511候補の全探索。
- **No 100%-predictive genuinely compressive candidate among the 511 natural-feature combinations** — regression check over `true_compression_all_511.csv`. / 511候補内では真の圧縮と100%予測の両立0件。
- **692-class constructive upper bound and exact lower bound** — `experiments/03_exact_partition/`; certificate in `results/summary_exact.json` and `anchor_group_chromatic.csv`. / 692クラスの上界構成と厳密下界。
- **352 singleton / 340 multi-field classes; maximum size 65** — `summary_exact.json` and partition-structure archived outputs. / 692分割の内部構造。
- **Main paper figures** — `paper/figures/`. / 論文掲載図。

- **Winner-row conflict criterion: 10,094 co-observed within-anchor field-pair/action comparisons, 0 mismatches** — `experiments/05_anchor_structure_analysis/verify_anchor_structure.py`; the count is the sum, over unordered pairs within each anchor fiber, of the number of actions observed for both fields. / winner-row criterion の実装独立チェック。
- **All 50 difficult anchor graphs satisfy `omega = chi`; distribution 39/8/2/1 for chi=2/3/4/7** — `experiments/05_anchor_structure_analysis/verify_anchor_structure.py`; archived witnesses in `results/chromatic_clique_summary.csv`, `maximum_clique_vertices.csv`, and `maximum_clique_pair_witnesses.csv`. This is an instance-specific certificate, not a general perfect-graph claim. / 50非自明anchor群のclique/coloring証明書。
- **Complex Systems submission candidate v0.5.1** — `paper/complex_systems_v0.5.1/`; included for traceability of the claims targeted by release 1.2.0. / v1.2.0が対応する改訂稿候補。
