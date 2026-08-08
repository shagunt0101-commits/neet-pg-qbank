# -*- coding: utf-8 -*-
import io, json, re, os
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
def R(p): return os.path.join(BASE, p)

# Load existing NEET PG bank (1000 items)
old_bank = json.loads(io.open(R('../questions/bank.js'), encoding='utf-8').read().split('=',1)[1].strip(';\n '))

# Load new INI-CET bank (1775 items)
inicet_bank = json.loads(io.open(R('_inicet_final.json'), encoding='utf-8').read())

def norm_q(q_text): return re.sub(r'\s+',' ',q_text.lower()).strip()[:80]

# Deduplicate logic: prioritize image-based INI-CET over non-image NEET, otherwise NEET has priority
all_merged_questions = []
final_seen_stems = set()

# Add existing NEET questions first
for q in old_bank:
    stem_norm = norm_q(q['q'])
    all_merged_questions.append(q)
    final_seen_stems.add(stem_norm)

# Add INI-CET questions, handling duplicates and image priority
for q_inicet in inicet_bank:
    stem_norm = norm_q(q_inicet['q'])
    if stem_norm not in final_seen_stems:
        all_merged_questions.append(q_inicet)
        final_seen_stems.add(stem_norm)
    else:
        # Duplicate found, check if INI-CET is image-based and existing is not
        existing_q_index = -1
        for i, mq in enumerate(all_merged_questions):
            if norm_q(mq['q']) == stem_norm:
                existing_q_index = i
                break

        if existing_q_index != -1 and not all_merged_questions[existing_q_index].get('img', False) and q_inicet.get('img', False):
            # Replace existing non-image question with INI-CET image question
            all_merged_questions[existing_q_index] = q_inicet

# Re-tag sources
for q in all_merged_questions:
    if q.get('e') == 'INI-CET':
        q['src'] = 'inicet'
    elif q.get('src') == 'medink' and q.get('e') == 'NEET PG':
        pass
    elif q.get('src') == 'expand' and q.get('e') == 'NEET PG':
        pass
    else:
        q['src'] = 'curated'

print('Total NEET PG Qs:', len(old_bank))
print('Total INI-CET Qs (after deduping against NEET):', len(all_merged_questions) - len(old_bank))
print('Total questions in merged bank:', len(all_merged_questions))

# Write merged bank.js
lines = [
    "// NEET PG / INI-CET practice bank — reconstructed from curated + deep-research expansions.",
    "// Sources tagged per-item: curated (hand-picked PYQs), expand (workflow-generated recall Qs),",
    "// medink (parsed from user-provided compiled PYQ PDF), inicet (parsed from INI-CET PDF).",
    "// Personal offline practice only — not for redistribution.",
    "window.QUESTIONS = ",
    json.dumps(all_merged_questions, ensure_ascii=False, indent=0),
    ";\n"
]
with io.open(R('../questions/bank.js'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('wrote questions/bank.js')

# Update science.html for img toggle + placeholder
html_path = R('../questions/science.html')
html_content = io.open(html_path, encoding='utf-8').read()

# Check if placeholder already exists
if 'class="img-placeholder"' not in html_content:
    html_content = re.sub(
        r'(question\.q)\s*(<div class="options">)',
        r'question.q + (question.img ? \'<div class=\"img-placeholder\">(Image based question - see source PDF)</div>\' : \'\') + \n\t\t\t$2',
        html_content, flags=re.S)
    print('inserted image placeholder')

# Check if toggle filter already exists
if 'id="fHasImg"' not in html_content:
    filter_insert_point = html_content.find('<div class="filters">')
    if filter_insert_point != -1:
        insert_at = html_content.find('</div>', filter_insert_point)
        if insert_at != -1:
            insert_text = '\n\t\t<label><input type="checkbox" id="fHasImg" checked> Show image Qs</label>'
            html_content = html_content[:insert_at] + insert_text + html_content[insert_at:]
            print('inserted image filter toggle')

# Update refreshPool to check fHasImg
refresh_pool_old = """  if (exam && q.e !== exam) return false;
  if (subject && q.s !== subject) return false;
  if (year && q.y !== year) return false;"""
refresh_pool_new = """  if (exam && q.e !== exam) return false;
  if (subject && q.s !== subject) return false;
  if (year && q.y !== year) return false;
  if (!hasImgFilter && q.img) return false;"""

if refresh_pool_new not in html_content:
    html_content = html_content.replace(refresh_pool_old, refresh_pool_new, 1)
    print('updated refreshPool logic')

# Get hasImgFilter status from checkbox
get_filter_status_old = """  var year = $("fYear").value;
  var num = numQuestions();"""
get_filter_status_new = """  var year = $("fYear").value;
  var num = numQuestions();
  var hasImgFilter = $("fHasImg").checked;"""

if get_filter_status_new not in html_content:
    html_content = html_content.replace(get_filter_status_old, get_filter_status_new, 1)
    print('updated filter status retrieval')

with io.open(html_path,'w',encoding='utf-8') as f:
    f.write(html_content)
print('updated questions/science.html')
