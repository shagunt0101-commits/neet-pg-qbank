# -*- coding: utf-8 -*-
import io, re, json

txt = io.open('research/inicet-yearwise.txt', encoding='utf-8').read()
pages = txt.split('===PAGE ')

SUBJ_KEYS = ['ANATOMY','BIOCHEMISTRY','PHYSIOLOGY','PATHOLOGY','PHARMACOLOGY','MICROBIOLOGY',
 'FORENSIC MEDICINE','PSM','COMMUNITY','ENT','OPHTHALMOLOGY','MEDICINE','SURGERY',
 'OBS & GYNE','OBG','PAEDIATRICS','PEDIATRICS','PSYCHIATRY','ANAESTHESIA','RADIOLOGY',
 'ORTHOPEDICS','ORTHOPAEDICS','DERMATOLOGY']
HDR = set(SUBJ_KEYS)

# contiguous page ranges per paper (paper + solution; we dedupe later)
RANGES = {
 'MAY 2025': (7, 81), 'MAY 2024': (81, 152), 'NOV 2024': (152, 225),
 'MAY 2023': (225, 296), 'NOV 2023': (296, 368), 'MAY 2022': (368, 449),
 'NOV 2022': (449, 527), 'MAY 2021': (527, 605), 'NOV 2021': (605, 684),
 'NOV 2020': (684, 754)}

def parse_lines(lines):
    qs = []
    subj = None
    i = 0
    n = len(lines)
    while i < n:
        ln = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', lines[i]).strip()
        if 2 <= len(ln) <= 34 and ln in HDR:
            subj = ln
            i += 1
            continue
        mq = re.match(r'^(\d{1,3})\.\s*(.*)', ln, re.S)
        if mq:
            qnum = int(mq.group(1))
            stem = [mq.group(2)]
            i += 1
            while i < n and '(A)' not in lines[i]:
                s = lines[i].strip()
                if s and not re.match(r'^(\(\w\)|AANS)', s):
                    stem.append(s)
                i += 1
            opts = []
            while i < n:
                s = lines[i].strip()
                mo = re.match(r'^\(([A-D])\)\s*([^\n]*)', s)
                if mo:
                    opts.append([mo.group(1), mo.group(2)])
                    i += 1
                    while i < n:
                        s4 = lines[i].strip()
                        if not s4 or re.match(r'^\(([A-D])\)\s*', s4) or s4.upper().startswith('AANS') or re.match(r'^\d{1,3}\.\s', s4) or (2 <= len(s4) <= 34 and s4 in HDR):
                            break
                        opts[-1][1] += ' ' + s4
                        i += 1
                    continue
                if s.upper().startswith('AANS'):
                    i += 1
                    break
                i += 1
            ans = None
            while i < n:
                s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', lines[i]).strip()
                ma = re.match(r'^\(([A-D])\)\s+(.*)', s, re.S)
                if ma:
                    t2 = ma.group(2)
                    if not (len(t2) < 12 and t2.upper() in ('A','B','C','D','ANSWER')):
                        ans = ma.group(1)
                        break
                if re.match(r'^\d{1,3}\.\t', s) or (2 <= len(s) <= 34 and s in HDR):
                    break
                i += 1
            explorer_text = []
            if ans:
                i += 1
                while i < n:
                    s7 = lines[i]
                    for ch in ['\x01', '\x00', '\x02', '\x03', '\x0b', '\x0c', '\x0e', '\x0f']:
                        s7 = s7.replace(ch, '')
                    s7 = s7.strip()
                    if not s7:
                        i += 1
                        continue
                    if re.match(r'^\d{1,3}\.\t', s7) or (2 <= len(s7) <= 34 and s7 in HDR):
                        break
                    explorer_text.append(s7)
                    i += 1
            if len(opts) == 4 and ans:
                ex = ' '.join(explorer_text).strip()
                qs.append(dict(num=qnum, subj=subj,
                               stem=' '.join(stem).strip(),
                               opts=[o[1].strip() for o in opts],
                               ans=ans, ex=ex))
            continue
        i += 1
    return qs

def lines_guard(x):
    return x

all_qs = []
for lab, (a, b) in RANGES.items():
    body_lines = []
    for pg in range(a, min(b, len(pages))):
        body_lines += pages[pg].split('\n')
    qs = parse_lines(body_lines)
    # dedupe by (num, stem) keeping first (question block, not answer reprint)
    seen = set()
    uniq = []
    for q in qs:
        k = (q['num'], re.sub(r'\s+',' ',q['stem']).strip().lower()[:80])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(q)
    print(f'{lab}: raw={len(qs)} uniq={len(uniq)}')
    for q in uniq:
        q['year'] = lab
        q['exam'] = 'INI-CET'
    all_qs += uniq

io.open('research/_inicet_parsed.json','w',encoding='utf-8').write(
    json.dumps(all_qs, ensure_ascii=False, indent=1))
print('TOTAL', len(all_qs))