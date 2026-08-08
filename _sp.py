import io, json
qs = json.loads(io.open('research/_parsed.json', encoding='utf-8').read())
for y in [2020, 2019, 2018]:
    surg = [q for q in qs if q['subj']=='Surgery' and q['year']==y]
    print(f'--- {y} Surgery count={len(surg)} ---')
    for q in surg[:12]:
        print('   Q%d | %s' % (q['n'], q['q'][:60]))
