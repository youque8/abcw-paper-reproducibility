import sys, itertools, csv
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0,'/mnt/data')
from abcw_n5_adaptive_strategy_v0_1 import ABCWAdaptiveSimulator, ABCWAdaptiveConfig, complete_directed_topology, pm_string, strategy_string

N=5
E=complete_directed_topology(N)
BASE=E.copy().astype(int)

def make_W(kind):
    W=BASE.copy()
    if kind=='baseline':
        return W
    if kind=='hub':
        edges=[(0,1),(0,2),(0,3),(0,4)]
    elif kind=='local':
        edges=[(0,1),(1,2),(2,3),(3,4)]
    elif kind=='hub_local':
        # two long-range hub edges + two local competitors into same targets
        edges=[(0,2),(0,4),(1,2),(3,4)]
    else: raise ValueError(kind)
    for i,j in edges: W[i,j]=4
    return W

def run_case(a0,s0,W0,max_steps=2000):
    sim=ABCWAdaptiveSimulator(ABCWAdaptiveConfig(E=E,eta=1), a0,s0,W0)
    seen={}
    for _ in range(max_steps):
        key=sim.state_key()
        if key in seen:
            return 'cycle', seen[key], sim.t-seen[key], sim
        seen[key]=sim.t
        sim.step()
    return 'no_cycle',None,None,sim

profiles=list(itertools.product([-1,1],repeat=N))
allrows=[]
summary=[]
for kind in ['baseline','hub','local','hub_local']:
    W0=make_W(kind)
    cnt=Counter(); trans=[]
    case=0
    for a0 in profiles:
        for s0 in profiles:
            status,start,period,sim=run_case(a0,s0,W0.copy())
            if status=='cycle':
                cnt[period]+=1; trans.append(start)
            else: cnt['no_cycle']+=1
            allrows.append(dict(kind=kind,case_id=case,a0=pm_string(a0),s0=strategy_string(s0),status=status,transient=start,period=period))
            case+=1
    summary.append((kind,cnt, max(trans) if trans else None, float(np.linalg.norm(W0-BASE)), int((W0-BASE).sum())))

with open('/mnt/data/ch7_pilot_cases.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=allrows[0].keys()); w.writeheader(); w.writerows(allrows)

# pairwise period classification differences among three experimental conditions
bykind=defaultdict(dict)
for r in allrows: bykind[r['kind']][r['case_id']]=r['period'] if r['status']=='cycle' else None
pairs=[]
ks=['hub','local','hub_local']
for i in range(len(ks)):
    for j in range(i+1,len(ks)):
        a,b=ks[i],ks[j]
        diff=sum(bykind[a][cid]!=bykind[b][cid] for cid in range(1024))
        pairs.append((a,b,diff))

print('MATRICES')
for k in ['hub','local','hub_local']:
    print(k); print(make_W(k))
print('\nSUMMARY')
for x in summary: print(x)
print('\nPAIRWISE DIFF')
for x in pairs: print(x)
