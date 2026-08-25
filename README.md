# ABCW Paper Reproducibility Archive / ABCW論文 再現性アーカイブ

## English
This repository is version **0.7.0** of the reproducibility package for **ABCW paper master v0.4**. It is organized so that the folder can be published on GitHub as-is. The core numerical chain can be regenerated from code: four initial fields × 1,024 action/strategy initial conditions produce **56,536 transitions**, **2,562 distinct current fields**, and **11,202 distinct `(action, field)` states**. The exact predictive-partition result is **692 field classes**.

The archive distinguishes three levels of evidence: **recomputed from model code**, **recomputed from stored conflict data**, and **archived result tables checked by regression tests**. This distinction is intentional; no unavailable source file has been silently reconstructed and presented as an original artifact.

### One-command full verification

For a genuinely new, disposable environment on macOS or Linux, run:

```bash
sh scripts/verify_clean.sh
```

The script requires CPython 3.12, creates a new temporary venv with system
site-packages disabled, installs `requirements-lock.txt`, runs `pip check`, runs
the complete verification, and removes the temporary environment after success
or failure. To select Python explicitly, use
`PYTHON=/path/to/python3.12 sh scripts/verify_clean.sh`. To retain the temporary
environment for inspection, set `ABCW_KEEP_CLEAN_ENV=1`.

For an already prepared environment, use:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-lock.txt
python scripts/verify_full.py
```

This command regenerates the complete dataset, rebuilds the incompatibility graph,
checks every conflict edge against the constructive 692-coloring, directly verifies
one-step determinism, exactly re-solves all 625 anchor groups, and recomputes and
compares all 511 natural-feature candidates. `python scripts/verify_all.py` remains
available as a faster smoke test, and `pytest -q` runs the lightweight regression tests.

Expected final line:
```bash
PASS FULL VERIFICATION
```

`requirements-lock.txt` records the exact CPython 3.12.13 verification
environment used for release 0.7.0. `requirements.txt` and `pyproject.toml`
retain broader lower bounds for development.

### License

Code is released under the MIT License. The paper, figures, documentation, and
generated data are released under CC BY 4.0. See `LICENSE`, `LICENSE-CODE`, and
`LICENSE-CONTENT`. Historical provenance files under `archive/` retain any
rights or notices applicable to their original sources.

### Repository layout
```text
abcw-paper-reproducibility/
├── README.md
├── CITATION.cff
├── requirements.txt
├── pyproject.toml
├── paper/                    # master v0.4 and figures
├── src/abcw/                 # preserved ABCW implementation
├── experiments/
│   ├── 01_dataset/           # regenerate the 56,536 transitions
│   ├── 02_natural_features/  # 511 natural-feature candidates + archived results
│   ├── 03_exact_partition/   # incompatibility graph, 692 coloring/lower-bound certificate
│   └── 04_partition_structure/ # archived internal-structure checks
├── data/processed/           # generated transition table (created by script)
├── docs/                     # bilingual reproducibility documentation
├── scripts/verify_all.py
├── tests/
└── archive/original_scripts/ # preserved historical scripts for provenance
```

## 日本語
このリポジトリは **ABCW paper master v0.4** に対応する再現性パッケージ **v0.7.0** です。フォルダをそのままGitHubへ公開できる構造にしています。主要な数値連鎖はコードから再生成できます。4種類の初期場 × 1,024の行動・戦略初期条件から、**56,536遷移**、**2,562種類の現在場**、**11,202種類の `(行動, 場)` 状態**が得られ、完全な一時刻先場予測を保つ最小field partitionは **692クラス**です。

本アーカイブでは証拠を、**モデルコードから再計算するもの**、**保存済みconflict dataから再計算するもの**、**保存済み結果表を回帰テストで検証するもの**の3段階に分けています。入手できなかった過去のソースを、元ファイルであるかのように黙って再構成することはしていません。

### ワンコマンド完全検証
macOSまたはLinuxでは、`sh scripts/verify_clean.sh`を実行してください。CPython 3.12から一時的な新規venvを作成し、system site-packagesを無効にしたことを確認したうえで、固定依存関係の導入、`pip check`、`verify_full.py`の実行まで行います。終了後、一時環境は自動削除されます。`verify_full.py`はデータセットの再生成、conflict graphの再構築、全conflict edgeに対する692彩色の検査、予測一価性の直接検査、625 anchor groupの厳密再求解、および511特徴候補の全再計算と保存表との照合を行います。`verify_all.py` は短時間のsmoke testとして残しています。

詳細は `docs/REPRODUCIBILITY.md`、論文中の主張とファイルの対応は `docs/PAPER_RESULT_MAP.md` を参照してください。

### ライセンス
コードはMIT License、論文・図・文書・生成データはCC BY 4.0です。詳細は`LICENSE`、`LICENSE-CODE`、`LICENSE-CONTENT`を参照してください。
