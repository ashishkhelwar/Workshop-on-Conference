#!/usr/bin/env python3
"""Charts + Excel + analytical report (PDF & DOCX) from elephant_death_data.R"""
import os
from collections import Counter, defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from elephant_death_data import R

DIR='/home/user/Workshop-on-Conference'
CH=os.path.join(DIR,'death_charts'); os.makedirs(CH,exist_ok=True)

DARK='#1B4332'; MED='#2D6A4F'; LIGHT='#52B788'; PALE='#95D5B2'; TINT='#D8F3DC'
RED='#8B0000'; AMBER='#B8860B'; STEEL='#34638B'; GREY='#8A8A8A'
plt.rcParams.update({'font.size':10,'font.family':'DejaVu Sans','axes.edgecolor':'#888',
                     'axes.grid':True,'grid.color':'#E2E2E2','grid.linewidth':0.7,
                     'axes.axisbelow':True,'figure.dpi':150})

def save(fig,name):
    p=os.path.join(CH,name); fig.tight_layout(); fig.savefig(p,bbox_inches='tight'); plt.close(fig); return p

DIVS=['Dharamjaigarh','Raigarh']
years=sorted({r['cyear'] for r in R})

# ---- Chart 1: deaths per calendar year, stacked by division ----
by_dy={d:[sum(1 for r in R if r['cyear']==y and r['division']==d) for y in years] for d in DIVS}
fig,ax=plt.subplots(figsize=(7,3.6))
bottom=[0]*len(years)
for d,col in zip(DIVS,[MED,LIGHT]):
    ax.bar(years,by_dy[d],bottom=bottom,label=d,color=col,edgecolor='white',width=0.62)
    bottom=[a+b for a,b in zip(bottom,by_dy[d])]
for i,y in enumerate(years):
    t=bottom[i]
    if t: ax.text(y,t+0.2,str(t),ha='center',fontweight='bold',fontsize=9)
ax.set_title('Elephant Deaths per Year (by Division)',fontweight='bold',color=DARK)
ax.set_xlabel('Calendar Year'); ax.set_ylabel('Deaths')
ax.yaxis.set_major_locator(MaxNLocator(integer=True)); ax.legend(frameon=False)
save(fig,'c1_year_division.png')

# ---- Chart 2: cause group (combined, horizontal) ----
cc=Counter(r['cause_group'] for r in R)
items=sorted(cc.items(),key=lambda x:x[1])
labels=[k for k,_ in items]; vals=[v for _,v in items]
cols=[RED if 'Electro' in l else STEEL if 'Drown' in l else AMBER if 'Disease' in l else MED for l in labels]
fig,ax=plt.subplots(figsize=(7,4.3))
ax.barh(labels,vals,color=cols,edgecolor='white')
for i,v in enumerate(vals): ax.text(v+0.15,i,str(v),va='center',fontweight='bold',fontsize=9)
ax.set_title('Deaths by Cause (both divisions, n=51)',fontweight='bold',color=DARK)
ax.set_xlabel('Deaths'); ax.grid(axis='y',visible=False); ax.set_xlim(0,max(vals)+2)
save(fig,'c2_cause.png')

# ---- Chart 3: cause profile by division (grouped, top causes) ----
top=['Electrocution','Drowning / water body','Old age / natural','Fall / difficult terrain',
     'Disease (infectious)','Lightning (vajrapat)','Birth / newborn complication',
     'Injury (fall in nala/brain)','Inter-elephant fight','Heat stroke','Weakness/emaciation','Train hit']
short={'Electrocution':'Electrocution','Drowning / water body':'Drowning','Old age / natural':'Old age',
       'Fall / difficult terrain':'Fall/terrain','Disease (infectious)':'Disease','Lightning (vajrapat)':'Lightning',
       'Birth / newborn complication':'Birth/newborn','Injury (fall in nala/brain)':'Injury','Inter-elephant fight':'Fight',
       'Heat stroke':'Heat stroke','Weakness/emaciation':'Weakness','Train hit':'Train'}
dj=[sum(1 for r in R if r['division']=='Dharamjaigarh' and r['cause_group']==c) for c in top]
rg=[sum(1 for r in R if r['division']=='Raigarh' and r['cause_group']==c) for c in top]
import numpy as np
x=np.arange(len(top)); w=0.4
fig,ax=plt.subplots(figsize=(8.2,3.9))
ax.bar(x-w/2,dj,w,label='Dharamjaigarh',color=MED,edgecolor='white')
ax.bar(x+w/2,rg,w,label='Raigarh',color=LIGHT,edgecolor='white')
ax.set_xticks(x); ax.set_xticklabels([short[c] for c in top],rotation=40,ha='right',fontsize=8)
ax.set_title('Cause Profile by Division',fontweight='bold',color=DARK)
ax.set_ylabel('Deaths'); ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.legend(frameon=False); ax.grid(axis='x',visible=False)
save(fig,'c3_cause_by_division.png')

# ---- Chart 4: age class distribution ----
order=['Newborn (<1 mo)','Calf (<1 yr)','Juvenile (1–5 yr)','Sub-adult (5–15 yr)','Adult (>15 yr)']
ac=Counter(r['age_class'] for r in R)
vals=[ac.get(o,0) for o in order]
fig,ax=plt.subplots(figsize=(7,3.5))
ax.bar([o.split(' (')[0] for o in order],vals,color=[PALE,LIGHT,MED,'#40916C',DARK],edgecolor='white')
for i,v in enumerate(vals):
    if v: ax.text(i,v+0.2,str(v),ha='center',fontweight='bold',fontsize=9)
ax.set_title('Deaths by Age Class (n=51)',fontweight='bold',color=DARK)
ax.set_ylabel('Deaths'); ax.grid(axis='x',visible=False)
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
save(fig,'c4_ageclass.png')

# ---- Chart 5: natural vs unnatural donut per division ----
fig,axs=plt.subplots(1,2,figsize=(7.4,3.5))
for ax,d in zip(axs,DIVS):
    nu=Counter(r['nat'] for r in R if r['division']==d)
    vals=[nu.get('Unnatural',0),nu.get('Natural',0)]
    ax.pie(vals,labels=[f'Unnatural\n{vals[0]}',f'Natural\n{vals[1]}'],colors=[RED,MED],
           wedgeprops=dict(width=0.42,edgecolor='white'),startangle=90,textprops={'fontsize':9})
    ax.set_title(f'{d}\n(n={sum(vals)})',fontweight='bold',color=DARK,fontsize=10)
fig.suptitle('Natural vs Unnatural Deaths',fontweight='bold',color=DARK,y=1.02)
save(fig,'c5_nat_unnat.png')

# ---- Chart 6: electrocution victims by age class ----
elec=[r for r in R if r['cause_group']=='Electrocution']
eac=Counter(r['age_class'] for r in elec)
vals=[eac.get(o,0) for o in order]
fig,ax=plt.subplots(figsize=(7,3.3))
ax.bar([o.split(' (')[0] for o in order],vals,color=RED,edgecolor='white',alpha=0.85)
for i,v in enumerate(vals):
    if v: ax.text(i,v+0.1,str(v),ha='center',fontweight='bold',fontsize=9)
ax.set_title(f'Electrocution Victims by Age Class (n={len(elec)})',fontweight='bold',color=DARK)
ax.set_ylabel('Deaths'); ax.grid(axis='x',visible=False)
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
save(fig,'c6_elec_age.png')

# ---- Chart 7: range hotspots ----
rc=Counter(r['range'] for r in R)
items=sorted(rc.items(),key=lambda x:x[1])
fig,ax=plt.subplots(figsize=(7,3.6))
ax.barh([k for k,_ in items],[v for _,v in items],color=MED,edgecolor='white')
for i,(k,v) in enumerate(items): ax.text(v+0.1,i,str(v),va='center',fontweight='bold',fontsize=9)
ax.set_title('Deaths by Range (Hotspots)',fontweight='bold',color=DARK)
ax.set_xlabel('Deaths'); ax.grid(axis='y',visible=False); ax.set_xlim(0,max(rc.values())+1.5)
save(fig,'c7_ranges.png')

print('Charts built in', CH)

# ============ aggregates for report ============
def agg():
    a={}
    a['total']=len(R)
    a['dj']=sum(1 for r in R if r['division']=='Dharamjaigarh')
    a['rg']=sum(1 for r in R if r['division']=='Raigarh')
    a['elec']=sum(1 for r in R if r['cause_group']=='Electrocution')
    a['drown']=sum(1 for r in R if r['cause_group']=='Drowning / water body')
    a['unnat']=sum(1 for r in R if r['nat']=='Unnatural')
    a['nat']=sum(1 for r in R if r['nat']=='Natural')
    a['disease']=sum(1 for r in R if r['cause_group']=='Disease (infectious)')
    a['elec_dj']=sum(1 for r in R if r['cause_group']=='Electrocution' and r['division']=='Dharamjaigarh')
    a['elec_rg']=sum(1 for r in R if r['cause_group']=='Electrocution' and r['division']=='Raigarh')
    a['drown_rg']=sum(1 for r in R if r['cause_group']=='Drowning / water body' and r['division']=='Raigarh')
    a['drown_dj']=sum(1 for r in R if r['cause_group']=='Drowning / water body' and r['division']=='Dharamjaigarh')
    a['action']=sum(1 for r in R if str(r['action']).startswith('Yes'))
    # calves/juveniles (<5)
    young=sum(1 for r in R if r['age_class'] in ('Newborn (<1 mo)','Calf (<1 yr)','Juvenile (1–5 yr)'))
    a['young']=young
    a['adult']=sum(1 for r in R if r['age_class']=='Adult (>15 yr)')
    elec=[r for r in R if r['cause_group']=='Electrocution']
    a['elec_adult']=sum(1 for r in elec if r['age_class']=='Adult (>15 yr)')
    a['pct']=lambda n: round(100*n/len(R))
    return a

if __name__=='__main__':
    a=agg()
    for k,v in a.items():
        if k!='pct': print(f'{k}: {v}')
