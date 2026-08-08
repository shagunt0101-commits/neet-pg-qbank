import io, json
from collections import Counter
qs = json.loads(io.open('research/_parsed.json', encoding='utf-8').read())
for y in [2025,2024,2023,2022,2021,2020,2019,2018]:
    yy=[q for q in qs if q['year']==y]
    c=Counter(q['subj'] for q in yy)
    print(y, 'total', len(yy), '|', ', '.join(f'{k}:{v}' for k,v in sorted(c.items(), key=lambda x:-x[1])))
