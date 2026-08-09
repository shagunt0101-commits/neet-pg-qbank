# -*- coding: utf-8 -*-
"""Strip PDF-extraction garbage tokens from stems/explanations."""
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
B = json.load(open(r'F:\NEET PG\research\corrected_bank.json', encoding='utf-8'))
TOKENS = [
    r'NODIA\s*\d+\s*===+\s*(?:page\s*)?\d+\s+(?:INICET|MEDINK)\s+Examination\s+Paper(?:\s+[A-Z]{3}-?\d{4})?',
    r'Downloaded\s+from\s+www\.pdf\.tube\s*\d*\s*===+\s*(?:page\s*)?\d+\s+(?:INICET|MEDINK)\s+Examination\s+Paper(?:\s+[A-Z]{3}-?\d{4})?',
    r'Click\s+Here\s+to\s+Buy\s+book\s+on\s+Amazon\s*\d*\s*===+\s*(?:page\s*)?\d+\s+(?:INICET|MEDINK)\s+Examination\s+Paper(?:\s+[A-Z]{3}-?\d{4})?',
    r'(?:INICET|MEDINK)\s+Examination\s+Paper(?:\s+[A-Z]{3}-?\d{4})?',
    r'===+\s*(?:page\s*)?\d+\s+(?:INICET|MEDINK)\s+Examination\s+Paper(?:\s+[A-Z]{3}-?\d{4})?',
    r'\bAAns\b',
    r'\bA\s*Ans\b',
]
pat = re.compile('|'.join(TOKENS), re.I)
n = 0
for q in B:
    changed = False
    for field in ('q', 'ex'):
        v = q.get(field) or ''
        v2 = pat.sub('', v)
        # collapse double spaces + leading question numbering like '150.	' leftovers
        v2 = re.sub(r'\s{2,}', ' ', v2).strip()
        if v2 != v:
            q[field] = v2
            changed = True
    if changed:
        n += 1
print('cleaned:', n)
json.dump(B, open(r'F:\NEET PG\research\corrected_bank.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
