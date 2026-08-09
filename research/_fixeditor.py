# -*- coding: utf-8 -*-
"""Dev-mode inline explanation editor — byte-stable patch for science.html.

Adds: boot vars (DEV_PIN/FIXMAP/DEV), 5x-title-tap + PIN unlock, formatEx(qid)
override + fix button, editExDialog with live preview, dev panel in Account
tab (queue list / export JSON / undo all / dev off). Bumps bank ?v= params.

science.html has 12 intentional NUL sentinel bytes — must stay 12.
Byte-level string replace only (no re-serialize, newline='' keeps LF).
"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

P = r'F:\NEET PG\questions\science.html'
d = io.open(P, 'r', encoding='utf-8').read()
assert d.count('\x00') == 12, 'NUL pre: %d' % d.count('\x00')

def sub(old, new, must=1):
    global d
    if new in d:  # already applied (idempotent re-run)
        return
    n = d.count(old)
    assert n == must, (old[:70], n, must)
    d = d.replace(old, new)

# a) boot vars + tap unlock + fix-button delegation, before FIREBASE_CONFIG
sub(r'''var REVIEW = null;
var FIREBASE_CONFIG = {''',
r'''var REVIEW = null;
var DEV_PIN = "2486", FIXMAP = lsGet("neet_exfix") || {}, DEV = { on: !!lsGet("neet_dev") };
var DEV_TAPS = 0, DEV_TAP_T = 0, _QID_MAP = null;
(function () {
  var h1 = document.querySelector('h1');
  if (!h1) return;
  h1.addEventListener('click', function () {
    var now = Date.now();
    if (now - DEV_TAP_T > 3000) DEV_TAPS = 0;
    DEV_TAP_T = now;
    if (++DEV_TAPS < 5) return;
    DEV_TAPS = 0;
    if (DEV.on) { alert('Dev mode already on.'); return; }
    var pin = prompt('Dev PIN:');
    if (pin === DEV_PIN) {
      lsSet('neet_dev', '1'); DEV.on = true;
      alert('Dev mode on. Fix buttons now appear under explanations.');
      var av = document.querySelector('.view.active');
      if (av) showView(av.id);
    } else if (pin !== null) { alert('Wrong PIN.'); }
  });
  document.addEventListener('click', function (e) {
    var b = e.target;
    while (b && b !== document && !(b.className && String(b.className).indexOf('ex-fixbtn') !== -1)) b = b.parentNode;
    if (b && b !== document) { e.preventDefault(); editExDialog(b.getAttribute('data-qid')); }
  });
})();
var FIREBASE_CONFIG = {''')

# b) formatEx: 2nd param qid + FIXMAP override at top
sub(r'''function formatEx(raw) {
  if (!raw) return '';''',
r'''function formatEx(raw, qid) {
  if (!raw) return '';
  if (qid && FIXMAP[qid]) raw = FIXMAP[qid];''')

# c) formatEx: dev-mode fix button around return
sub(r'''  flushBullets();

  return html;
}''',
r'''  flushBullets();

  if (DEV.on && qid) {
    return '<div class="ex-edit">' + html + '<div style="margin-top:8px"><button class="ex-fixbtn" data-qid="' + qid + '" style="font-size:.8rem;padding:4px 10px;border:1px solid var(--panel2);border-radius:6px;background:var(--panel);cursor:pointer">\u270f Fix explanation</button></div></div>';
  }
  return html;
}''')

# d) call site 1: openRepQ dialog
sub(r"""'<div class="ex-box" style="margin-top:8px">' + formatEx(q.ex) + '</div>'""",
    r"""'<div class="ex-box" style="margin-top:8px">' + formatEx(q.ex, q.qid) + '</div>'""")

# e) call sites 2+3: renderQuestion + grade (identical strings)
sub(r"""'</span><div class="explain">' + formatEx(q.ex) + '</div>'""",
    r"""'</span><div class="explain">' + formatEx(q.ex, q.qid) + '</div>'""", 2)

# f) call site 4: openReview
sub(r"""'</span><div>' + formatEx(q.ex) + '</div></div></div>';""",
    r"""'</span><div>' + formatEx(q.ex, q.qid) + '</div></div></div>';""")

# g) editor dialog + helpers before showDialog
sub(r'''function showDialog(html) {''',
r'''function qByQid(qid) {
  if (!_QID_MAP) {
    _QID_MAP = {};
    BANK.concat(PAPER).forEach(function (qq) { if (qq.qid) _QID_MAP[qq.qid] = qq; });
  }
  return _QID_MAP[qid];
}
function editExDialog(qid) {
  var q = qByQid(qid);
  if (!q) { alert('Question ' + qid + ' not found.'); return; }
  var cur = (FIXMAP[qid] !== undefined) ? FIXMAP[qid] : (q.ex || '');
  var html = '<div class="score-note" style="margin-bottom:6px"><b>' + qid + '</b> \u2014 raw markup: **bold**, | col1 | col2 |, * bullets</div>' +
    '<textarea id="exEditArea" rows="10" style="width:100%;font-family:monospace;font-size:.82rem">' + escapeHtml(cur) + '</textarea>' +
    '<div class="score-note" style="margin-top:6px">Preview:</div>' +
    '<div id="exEditPrev" style="margin-top:4px;max-height:220px;overflow:auto"></div>' +
    '<div class="ctrl" style="margin-top:10px">' +
    '<button class="btn" id="exSave">Save</button>' +
    '<button class="btn secondary" id="exCancel">Cancel</button>' +
    (FIXMAP[qid] !== undefined ? '<button class="btn secondary" id="exReset">Reset to original</button>' : '') +
    '</div>';
  showDialog(html);
  exEditPrev();
  $('exEditArea').addEventListener('input', exEditPrev);
  $('exSave').addEventListener('click', function () {
    var v = $('exEditArea').value;
    if (v.trim()) FIXMAP[qid] = v; else delete FIXMAP[qid];
    lsSet('neet_exfix', FIXMAP);
    location.reload();
  });
  $('exCancel').addEventListener('click', function () { document.querySelector('#dlgClose').click(); });
  var rs = $('exReset');
  if (rs) rs.addEventListener('click', function () {
    delete FIXMAP[qid];
    lsSet('neet_exfix', FIXMAP);
    location.reload();
  });
}
function exEditPrev() {
  var el = $('exEditPrev');
  if (el) el.innerHTML = formatEx($('exEditArea').value, null);
}
function devExport() {
  lsSet('neet_exfix_export', FIXMAP);
  var json = JSON.stringify(FIXMAP, null, 2);
  showDialog('<div class="score-note" style="margin-bottom:6px">Fix queue JSON \u2014 copied to clipboard. Paste it back to the developer to apply to the bank files.</div>' +
    '<textarea id="exExpArea" rows="12" style="width:100%;font-family:monospace;font-size:.72rem" readonly>' + escapeHtml(json) + '</textarea>');
  var ta = $('exExpArea');
  if (ta) { ta.focus(); ta.select(); try { document.execCommand('copy'); } catch (e) {} }
}
function showDialog(html) {''')

# h) dev panel at end of syncUI (both signed-in and signed-out states)
sub(r'''    $('accReset').addEventListener('click', function (e) { e.preventDefault(); syncResetPw(); });
  }
}''',
r'''    $('accReset').addEventListener('click', function (e) { e.preventDefault(); syncResetPw(); });
  }
  if (DEV.on) {
    var n = 0, lh = '';
    for (var kk in FIXMAP) {
      n++;
      lh += '<div class="score-note" style="font-size:.78rem;margin-top:2px">' + kk + ' \u2014 ' + escapeHtml(String(FIXMAP[kk]).substring(0, 45)) + '</div>';
    }
    body.innerHTML += '<div class="score-note" style="margin-top:12px;border-top:1px solid var(--panel2);padding-top:8px"><b>Dev fixes queued: ' + n + '</b></div>' + lh +
      '<div class="fit-row" style="margin-top:8px">' +
      '<button class="btn small" id="exExport">Export fixes JSON</button>' +
      '<button class="btn small secondary" id="exUndoAll">Undo all</button>' +
      '<button class="btn small secondary" id="exOff">Dev mode off</button></div>' +
      '<div class="score-note" style="margin-top:8px;font-size:.78rem">Tap the app title 5\u00d7 to re-enable. Queued fixes reach everyone only after the developer applies the exported JSON to the bank files.</div>';
    $('exExport').addEventListener('click', devExport);
    $('exUndoAll').addEventListener('click', function () {
      if (!confirm('Remove all ' + n + ' queued fixes?')) return;
      lsSet('neet_exfix', {}); FIXMAP = {};
      syncUI();
    });
    $('exOff').addEventListener('click', function () {
      lsSet('neet_dev', ''); DEV.on = false;
      syncUI();
    });
  }
}''')

# i) cache-busting version bumps for bank files
sub('bank.js?v=10', 'bank.js?v=11')
sub('core_btr.js?v=5', 'core_btr.js?v=6')

assert d.count('\x00') == 12, 'NUL post: %d' % d.count('\x00')
io.open(P, 'w', encoding='utf-8', newline='').write(d)
print('patched OK — NUL 12 pre/post, all anchors asserted')
