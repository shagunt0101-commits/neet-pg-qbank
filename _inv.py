import io, json, re
qs = json.loads(io.open('research/_parsed.json', encoding='utf-8').read())
from collections import Counter
byyear = Counter(q['year'] for q in qs if q['subj']=='Surgery')
print('Surgery by year:', dict(sorted(byyear.items())))
print()
byyear2 = Counter(q['year'] for q in qs if q['subj']=='OBG')
print('OBG by year:', dict(sorted(byyear2.items())))
print()
# print unique qnumbers for surgery 2024 to see inflation source
s2024 = [q for q in qs if q['subj']=='Surgery' and q['year']==2024]
ns = sorted(set(q['n'] for q in s2024))
print('2024 Surgery qn range:', ns[0], '-', ns[-1], 'count', len(ns))
# gaps
gaps=[n for n in range(min(ns),max(ns)+1) if n not in set(ns)]
print('2024 gaps (missing qns inside range):', gaps)
# examine 2023 surgery qnums
s2023 = [q for q in qs if q['subj']=='Surgery' and q['year']==2023]
ns3 = sorted(set(q['n'] for q in s2023))
print('2023 Surgery qns:', ns3[:10], '...', ns3[-5:], 'count', len(ns3))
