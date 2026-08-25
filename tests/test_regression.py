import json,pandas as pd
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_exact_summary():
 s=json.load(open(R/'experiments/03_exact_partition/results/summary_exact.json'))
 assert (s['transitions'],s['distinct_fields'],s['distinct_aW'],s['exact_minimum_classes'])==(56536,2562,11202,692)
def test_anchor_certificate():
 a=pd.read_csv(R/'experiments/03_exact_partition/results/anchor_group_chromatic.csv')
 assert len(a)==625 and a.chi.sum()==692 and (a.chi>1).sum()==50
def test_feature_scan():
 f=pd.read_csv(R/'experiments/02_natural_features/results/true_compression_all_511.csv')
 assert len(f)==511 and (f.B_unique_DeltaW<2562).sum()==261
 assert (((f.B_unique_DeltaW<2562)&(f.D_state==1.0)).sum())==0
