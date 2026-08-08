# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
b = json.load(open(r'F:\NEET PG\research\orig_bank.json', encoding='utf-8'))
byid = {q['qid']: q for q in b}
q = byid['q334']
print('img field:', q['img'], type(q['img']))
im = q.get('imgdata')
print('imgdata type:', type(im))
if isinstance(im, list):
    print('imgdata len:', len(im), 'first entry type:', type(im[0]))
    print('first 80 chars:', str(im[0])[:80])
elif im:
    print('imgdata 80 chars:', str(im)[:80])
else:
    print('no imgdata')
# count total images in bank
tot = 0
nq = 0
for qq in b:
    if qq.get('img'):
        nq += 1
        im2 = qq.get('imgdata')
        tot += len(im2) if isinstance(im2, list) else (1 if im2 else 0)
print('img qs:', nq, 'total images:', tot)
