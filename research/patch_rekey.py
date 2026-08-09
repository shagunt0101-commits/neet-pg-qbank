# -*- coding: utf-8 -*-
"""Patch mergeHist to re-key hist records by qid -> current bank stem.

Old mobile records synced under pre-corruption stem keys; laptop's new bank
has different stems -> keys never matched -> progress invisible. qids are
stable across bank versions, so map qid -> current stem(50) at merge time.
File on disk is LF-normalized (core.autocrlf=true); git stores CRLF.
"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'F:\NEET PG\questions\science.html'
d = io.open(p, 'r', encoding='utf-8', errors='replace').read()
nul_before = d.count('\x00')
nl = '\n'  # disk is LF-normalized

s = d.find('function mergeHist(remote) {')
e = d.find('function unionTimes', s)
assert s != -1 and e != -1, 'anchors not found'
old = d[s:e]

new = (
'function mergeHist(remote) {' + nl +
'  var hist = lsGet(\'neet_hist\') || {};' + nl +
'  var c = 0, rekeyed = 0;' + nl +
'  var keys = {};' + nl +
'  for (var k in hist) { // local records: normalize pre-corruption keys too' + nl +
'    var nk = stemKeyFor(hist[k]) || k;' + nl +
'    if (nk !== k) rekeyed++;' + nl +
'    keys[nk] = hist[k];' + nl +
'  }' + nl +
'  for (var k2 in remote) {' + nl +
'    var r = remote[k2];' + nl +
'    if (!r || typeof r !== \'object\') continue;' + nl +
'    var nk2 = stemKeyFor(r) || k2;' + nl +
'    if (nk2 !== k2) rekeyed++;' + nl +
'    var l = keys[nk2];' + nl +
'    if (!l) { keys[nk2] = r; c++; continue; }' + nl +
'    var nr = (r.ts || 0) > (l.ts || 0) ? r : l; // newer record wins scalars' + nl +
'    var merged = {};' + nl +
'    for (var kk in nr) merged[kk] = nr[kk];' + nl +
'    merged.times = unionTimes(l.times || [], r.times || []);' + nl +
'    if (JSON.stringify(merged) !== JSON.stringify(l)) { keys[nk2] = merged; c++; }' + nl +
'  }' + nl +
'  if (c || rekeyed) lsSet(\'neet_hist\', keys);' + nl +
'  return c;' + nl +
'}'
)

d = d.replace(old, new)
nul_after = d.count('\x00')
assert nul_before == nul_after, 'NUL count changed! %d -> %d' % (nul_before, nul_after)

# add stemKeyFor helper after mergeHist block + _STEM_BY_QID decl near SYNC
anchor = new + nl + nl
helper = (
'function stemKeyFor(r) { // qid -> current bank stem(50); stable across bank fixes' + nl +
'  if (!_STEM_BY_QID) {' + nl +
'    _STEM_BY_QID = {};' + nl +
'    for (var i = 0; i < BANK.length; i++) {' + nl +
'      var q = BANK[i];' + nl +
'      if (q && q.qid) _STEM_BY_QID[q.qid] = q.q.substring(0, 50);' + nl +
'    }' + nl +
'  }' + nl +
'  return (r && r.qid && _STEM_BY_QID[r.qid]) || null;' + nl +
'}'
)
d = d.replace(anchor, anchor + helper + nl)

d = d.replace(
    "var SYNC = { f: null, db: null, user: null, lsn: null, dirty: false, timer: null, init: false };",
    "var SYNC = { f: null, db: null, user: null, lsn: null, dirty: false, timer: null, init: false };\nvar _STEM_BY_QID = null;"
)

io.open(p, 'w', encoding='utf-8', newline='').write(d)
print('patched. NUL:', nul_before, '->', nul_after)
