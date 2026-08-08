import io, re
t = io.open('research/neetpg-yearwise.txt', encoding='utf-8').read()
pages = t.split('===PAGE ')
# 2023 q paper starts book page 227 => page idx 225
hdr='\n'.join(pages[225:232])
for ln in hdr.strip().split('\n')[:60]:
    print(repr(ln[:80]))
