import io, re
t = io.open('research/neetpg-yearwise.txt', encoding='utf-8').read()
pages = t.split('===PAGE ')
bounds = {'2025': [7, 81], '2024': [81, 225], '2023': [225, 298], '2022': [298, 381], '2021': [381, 450], '2020': [450, 559], '2019': [559, 656], '2018': [656, 685]}
for y,(a,b) in bounds.items():
    body='\n'.join(pages[a:b])
    cut=['EXAMINATION PAPER 2025 SOLUTION','EXAMINATION PAPER 2024','EXAMINATION PAPER 2023','EXAMINATION PAPER 2022','EXAMINATION PAPER 2021','EXAMINATION PAPER 2020','EXAMINATION PAPER 2019','EXAMINATION PAPER 2018']
    for c in cut:
        p=body.find(c)
        if p>0: body=body[:p]; 
    body=body[:body.find('EXAMINATION PAPER 2025 SOLUTION')] if 'SOLUTION' in body else body
    # restrict to question paper block (first 500 lines after header)
    cands={}
    for ln in body.split('\n'):
        s=ln.strip()
        if 2<=len(s)<=38 and re.match(r"^[A-Z][A-Z &,()'/.\-]{1,36}$", s):
            cands.setdefault(s.upper(),0); cands[s.upper()]+=1
    known=[k for k in cands if k in ('ANATOMY','BIOCHEMISTRY','PHYSIOLOGY','PATHOLOGY','PHARMACOLOGY','MICROBIOLOGY','FORENSIC MEDICINE','PSM','COMMUNITY MEDICINE','MEDICINE','GENERAL MEDICINE','SURGERY','GENERAL SURGERY','ORTHOPEDICS','ORTHOPAEDICS','OBSTETRICS','OBG','GYNAECOLOGY','GYNECOLOGY','OBS & GYNE','PAEDIATRICS','PEDIATRICS','ENT','OPHTHALMOLOGY','OPTHALMOLOGY','PSYCHIATRY','ANAESTHESIA','ANESTHESIA','ANAESTHESIOLOGY','RADIOLOGY','DERMATOLOGY','RADIO DIAGNOSIS','OPHTHALMO','GEN SURGERY')]
    print(y, '->', known, {k:v for k,v in cands.items() if any(w in k for w in ['GYN','OBST','PAED','PEDIAT','ORTHO','ANESTH','ANAESTH','MEDICA','SURG','OPHTH','RADIO','DERM'])})
