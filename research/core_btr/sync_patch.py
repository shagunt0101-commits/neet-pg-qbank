# -*- coding: utf-8 -*-
"""Byte-stable patch of questions/science.html: Firebase sync.

science.html contains 12 intentional NUL sentinel bytes (table-extraction
regexes). The Edit tool corrupts them, so this script does rb->utf-8
decode->str.replace on unique anchors->wb write. Verify NUL count == 12
before and after.
"""
import sys, re

sys.stdout.reconfigure(encoding='utf-8')
PATH = r'F:\NEET PG\questions\science.html'

with open(PATH, 'rb') as f:
    raw = f.read()
nul_before = raw.count(b'\x00')
print(f'NUL bytes before: {nul_before}')
assert nul_before == 12, nul_before

s = raw.decode('utf-8')

def rep(old, new, count=1, label=''):
    global s
    n = s.count(old)
    if n == 0:
        # already applied — allow rerun safety
        return
    if count is not None:
        assert n == count, f'anchor count {n} != {count}: {label or old[:60]!r}'
    s = s.replace(old, new)

# 1) Account tab button (after Bookmarks tab)
rep('    <button class="tab" data-v="marks">Bookmarks</button>',
    '    <button class="tab" data-v="marks">Bookmarks</button>\n'
    '    <button class="tab" data-v="account">Account</button>',
    label='account tab')

# 2) Account view div (before QUIZ view)
rep('  <!-- QUIZ -->',
    '  <!-- ACCOUNT -->\n'
    '  <div id="account" class="view">\n'
    '    <div class="card">\n'
    '      <h3 style="margin-bottom:10px;">Account \u2014 Cloud Sync</h3>\n'
    '      <div id="accStatus" class="score-note">Loading\u2026</div>\n'
    '      <div id="accBody" style="margin-top:12px"></div>\n'
    '    </div>\n'
    '  </div>\n\n'
    '  <!-- QUIZ -->',
    label='account view')

# 3) Firebase SDK tags (before bank scripts)
rep('<script src="/questions/bank.js?v=7"></script>',
    '<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>\n'
    '<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-auth.js"></script>\n'
    '<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-firestore.js"></script>\n'
    '<script src="/questions/bank.js?v=7"></script>',
    label='sdk tags')

# 4) Firebase config (after REVIEW)
rep('var REVIEW = null;',
    'var REVIEW = null;\n'
    'var FIREBASE_CONFIG = {\n'
    '  apiKey: "AIzaSyAtrT9MUftaETLK6POs3lwy3oFsHd6ALs4",\n'
    '  authDomain: "neet-pg-qbank.firebaseapp.com",\n'
    '  projectId: "neet-pg-qbank",\n'
    '  storageBucket: "neet-pg-qbank.firebasestorage.app",\n'
    '  messagingSenderId: "480539373023",\n'
    '  appId: "1:480539373023:web:e203cb7ce2460a552ce86a"\n'
    '};',
    label='config')

# 5) lsSet2 at the 7 data write sites (exact indented strings)
SITES = [
    '  lsSet(\'neet_hist\', {});',            # repClear
    '    lsSet(\'neet_hist\', hist);',        # grade
    '  lsSet(\'neet_marks\', marks);',        # toggleMark
    '  lsSet(\'neet_results\', results);',    # finish
    '      tests.splice(parseInt(b.dataset.d, 10), 1);\r\n      lsSet(\'neet_tests\', tests);',  # test delete (anchored on splice line)
    '      lsSet(\'neet_results\', res);',    # result delete
    '  tests.unshift(t);\r\n  lsSet(\'neet_tests\', tests);',  # test create (anchored on unshift line)
]
for site in SITES:
    rep(site, site.replace('lsSet(', 'lsSet2('), label='lsSet2 site')

# 6) Sync engine (after lsSet definition)
ENGINE = r'''function lsSet2(k, v) { lsSet(k, v); if (SYNC_KEYS.indexOf(k) !== -1) syncPush(); }

/* ---------------- Firebase sync ---------------- */
var SYNC = { f: null, db: null, user: null, lsn: null, dirty: false, timer: null, init: false };
var SYNC_KEYS = ['neet_hist', 'neet_results', 'neet_marks', 'neet_tests'];

function syncInit() {
  if (SYNC.init) return;
  SYNC.init = true;
  if (!FIREBASE_CONFIG || !FIREBASE_CONFIG.projectId) return; // no config — sync off
  SYNC.f = firebase.initializeApp(FIREBASE_CONFIG);
  SYNC.db = firebase.firestore(SYNC.f);
  if (SYNC.db.enablePersistence) {
    SYNC.db.enablePersistence({ synchronizeTabs: true }).catch(function () {});
  }
  firebase.auth(SYNC.f).onAuthStateChanged(syncAfterAuth);
}

function syncAfterAuth(u) {
  if (SYNC.lsn) { SYNC.lsn(); SYNC.lsn = null; }
  SYNC.user = u;
  if (u) {
    SYNC.lsn = SYNC.db.collection('users').doc(u.uid).onSnapshot(function (snap) {
      if (!SYNC.user) return;
      var d = snap.data();
      if (!d) { syncPush(); return; } // first login: seed doc from local
      syncMerge(d);
    }, function (err) { console.warn('sync snapshot err', err); });
    syncPush(); // ensure latest local state is up
  }
  syncUI();
}

function syncUI() {
  var st = $('accStatus'), body = $('accBody');
  if (!st || !body) return;
  if (!SYNC.init || !SYNC.f) { st.innerHTML = 'Sync disabled \u2014 Firebase not configured.'; body.innerHTML = ''; return; }
  if (SYNC.user) {
    st.innerHTML = 'Signed in as <b>' + SYNC.user.email + '</b> \u2014 progress auto-syncs across devices.';
    body.innerHTML = '<div class="fit-row"><button class="btn secondary" id="accLogout">Sign out</button></div>' +
      '<div class="score-note" style="margin-top:10px">Offline answers queue and sync when you reconnect. Merge is a union \u2014 nothing gets overwritten.</div>';
    var lo = $('accLogout');
    if (lo) lo.addEventListener('click', function () { firebase.auth(SYNC.f).signOut().catch(function (e) { console.warn(e); }); });
  } else {
    st.innerHTML = 'Not signed in \u2014 progress stays on this device only.';
    body.innerHTML = '<div class="fit-row">' +
      '<div><label>Email</label><input id="accEmail" type="email" style="width:230px"></div>' +
      '<div><label>Password</label><input id="accPass" type="password" style="width:230px"></div>' +
      '<div style="flex-direction:row"><button class="btn" id="accLogin">Sign in</button>' +
      '<button class="btn secondary" id="accSignup">Create account</button></div></div>' +
      '<div class="score-note" style="margin-top:10px"><a href="#" id="accReset">Forgot password?</a></div>';
    $('accLogin').addEventListener('click', syncLogin);
    $('accSignup').addEventListener('click', syncSignup);
    $('accReset').addEventListener('click', function (e) { e.preventDefault(); syncResetPw(); });
  }
}

function syncLogin() {
  var email = $('accEmail').value.trim(), pw = $('accPass').value;
  if (!email || !pw) { alert('Enter email and password.'); return; }
  firebase.auth(SYNC.f).signInWithEmailAndPassword(email, pw).catch(function (e) { alert('Sign-in failed: ' + e.message); });
}
function syncSignup() {
  var email = $('accEmail').value.trim(), pw = $('accPass').value;
  if (!email || pw.length < 6) { alert('Enter email and a password of at least 6 characters.'); return; }
  firebase.auth(SYNC.f).createUserWithEmailAndPassword(email, pw).catch(function (e) { alert('Sign-up failed: ' + e.message); });
}
function syncResetPw() {
  var email = $('accEmail').value.trim();
  if (!email) { alert('Enter your email first.'); return; }
  firebase.auth(SYNC.f).sendPasswordResetEmail(email).then(function () { alert('Reset link sent to ' + email); }).catch(function (e) { alert(e.message); });
}

function syncPush() {
  if (!SYNC.user || !SYNC.db) return;
  SYNC.dirty = true;
  if (SYNC.timer) clearTimeout(SYNC.timer);
  SYNC.timer = setTimeout(doPush, 1500);
}
function doPush() {
  SYNC.timer = null;
  if (!SYNC.dirty || !SYNC.user) return;
  SYNC.dirty = false;
  SYNC.db.collection('users').doc(SYNC.user.uid).set({
    hist: lsGet('neet_hist') || {},
    results: lsGet('neet_results') || [],
    marks: lsGet('neet_marks') || {},
    tests: lsGet('neet_tests') || [],
    synced: firebase.firestore.FieldValue.serverTimestamp()
  }).catch(function (e) { console.warn('sync push err', e); SYNC.dirty = true; });
}

function syncMerge(d) {
  if (!SYNC.user) return;
  var c = mergeHist(d.hist || {}) + mergeMarks(d.marks || {}) + mergeResults(d.results || []) + mergeTests(d.tests || []);
  if (!c) return;
  if ($('dash').classList.contains('active')) renderDash();
  if ($('report').classList.contains('active')) { fillRepSubj(); renderReport(); }
  if ($('marks').classList.contains('active')) renderMarks();
  syncPush(); // merged result goes back up
}

function mergeHist(remote) {
  var hist = lsGet('neet_hist') || {};
  var c = 0;
  for (var k in remote) {
    var r = remote[k];
    if (!r || typeof r !== 'object') continue;
    var l = hist[k];
    if (!l) { hist[k] = r; c++; continue; }
    var nr = (r.ts || 0) > (l.ts || 0) ? r : l; // newer record wins scalars
    var merged = {};
    for (var kk in nr) merged[kk] = nr[kk];
    merged.times = unionTimes(l.times || [], r.times || []);
    if (JSON.stringify(merged) !== JSON.stringify(l)) { hist[k] = merged; c++; }
  }
  if (c) lsSet('neet_hist', hist);
  return c;
}
function unionTimes(a, b) { // ponytail: dedup by outcome+rounded sec, collisions rare
  var seen = {}, out = [];
  for (var i = 0; i < a.length; i++) {
    var t = a[i];
    var key = (t.c ? '1' : '0') + '-' + Math.round(t.sec || 0);
    if (!seen[key]) { seen[key] = true; out.push(t); }
  }
  for (var j = 0; j < b.length; j++) {
    var t2 = b[j];
    var key2 = (t2.c ? '1' : '0') + '-' + Math.round(t2.sec || 0);
    if (!seen[key2]) { seen[key2] = true; out.push(t2); }
  }
  return out;
}

function mergeMarks(remote) {
  var local = lsGet('neet_marks') || {};
  var c = 0;
  // map question stem -> local key ('123' bank index or 'p0' paper)
  var idx = {};
  for (var i = 0; i < BANK.length; i++) {
    var q = BANK[i];
    if (q && q.q) idx[q.q.substring(0, 50)] = String(i);
  }
  for (var j = 0; j < PAPER.length; j++) {
    var p = PAPER[j];
    if (p && p.q) idx[p.q.substring(0, 50)] = 'p' + j;
  }
  var union = {};
  var take = function (key, m) {
    var q = qAt(key);
    var stem = q && q.q ? q.q.substring(0, 50) : key;
    if (!union[stem] && idx[stem] !== undefined) { union[stem] = m; c++; }
  };
  for (var k in local) take(k, local[k]);
  for (var k2 in remote) take(k2, remote[k2]);
  if (!c) return 0;
  var out = {};
  for (var s in union) out[idx[s]] = union[s];
  lsSet('neet_marks', out);
  return c;
}

function mergeResults(remote) {
  var local = lsGet('neet_results') || [];
  var c = 0;
  var byId = {};
  var maxId = 0;
  local.forEach(function (r) { if (r && r.id) { byId[r.id] = r; if (r.id > maxId) maxId = r.id; } });
  remote.forEach(function (r) {
    if (!r || !r.id) return;
    if (byId[r.id]) {
      var l = byId[r.id];
      if (l.name === r.name && l.t === r.t) return; // duplicate
      r.id = ++maxId; // same-millisecond collision, different content: keep both
    }
    byId[r.id] = r;
    c++;
  });
  if (!c) return 0;
  var out = [];
  for (var id in byId) out.push(byId[id]);
  out.sort(function (a, b) { return b.id - a.id; });
  lsSet('neet_results', out);
  return c;
}

function mergeTests(remote) {
  var local = lsGet('neet_tests') || [];
  var c = 0;
  var byName = {};
  local.forEach(function (t) { if (t && t.name) byName[t.name] = t; });
  remote.forEach(function (t) {
    if (!t || !t.name) return;
    var l = byName[t.name];
    if (!l) { byName[t.name] = t; c++; }
    else if ((t.n || 0) > (l.n || 0)) { byName[t.name] = t; c++; }
  });
  if (!c) return 0;
  var out = [];
  for (var n in byName) out.push(byName[n]);
  lsSet('neet_tests', out);
  return c;
}

window.addEventListener('beforeunload', function () {
  if (SYNC.dirty && SYNC.user) { SYNC.dirty = false; doPush(); }
});
'''
rep('function lsSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }',
    'function lsSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }\n' + ENGINE,
    label='engine')

# 7) showView — account render hook in BOTH defs (replace_all)
rep('  if (v === \'marks\') renderMarks();',
    '  if (v === \'marks\') renderMarks();\n  if (v === \'account\') syncUI();',
    count=2, label='showView marks')

# 8) Startup: syncInit after renderDash
rep('renderDash();\r\n</script>',
    'renderDash();\r\ntry { syncInit(); } catch (e) { console.warn(\'sync disabled\', e); }\r\n</script>',
    label='startup')

# --- post checks ---
with open(PATH, 'wb') as f:
    f.write(s.encode('utf-8'))
nul_after = s.encode('utf-8').count(b'\x00')
print(f'NUL bytes after:  {nul_after}')
assert nul_after == 12, nul_after
assert s.count('function lsSet2') == 1
assert s.count('lsSet2(') == 8  # 1 def + 7 call sites
assert s.count('syncInit') == 2  # def + startup call
print('patch OK')
