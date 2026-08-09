# -*- coding: utf-8 -*-
"""Detect stems (q) that embed the option list (letter-prefixed blocks)."""
import io, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

def load(p):
    d = io.open(p, 'r', encoding='utf-8', errors='replace').read()
    s = d.find('['); e = d.rfind('];')
    return json.loads(d[s:e+1])

def esc(t):
    return re.escape(t)

LETTERS = 'ABCD'

def find_letter_block(stem, opts):
    """Return (marker, start, end) if stem contains letter-prefixed block of all options in order."""
    best = None
    for marker in ['.', ')', '-', ':']:
        # build pattern: A<marker> opt0 ... B<marker> opt1 ... C<marker> opt2 ... D<marker> opt3
        pat = ''
        for i, o in enumerate(opts):
            pat += LETTERS[i] + re.escape(marker) + r'\s*' + esc(o) + r'\s*'
        m = re.search(pat, stem)
        if m:
            # prefer the marker style that matches
            return (marker, m.start(), m.end())
    return None

out = []
for f in [r'questions\core_btr.js', r'questions\bank.js', r'questions\test_2026.js']:
    data = load(f)
    print('=====', f, len(data))
    for q in data:
        stem = q.get('q', ''); opts = q.get('o', [])
        if not stem or not opts or len(opts) < 2: continue
        r = find_letter_block(stem, opts)
        if r:
            marker, s, e = r
            print('BUG?', q.get('qid'), '|', q.get('subj'), '| marker', repr(marker))
            print('   stem:', stem[:150])
            print('   o0  :', opts[0][:80])
            print('   a   :', q.get('a'))
            out.append((f, q.get('qid')))
    print()
print('total bugs:', len(out), out)
