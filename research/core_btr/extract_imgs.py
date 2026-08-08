# -*- coding: utf-8 -*-
"""Map PDF images to questions via block positions, embed as base64 imgdata.
Strategy: for each question page, get text dict blocks; find Q headers (y-order);
find image blocks (via get_image_rects per xref); assign each image to the
question whose header is the nearest above it (or first Q on page if none above).
Images may be wrapped in Form XObjects; get_image_rects maps the placement rect.
"""
import fitz, re, json, io, os, base64
from collections import OrderedDict

PDF = r'C:\Users\navne\Downloads\Mobile Devices\Core Btr Complete PYQ Book.pdf'
BASE = os.path.dirname(__file__)
doc = fitz.open(PDF)

merged = json.load(io.open(os.path.join(BASE, 'merged.json'), encoding='utf-8'))

QHDR = re.compile(r'^Q(\d+):')
img_count = 0

# group questions by page
by_page = OrderedDict()
for q in merged:
    by_page.setdefault(q['page'], []).append(q)

def prev_page_qs(pno):
    """Last question on previous page — owner of figures that drift to top of next page."""
    prev = by_page.get(pno - 1)
    return prev[-1] if prev else None

for pno, qs in by_page.items():
    try:
        blocks = doc[pno].get_text('dict')['blocks']
    except Exception:
        continue
    # Q header y positions
    q_headers = []  # (y_top, num)
    for b in blocks:
        if b['type'] != 0:
            continue
        for ln in b['lines']:
            text = ''.join(sp['text'] for sp in ln['spans']).strip()
            m = QHDR.match(text)
            if m:
                q_headers.append((b['bbox'][1], int(m.group(1))))
    q_headers.sort()
    if not q_headers:
        continue
    # image placement rects per xref
    img_blocks = []  # (y_top, xref)
    try:
        seen = set()
        for im in doc[pno].get_images(full=True):
            xref = im[0]
            if xref in seen:
                continue
            seen.add(xref)
            try:
                for r in doc[pno].get_image_rects(xref):
                    img_blocks.append((r.y0, xref))
            except Exception:
                pass
    except Exception:
        pass
    img_blocks.sort()
    if not img_blocks:
        continue
    # assign each image: to last Q header above it; if none above, last Q on previous page
    # (figures drift to top of the page following their question's stem); else first Q on page
    for y_img, xref in img_blocks:
        owner = None
        for y_h, num in q_headers:
            if y_h <= y_img + 1:
                owner = num
            else:
                break
        if owner is None:
            target = prev_page_qs(pno)
            if target is None:
                target = qs[0]
        else:
            target = next((q for q in qs if q['num'] == owner), None)
        if target is None:
            continue
        try:
            info = doc.extract_image(xref)
        except Exception:
            continue
        target.setdefault('imgdata', []).append(info['image'])
        target['img'] = True
        img_count += 1

out = []
for q in merged:
    if q.get('imgdata'):
        q['imgdata'] = [base64.b64encode(b).decode('ascii') for b in q['imgdata']]
    out.append(q)

json.dump(out, io.open(os.path.join(BASE, 'with_imgs.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
io.open(os.path.join(BASE, '..', '..', 'questions', 'core_btr.js'), 'w', encoding='utf-8').write('window.CORE_BTR = ' + json.dumps(out, ensure_ascii=False, indent=1) + ';\n')
print('questions:', len(out), '| with images:', sum(1 for q in out if q.get('img')), '| total imgs:', img_count)
