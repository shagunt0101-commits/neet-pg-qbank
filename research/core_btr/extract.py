# -*- coding: utf-8 -*-
"""Core Btr Complete PYQ Book — full extraction.
Vol A (Part A): questions. Vol B (Part B): reprint + Correct Answer + Explanation.
Index (Quick Jump) pages give exact Q -> answer page mapping.
Outputs questions.json with {subj, topic, q, o[4], a, ex, qid, src, img, imgdata}.
"""
import fitz, re, io, os, json
from collections import OrderedDict

PDF = r'C:\Users\navne\Downloads\Mobile Devices\Core Btr Complete PYQ Book.pdf'
OUT = os.path.join(os.path.dirname(__file__), 'questions.json')

doc = fitz.open(PDF)
toc = doc.get_toc()
partA_start = 33
partB_start = next(t[2] for t in toc if 'Part B' in t[1])

def sec_label(name):
    n = re.sub(r'^[•»\s]+', '', name.strip())
    m = re.match(r'\[(\w[\w &-]*?)\]\s*(\d+)-(.*)', n)
    if m:
        return m.group(1).strip(), m.group(3).strip()
    m2 = re.match(r'\[(\w[\w &-]*?)\]\s*(.*)', n)
    if m2:
        return m2.group(1).strip(), m2.group(2).strip()
    return n.strip(), ''

# Part A sections: index page at t[2]-1 (holds Q1 content), content pages follow.
# Range = [t[2]-1, next_t[2]-1) so each section includes its own index page
# and excludes the next section's index page.
pa = [t for t in toc if t[0] == 2 and partA_start <= t[2] < partB_start]
sections = []
for i, t in enumerate(pa):
    subj, topic = sec_label(t[1])
    start = t[2] - 1
    end = (pa[i + 1][2] - 1) if i + 1 < len(pa) else partB_start - 1
    sections.append(dict(subj=subj, topic=topic, start=start, end=end, name=t[1]))

# Part B sections: index page at t[2]-1 (holds Q1 content), content pages follow.
pb_entries = [t for t in toc if t[0] == 2 and t[2] >= partB_start]
b_sections = []
for i, t in enumerate(pb_entries):
    subj, topic = sec_label(t[1])
    start = t[2] - 1
    end = (pb_entries[i + 1][2] - 1) if i + 1 < len(pb_entries) else doc.page_count
    b_sections.append(dict(subj=subj, topic=topic, start=start, end=end, name=t[1]))
print('Part B sections:', len(b_sections))

# ---------- Part A questions ----------
QSTART = re.compile(r'^Q(\d+):\s*(.*)$')

def extract_partA():
    out = []
    for sec in sections:
        cur = None
        for pno in range(sec['start'], sec['end']):
            txt = doc[pno].get_text()
            # image rects on this page, sorted by y (top of image)
            try:
                pimgs = doc[pno].get_image_info()
            except Exception:
                pimgs = []
            for ln in txt.split('\n'):
                s = ln.rstrip()
                if not s.strip():
                    continue
                m = QSTART.match(s)
                if m:
                    if cur is not None:
                        out.append(cur)
                    cur = dict(subj=sec['subj'], topic=sec['topic'],
                                num=int(m.group(1)), stem=m.group(2).strip(), opts=[],
                                page=pno, img=0)
                elif cur is not None:
                    if re.match(r'^\s*[A-D][\s.\t]', s) and len(cur['opts']) < 4:
                        cur['opts'].append(re.sub(r'^\s*[A-D][\s.\t]*', '', s).strip())
                    else:
                        cur['stem'] += ' ' + s.strip()
        if cur is not None:
            out.append(cur)
    return out

QJ = re.compile(r'^Q(\d+)\s*\(p\.\s*(\d+)\)$')
BQSTART = re.compile(r'^Q(\d+):\s*(.*)$')
BANS = re.compile(r'^Correct Answer:\s*([A-D])[.\s]\s*(.*)$')
BEXP = re.compile(r'^Explanation:\s*(.*)$')

def parse_b_section(sec):
    """Parse one Part B section sequentially. Returns {num: q}.
    Sequential walk from sec['start'] to sec['end'] (which excludes the next
    section's index page), tracking current Q across page breaks.
    """
    cur = None
    out = {}
    for pno in range(sec['start'], sec['end']):
        for s0 in doc[pno].get_text().split('\n'):
            s = s0.strip()
            if not s:
                continue
            m = BQSTART.match(s)
            if m:
                if cur is not None:
                    out[cur['num']] = cur
                num = int(m.group(1))
                cur = dict(subj=sec['subj'], topic=sec['topic'], num=num,
                            stem=m.group(2), opts=[], ans=None, ans_txt='', ex='', page=pno)
                continue
            if cur is None:
                continue
            if re.match(r'^[A-D][\s.\t]', s) and len(cur['opts']) < 4:
                cur['opts'].append(re.sub(r'^\s*[A-D][\s.\t]*', '', s).strip())
                continue
            if 'Back to this question' in s or s == '@Neet_pg_bot':
                continue
            if BANS.match(s) and cur['ans'] is None:
                m2 = BANS.match(s)
                cur['ans'] = ord(m2.group(1)) - ord('A')
                cur['ans_txt'] = m2.group(2)
                continue
            if BEXP.match(s) and not cur['ex']:
                cur['ex'] = BEXP.match(s).group(1)
                continue
            if cur['ex']:
                cur['ex'] += '\n' + s
    if cur is not None:
        out[cur['num']] = cur
    return out

def extract_partB():
    allb = {}
    for sec in b_sections:
        qs = parse_b_section(sec)
        bad = [n for n in qs if qs[n]['ans'] is None]
        if bad:
            print('  ', sec['name'], '| parsed', len(qs), '| no-ans:', bad[:8])
        for n, q in qs.items():
            q['sec_name'] = sec['name']
            allb[(sec['name'], n)] = q
    return allb

qs = extract_partA()
print('Part A parsed:', len(qs))
pb = extract_partB()
print('Part B parsed:', len(pb))

json.dump(dict(questions=qs, answers=[pb[k] for k in sorted(pb, key=lambda x: (x[0], x[1]))]),
          io.open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved', OUT, '| Part A:', len(qs), '| Part B:', len(pb))
