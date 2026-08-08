# -*- coding: utf-8 -*-
# Extract embedded images from INI-CET Yearwise PDF, associate with question
# numbers via nearest-preceding marker, then fuzzy-match to bank.js entries.
import io, re, json, hashlib, base64, difflib
import fitz

PDF = r'C:\Users\navne\Downloads\INICET-Yearwise.pdf'
RANGES = {
 'MAY 2025': (7, 81), 'MAY 2024': (81, 152), 'NOV 2024': (152, 225),
 'MAY 2023': (225, 296), 'NOV 2023': (296, 368), 'MAY 2022': (368, 449),
 'NOV 2022': (449, 527), 'MAY 2021': (527, 605), 'NOV 2021': (605, 684),
 'NOV 2020': (684, 754)}
QRE = re.compile(r'^(\d{1,3})\.\s*')

doc = fitz.open(PDF)

def norm(s):
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()

def page_questions(pn):
    """Return ordered list of (qnum, stem_text, img_xrefs) for a page."""
    page = doc[pn]
    words = page.get_text('words')
    marks = []
    for w in words:
        m = QRE.match(w[4])
        if m and w[1] < 200:
            marks.append((int(m.group(1)), w[1], w[0]))
    marks.sort(key=lambda m: (m[1], m[2]))
    # image rects
    imgrects = []
    for im in page.get_images(full=True):
        xref = im[0]
        for r in page.get_image_rects(xref):
            imgrects.append((r.y0, r.y1, xref))
    # text blocks (excluding header/footer, answer blocks)
    blocks = []
    for b in page.get_text('blocks'):
        x0, y0, x1, y1, txt = b[0], b[1], b[2], b[3], b[4]
        if y1 < 60 or y0 > 780:
            continue
        t = re.sub(r'[\x00-\x1f]', '', txt)
        if 'AAns' in t or 'MEDINK' in t or 'INICET Examination' in t or 'page  ' in t[:20]:
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
        imgs = [x for (iy0, iy1, x) in imgrects if iy0 >= y0 - 4 and iy0 < nxt_y]
        if imgs or text.strip():
            out.append((qnum, text.strip(), sorted(set(imgs))))
    return out

# 1) collect per-year question text + images
per_year = {}
for year, (a, b) in RANGES.items():
    qs = {}
    for pn in range(a, min(b, len(doc))):
        for qnum, text, imgs in page_questions(pn):
            # append text across page breaks
            if qnum in qs:
                qs[qnum] = (qs[qnum][0] + ' ' + text, qs[qnum][1] | set(imgs))
            else:
                qs[qnum] = (text, set(imgs))
    per_year[year] = qs

# 2) extract image bytes (downscaled, compressed), dedupe by hash
imgcache = {}
def img_data(xref):
    if xref in imgcache:
        return imgcache[xref]
    try:
        pix = fitz.Pixmap(doc, xref)
        if pix.n - pix.alpha > 3:  # CMYK
            pix = fitz.Pixmap(fitz.csRGB, pix)
        # downscale: max dimension ~360px
        maxdim = max(pix.width, pix.height)
        if maxdim > 360:
            scale = 360 / maxdim
            pix = fitz.Pixmap(pix, int(pix.width * scale + .5), int(pix.height * scale + .5))
        # JPEG compression (quality 70); keep PNG only if image has alpha/small
        has_alpha = pix.alpha > 0
        if has_alpha:
            data = base64.b64encode(pix.tobytes('png')).decode()
        else:
            data = base64.b64encode(pix.tobytes('jpeg', jpg_quality=70)).decode()
        imgcache[xref] = data
        return data
    except Exception:
        return None

# 3) load bank
src = io.open('questions/bank.js', encoding='utf-8').read()
bank = json.loads(re.search(r'window\.QUESTIONS\s*=\s*(\[.*\])\s*;', src, re.S).group(1))

def find_bank(qtext, year):
    nq = norm(qtext)
    if not nq:
        return None
    cands = [q for q in bank if q.get('e') == 'INI-CET' and q.get('y') == year]
    if not cands:
        return None
    best, br = None, 0.0
    for q in cands:
        nb = norm(q['q'])
        if not nb:
            continue
        r = difflib.SequenceMatcher(None, nq[:120], nb[:120]).ratio()
        if r > br:
            br, best = r, q
    return best if br > 0.35 else None

# 4) attach images
matched, unmatched = 0, 0
for year, qs in per_year.items():
    for qnum, (text, xrefs) in qs.items():
        if not xrefs:
            continue
        q = find_bank(text, year)
        if q is None:
            unmatched += 1
            continue
        datas = [img_data(x) for x in xrefs if img_data(x)]
        if not datas:
            unmatched += 1
            continue
        q['imgdata'] = datas  # base64 PNG array
        q['img'] = True
        matched += 1

print('matched:', matched, 'unmatched:', unmatched)

# 4.5) drop stale img flags without data
for q in bank:
    if q.get('img') and not q.get('imgdata'):
        q['img'] = False

# 5) save back to bank.js
out = []
out.append("// NEET PG / INI-CET practice bank — reconstructed from curated + deep-research expansions.")
out.append("// Sources tagged per-item: src=\"curated\" (hand-picked PYQs), \"expand\" (workflow-generated recall Qs),")
out.append("// \"medink\" (parsed from user-provided compiled PYQ PDF). Personal offline practice use only.")
out.append("window.QUESTIONS = ")
out.append(json.dumps(bank, ensure_ascii=False, indent=0))
out.append(';\n')
io.open('questions/bank.js', 'w', encoding='utf-8').write('\n'.join(out))
print('wrote questions/bank.js, total', len(bank))
io.open('research/_img_match_report.json', 'w', encoding='utf-8').write(
    json.dumps({y: {str(qn): (t[:60], list(xs)) for qn, (t, xs) in qs.items() if xs}
                for y, qs in per_year.items()}, ensure_ascii=False, indent=1))
