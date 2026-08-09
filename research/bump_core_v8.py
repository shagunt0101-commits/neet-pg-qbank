# -*- coding: utf-8 -*-
"""Bump core_btr.js ?v=7 -> ?v=8 and sw.js qbank-v16 -> qbank-v17 after leak fixes."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

def patch(path, subs, nul_check=True):
    raw = open(path, 'rb').read()
    if nul_check:
        assert raw.count(b'\x00') == 12, 'NUL %d' % raw.count(b'\x00')
    s = raw.decode('utf-8')
    for old, new in subs:
        n = s.count(old)
        assert n == 1, '%s: %r count %d' % (path, old, n)
        s = s.replace(old, new)
    out = s.encode('utf-8')
    if nul_check:
        assert out.count(b'\x00') == 12
    open(path, 'wb').write(out)
    print('patched', path)

patch(r'F:\NEET PG\questions\science.html',
      [('core_btr.js?v=7', 'core_btr.js?v=8')])
patch(r'F:\NEET PG\sw.js',
      [("var CACHE = 'qbank-v16';", "var CACHE = 'qbank-v17';"),
       ("'/questions/core_btr.js?v=7'", "'/questions/core_btr.js?v=8'")], nul_check=False)
print('done')
