import io, json
qs = json.loads(io.open('research/_parsed.json', encoding='utf-8').read())
for y in [2021,2020,2019,2018]:
    yy=[q for q in qs if q['year']==y]
    ns=sorted(set(q['n'] for q in yy))
    over=[n for n in ns if n>240]
    print(y,'max',max(ns),'uniq',len(ns),'over200',len(over), 'e.g.',over[:10])
    # duplicate same n across different subj?
    from collections import Counter
    cn=Counter(q['n'] for q in yy)
    dup=[n for n,c in cn.items() if c>1]
    print('   dup qn count:', len(dup), 'e.g.', dup[:8])
    subj_of=[ (n, sorted(set(qq['subj'] for qq in yy if qq['n']==n))) for n in dup[:5]]
    print('   dup qn -> subjs:', subj_of)
