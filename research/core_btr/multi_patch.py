# -*- coding: utf-8 -*-
"""Byte-stable multi-select patch for questions/science.html (17 steps, spec
from wavmnjhho workflow). CRLF-aware, NUL sentinels preserved (12)."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'F:\NEET PG\questions\science.html'

with open(PATH, 'rb') as f:
    raw = f.read()
assert raw.count(b'\x00') == 12
s = raw.decode('utf-8')
orig_crlf = s.count('\r\n')
orig_lf = s.count('\n') - orig_crlf

def rep(old, new, label=''):
    global s
    n = s.count(old)
    if n == 0:
        print(f'  skip (already applied): {label}')
        return
    assert n == 1, f'{label}: count {n} != 1\n{old[:120]!r}'
    s = s.replace(old, new)
    print(f'  ok: {label}')

# --- P1: delete qbSubj/qbTopic selects from QBank card ---
rep('        <div><label>Subject</label><select id="qbSubj"><option value="">All Subjects</option></select></div>\r\n'
    '        <div><label>Topic</label><select id="qbTopic"><option value="">All Topics</option></select></div>\r\n',
    '', 'P1 drop qb selects')

# --- P2: chip cards before qbTree card ---
rep('      <div class="score-note" style="margin-top:8px">Tap a subject to drill into topics.</div>\r\n'
    '    </div>\r\n'
    '    <div class="card"><div id="qbTree"></div></div>',
    '      <div class="score-note" style="margin-top:8px">Tap a subject to drill into topics, or toggle chips below for a mixed set.</div>\r\n'
    '    </div>\r\n'
    '    <div class="card"><h3 style="margin-bottom:10px;">Subjects <span class="score-note">(click to toggle)</span></h3><div id="qbSubjList" class="chip-list"></div></div>\r\n'
    '    <div class="card"><h3 style="margin-bottom:10px;">Topics <span class="score-note">(shown for selected subjects)</span></h3><div id="qbTopicList" class="chip-list"></div></div>\r\n'
    '    <div class="card"><div id="qbTree"></div></div>',
    'P2 chip cards')

# --- P3: tSubj select -> chip container ---
rep('        <div><label>Subject</label><select id="tSubj"><option value="">All subjects</option></select></div>',
    '        <div><label>Subjects</label><div id="tSubj" class="chip-list"></div></div>',
    'P3 tSubj chips')

# --- P4: drop qb lines from populateBrowseDropdowns ---
rep("  addOpts($('qbSubj'), subjOpts);\r\n  addOpts($('qbTopic'), topicOpts);\r\n",
    '', 'P4 drop qb addOpts')

# --- P5: refactor cmTopicsForSubjs -> shared topicsFor ---
rep('function cmTopicsForSubjs() {\r\n'
    '  var t = new Set();\r\n'
    '  var src = $(\'cmSource\').value;\r\n'
    '  BANK.forEach(function (q) {\r\n'
    '    if (src && (q.src || \'original\') !== src) return;\r\n'
    '    if (CM.subjs[q.s] || Object.keys(CM.subjs).length === 0) t.add(topicOf(q));\r\n'
    '  });\r\n'
    '  return Array.from(t).sort();\r\n'
    '}',
    'function topicsFor(selSubjs, src) {\r\n'
    '  var t = new Set();\r\n'
    '  BANK.forEach(function (q) {\r\n'
    '    if (src && (q.src || \'original\') !== src) return;\r\n'
    '    if (selSubjs[q.s] || Object.keys(selSubjs).length === 0) t.add(topicOf(q));\r\n'
    '  });\r\n'
    '  return Array.from(t).sort();\r\n'
    '}\r\n'
    'function cmTopicsForSubjs() { return topicsFor(CM.subjs, $(\'cmSource\').value); }',
    'P5 shared topicsFor')

# --- P6: renderTree header: single values -> arrays ---
rep('  var mode = $(\'qbMode\').value;\r\n'
    '  var srcFilter = $(\'qbSource\').value;\r\n'
    '  var subjFilter = $(\'qbSubj\').value;\r\n'
    '  var topicFilter = $(\'qbTopic\').value;\r\n'
    '  var attemptFilter = $(\'qbAttempt\').value;',
    '  var mode = $(\'qbMode\').value;\r\n'
    '  var srcFilter = $(\'qbSource\').value;\r\n'
    '  var subjFilter = Object.keys(QB.subjs).length ? Object.keys(QB.subjs) : null;\r\n'
    '  var topicFilter = Object.keys(QB.topics).length ? Object.keys(QB.topics) : null;\r\n'
    '  var attemptFilter = $(\'qbAttempt\').value;',
    'P6 renderTree arrays')

# --- P7: renderTree filter uses array membership + empty-state guard ---
rep('    if (subjFilter && q.s !== subjFilter) return;\r\n'
    '    if (topicFilter && topicOf(q) !== topicFilter) return;\r\n'
    '    if (attemptFilter !== \'all\') {\r\n'
    '      var status = getAttemptStatus(i);\r\n'
    '      if (attemptFilter === \'unattempted\' && status !== \'unattempted\') return;\r\n'
    '      if (attemptFilter === \'correct\' && status !== \'correct\') return;\r\n'
    '      if (attemptFilter === \'wrong\' && status !== \'wrong\') return;\r\n'
    '      if (attemptFilter === \'skipped\' && status !== \'skipped\') return;\r\n'
    '    }\r\n'
    '    totalCount++;\r\n'
    '    if (!idxBySubj[q.s]) idxBySubj[q.s] = [];\r\n'
    '    idxBySubj[q.s].push(i);\r\n'
    '  });\r\n'
    '  var html = \'<div class="score-note" style="margin-bottom:8px">Showing \' + totalCount + \' questions</div>\';',
    '    if (subjFilter && subjFilter.indexOf(q.s) === -1) return;\r\n'
    '    if (topicFilter && topicFilter.indexOf(topicOf(q)) === -1) return;\r\n'
    '    if (attemptFilter !== \'all\') {\r\n'
    '      var status = getAttemptStatus(i);\r\n'
    '      if (attemptFilter === \'unattempted\' && status !== \'unattempted\') return;\r\n'
    '      if (attemptFilter === \'correct\' && status !== \'correct\') return;\r\n'
    '      if (attemptFilter === \'wrong\' && status !== \'wrong\') return;\r\n'
    '      if (attemptFilter === \'skipped\' && status !== \'skipped\') return;\r\n'
    '    }\r\n'
    '    totalCount++;\r\n'
    '    if (!idxBySubj[q.s]) idxBySubj[q.s] = [];\r\n'
    '    idxBySubj[q.s].push(i);\r\n'
    '  });\r\n'
    '  var html = totalCount ? \'<div class="score-note" style="margin-bottom:8px">Showing \' + totalCount + \' questions</div>\' : \'<div class="empty" style="margin-bottom:8px">No questions match the selected chips.</div>\';',
    'P7 array filter + empty guard')

# --- P8: qbStart passes multiS/multiT ---
rep("$('qbStart').addEventListener('click', function () {\r\n"
    "  startQuiz('qbank', 'QBank Set', { src: $('qbSource').value, s: $('qbSubj').value || undefined, t: $('qbTopic').value || undefined, attempt: $('qbAttempt').value, mode: $('qbMode').value, n: parseInt($('qbCount').value, 10) || 10 });\r\n"
    "});",
    "$('qbStart').addEventListener('click', function () {\r\n"
    "  startQuiz('qbank', 'QBank Set', { src: $('qbSource').value, multiS: Object.keys(QB.subjs), multiT: Object.keys(QB.topics), attempt: $('qbAttempt').value, mode: $('qbMode').value, n: parseInt($('qbCount').value, 10) || 10 });\r\n"
    "});",
    'P8 qbStart multi')

# --- P9: qbSource resets topics + re-renders chips; drop dead qbSubj/qbTopic listeners ---
rep("$('qbSource').addEventListener('change', function() { filterBrowseTopics(); renderTree(); });\r\n"
    "$('qbSubj').addEventListener('change', function() { filterBrowseTopics(); renderTree(); });\r\n"
    "$('qbTopic').addEventListener('change', renderTree);\r\n",
    "$('qbSource').addEventListener('change', function() { QB.topics = {}; renderQBChips(); renderTree(); });\r\n",
    'P9 qb listeners')

# --- P10: delete dead filterBrowseTopics ---
rep('function filterBrowseTopics() {\r\n'
    '  var subjFilter = $(\'qbSubj\').value;\r\n'
    '  var topicFilter = $(\'qbTopic\').value;\r\n'
    '  var html = \'<option value="">All Topics</option>\';\r\n'
    '  var topicSet = new Set();\r\n'
    '  BANK.forEach(function (q) {\r\n'
    '    if (subjFilter && q.s !== subjFilter) return;\r\n'
    '    topicSet.add(topicOf(q));\r\n'
    '  });\r\n'
    '  Array.from(topicSet).sort().forEach(function (t) {\r\n'
    '    html += \'<option value="\' + t + \'">\' + t + \'</option>\';\r\n'
    '  });\r\n'
    '  $(\'qbTopic\').innerHTML = html;\r\n'
    '  if (topicFilter) $(\'qbTopic\').value = topicFilter;\r\n'
    '}\r\n\r\n',
    '', 'P10 drop filterBrowseTopics')

# --- P11: append QB/T state + chip renderers after cmStart listener ---
rep("$('cmStart').addEventListener('click', function () {\r\n"
    "  var sel = { src: $('cmSource').value, mode: $('cmMode').value, n: parseInt($('cmCount').value, 10) || 10, timed: $('cmTimed').value === '1' };\r\n"
    "  sel.multiS = Object.keys(CM.subjs);\r\n"
    "  sel.multiT = Object.keys(CM.topics);\r\n"
    "  var name = $('cmName').value.trim() || 'My Module';\r\n"
    "  startQuiz('qbank', 'Custom: ' + name, sel);\r\n"
    "});",
    "$('cmStart').addEventListener('click', function () {\r\n"
    "  var sel = { src: $('cmSource').value, mode: $('cmMode').value, n: parseInt($('cmCount').value, 10) || 10, timed: $('cmTimed').value === '1' };\r\n"
    "  sel.multiS = Object.keys(CM.subjs);\r\n"
    "  sel.multiT = Object.keys(CM.topics);\r\n"
    "  var name = $('cmName').value.trim() || 'My Module';\r\n"
    "  startQuiz('qbank', 'Custom: ' + name, sel);\r\n"
    "});\r\n"
    "\r\n"
    "/* ---------------- Multi-select chips: QBank + Test Series ---------------- */\r\n"
    "var QB = { subjs: {}, topics: {} };  // QBank chip toggle sets\r\n"
    "var T = { subjs: {} };               // Test Series subject chips (isolated)\r\n"
    "\r\n"
    "function renderQBChips() {\r\n"
    "  var subjs = cmAllSubjects();\r\n"
    "  $('qbSubjList').innerHTML = subjs.map(function (s) {\r\n"
    "    return '<span class=\"chip' + (QB.subjs[s] ? ' on' : '') + '\" data-s=\"' + s + '\">' + s + '</span>';\r\n"
    "  }).join('');\r\n"
    "  var topics = topicsFor(QB.subjs, $('qbSource').value);\r\n"
    "  $('qbTopicList').innerHTML = topics.map(function (t) {\r\n"
    "    return '<span class=\"chip' + (QB.topics[t] ? ' on' : '') + '\" data-t=\"' + t + '\">' + t + '</span>';\r\n"
    "  }).join('');\r\n"
    "  $('qbSubjList').querySelectorAll('.chip').forEach(function (el) {\r\n"
    "    el.addEventListener('click', function () {\r\n"
    "      var s = el.dataset.s;\r\n"
    "      if (QB.subjs[s]) delete QB.subjs[s]; else QB.subjs[s] = true;\r\n"
    "      QB.topics = {};  // subject set changed -> topic list rebuilt\r\n"
    "      renderQBChips();\r\n"
    "      renderTree();\r\n"
    "    });\r\n"
    "  });\r\n"
    "  $('qbTopicList').querySelectorAll('.chip').forEach(function (el) {\r\n"
    "    el.addEventListener('click', function () {\r\n"
    "      var t = el.dataset.t;\r\n"
    "      if (QB.topics[t]) delete QB.topics[t]; else QB.topics[t] = true;\r\n"
    "      renderQBChips();\r\n"
    "      renderTree();\r\n"
    "    });\r\n"
    "  });\r\n"
    "}\r\n"
    "\r\n"
    "function renderTChips() {\r\n"
    "  $('tSubj').innerHTML = SUBJECTS.map(function (s) {\r\n"
    "    return '<span class=\"chip' + (T.subjs[s] ? ' on' : '') + '\" data-s=\"' + s + '\">' + s + '</span>';\r\n"
    "  }).join('');\r\n"
    "  $('tSubj').querySelectorAll('.chip').forEach(function (el) {\r\n"
    "    el.addEventListener('click', function () {\r\n"
    "      var s = el.dataset.s;\r\n"
    "      if (T.subjs[s]) delete T.subjs[s]; else T.subjs[s] = true;\r\n"
    "      renderTChips();\r\n"
    "    });\r\n"
    "  });\r\n"
    "}",
    'P11 QB/T state + renderers')

# --- P12: populateSubjects -> chips (replace body, keep name) ---
rep('function populateSubjects() {\r\n'
    '  var sel = tSubj;\r\n'
    '  var any = document.createElement(\'option\'); any.value = \'\'; any.textContent = \'All subjects\';\r\n'
    '  sel.appendChild(any);\r\n'
    '  SUBJECTS.forEach(function (s) { var o = document.createElement(\'option\'); o.value = s; o.textContent = s; sel.appendChild(o); });\r\n'
    '}',
    'function populateSubjects() {\r\n'
    '  renderTChips();\r\n'
    '}',
    'P12 populateSubjects -> chips')

# --- P13: drop dead var tSubj select capture ---
rep('var tSubj = $(\'tSubj\'), tYear = $(\'tYear\');',
    'var tYear = $(\'tYear\');',
    'P13 drop tSubj var')

# --- P14: tCreate stores multiS ---
rep("  var t = { name: name, e: $('tExam').value, s: $('tSubj').value, y: $('tYear').value, n: parseInt($('tCount').value, 10) || 20, timed: $('tTimed').value === '1' };",
    "  var t = { name: name, e: $('tExam').value, multiS: Object.keys(T.subjs), s: $('tExam').value ? undefined : undefined, y: $('tYear').value, n: parseInt($('tCount').value, 10) || 20, timed: $('tTimed').value === '1' };",
    'P14 tCreate multiS')

# --- P15: saved-test attempt passes multiS + legacy s fallback ---
rep("      startQuiz('test', t.name, { exam: t.e, s: t.s, y: t.y, n: t.n, timed: !!t.timed });",
    "      startQuiz('test', t.name, { exam: t.e, multiS: t.multiS, s: t.s, y: t.y, n: t.n, timed: !!t.timed });",
    'P15 test attempt multi')

# --- P16: renderTestList meta shows multiS ---
rep('      \'<div class="res-meta">\' + t.n + \' Qs\' + (t.s ? \' • \' + t.s : \'\') + (t.y !== \'any\' ? \' • \' + t.y : \'\') + (t.timed ? \' • Timed\' : \' • Untimed\') + \'</div></div>\' +',
    '      \'<div class="res-meta">\' + t.n + \' Qs\' + ((t.multiS && t.multiS.length) ? \' • \' + t.multiS.join(\', \') : (t.s ? \' • \' + t.s : \'\')) + (t.y !== \'any\' ? \' • \' + t.y : \'\') + (t.timed ? \' • Timed\' : \' • Untimed\') + \'</div></div>\' +',
    'P16 test meta multiS')

# --- P17: live showView re-renders chips ---
rep("  if (v === 'qbank') { populateBrowseDropdowns(); renderTree(); }",
    "  if (v === 'qbank') { populateBrowseDropdowns(); renderQBChips(); renderTree(); }",
    'P17 showView qbank chips')

# --- verify ---
assert s.count('\x00') == 12, 'NUL count changed'
assert s.count('id="qbSubj"') == 0 and s.count('id="qbTopic"') == 0
assert s.count('filterBrowseTopics(') == 0 and s.count('filterBrowseTopics2') > 0
for tok in ['qbSubjList', 'qbTopicList', 'multiS', 'topicsFor', 'renderQBChips', 'renderTChips', 'var QB', 'var T = ']:
    assert tok in s, tok
crlf = s.count('\r\n'); lf = s.count('\n') - crlf
print(f'CRLF {orig_crlf}->{crlf}, lone LF {orig_lf}->{lf}')
assert lf == orig_lf, 'lone LF count changed'

with open(PATH, 'wb') as f:
    f.write(s.encode('utf-8'))
print('multi-select patch OK')
