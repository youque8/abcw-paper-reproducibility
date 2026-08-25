# Data Dictionary / データ辞書

## English
`data/processed/transitions_56536.csv` is generated, not stored initially. Columns: `field` (initial-field family), `a` (current action vector), `s` (current strategy vector), `W` (current 5×5 field, rows separated by `;`), `W_next`, `a_next`, `s_next`.

`anchor_group_chromatic.csv`: `future_id`, group size `n`, internal conflict `edges`, exact `chi`, clique lower bound `lb`, search upper bound `ub`, and runtime `seconds`.

`min_partition_upper692.csv` stores the constructive 692-class assignment used for the upper bound.

## 日本語
`transitions_56536.csv` は初期状態では同梱せず、スクリプトで生成します。列は `field`（初期場種別）、`a`（現在行動）、`s`（現在戦略）、`W`（現在の5×5場。行区切りは`;`）、`W_next`、`a_next`、`s_next` です。

`anchor_group_chromatic.csv` は各anchor groupについて、`future_id`、群サイズ `n`、内部conflict辺数 `edges`、厳密 `chi`、clique下界 `lb`、探索上界 `ub`、計算時間 `seconds` を保存します。

`min_partition_upper692.csv` は上界を与える692クラスの構成的割当です。
