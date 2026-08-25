import pandas as pd, numpy as np, json, ast
from collections import defaultdict, Counter

CSV='/mnt/data/transitions_56536.csv'
df=pd.read_csv(CSV)
N=len(df)

def parse_vec(s): return tuple(int(x) for x in str(s).split())
def parse_mat(s): return np.array([[int(x) for x in row.split()] for row in str(s).split(';')],dtype=int)
def mat_tuple(M): return tuple(int(x) for x in M.ravel())
def mat_str(M): return ';'.join(' '.join(str(int(x)) for x in row) for row in M)

Wstar=np.ones((5,5),dtype=int); np.fill_diagonal(Wstar,0)
Ws=[parse_mat(s)-Wstar for s in df['W']]
Wns=[parse_mat(s)-Wstar for s in df['W_next']]
a=[parse_vec(s) for s in df['a']]
fields=df['field'].astype(str).tolist()

def outv(M): return tuple(int(x) for x in M.sum(axis=1))
def frob2(M): return int(np.sum(M*M))

# Base groups: (a,out-strength vector)
base=defaultdict(list)
for i,(ai,M,Mn) in enumerate(zip(a,Ws,Wns)):
    base[(ai,outv(M))].append(i)

# identify nondeterministic groups
amb=[]
for key,idxs in base.items():
    tg=Counter(mat_tuple(Wns[i]) for i in idxs)
    if len(tg)>1:
        amb.append((key,idxs,tg))
amb.sort(key=lambda x:(x[0][0],x[0][1]))
assert len(amb)==58, len(amb)

# Detailed group summary and row-level members
summ=[]; members=[]
for gid,(key,idxs,tg) in enumerate(amb,1):
    ai,ov=key
    fgroups=defaultdict(list)
    micro=defaultdict(list)
    for i in idxs:
        fgroups[frob2(Ws[i])].append(i)
        micro[mat_tuple(Ws[i])].append(i)
    # modal errors before
    modal=max(tg.values()); errors=len(idxs)-modal
    # after frob target sets
    f_target_counts={f:Counter(mat_tuple(Wns[i]) for i in ii) for f,ii in fgroups.items()}
    after_det=all(len(c)==1 for c in f_target_counts.values())
    # one-to-one target vs frob? different frob values can lead same target
    target_by_f={f:next(iter(c)) if len(c)==1 else None for f,c in f_target_counts.items()}
    n_unique_target=len(tg)
    n_frob=len(fgroups)
    summ.append({
        'collision_id':gid,
        'a':' '.join(map(str,ai)),
        'out_strength_vector':' '.join(map(str,ov)),
        'n_transition_rows':len(idxs),
        'n_distinct_current_DeltaW':len(micro),
        'n_distinct_next_DeltaW':n_unique_target,
        'n_frob2_values':n_frob,
        'frob2_values':'|'.join(map(str,sorted(fgroups))),
        'modal_errors_before':errors,
        'resolved_by_frob2':after_det,
        'field_values':'|'.join(sorted(set(fields[i] for i in idxs))),
    })
    # enumerate unique current microstate x target combinations, frequency
    combo=Counter((mat_tuple(Ws[i]),frob2(Ws[i]),mat_tuple(Wns[i]),fields[i]) for i in idxs)
    for (cur,f,targ,field),freq in combo.items():
        M=np.array(cur,dtype=int).reshape(5,5); Mn=np.array(targ,dtype=int).reshape(5,5)
        members.append({
            'collision_id':gid,'a':' '.join(map(str,ai)),'out_strength_vector':' '.join(map(str,ov)),
            'frob2':f,'field':field,'frequency':freq,
            'DeltaW':mat_str(M),'DeltaW_next':mat_str(Mn)
        })

sdf=pd.DataFrame(summ); mdf=pd.DataFrame(members)
sdf.to_csv('/mnt/data/collision_58_summary.csv',index=False)
mdf.to_csv('/mnt/data/collision_58_members.csv',index=False)

# Compression analysis on observed distinct current states
micro_keys=[(a[i],mat_tuple(Ws[i])) for i in range(N)]
pstar_keys=[(a[i],outv(Ws[i]),frob2(Ws[i])) for i in range(N)]
out_keys=[(a[i],outv(Ws[i])) for i in range(N)]
B_micro=[mat_tuple(Ws[i]) for i in range(N)]
B_pstar=[(outv(Ws[i]),frob2(Ws[i])) for i in range(N)]
B_out=[outv(Ws[i]) for i in range(N)]

unique_micro=set(micro_keys); unique_pstar=set(pstar_keys); unique_out=set(out_keys)
unique_DW=set(B_micro); unique_Bstar=set(B_pstar); unique_out_only=set(B_out)

# Map P* to observed microstates; collision here would mean true compression
p_to_micro=defaultdict(set)
for mk,pk in zip(micro_keys,pstar_keys): p_to_micro[pk].add(mk)
compressed_classes={k:v for k,v in p_to_micro.items() if len(v)>1}
# Map B* to DeltaW irrespective of a
bp_to_dw=defaultdict(set)
for dw,bp in zip(B_micro,B_pstar): bp_to_dw[bp].add(dw)
Bcompressed={k:v for k,v in bp_to_dw.items() if len(v)>1}

# base mapping compression
out_to_micro=defaultdict(set)
for mk,ok in zip(micro_keys,out_keys): out_to_micro[ok].add(mk)
base_compressed=[len(v) for v in out_to_micro.values() if len(v)>1]

# Ambiguous group aggregate anatomy
split_counts=sdf['n_frob2_values'].value_counts().sort_index().to_dict()
target_counts=sdf['n_distinct_next_DeltaW'].value_counts().sort_index().to_dict()
current_counts=sdf['n_distinct_current_DeltaW'].value_counts().sort_index().to_dict()
field_counts=Counter()
for _,row in sdf.iterrows():
    for f in str(row.field_values).split('|'): field_counts[f]+=1

result={
 'N_transition_rows':N,
 'base_unique_observation_groups':len(unique_out),
 'base_ambiguous_groups':len(amb),
 'base_deterministic_groups':len(unique_out)-len(amb),
 'ambiguous_transition_rows':int(sum(len(x[1]) for x in amb)),
 'modal_errors_base':int(sum(len(idxs)-max(tg.values()) for _,idxs,tg in amb)),
 'ambiguous_groups_resolved_by_frob2':int(sdf.resolved_by_frob2.sum()),
 'pstar_unique_groups':len(unique_pstar),
 'micro_unique_a_DeltaW_states':len(unique_micro),
 'pstar_to_micro_multimember_classes':len(compressed_classes),
 'pstar_max_microstates_per_class':max((len(v) for v in p_to_micro.values()),default=0),
 'Bstar_unique_values':len(unique_Bstar),
 'unique_DeltaW_values':len(unique_DW),
 'Bstar_to_DeltaW_multimember_classes':len(Bcompressed),
 'Bstar_max_DeltaW_per_class':max((len(v) for v in bp_to_dw.values()),default=0),
 'out_only_unique_a_groups':len(unique_out),
 'out_only_multimember_micro_classes':len(base_compressed),
 'out_only_max_microstates_per_class':max(base_compressed) if base_compressed else 1,
 'frob_split_count_distribution':{str(k):int(v) for k,v in split_counts.items()},
 'next_target_count_distribution':{str(k):int(v) for k,v in target_counts.items()},
 'current_micro_count_distribution':{str(k):int(v) for k,v in current_counts.items()},
 'collision_groups_by_field_membership':dict(field_counts),
 'extra_groups_from_frob2':len(unique_pstar)-len(unique_out),
}

# Are partitions exactly bijective micro <-> P*?
result['pstar_is_bijective_on_observed_microstates']=(len(unique_pstar)==len(unique_micro) and len(compressed_classes)==0)
result['Bstar_is_bijective_on_observed_DeltaW']=(len(unique_Bstar)==len(unique_DW) and len(Bcompressed)==0)

with open('/mnt/data/collision_compression_summary.json','w') as f: json.dump(result,f,indent=2,ensure_ascii=False)

print(json.dumps(result,indent=2,ensure_ascii=False))
print('\nTop 15 collision groups by transition rows:')
print(sdf.sort_values(['n_transition_rows','modal_errors_before'],ascending=False).head(15).to_string(index=False))
