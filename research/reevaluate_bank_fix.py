# -*- coding: utf-8 -*-
"""Reevaluate all questions: fix image flag, ensure 4 options, valid answer, add topic tags.
"""
import io, json, re, sys

BANK_PATH = 'questions/bank.js'

def load_bank():
    src = io.open(BANK_PATH, encoding='utf-8').read()
    m = re.search(r'window\.QUESTIONS\s*=\s*(\[.*\])\s*;', src, re.S)
    if not m:
        print('Cannot parse bank.js', file=sys.stderr)
        sys.exit(1)
    return json.loads(m.group(1))

def save_bank(bank):
    out = []
    out.append('// Updated bank after reevaluation')
    out.append('window.QUESTIONS = ')
    out.append(json.dumps(bank, ensure_ascii=False, indent=0))
    out.append('\n;')
    io.open(BANK_PATH, 'w', encoding='utf-8').write('\n'.join(out))
    print('Bank saved, total', len(bank))

def infer_topic(stem):
    low = stem.lower()
    if 'heart' in low or 'cardiac' in low:
        return 'Cardiology'
    if 'brain' in low or 'neuro' in low:
        return 'Neurology'
    if 'bone' in low or 'orthopaedic' in low:
        return 'Orthopaedics'
    if 'skin' in low or 'dermat' in low:
        return 'Dermatology'
    return 'General'

def main():
    bank = load_bank()
    fixed = 0
    for q in bank:
        # img flag consistency
        if q.get('img') and (not q.get('imgdata') or len(q.get('imgdata', [])) == 0):
            q['img'] = False
            fixed += 1
        # options length
        if not isinstance(q.get('o'), list) or len(q.get('o')) != 4:
            q['o'] = (q.get('o') or [])[:4] + [''] * (4 - (len(q.get('o') or [])))
            fixed += 1
        # answer index
        if not isinstance(q.get('a'), int) or q['a'] < 0 or q['a'] > 3:
            q['a'] = 0
            fixed += 1
        # topic tag
        topic = infer_topic(q.get('q',''))
        if q.get('topic') != topic:
            q['topic'] = topic
            fixed += 1
    print('Total fields corrected', fixed)
    save_bank(bank)

if __name__ == '__main__':
    main()
