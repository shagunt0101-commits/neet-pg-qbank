import io, json
qs = json.loads(io.open('research/_parsed.json', encoding='utf-8').read())
# How many Surgery parsed, per-year, and what subjects would they map to
from collections import Counter
surg = [q for q in qs if q['subj'] == 'Surgery']
print('total Surgery:', len(surg))
c = Counter(q['year'] for q in surg)
print('by year:', dict(sorted(c.items())))
# first 40 surgery stems first words hint
for q in surg[:20]:
    print(q['year'], q['n'], '|', q['q'][:70])
