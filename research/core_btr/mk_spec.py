# -*- coding: utf-8 -*-
import json

CR = "\r\n"

P = [
# P1
{
"anchor": '        <div><label>Subject</label><select id="qbSubj"><option value="">All Subjects</option></select></div>' + CR + '        <div><label>Topic</label><select id="qbTopic"><option value="">All Topics</option></select></div>',
"replacement": "",
"note": "P1 (B-STEP1) HTML qbank: delete qbSubj/qbTopic selects (lines 173-174). Remaining fit-row: Exam, Source, Attempt, Mode, Count, Start."
},
# P2
{
"anchor": '      <div class="score-note" style="margin-top:8px">Tap a subject to drill into topics.</div>' + CR + '    </div>' + CR + '    <div class="card"><div id="qbTree"></div></div>',
"replacement": '      <div class="score-note" style="margin-top:8px">Tap a subject to drill into topics, or toggle chips below for a mixed set.</div>' + CR + '    </div>' + CR + '    <div class="card"><h3 style="margin-bottom:10px;">Subjects <span class="score-note">(click to toggle)</span></h3><div id="qbSubjList" class="chip-list"></div></div>' + CR + '    <div class="card"><h3 style="margin-bottom:10px;">Topics <span class="score-note">(click to toggle)</span></h3><div id="qbTopicList" class="chip-list"></div></div>' + CR + '    <div class="card"><div id="qbTree"></div></div>',
"note": "P2 (B-STEP2) insert 2 chip cards before qbTree card. Match includes drill hint (lines 185-187)."
},
# P3
{
"anchor": '        <div><label>Subject</label><select id="tSubj"><option value="">All subjects</option></select></div>',
"replacement": '        <div><label>Subjects</label><div id="tSubj" class="chip-list"></div></div>',
"note": "P3 (B-STEP3) tSubj select -> chip container (line 242). Same element id reused; JS no longer builds options."
},
# P4
{
"anchor": "  addOpts($('qbSubj'), subjOpts);" + CR + "  addOpts($('qbTopic'), topicOpts);",
"replacement": "",
"note": "P4 (B-STEP4) populateBrowseDropdowns: drop qb lines (912-913). browseSubj/browseTopic addOpts lines stay. REQUIRED - showView('qbank') + init call this; qbSubj/qbTopic elements are gone."
},
# P5
{
"anchor": "function cmTopicsForSubjs() {" + CR + "  var t = new Set();" + CR + "  var src = $('cmSource').value;" + CR + "  BANK.forEach(function (q) {" + CR + "    if (src && (q.src || 'original') !== src) return;" + CR + "    if (CM.subjs[q.s] || Object.keys(CM.subjs).length === 0) t.add(topicOf(q));" + CR + "  });" + CR + "  return Array.from(t).sort();" + CR + "}",
"replacement": "function topicsFor(selSubjs, src) {" + CR + "  var t = new Set();" + CR + "  BANK.forEach(function (q) {" + CR + "    if (src && (q.src || 'original') !== src) return;" + CR + "    if (selSubjs[q.s] || Object.keys(selSubjs).length === 0) t.add(topicOf(q));" + CR + "  });" + CR + "  return Array.from(t).sort();" + CR + "}" + CR + "function cmTopicsForSubjs() { return topicsFor(CM.subjs, $('cmSource').value); }",
"note": "P5 (B-STEP9) refactor shared topicsFor; CM behavior byte-identical (lines 1029-1037)."
},
# P6
{
"anchor": "  var mode = $('qbMode').value;" + CR + "  var srcFilter = $('qbSource').value;" + CR + "  var subjFilter = $('qbSubj').value;" + CR + "  var topicFilter = $('qbTopic').value;" + CR + "  var attemptFilter = $('qbAttempt').value;" + CR + "  var counts = {};" + CR + "  var idxBySubj = {};" + CR + "  var totalCount = 0;" + CR + "  BANK.forEach(function (q, i) {" + CR + "    if (srcFilter) {" + CR + "      var qsrc = q.src || 'original';" + CR + "      if (qsrc !== srcFilter) return;" + CR + "    }" + CR + "    if (subjFilter && q.s !== subjFilter) return;" + CR + "    if (topicFilter && topicOf(q) !== topicFilter) return;",
"replacement": "  var mode = $('qbMode').value;" + CR + "  var srcFilter = $('qbSource').value;" + CR + "  var subjFilter = Object.keys(QB.subjs).length ? Object.keys(QB.subjs) : null;" + CR + "  var topicFilter = Object.keys(QB.topics).length ? Object.keys(QB.topics) : null;" + CR + "  var attemptFilter = $('qbAttempt').value;" + CR + "  var counts = {};" + CR + "  var idxBySubj = {};" + CR + "  var totalCount = 0;" + CR + "  BANK.forEach(function (q, i) {" + CR + "    if (srcFilter) {" + CR + "      var qsrc = q.src || 'original';" + CR + "      if (qsrc !== srcFilter) return;" + CR + "    }" + CR + "    if (subjFilter && subjFilter.indexOf(q.s) === -1) return;" + CR + "    if (topicFilter && topicFilter.indexOf(topicOf(q)) === -1) return;",
"note": "P6 (B-STEP5) renderTree: header spans var mode..var attemptFilter (lines 776-780) making anchor unique against byte-identical renderBrowse header (858-860, no qbMode); filter ifs -> array membership."
},
# P7
{
"anchor": "  var html = '<div class=\"score-note\" style=\"margin-bottom:8px\">Showing ' + totalCount + ' questions</div>';" + CR + "  Object.keys(idxBySubj).sort(function (a, b) { return SUBJECTS.indexOf(a) - SUBJECTS.indexOf(b); }).forEach(function (s) {",
"replacement": "  var html = '<div class=\"score-note\" style=\"margin-bottom:8px\">Showing ' + totalCount + ' questions</div>';" + CR + "  if (!totalCount) {" + CR + "    $('qbTree').innerHTML = html + '<div class=\"empty\">No questions match current filters.</div>';" + CR + "    return;" + CR + "  }" + CR + "  Object.keys(idxBySubj).sort(function (a, b) { return SUBJECTS.indexOf(a) - SUBJECTS.indexOf(b); }).forEach(function (s) {",
"note": "P7 (Design A P8 addition) empty-state guard for zero-match (multi-topic + attempt can yield 0). Anchor is line-802 prefix up to sort opener - unique (renderBrowse line 863 opens with '<div class=\"q-nav-list\">')."
},
# P8
{
"anchor": "$('qbStart').addEventListener('click', function () {" + CR + "  startQuiz('qbank', 'QBank Set', { src: $('qbSource').value, s: $('qbSubj').value || undefined, t: $('qbTopic').value || undefined, attempt: $('qbAttempt').value, mode: $('qbMode').value, n: parseInt($('qbCount').value, 10) || 10 });" + CR + "});",
"replacement": "$('qbStart').addEventListener('click', function () {" + CR + "  startQuiz('qbank', 'QBank Set', { src: $('qbSource').value, multiS: Object.keys(QB.subjs), multiT: Object.keys(QB.topics), attempt: $('qbAttempt').value, mode: $('qbMode').value, n: parseInt($('qbCount').value, 10) || 10 });" + CR + "});",
"note": "P8 (B-STEP6) qbStart passes multiS/multiT. Empty arrays -> poolFor multiS.length falsy -> null -> all subjects (old All behavior)."
},
# P9
{
"anchor": "$('qbSource').addEventListener('change', function() { filterBrowseTopics(); renderTree(); });" + CR + "$('qbSubj').addEventListener('change', function() { filterBrowseTopics(); renderTree(); });" + CR + "$('qbTopic').addEventListener('change', renderTree);",
"replacement": "$('qbSource').addEventListener('change', function() { QB.topics = {}; renderQBChips(); renderTree(); });",
"note": "P9 (B-STEP7) drop qbSubj/qbTopic change listeners (dead elements); qbSource resets topics then re-renders chips. qbAttempt/qbMode listeners on next lines untouched."
},
# P10
{
"anchor": "function filterBrowseTopics() {" + CR + "  var subjFilter = $('qbSubj').value;" + CR + "  var topicFilter = $('qbTopic').value;" + CR + "  var html = '<option value=\"\">All Topics</option>';" + CR + "  var topicSet = new Set();" + CR + "  BANK.forEach(function (q) {" + CR + "    if (subjFilter && q.s !== subjFilter) return;" + CR + "    topicSet.add(topicOf(q));" + CR + "  });" + CR + "  Array.from(topicSet).sort().forEach(function (t) {" + CR + "    html += '<option value=\"' + t + '\">' + t + '</option>';" + CR + "  });" + CR + "  $('qbTopic').innerHTML = html;" + CR + "  if (topicFilter) $('qbTopic').value = topicFilter;" + CR + "}" + CR + CR + "function filterBrowseTopics2() {",
"replacement": "function filterBrowseTopics2() {",
"note": "P10 (B-STEP8) delete dead filterBrowseTopics + following blank + keep filterBrowseTopics2 signature in anchor (unique continuation; filterBrowseTopics2 intact for browse)."
},
# P11
{
"anchor": "  var name = $('cmName').value.trim() || 'My Module';" + CR + "  startQuiz('qbank', 'Custom: ' + name, sel);" + CR + "});",
"replacement": "  var name = $('cmName').value.trim() || 'My Module';" + CR + "  startQuiz('qbank', 'Custom: ' + name, sel);" + CR + "});" + CR + CR + "/* ---------------- QBank + Test multi-select chips ---------------- */" + CR + "var QB = { subjs: {}, topics: {} };" + CR + "var T = { subjs: {} };" + CR + "function renderQBChips() {" + CR + "  var subjHtml = cmAllSubjects().map(function (s) {" + CR + "    return '<span class=\"chip' + (QB.subjs[s] ? ' on' : '') + '\" data-s=\"' + s + '\">' + s + '</span>';" + CR + "  }).join('');" + CR + "  $('qbSubjList').innerHTML = subjHtml;" + CR + "  var topicHtml = topicsFor(QB.subjs, $('qbSource').value).map(function (t) {" + CR + "    return '<span class=\"chip' + (QB.topics[t] ? ' on' : '') + '\" data-t=\"' + t + '\">' + t + '</span>';" + CR + "  }).join('');" + CR + "  $('qbTopicList').innerHTML = topicHtml;" + CR + "  $('qbSubjList').querySelectorAll('.chip').forEach(function (el) {" + CR + "    el.addEventListener('click', function () {" + CR + "      var s = el.dataset.s;" + CR + "      if (QB.subjs[s]) delete QB.subjs[s]; else QB.subjs[s] = true;" + CR + "      QB.topics = {};" + CR + "      renderQBChips();" + CR + "      renderTree();" + CR + "    });" + CR + "  });" + CR + "  $('qbTopicList').querySelectorAll('.chip').forEach(function (el) {" + CR + "    el.addEventListener('click', function () {" + CR + "      var t = el.dataset.t;" + CR + "      if (QB.topics[t]) delete QB.topics[t]; else QB.topics[t] = true;" + CR + "      renderQBChips();" + CR + "      renderTree();" + CR + "    });" + CR + "  });" + CR + "}" + CR + "function renderTChips() {" + CR + "  $('tSubj').innerHTML = SUBJECTS.map(function (s) {" + CR + "    return '<span class=\"chip' + (T.subjs[s] ? ' on' : '') + '\" data-s=\"' + s + '\">' + s + '</span>';" + CR + "  }).join('');" + CR + "  $('tSubj').querySelectorAll('.chip').forEach(function (el) {" + CR + "    el.addEventListener('click', function () {" + CR + "      var s = el.dataset.s;" + CR + "      if (T.subjs[s]) delete T.subjs[s]; else T.subjs[s] = true;" + CR + "      renderTChips();" + CR + "    });" + CR + "  });" + CR + "}",
"note": "P11 (B-STEP10) append state + renderers after cmStart listener (lines 1079-1081). Both renderers attach listeners AFTER innerHTML assignment - no stale-listener risk on re-render. cmAllSubjects hoisted (line 1024), topicsFor defined at P5 - safe."
},
# P12
{
"anchor": "function populateSubjects() {" + CR + "  var sel = tSubj;" + CR + "  var any = document.createElement('option'); any.value = ''; any.textContent = 'All subjects';" + CR + "  sel.appendChild(any);" + CR + "  SUBJECTS.forEach(function (s) { var o = document.createElement('option'); o.value = s; o.textContent = s; sel.appendChild(o); });" + CR + "}",
"replacement": "function populateSubjects() { renderTChips(); }",
"note": "P12 (B-STEP11) populateSubjects -> wrapper (lines 1363-1368)."
},
# P13
{
"anchor": "var tSubj = $('tSubj'), tYear = $('tYear');",
"replacement": "var tYear = $('tYear');",
"note": "P13 (Design A P17) tSubj is now a div; var capture dead. Drop."
},
# P14
{
"anchor": "  var t = { name: name, e: $('tExam').value, s: $('tSubj').value, y: $('tYear').value, n: parseInt($('tCount').value, 10) || 20, timed: $('tTimed').value === '1' };",
"replacement": "  var t = { name: name, e: $('tExam').value, multiS: Object.keys(T.subjs), y: $('tYear').value, n: parseInt($('tCount').value, 10) || 20, timed: $('tTimed').value === '1' };",
"note": "P14 (B-STEP12) tCreate stores multiS instead of s (line 1408)."
},
# P15
{
"anchor": "      startQuiz('test', t.name, { exam: t.e, s: t.s, y: t.y, n: t.n, timed: !!t.timed });",
"replacement": "      startQuiz('test', t.name, { exam: t.e, multiS: t.multiS, s: t.s, y: t.y, n: t.n, timed: !!t.timed });",
"note": "P15 (B-STEP13) saved-test attempt passes multiS + legacy s fallback (line 1297). poolFor: multiS empty -> s. New tests: multiS only (s undefined). Old tests: s only. Both work."
},
# P16
{
"anchor": "      '<div class=\"res-meta\">' + t.n + ' Qs' + (t.s ? ' \u2022 ' + t.s : '') + (t.y !== 'any' ? ' \u2022 ' + t.y : '') + (t.timed ? ' \u2022 Timed' : ' \u2022 Untimed') + '</div></div>' +",
"replacement": "      '<div class=\"res-meta\">' + t.n + ' Qs' + (t.multiS && t.multiS.length ? ' \u2022 ' + t.multiS.join(', ') : t.s ? ' \u2022 ' + t.s : '') + (t.y !== 'any' ? ' \u2022 ' + t.y : '') + (t.timed ? ' \u2022 Timed' : ' \u2022 Untimed') + '</div></div>' +",
"note": "P16 (B-STEP14) renderTestList meta shows multiS join; bullet is U+2022 - anchor must use it verbatim (line 1290)."
},
# P17
{
"anchor": "  if (v === 'qbank') { populateBrowseDropdowns(); renderTree(); }",
"replacement": "  if (v === 'qbank') { populateBrowseDropdowns(); renderQBChips(); renderTree(); }",
"note": "P17 (B-STEP15) live showView (def 2, line 1398) re-renders chips on entry so listeners never stale. Def 1 (line 718) left untouched - dead code (hoisted, def 2 wins); patching it adds zero value."
},
]

spec = {
"winner": "chips-inline: Design B base + Design A empty-tree guard. B verified byte-exact against F:/NEET PG/questions/science.html (12 NUL, 1207 CRLF, 1439 lines confirmed). Design A rejected: P9 anchor byte-broken (file line 1071 has en-dash U+2013 where A assumed hyphen) and shared-QBS state bleeds Test Series selection into QBank (real defect). B's separate QB/T state + topicsFor refactor is smaller and safer.",
"stateObjects": "Two state objects appended after cmStart listener block:\nvar QB = { subjs: {}, topics: {} };  // QBank chips, object-keyed toggle sets, mirrors CM exactly\nvar T  = { subjs: {} };              // Test Series subject chips, isolated from QB - no cross-card bleed\nCM untouched. poolFor (lines 827-830) already accepts multiS/multiT with s/t fallback - do not touch. No summary/clear element (chip tap-again toggles off = CM parity). .chip/.chip.on/.chip-list CSS already at lines 124-127 - zero new styles.",
"patchSteps": P,
"staysSingle": [
"browseSubj/browseTopic (browse tab): single-select list drill-down; per-question navigation where one subject/topic is the intent; multi-select value near zero; filterBrowseTopics2/renderBrowse untouched",
"qbAttempt (Attempt Status): mutually exclusive statuses; select composes unchanged with chip arrays in renderTree",
"qbMode (Image/Clinical focus): exclusive modes; untouched",
"qbSource: single source or All; chip topic regen reads it",
"qbExam, tExam, tYear (Year): year filter inherently exclusive (2021-2026)",
"browseSearch: text filter; untouched",
"tTimed/cmTimed/qbCount/tCount: orthogonal controls",
"Custom Module (CM): already chip multi-select; untouched"
],
"verification": [
"Post-patch assert: data.count(b'\\x00') == 12 (was 12)",
"assert data.count(b'\\r\\n') == 1207 (was 1207)",
"assert s.count('qbSubj') == 0 and s.count('qbTopic') == 0 (zero hits)",
"s.count('filterBrowseTopics') == 1 (only filterBrowseTopics2 remains)",
"'qbSubjList'/'qbTopicList'/'multiS'/'topicsFor'/'QB'/'renderTChips'/'renderQBChips' all present; 'cmTopicsForSubjs' present as wrapper",
"Browser: qbank view shows chips; toggle subject -> topic list regenerates + topic chips cleared; toggle topics; Start builds multi-subject set; attempt filter composes; drill-row click still starts single s/t quiz",
"Test Series: subject chips toggle; Create stores multiS; Attempt works; old saved test (s-only) still attempts",
"Source change clears topics + re-renders chips + tree",
"No console errors; no stale $('qbSubj').value reads (grep proves none)",
"Patch procedure: python open(path,'rb') -> assert NUL==12 -> decode('utf-8') -> str.replace(old,new,1) per step -> encode('utf-8') -> open(path,'wb').write. NEVER Edit tool, never text-mode write, never line-splitting."
],
"risks": [
"P6/P7 anchor uniqueness: assert s.count(old)==1 before each replace; renderBrowse header (858-860) differs (browseSource/browseSubj/browseTopic, no qbMode, no counts vars) so P6 anchor is unique",
"Special chars: P16 anchor contains U+2022 bullet - copy verbatim from file; line 1071 renderCMChips contains U+2013 en-dash (untouched by this spec) - never retype anchors from memory",
"qbSource change listener body executes lazily on change event, after all defs exist at script eval - safe",
"Init order: P11 appends QB/renderQBChips before Init section (line 1422+); script is single pass top-to-bottom, so QB defined before populateSubjects()/populateBrowseDropdowns() at lines 1423-1425 run",
"Chip overflow with many selections: .chip-list flex-wrap handles it; ~100 topic chips wrap into ~5 rows; add .chip-list{max-height:...;overflow-y:auto} later if unwieldy (ponytail: not added now)",
"Old saved tests display: renderTestList shows bullet + t.s for legacy - covered by P16 fallback",
"Drill-row click path unchanged - passes single s/t directly, not through chip state"
],
}
out = json.dumps(spec, ensure_ascii=False)
print('json len', len(out))
open(r'F:\NEET PG\research\core_btr\spec.json', 'w', encoding='utf-8').write(out)
print('written')
