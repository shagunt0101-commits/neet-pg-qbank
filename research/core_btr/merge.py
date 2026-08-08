# -*- coding: utf-8 -*-
"""Merge Part A (questions) with Part B (answers) from extract output.
Match key: (section name, Q num). Produces final questions.json:
{subj, topic, q, o[4], a, ex, num, src}
"""
import json, io, re, os, sys
def clean_q(txt):
    t = ' '.join(txt.split())
    t = re.sub(r'\s*See Answer in Part B → Q\d+\s*@Neet_pg_bot\s*$', '', t)
    t = re.sub(r'\s*See Answer in Part B → Q\d+\s*$', '', t)
    t = re.sub(r'\s*@Neet_pg_bot\s*$', '', t)
    # strip stray Quick Jump index lines absorbed into a stem
    t = re.sub(r'\s*Q\d+\s*\(p\.\s*\d+\)(?:\s*Q\d+\s*\(p\.\s*\d+\))*\s*$', '', t)
    return t

BASE = os.path.dirname(__file__)
data = json.load(io.open(os.path.join(BASE, 'questions.json'), encoding='utf-8'))
qs = data['questions']
ans = data['answers']
print('Part A questions:', len(qs))
print('Part B answers:', len(ans))

# B answers keyed by (sec_name, num) — already in data
b_by_key = {}
for a in ans:
    b_by_key[(a['sec_name'], a['num'])] = a

# Part A: we didn't store sec_name; sections list needed. Rebuild from TOC.
import fitz
doc = fitz.open(r'C:\Users\navne\Downloads\Mobile Devices\Core Btr Complete PYQ Book.pdf')
toc = doc.get_toc()
partB_start = next(t[2] for t in toc if 'Part B' in t[1])
pa = [t for t in toc if t[0] == 2 and 33 <= t[2] < partB_start]
sec_names = [t[1] for t in pa]

# Assign sec_name to each Part A question by its page (section start..end).
# Each section includes its index page (t[2]-1) and excludes the next index page.
sec_bounds = []
for i, t in enumerate(pa):
    start = t[2] - 1
    end = (pa[i + 1][2] - 1) if i + 1 < len(pa) else partB_start
    sec_bounds.append((t[1], start, end))

def sec_for_page(p):
    for name, s, e in sec_bounds:
        if s <= p < e:
            return name
    return None

matched = 0
no_b = 0
dup = 0
out = []
for q in qs:
    sn = sec_for_page(q['page'])
    if sn is None:
        print('NO SECTION for page', q['page'], q['num'])
        continue
    a = b_by_key.get((sn, q['num']))
    if a is None:
        no_b += 1
        out.append(dict(subj=q['subj'], topic=q['topic'], num=q['num'],
                        q=clean_q(q['stem']), o=q['opts'],
                        a=None, ex='', sec=sn, src='core_btr', page=q['page']))
        continue
    matched += 1
    out.append(dict(subj=q['subj'], topic=q['topic'], num=q['num'],
                    q=clean_q(q['stem']), o=q['opts'],
                    a=a['ans'], ex=' '.join(a['ex'].split()),
                    sec=sn, src='core_btr', page=q['page']))

print('matched:', matched, '| Part A w/o Part B:', no_b, '| total:', len(out))
# save merged
final = []
for i, x in enumerate(out):
    final.append(dict(x, qid='cb%d' % i))
json.dump(final, io.open(os.path.join(BASE, 'merged.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved merged.json', len(final))
