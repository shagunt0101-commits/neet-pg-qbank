import io, json
qs = json.loads(io.open('research/_parsed.json', encoding='utf-8').read())
from collections import Counter
# inspect 2024 qn>200 & duplicate-stemming
y24=[q for q in qs if q['year']==2024]
big=[q for q in y24 if q['n']>200]
print('2024 qn>200 count:', len(big))
for q in big[:6]:
    print(' q%d %s | %s' % (q['n'], q['subj'], q['q'][:50]))
# count stem duplicates across all
from collections import defaultdict
seen=defaultdict(list)
for q in qs: seen[q['q']].append((q['year'],q['subj'],q['n']))
d={k:v for k,v in seen.items() if len(v)>1}
print('dup stems total:', len(d))
for k,v in list(d.items())[:6]:
    print(' DUP:', v, '::', k[:45])
