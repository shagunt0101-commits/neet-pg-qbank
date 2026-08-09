# -*- coding: utf-8 -*-
"""Fix q1725: fused stem + wrong answer index."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
B = json.load(open(r'F:\NEET PG\research\corrected_bank.json', encoding='utf-8'))
q = next(x for x in B if x['qid'] == 'q1725')
print('BEFORE a:', q['a'])
q['q'] = 'A woman with PCOS presents with significant facial hair, infertility, and a BMI of 40. Which of the following is the most appropriate management plan?'
q['a'] = 2  # ex: "Weight reduction + Folic acid + Ovulation induction" (option 3); finasteride teratogenic (A wrong)
print('AFTER a:', q['a'])
json.dump(B, open(r'F:\NEET PG\research\corrected_bank.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved')
