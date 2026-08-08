# -*- coding: utf-8 -*-
import io, json
qs = json.loads(io.open('research/_parsed.json', encoding='utf-8').read())
for s in ['Ophthalmology','Pathology']:
    sub=[q for q in qs if q['subj']==s and q['year'] in (2023,2024)]
    print(s, len(sub))
    # sample
    for q in sub[:3]:
        print('  y%d q%d | %s | A=%s' % (q['year'], q['n'], q['q'][:50], q['o'][q['a']] if q['a']<len(q['o']) else '?'))
