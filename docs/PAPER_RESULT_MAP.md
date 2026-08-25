# Paper-to-Artifact Map / 論文結果とアーティファクトの対応

## English / 日本語
- **56,536 transitions; 2,562 fields; 11,202 `(a, field)` states** — `experiments/01_dataset/generate_transitions.py`; regenerated directly from the ABCW rules. / ABCW更新則から直接再生成。
- **Field-only determinism 1,390 / 2,562** and **out-strength 11,084 / 11,142** — printed by the historical minimum-partition pipeline and derivable from the regenerated transitions. / 再生成遷移から導出可能。
- **511 natural feature combinations** — `experiments/02_natural_features/run_511_features.py`; archived reference table `results/true_compression_all_511.csv`. / 511候補の全探索。
- **No 100%-predictive genuinely compressive candidate among the 511 natural-feature combinations** — regression check over `true_compression_all_511.csv`. / 511候補内では真の圧縮と100%予測の両立0件。
- **692-class constructive upper bound and exact lower bound** — `experiments/03_exact_partition/`; certificate in `results/summary_exact.json` and `anchor_group_chromatic.csv`. / 692クラスの上界構成と厳密下界。
- **352 singleton / 340 multi-field classes; maximum size 65** — `summary_exact.json` and partition-structure archived outputs. / 692分割の内部構造。
- **Main paper figures** — `paper/figures/`. / 論文掲載図。
