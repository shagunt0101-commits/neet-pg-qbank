# -*- coding: utf-8 -*-
"""Rebuild bank.js from corrected INI-CET final JSON.
Updates subject tags for existing INI-CET entries while preserving any embedded image data.
Adds any missing entries from final JSON.
"""
import io, json, difflib, re, sys

BANK_PATH = 'questions/bank.js'
FINAL_PATH = 'research/_inicet_final.json'

def load_bank():
    src = io.open(BANK_PATH, encoding='utf-8').read()
    # extract JSON array from window.QUESTIONS assignment
    m = re.search(r'window\.QUESTIONS\s*=\s*(\[.*\])\s*;', src, re.S)
    if not m:
        print('Failed to parse bank.js', file=sys.stderr)
        sys.exit(1)
    return json.loads(m.group(1))

def save_bank(bank):
    out = []
    out.append('// NEET PG / INI-CET practice bank — reconstructed from curated + deep-research expansions.')
    out.append('// Sources tagged per-item: src="curated" (hand-picked PYQs), "expand" (workflow-generated recall Qs),')
    out.append('// "medink" (parsed from user-provided compiled PYQ PDF). Personal offline practice use only.')
    out.append('window.QUESTIONS = ')
    out.append(json.dumps(bank, ensure_ascii=False, indent=0))
    out.append('\n;')
    io.open(BANK_PATH, 'w', encoding='utf-8').write('\n'.join(out))
    print('wrote', BANK_PATH, 'entries', len(bank))

def norm(s):
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()

def find_best_match(qtext, candidates):
    nq = norm(qtext)[:160]
    best = None
    best_score = 0.0
    for cand in candidates:
        nb = norm(cand['q'])[:160]
        if not nb:
            continue
        score = difflib.SequenceMatcher(None, nq, nb).ratio()
        if score > best_score:
            best_score = score
            best = cand
    return best, best_score

def main():
    bank = load_bank()
    final = json.load(io.open(FINAL_PATH, encoding='utf-8'))
    # Index old INI-CET entries
    inicet_entries = [q for q in bank if q.get('e') == 'INI-CET']
    updated = 0
    added = 0
    for fq in final:
        # find best match among existing INI-CET entries
        match, score = find_best_match(fq['q'], inicet_entries)
        if match and score >= 0.5:
            # replace subject if differs
            if match.get('s') != fq.get('s'):
                match['s'] = fq['s']
                updated += 1
        else:
            # no match, add as new entry (no imgdata)
            # ensure required fields present
            new_entry = {
                'q': fq['q'],
                'o': fq['o'],
                'a': fq['a'],
                'ex': fq.get('ex',''),
                'e': fq['e'],
                'y': fq['y'],
                's': fq['s'],
                'img': fq.get('img', False)
            }
            # imgdata maybe missing; keep as is
            bank.append(new_entry)
            added += 1
    print(f'Updated subjects: {updated}, added entries: {added}')
    save_bank(bank)

if __name__ == '__main__':
    main()
