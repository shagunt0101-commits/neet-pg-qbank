# -*- coding: utf-8 -*-
"""Fix 'Sync disabled — Firebase not configured' misleading message.

Root cause: gstatic SDK fails to load → firebase undefined → ReferenceError in
syncInit() caught by startup try/catch → SYNC.init already true, SYNC.f null →
syncUI() prints 'not configured' but real cause was SDK load failure. No retry.

Fix:
1. syncInit: guard, set init=true ONLY on success, capture SYNC.err.
2. syncUI: accurate messages + self-healing retry when Account tab visited.
3. ensureFirebaseSDK: dynamic SDK script injection for retry.
"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

P = r'F:\NEET PG\questions\science.html'
d = io.open(P, 'r', encoding='utf-8').read()
assert d.count('\x00') == 12, 'NUL pre: %d' % d.count('\x00')

def sub(old, new, must=1):
    global d
    if new in d:
        return
    n = d.count(old)
    assert n == must, (old[:80], n, must)
    d = d.replace(old, new)

# a) syncInit: make retryable, set init=true only after success, capture SYNC.err
sub(r'''function syncInit() {
  if (SYNC.init) return;
  SYNC.init = true;
  if (!FIREBASE_CONFIG || !FIREBASE_CONFIG.projectId) return; // no config — sync off
  SYNC.f = firebase.initializeApp(FIREBASE_CONFIG);''',
r'''function syncInit() {
  if (SYNC.init && SYNC.f) return;
  if (!FIREBASE_CONFIG || !FIREBASE_CONFIG.projectId) { SYNC.err = 'no config'; return; }
  if (typeof firebase === 'undefined') { SYNC.err = 'firebase SDK not loaded'; return; }
  SYNC.f = firebase.initializeApp(FIREBASE_CONFIG);
  SYNC.db = firebase.firestore(SYNC.f);
  SYNC.init = true;''')

# b) ensureFirebaseSDK function (before syncInit or anywhere in State section)
sub(r'''var QUIZ_TIME = { test: 10, mock: 180 }; /* minutes; 'mock' = preset paper */
var REVIEW = null;''',
r'''var QUIZ_TIME = { test: 10, mock: 180 }; /* minutes; 'mock' = preset paper */
var REVIEW = null;
function ensureFirebaseSDK(cb) {
  if (typeof firebase !== 'undefined') return cb(true);
  var loaded = 0, total = 3;
  function done() { if (++loaded === total) cb(typeof firebase !== 'undefined'); }
  var urls = [
    'https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js',
    'https://www.gstatic.com/firebasejs/8.10.1/firebase-auth.js',
    'https://www.gstatic.com/firebasejs/8.10.1/firebase-firestore.js'
  ];
  urls.forEach(function (u) {
    var s = document.createElement('script');
    s.src = u;
    s.onload = done;
    s.onerror = function () { done(); console.warn('SDK load failed:', u); };
    document.head.appendChild(s);
  });
}''')

# c) syncUI: accurate messages + auto-retry on Account tab visit
sub(r'''function syncUI() {
  var st = $('accStatus'), body = $('accBody');
  if (!st || !body) return;
  if (!SYNC.init || !SYNC.f) { st.innerHTML = 'Sync disabled \u2014 Firebase not configured.'; body.innerHTML = ''; return; }
  if (SYNC.user) {''',
r'''function syncUI() {
  var st = $('accStatus'), body = $('accBody');
  if (!st || !body) return;
  if (!FIREBASE_CONFIG || !FIREBASE_CONFIG.projectId) {
    st.innerHTML = 'Sync disabled \u2014 Firebase not configured.';
    body.innerHTML = '';
    return;
  }
  if (!SYNC.f) {
    if (typeof firebase !== 'undefined') {
      try { syncInit(); } catch (e) { SYNC.err = String(e && e.message || e); }
    } else {
      ensureFirebaseSDK(function (ok) {
        if (ok) { try { syncInit(); } catch (e) { SYNC.err = String(e && e.message || e); } }
        var st2 = $('accStatus'), body2 = $('accBody');
        if (st2 && body2) syncUI(); // re-render after retry
      });
    }
    st.innerHTML = 'Sync unavailable \u2014 Firebase SDK failed to load. Retrying...' + (SYNC.err ? ' (' + SYNC.err + ')' : '');
    body.innerHTML = '';
    return;
  }
  if (SYNC.user) {''')

# d) startup try/catch: remove (syncInit now handles its own errors)
sub(r'''try { syncInit(); } catch (e) { console.warn('sync disabled', e); }''',
r'''try { syncInit(); } catch (e) { SYNC.err = String(e && e.message || e); console.warn('sync init error', e); }''')

assert d.count('\x00') == 12, 'NUL post: %d' % d.count('\x00')
io.open(P, 'w', encoding='utf-8', newline='').write(d)
print('patched OK — NUL 12 pre/post, all anchors asserted')