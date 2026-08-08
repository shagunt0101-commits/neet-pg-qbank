# -*- coding: utf-8 -*-
# Extract embedded images from NEET PG Yearwise PDF, associate with questions
# by nearest-preceding marker, fuzzy-match to bank.js NEET entries.
import io, re, json, base64, difflib
import fitz

PDF = r'C:\Users\navne\Downloads\NEETPG-Yearwise.pdf'
PAPERS = {  # year -> (paper_start, paper_end_exclusive)
 '2025': (6, 33), '2024': (80, 139), '2023': (224, 297),
 '2022': (297, 331), '2021': (380, 406), '2020': (449, 484),
 '2019': (558, 655), '2018': (655, 684)}
QRE = re.compile(r'^(\d{1,3})\.\s*')
# bank only covers 2021-2025 NEET
TARGET = ['2025', '2024', '2023', '2022', '2021']
SUBJ_KEYS = ['ANATOMY','BIOCHEMISTRY','PHYSIOLOGY','PATHOLOGY','PHARMACOLOGY','MICROBIOLOGY',
 'FORENSIC MEDICINE','FORENSIC','PSM','COMMUNITY','ENT','OPHTHALMOLOGY','MEDICINE','SURGERY',
 'OBS & GYNE','OBSTETRICS','PEDIATRICS','PAEDIATRICS','PSYCHIATRY','ANAESTHESIA','ANESTHESIA',
 'RADIOLOGY','ORTHOPEDICS','ORTHOPAEDICS','DERMATOLOGY']

def page_subject(pn):
    """Subject section header on page (first match), normalized."""
    for b in doc[pn].get_text('blocks'):
        t = re.sub(r'[\x00-\x1f]', '', b[4]).strip().upper()
        for s in SUBJ_KEYS:
            if t == s or t.startswith(s + ' '):
                return s
    return None

doc = fitz.open(PDF)

def norm(s):
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()

def page_questions(pn):
    page = doc[pn]
    words = page.get_text('words')
    marks = []
    for w in words:
        m = QRE.match(w[4])
        if m and w[1] < 180:
            marks.append((int(m.group(1)), w[1], w[0]))
    marks.sort(key=lambda m: (m[1], m[2]))
    imgrects = []
    for im in page.get_images(full=True):
        xref = im[0]
        for r in page.get_image_rects(xref):
            imgrects.append((r.y0, r.y1, xref))
    blocks = []
    for b in page.get_text('blocks'):
        x0, y0, x1, y1, txt = b[0], b[1], b[2], b[3], b[4]
        if y1 < 60 or y0 > 780:
            continue
        t = re.sub(r'[\x00-\x1f]', '', txt)
        if 'MEDINK' in t or 'PAGE' in t[:20]:
            continue
        blocks.append((y0, y1, t))
    blocks.sort(key=lambda b: b[0])
    out = []
    for i, (qnum, y0, x0) in enumerate(marks):
        nxt_y = marks[i+1][1] if i+1 < len(marks) else 1e9
        stem = []
        for (by0, by1, bt) in blocks:
            if by0 >= y0 - 2 and by1 <= nxt_y + 2:
                stem.append(bt)
        text = ' '.join(stem)
        # strip 'Ans : ...' trailing (answer text in same block)
        text = re.split(r'\s*Ans\s*:', text, maxsplit=1)[0]
        imgs = [x for (iy0, iy1, x) in imgrects if iy0 >= y0 - 4 and iy0 < nxt_y]
        if imgs or text.strip():
            out.append((qnum, text.strip(), sorted(set(imgs))))
    return out

per_year = {}
for year, (a, b) in PAPERS.items():
    if year not in TARGET:
        continue
    qs = {}
    cur_subj = None
    for pn in range(a, b):
        s = page_subject(pn)
        if s:
            cur_subj = s
        for qnum, text, imgs in page_questions(pn):
            if qnum in qs:
                qs[qnum] = (qs[qnum][0] + ' ' + text, qs[qnum][1] | set(imgs), qs[qnum][2] or cur_subj)
            else:
                qs[qnum] = (text, set(imgs), cur_subj)
    per_year[year] = qs

imgcache = {}
def img_data(xref):
    if xref in imgcache:
        return imgcache[xref]
    try:
        pix = fitz.Pixmap(doc, xref)
        if pix.n - pix.alpha > 3:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        maxdim = max(pix.width, pix.height)
        if maxdim > 360:
            scale = 360 / maxdim
            pix = fitz.Pixmap(pix, int(pix.width * scale + .5), int(pix.height * scale + .5))
        if pix.alpha > 0:
            data = base64.b64encode(pix.tobytes('png')).decode()
        else:
            data = base64.b64encode(pix.tobytes('jpeg', jpg_quality=70)).decode()
        imgcache[xref] = data
        return data
    except Exception:
        return None

src = io.open('questions/bank.js', encoding='utf-8').read()
bank = json.loads(re.search(r'window\.QUESTIONS\s*=\s*(\[.*\])\s*;', src, re.S).group(1))
# clean slate: drop all NEET img flags (stale loose matches)
for q in bank:
    if q.get('e') == 'NEET PG':
        q.pop('imgdata', None)
        q['img'] = False

# subject name mapping PDF->bank
SUBJ_MAP = {
 'FORENSIC MEDICINE': 'Forensic Medicine', 'FORENSIC': 'Forensic Medicine',
 'PSM': 'PSM', 'COMMUNITY': 'PSM',
 'OBS & GYNE': 'OBG', 'OBSTETRICS': 'OBG',
 'PEDIATRICS': 'Paediatrics', 'PAEDIATRICS': 'Paediatrics',
 'ANESTHESIA': 'Anaesthesia', 'ANAESTHESIA': 'Anaesthesia',
 'ORTHOPEDICS': 'Orthopaedics', 'ORTHOPAEDICS': 'Orthopaedics',
}
for s in ['ANATOMY','BIOCHEMISTRY','PHYSIOLOGY','PATHOLOGY','PHARMACOLOGY','MICROBIOLOGY',
          'ENT','OPHTHALMOLOGY','MEDICINE','SURGERY','PSYCHIATRY','RADIOLOGY','DERMATOLOGY']:
    SUBJ_MAP[s] = s.title()

def tok_set(s):
    return set(norm(s).split())

def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def find_bank(qtext, year, subj):
    nq = norm(qtext)
    if len(nq) < 25:
        return None
    cands = [q for q in bank if q.get('e') == 'NEET PG' and str(q.get('y')) == year]
    if not cands:
        return None
    best, br = None, 0.0
    for q in cands:
        nb = norm(q['q'])
        if len(nb) < 10:
            continue
        r = difflib.SequenceMatcher(None, nq[:160], nb[:160]).ratio()
        # subject bonus: PDF subject == bank subject nudges confidence
        if q.get('s') == SUBJ_MAP.get(subj, subj):
            r += 0.03
        if r > br:
            br, best = r, q
    return best if br >= 0.5 else None

matched, unmatched = 0, 0
report = {}
for year, qs in per_year.items():
    for qnum, (text, xrefs, subj) in qs.items():
        if not xrefs:
            continue
        q = find_bank(text, year, subj)
        report.setdefault(year, {})[str(qnum)] = (text[:80], list(xrefs))
        if q is None:
            unmatched += 1
            continue
        datas = [img_data(x) for x in xrefs if img_data(x)]
        if not datas:
            unmatched += 1
            continue
        q['imgdata'] = datas
        q['img'] = True
        matched += 1

print('matched:', matched, 'unmatched:', unmatched)
io.open('research/_neet_img_report.json', 'w', encoding='utf-8').write(
    json.dumps(report, ensure_ascii=False, indent=1))

for q in bank:
    if q.get('img') and not q.get('imgdata'):
        q['img'] = False

out = []
out.append("// NEET PG / INI-CET practice bank — reconstructed from curated + deep-research expansions.")
out.append("// Sources tagged per-item: src=\"curated\" (hand-picked PYQs), \"expand\" (workflow-generated recall Qs),")
out.append("// \"medink\" (parsed from user-provided compiled PYQ PDF). Personal offline practice use only.")
out.append("window.QUESTIONS = ")
out.append(json.dumps(bank, ensure_ascii=False, indent=0))
out.append(';\n')
io.open('questions/bank.js', 'w', encoding='utf-8').write('\n'.join(out))
print('wrote questions/bank.js, total', len(bank))
