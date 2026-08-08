# -*- coding: utf-8 -*-
import io, json, re
from collections import defaultdict
qs = json.loads(io.open('research/_inicet_parsed.json',encoding='utf-8').read())
# Fix MAY 2022 Q1 subj manually first
for q in qs:
    if q['year']=='MAY 2022' and q['num']==1:
        q['subj'] = 'Physiology'
# Subject mapping
SUBJMAP = {'ANATOMY':'Anatomy','BIOCHEMISTRY':'Biochemistry','PHYSIOLOGY':'Physiology',
 'PATHOLOGY':'Pathology','PHARMACOLOGY':'Pharmacology','MICROBIOLOGY':'Microbiology',
 'FORENSIC MEDICINE':'Forensic Medicine','COMMUNITY MEDICINE':'PSM','PSM':'PSM',
 'ENT':'ENT','OPHTHALMOLOGY':'Ophthalmology','MEDICINE':'Medicine','SURGERY':'Surgery',
 'OBG':'OBG','OBS & GYNE':'OBG','OBS&GYNE':'OBG','PAEDIATRICS':'Paediatrics','PEDIATRICS':'Paediatrics',
 'PSYCHIATRY':'Psychiatry','ANAESTHESIA':'Anaesthesia','ANESTHESIA':'Anaesthesia',
 'RADIOLOGY':'Radiology','ORTHOPEDICS':'Orthopaedics','ORTHOPAEDICS':'Orthopaedics',
 'DERMATOLOGY':'Dermatology'}
# Fix NONE subjects
by_paper = defaultdict(list)
for q in qs: by_paper[q['year']].append(q)
def norm_subj(s):
    if not s:
        return None
    s = s.strip().upper()
    # handle plural/singular variants
    return s
for y, qq in by_paper.items():
    qq.sort(key=lambda x: x['num'])
    last = None
    for q in qq:
        key = norm_subj(q.get('subj'))
        if key in SUBJMAP: last = SUBJMAP[key]
        elif last: q['subj'] = last
for q in qs:
    key = norm_subj(q.get('subj'))
    if key in SUBJMAP: q['subj']=SUBJMAP[key]
    q['exam']='INI-CET'
imgpat = re.compile(r'(image|figure|diagram|photo|radiograph|ct scan|mri|histolog|microscop|show+n|\barrow)', re.I)
for q in qs:
    if imgpat.search(q.get('stem','')): q['img']=True
    else: q['img']=False
# Re-format to NEET schema
final=[]
for q in qs:
    if len(q.get('opts',[]))==4 and q.get('ans') in 'ABCD':
        q_new = {'q':q['stem'],'o':q['opts'],'a':{'A':0,'B':1,'C':2,'D':3}[q['ans']],
                 'ex':q.get('ex',''),'e':'INI-CET','y':q['year'],'s':q['subj'],'img':q.get('img',False)}
        final.append(q_new)
io.open('research/_inicet_final.json','w',encoding='utf-8').write(json.dumps(final,ensure_ascii=False,indent=0))
print('total', len(final))
