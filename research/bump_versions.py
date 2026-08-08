# -*- coding: utf-8 -*-
"""Bump bank.js version refs after corrected bank (v7 -> v8). NUL-safe."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

def patch(path, subs, nul_check=True):
    raw = open(path, 'rb').read()
    if nul_check:
        assert raw.count(b'\x00') == 12, f'NUL count {raw.count(b"\x00")}'
    s = raw.decode('utf-8')
    for old, new in subs:
        n = s.count(old)
        assert n == 1, f'{path}: {old!r} count {n}'
        s = s.replace(old, new)
    out = s.encode('utf-8')
    if nul_check:
        assert out.count(b'\x00') == 12
    open(path, 'wb').write(out)
    print('patched', path)

patch(r'F:\NEET PG\questions\science.html',
      [('<script src="/questions/bank.js?v=7"></script>',
        '<script src="/questions/bank.js?v=8"></script>')])
patch(r'F:\NEET PG\sw.js',
      [("var CACHE = 'qbank-v5';", "var CACHE = 'qbank-v6';"),
       ("'/questions/bank.js?v=7',", "'/questions/bank.js?v=8',")], nul_check=False)
print('done')
