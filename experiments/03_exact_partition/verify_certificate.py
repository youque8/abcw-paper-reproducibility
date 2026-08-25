from pathlib import Path
import json,pandas as pd
R=Path(__file__).resolve().parent/'results'
s=json.load(open(R/'summary_exact.json'))
a=pd.read_csv(R/'anchor_group_chromatic.csv')
assert s['exact_minimum_classes']==692 and s['minimum_proved'] is True
assert len(a)==625 and int(a['chi'].sum())==692
assert int((a['chi']>1).sum())==50
counts=a['chi'].value_counts().to_dict()
assert counts.get(1)==575 and counts.get(2)==39 and counts.get(3)==8 and counts.get(4)==2 and counts.get(7)==1
print('PASS exact certificate: chi(G)=692; 575/39/8/2/1 anchor-group distribution')
