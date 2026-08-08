# -*- coding: utf-8 -*-
"""Efficient rebuild of bank.js correcting INI-CET subjects.
Preserves existing imgdata for matched entries.
Adds missing entries without imgdata.
"""
import io, json, re, sys

BANK_PATH = 'questions/bank.js'
FINAL_PATH = 'research/_inicet_final.json'

def load_bank():
    src = io.open(BANK_PATH, encoding='utf-8').read()
    m = re.search(r'window\.QUESTIONS\s*=\s*(\[.*\])\s*;', src, re.S)
    if not m:
        print('Cannot parse bank.js', file=sys.stderr)
        sys.exit(1)
    return json.loads(m.group(1))

def save_bank(bank):
    out = []
    out.append('// NEET PG / INI-CET practice bank — reconstructed from curated + deep-research expansions.')
    out.append('// Sources tagged per-item: src="curated", "expand", "medink".')
    out.append('window.QUESTIONS = ')
    out.append(json.dumps(bank, ensure_ascii=False, indent=0))
    out.append('\n;')
    io.open(BANK_PATH, 'w', encoding='utf-8').write('\n'.join(out))
    print('Bank rewritten, total', len(bank))

def norm(s):
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()

def key_for(q):
    return norm(q.get('q',''))

def main():
    bank = load_bank()
    final = json.load(io.open(FINAL_PATH, encoding='utf-8'))
    # map existing INI-CET entries by normalized stem
    existing = {key_for(q): q for q in bank if q.get('e') == 'INI-CET'}
    updated = 0
    added = 0
    for fq in final:
        k = key_for(fq)
        if not k:
            continue
        if k in existing:
            ent = existing[k]
            if ent.get('s') != fq.get('s'):
                ent['s'] = fq['s']
                updated += 1
            # keep existing imgdata/img flag untouched
        else:
            # new entry – no imgdata, preserve img flag if present
            new = {
                'q': fq['q'],
                'o': fq['o'],
                'a': fq['a'],
                'ex': fq.get('ex',''),
                'e': fq['e'],
                'y': fq['y'],
                's': fq['s'],
                'img': fq.get('img', False)
            }
            # if final had imgdata (unlikely), ignore – will be added later via image scripts
            bank.append(new)
            added += 1
    print(f'Updated subjects {updated}, added {added}')
    save_bank(bank)

if __name__ == '__main__':
    main()
