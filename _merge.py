# -*- coding: utf-8 -*-
import io, json, re, hashlib
# load existing bank.js (parse window.QUESTIONS array)
src = io.open('questions/bank.js', encoding='utf-8').read()
m = re.search(r'window\.QUESTIONS\s*=\s*(\[.*\])\s*;', src, re.S)
old = json.loads(m.group(1))
print('existing bank:', len(old))
subs = json.loads(io.open('research/_expand_bank.json',encoding='utf-8').read())
news=[]
for subj, qq in subs.items():
    for q in qq:
        news.append(dict(q, s=subj))   # ensure subject field
print('expand:', len(news))
# canonical subject names check vs app 19
APP = ["Anatomy","Biochemistry","Physiology","Pathology","Pharmacology","Microbiology","Forensic Medicine","PSM","ENT","Ophthalmology","Medicine","Surgery","OBG","Paediatrics","Psychiatry","Anaesthesia","Radiology","Orthopaedics","Dermatology"]
snew=sorted(set(q['s'] for q in news))
print('expand subj names:', snew)
print('not in app subjects:', [s for s in snew if s not in APP])
oldsub=sorted(set(q['s'] for q in old))
print('old subj:', oldsub)
print('old not in app:', [s for s in oldsub if s not in APP])
# cross dup by q normalized
def norm(x):
    return re.sub(r'[^a-z0-9]+',' ', x.lower()).strip()
seen=set()
cross=0
for q in old:
    seen.add(norm(q['q']))
for q in news:
    if norm(q['q']) in seen: cross+=1
    seen.add(norm(q['q']))
print('cross-dupes old/new:', cross)
