import pandas as pd, numpy as np, itertools, math, json
from collections import defaultdict, Counter

from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CSV=ROOT/'data'/'processed'/'transitions_56536.csv'
OUT=Path(__file__).resolve().parent/'results'
df=pd.read_csv(CSV)
N=len(df)

def parse_vec(s): return tuple(int(x) for x in s.split())
def parse_mat(s): return np.array([[int(x) for x in row.split()] for row in s.split(';')],dtype=int)
Wstar=np.ones((5,5),dtype=int); np.fill_diagonal(Wstar,0)

def canon(x):
    if isinstance(x,np.ndarray): x=x.tolist()
    if isinstance(x,(tuple,list)):
        return '('+','.join(canon(y) for y in x)+')'
    if isinstance(x,float): return f'{x:.10g}'
    return str(int(x) if isinstance(x,(np.integer,)) else x)

# parse all matrices
Ws=[parse_mat(s)-Wstar for s in df['W']]
Wns=[parse_mat(s)-Wstar for s in df['W_next']]
a=[parse_vec(s) for s in df['a']]

def f_frob2(M): return int(np.sum(M*M))
def f_rank(M): return int(np.linalg.matrix_rank(M.astype(float)))
def f_stable(M):
    sv=np.linalg.svd(M.astype(float),compute_uv=False)
    return 0.0 if len(sv)==0 or sv[0]<1e-12 else round(float(np.sum(sv*sv)/(sv[0]**2)),10)
def f_sv(M): return tuple(round(float(x),10) for x in np.linalg.svd(M.astype(float),compute_uv=False))
def outv(M): return tuple(int(x) for x in M.sum(axis=1))
def inv(M): return tuple(int(x) for x in M.sum(axis=0))
def outd(M): return tuple(sorted(outv(M)))
def ind(M): return tuple(sorted(inv(M)))
def inoutd(M): return tuple(sorted(zip(inv(M),outv(M))))
FEATURES={
'frob2':f_frob2,'rank':f_rank,'stable_rank':f_stable,'singular_values':f_sv,
'out_strength_distribution':outd,'in_strength_distribution':ind,'in_out_strength_distribution':inoutd,
'out_strength_vector':outv,'in_strength_vector':inv,
}
names=list(FEATURES)
# categorical codes exact per feature and target
feat_codes=[]
for name in names:
    vals=[canon(FEATURES[name](M)) for M in Ws]
    feat_codes.append(pd.factorize(np.asarray(vals, dtype=object), sort=False)[0].astype(np.uint64)+1)
a_codes=pd.factorize(np.asarray([canon(x) for x in a], dtype=object),sort=False)[0].astype(np.uint64)+1
target_codes=pd.factorize(np.asarray([canon(tuple(int(x) for x in M.ravel())) for M in Wns], dtype=object),sort=False)[0].astype(np.int64)

# combine codes using independent 64bit mixing; later verify frontier exactly
MASK=np.uint64(0xFFFFFFFFFFFFFFFF)
def mix(h,x,seed):
    # FNV-like with feature-specific odd constants
    return (h ^ (x + np.uint64(seed))) * np.uint64(1099511628211)

def metrics_from_keys(keys):
    # sort by observation key, target
    order=np.lexsort((target_codes, keys))
    k=keys[order]; t=target_codes[order]
    # run boundaries for (k,t)
    pair_start=np.r_[True,(k[1:]!=k[:-1]) | (t[1:]!=t[:-1])]
    pair_idx=np.flatnonzero(pair_start)
    pair_counts=np.diff(np.r_[pair_idx,N])
    pair_keys=k[pair_idx]
    # group pair records by key
    gstart=np.r_[True,pair_keys[1:]!=pair_keys[:-1]]
    gi=np.flatnonzero(gstart)
    groups=len(gi)
    n_targets=np.diff(np.r_[gi,len(pair_keys)])
    det=int(np.sum(n_targets==1))
    # modal counts by group
    modal=0
    for st,en in zip(gi,np.r_[gi[1:],len(pair_keys)]): modal += int(pair_counts[st:en].max())
    return groups,det,det/groups,modal/N

results=[]
seeds=[1469598103934665603 + i*1000003 for i in range(len(names))]
for mask in range(1,1<<len(names)):
    h=(a_codes*np.uint64(11400714819323198485)) ^ np.uint64(0x9e3779b97f4a7c15)
    subset=[]
    for i,name in enumerate(names):
        if mask>>i & 1:
            h=mix(h,feat_codes[i],seeds[i]); subset.append(name)
    g,d,rate,acc=metrics_from_keys(h)
    results.append((mask,'+'.join(subset),len(subset),g,d,rate,acc))

res=pd.DataFrame(results,columns=['mask','features','n_features','unique_groups','deterministic_groups','D_state','A_freq'])

# Actual field compression: count distinct B(DeltaW) values among the 2,562 distinct current fields.
field_first={}
for j,M in enumerate(Ws):
    key=canon(tuple(int(x) for x in M.ravel()))
    field_first.setdefault(key,j)
field_rows=np.array(list(field_first.values()),dtype=int)
assert len(field_rows)==2562
b_unique=[]
for mask in res['mask']:
    cols=[feat_codes[i][field_rows] for i in range(len(names)) if (int(mask)>>i)&1]
    X=np.stack(cols,axis=1)
    b_unique.append(len(np.unique(X,axis=0)))
res['B_unique_DeltaW']=b_unique
res['DeltaW_compression_rate']=1.0-res['B_unique_DeltaW']/2562.0

# dedupe same outcome metrics conservatively for summary only
# Pareto: lower groups, higher score; strict non-domination

def frontier(score):
    rr=res.sort_values(['unique_groups',score],ascending=[True,False])
    best=-1; idx=[]
    for i,row in rr.iterrows():
        if row[score] > best + 1e-15:
            idx.append(i); best=row[score]
    return res.loc[idx].sort_values('unique_groups')
fd=frontier('D_state'); fa=frontier('A_freq')

# exact verification of all frontier candidates using Python tuple keys
vals_by_name={name:[FEATURES[name](M) for M in Ws] for name in names}
def exact_metrics(feature_list):
    groups=defaultdict(Counter)
    for j in range(N):
        key=(a[j],)+tuple(vals_by_name[n][j] for n in feature_list)
        targ=tuple(int(x) for x in Wns[j].ravel())
        groups[key][targ]+=1
    g=len(groups); d=sum(len(c)==1 for c in groups.values()); modal=sum(max(c.values()) for c in groups.values())
    return g,d,d/g,modal/N
for frame in (fd,fa):
    for i,row in frame.iterrows():
        fl=row.features.split('+')
        g,d,ds,af=exact_metrics(fl)
        assert (g,d)==(int(row.unique_groups),int(row.deterministic_groups)),(row.features,g,d,row.unique_groups,row.deterministic_groups)
        assert abs(ds-row.D_state)<1e-15 and abs(af-row.A_freq)<1e-15

# Save
res.to_csv(OUT/'true_compression_all_511_recomputed.csv',index=False)
fd.to_csv(OUT/'pareto_frontier_D_state.csv',index=False)
fa.to_csv(OUT/'pareto_frontier_A_freq.csv',index=False)
summary={
 'N_transitions':N,'candidate_subsets':len(res),
 'D_frontier_n':len(fd),'A_frontier_n':len(fa),
 'D_frontier':fd.to_dict(orient='records'),'A_frontier':fa.to_dict(orient='records'),
}
with open(OUT/'pareto_summary.json','w') as f: json.dump(summary,f,ensure_ascii=False,indent=2)
print('N',N,'candidates',len(res))
print('\nD frontier')
print(fd[['features','n_features','unique_groups','deterministic_groups','D_state','A_freq']].to_string(index=False))
print('\nA frontier')
print(fa[['features','n_features','unique_groups','deterministic_groups','D_state','A_freq']].to_string(index=False))
print('\nTop lowest-cost >= thresholds D')
for th in [0.8,0.9,0.95,0.99,0.995,1.0]:
    q=res[res.D_state>=th-1e-15].sort_values(['unique_groups','n_features','D_state'],ascending=[True,True,False]).head(1)
    print(th, q[['features','unique_groups','D_state','A_freq']].to_dict(orient='records'))
