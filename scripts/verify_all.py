#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,json,pandas as pd
R=Path(__file__).resolve().parents[1]
def run(rel):
 print('\n==',rel,'=='); subprocess.run([sys.executable,str(R/rel)],check=True,cwd=R)
run('experiments/01_dataset/generate_transitions.py')
run('experiments/03_exact_partition/build_conflict_data.py')
run('experiments/03_exact_partition/verify_certificate.py')
# lightweight archived natural-feature checks
f=pd.read_csv(R/'experiments/02_natural_features/results/true_compression_all_511.csv')
assert len(f)==511
assert int((f.B_unique_DeltaW<2562).sum())==261
assert int(((f.B_unique_DeltaW<2562)&(f.D_state==1.0)).sum())==0
s=json.load(open(R/'experiments/03_exact_partition/results/summary_exact.json'))
assert s['transitions']==56536 and s['distinct_fields']==2562 and s['distinct_aW']==11202 and s['exact_minimum_classes']==692
print('\nPASS: core paper reproducibility checks completed.')
print('For a full recomputation of all 511 natural-feature candidates, run: python experiments/02_natural_features/run_511_features.py')
print('For exact re-solving of all 50 difficult anchor groups, run: python experiments/03_exact_partition/exact_anchor_refinement.py')
