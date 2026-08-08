import io, re, json

t = io.open('research/neetpg-yearwise.txt', encoding='utf-8').read()
pages = t.split('===PAGE ')

doc_order = [2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018]
first_sec = {2025: 7, 2024: 81, 2023: 225, 2022: 298, 2021: 381, 2020: 450, 2019: 559, 2018: 656}
bounds = {}
for i, y in enumerate(doc_order):
    start = first_sec[y]
    end = first_sec[doc_order[i + 1]] if i + 1 < len(doc_order) else 685
    bounds[y] = (start, end)

SUBJ_SET = {
    'ANATOMY', 'BIOCHEMISTRY', 'PHYSIOLOGY', 'PATHOLOGY', 'PHARMACOLOGY', 'MICROBIOLOGY',
    'FORENSIC MEDICINE', 'COMMUNITY MEDICINE', 'PSM', 'ENT', 'OPHTHALMOLOGY', 'MEDICINE', 'SURGERY',
    'OBSTETRICS', 'OBG', 'GYNAECOLOGY', 'PAEDIATRICS', 'PSYCHIATRY', 'ANAESTHESIOLOGY', 'ANAESTHESIA',
    'RADIOLOGY', 'ORTHOPAEDICS', 'DERMATOLOGY', 'SKIN', 'TOXICOLOGY', 'IMMUNOLOGY', 'ENDOCRINOLOGY'
}
SUBJECT_CANON = {
    'ANATOMY': 'Anatomy', 'BIOCHEMISTRY': 'Biochemistry', 'PHYSIOLOGY': 'Physiology',
    'PATHOLOGY': 'Pathology', 'PHARMACOLOGY': 'Pharmacology', 'MICROBIOLOGY': 'Microbiology',
    'FORENSIC MEDICINE': 'Forensic Medicine', 'COMMUNITY MEDICINE': 'PSM', 'PSM': 'PSM',
    'ENT': 'ENT', 'OPHTHALMOLOGY': 'Ophthalmology', 'MEDICINE': 'Medicine', 'SURGERY': 'Surgery',
    'OBG': 'OBG', 'OBSTETRICS': 'OBG', 'GYNAECOLOGY': 'OBG', 'PAEDIATRICS': 'Paediatrics',
    'PSYCHIATRY': 'Psychiatry', 'ANAESTHESIOLOGY': 'Anaesthesia', 'ANAESTHESIA': 'Anaesthesia',
    'RADIOLOGY': 'Radiology', 'ORTHOPAEDICS': 'Orthopaedics', 'DERMATOLOGY': 'Dermatology',
    'SKIN': 'Dermatology', 'TOXICOLOGY': 'Forensic Medicine', 'IMMUNOLOGY': 'Pathology',
    'ENDOCRINOLOGY': 'Medicine'
}

all_qs = []

def parse_year(y):
    a, b = bounds[y]
    body = '\n'.join(pages[a:b])
    if y != 2018:
        nx = doc_order[doc_order.index(y) + 1]
        cut = body.find(f'EXAMINATION PAPER {nx}')
        if cut != -1:
            body = body[:cut]
    body = re.sub(r'^\s*(?:PAGE\s+\d+|MEDINK|NEET\s+PG)\s*\n', '', body, flags=re.M)
    blocks = {}
    order = []
    cur = None
    for ln in body.split('\n'):
        s = ln.strip()
        if len(s) <= 40 and s.upper() in SUBJ_SET:
            key = s.upper()
            if key not in blocks:
                blocks[key] = []
                order.append(key)
            cur = key
            continue
        if cur is not None:
            blocks[cur].append(ln)

    for subj in order:
        text = '\n'.join(blocks[subj])
        if not text.strip():
            continue
        chunks = re.split(r'(?=^\s*\d{1,3}\.\s)', text, flags=re.M)
        for ch in chunks:
            mo = re.match(r'\s*(\d{1,3})\.\s*(.*)', ch, re.S)
            if not mo:
                continue
            qnum = int(mo.group(1))
            rest = mo.group(2)
            mopt = re.search(
                r'\(A\)\s*(.*?)\s*\(B\)\s*(.*?)\s*\(C\)\s*(.*?)\s*\(D\)\s*(.*?)\s*Ans\s*:\s*\(([A-D])\)\s*(.*)$',
                rest, re.S)
            if not mopt:
                continue
            oA, oB, oC, oD, ans, exp = mopt.groups()
            idx = {'A': 0, 'B': 1, 'C': 2, 'D': 3}[ans]
            stem = rest[:rest.index('(A)')]
            all_qs.append(dict(
                year=y, subj=SUBJECT_CANON.get(subj, subj.title()), n=qnum,
                q=' '.join(stem.split()),
                o=[' '.join(x.split()) for x in (oA, oB, oC, oD)],
                a=idx, ex=' '.join(exp.split())
            ))

for y in doc_order:
    before = len(all_qs)
    parse_year(y)
    print(y, 'parsed', len(all_qs) - before)
print('TOTAL', len(all_qs))
with io.open('research/_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(all_qs, f, ensure_ascii=False, indent=1)