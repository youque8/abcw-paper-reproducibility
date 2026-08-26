# Reproducibility Guide / 再現手順

## English
### Automated GitHub verification

`.github/workflows/reproducibility.yml` runs the full clean-environment audit
on every push and pull request. It can also be launched with **Run workflow**
from the repository's GitHub Actions tab. The job has read-only repository
permissions, verifies `SHA256SUMS.txt`, selects CPython 3.12, and runs
`sh scripts/verify_clean.sh` on a fresh Ubuntu runner.

### Full one-command audit
On macOS or Linux, create a disposable clean environment and run the complete
audit with one command:

```bash
sh scripts/verify_clean.sh
```

The wrapper requires CPython 3.12 and creates a new temporary venv. It checks
that system site-packages are disabled, installs the exact locked dependencies,
runs `pip check`, and launches `verify_full.py`. The temporary environment is
removed on both success and failure. Use `PYTHON=/path/to/python3.12` to select
the interpreter or `ABCW_KEEP_CLEAN_ENV=1` to retain the environment for audit.

The equivalent manual commands are:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python scripts/verify_full.py
```

The command performs the entire evidence chain rather than trusting the stored
summary values. It regenerates the 56,536 transitions; rebuilds the 2,562-vertex
incompatibility graph; checks the stored 692-coloring against every conflict edge;
directly verifies that every observed `(action, color)` has a unique next field;
re-solves all 625 anchor groups and compares their exact chromatic numbers with the
archived certificate; and recomputes all 511 natural-feature candidates and compares
their complete result rows with the archived reference table.

The expected final status is `PASS FULL VERIFICATION`.

### Level A — regenerate from the ABCW rules
Run `python experiments/01_dataset/generate_transitions.py`. Expected output: 56,536 transitions, 2,562 distinct fields, 11,202 distinct `(a, field)` states. The implementation uses five agents, learning rate `eta=1`, baseline off-diagonal weight 1, and the Hub/Local/Hub+Local edge sets specified in paper v1.1.

Run `python experiments/03_exact_partition/build_conflict_data.py` to independently rebuild the field-action response table and incompatibility matrix from the same rules.

### Level B — exact minimum certificate
`experiments/03_exact_partition/results/anchor_group_chromatic.csv` stores the exact chromatic numbers of the 625 anchor groups. Their sum is 692: 575 groups need 1 color, 39 need 2, 8 need 3, 2 need 4, and 1 needs 7. `verify_certificate.py` checks this certificate. `exact_anchor_refinement.py` can re-solve the difficult groups from recomputed conflict data.

### Level C — archived analysis tables
The 511-feature tables and partition-structure tables are retained as published experiment outputs and are covered by regression checks. Historical scripts are kept under `archive/original_scripts/` when available.

## 日本語
### GitHub上の自動検証

`.github/workflows/reproducibility.yml`は、pushおよびPull Requestのたびにclean environment完全監査を実行します。GitHubリポジトリのActions画面にある**Run workflow**から手動実行することもできます。ジョブのリポジトリ権限は読み取り専用で、`SHA256SUMS.txt`の検査、CPython 3.12の設定、および新規Ubuntu runner上での`sh scripts/verify_clean.sh`を実行します。

### ワンコマンド完全監査
macOSまたはLinuxでは、次の一コマンドで一時的なclean environmentを作成し、完全監査を実行できます。

```bash
sh scripts/verify_clean.sh
```

このラッパーはCPython 3.12を使用して一時ディレクトリに新規venvを作り、system site-packagesが無効であることを確認します。その後、固定依存関係の導入、`pip check`、`verify_full.py`の実行を行い、成功・失敗のいずれの場合も一時環境を削除します。Pythonを指定する場合は`PYTHON=/path/to/python3.12`、環境を監査用に残す場合は`ABCW_KEEP_CLEAN_ENV=1`を使用します。

手動で同じ処理を行う場合は次のとおりです。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python scripts/verify_full.py
```

このコマンドは保存済みsummaryの数値を信用するだけでなく、証拠連鎖全体を再計算します。56,536遷移の再生成、2,562頂点のincompatibility graph再構築、全conflict edgeに対する692彩色の検査、すべての観測された `(action, color)` から次場が一意に決まることの直接検査、625 anchor groupの厳密再求解と保存証明書との照合、および511自然特徴候補の全再計算と保存表との照合を行います。

最終行の期待値は `PASS FULL VERIFICATION` です。

### Level A — ABCW更新則から再生成
`python experiments/01_dataset/generate_transitions.py` を実行します。期待値は56,536遷移、2,562種類の場、11,202種類の `(a, field)` 状態です。5主体、学習率 `eta=1`、baselineの非対角重み1、および論文v1.1に明記したHub/Local/Hub+Localの強化辺を用います。

`python experiments/03_exact_partition/build_conflict_data.py` は同じ更新則からfield-action応答表とincompatibility matrixを独立に再構築します。

### Level B — 厳密最小値の証明書
`anchor_group_chromatic.csv` は625個のanchor groupそれぞれの厳密chromatic numberを保存しています。内訳は `575×1 + 39×2 + 8×3 + 2×4 + 1×7 = 692` です。`verify_certificate.py` がこれを検査します。`exact_anchor_refinement.py` では再生成したconflict dataから難しい群を再度解けます。

### Level C — 保存済み解析表
511特徴候補および692クラス内部構造の表は、実験時の出力として保存し回帰検査の対象にしています。入手できた歴史的スクリプトは `archive/original_scripts/` に原形で保存しています。
