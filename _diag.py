import io, json
qs = json.loads(io.open('research/_parsed.json', encoding='utf-8').read())
out = []
empty = [q for q in qs if len(q['q']) < 8]
out.append('empty stems: %d' % len(empty))
for q in empty[:8]:
    out.append('  %s %s Q%s stem=%r opts=%s' % (q['year'], q['subj'], q['n'], q['q'][:50], q['o'][:1]))
c = {}
for q in qs:
    s = q['subj']
    c[s] = c.get(s, 0) + 1
out.append('subjects:')
for k, v in sorted(c.items(), key=lambda x: -x[1]):
    out.append('  %-22s %d' % (k, v))
io.open('research/_diag.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done')
