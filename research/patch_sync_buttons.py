# -*- coding: utf-8 -*-
"""Add manual Push / Pull sync buttons to Account tab (signed-in view)."""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'F:\NEET PG\questions\science.html'
d = io.open(p, 'r', encoding='utf-8', errors='replace').read()
nul0 = d.count('\x00')
nl = '\n'

# 1) syncUI signed-in body: add buttons row + status line
old1 = """    body.innerHTML = '<div class="fit-row"><button class="btn secondary" id="accLogout">Sign out</button></div>' +
      '<div class="score-note" style="margin-top:10px">Offline answers queue and sync when you reconnect. Merge is a union \\u2014 nothing gets overwritten.</div>';
    var lo = $('accLogout');
    if (lo) lo.addEventListener('click', function () { firebase.auth(SYNC.f).signOut().catch(function (e) { console.warn(e); }); });"""
assert d.count(old1) == 1, 'anchor1 count %d' % d.count(old1)
new1 = """    body.innerHTML = '<div class="fit-row"><button class="btn secondary" id="accLogout">Sign out</button></div>' +
      '<div class="fit-row"><button class="btn" id="accSyncPush">Push to cloud</button><button class="btn secondary" id="accSyncPull">Pull from cloud</button></div>' +
      '<div class="score-note" id="accSyncStatus" style="margin-top:10px"></div>' +
      '<div class="score-note" style="margin-top:10px">Offline answers queue and sync when you reconnect. Merge is a union \\u2014 nothing gets overwritten.</div>';
    var lo = $('accLogout');
    if (lo) lo.addEventListener('click', function () { firebase.auth(SYNC.f).signOut().catch(function (e) { console.warn(e); }); });
    var pu = $('accSyncPush');
    if (pu) pu.addEventListener('click', syncNow);
    var pl = $('accSyncPull');
    if (pl) pl.addEventListener('click', syncPullNow);"""
d = d.replace(old1, new1)

# 2) syncMerge: return change count so the button can report
old2 = """function syncMerge(d) {
  if (!SYNC.user) return;
  var c = mergeHist(d.hist || {}) + mergeMarks(d.marks || {}) + mergeResults(d.results || []) + mergeTests(d.tests || []);
  if (!c) return;
  if ($('dash').classList.contains('active')) renderDash();
  if ($('report').classList.contains('active')) { fillRepSubj(); renderReport(); }
  if ($('marks').classList.contains('active')) renderMarks();
  syncPush(); // merged result goes back up
}"""
assert d.count(old2) == 1, 'anchor2 count %d' % d.count(old2)
new2 = """function syncMerge(d) {
  if (!SYNC.user) return 0;
  var c = mergeHist(d.hist || {}) + mergeMarks(d.marks || {}) + mergeResults(d.results || []) + mergeTests(d.tests || []);
  if (c) {
    if ($('dash').classList.contains('active')) renderDash();
    if ($('report').classList.contains('active')) { fillRepSubj(); renderReport(); }
    if ($('marks').classList.contains('active')) renderMarks();
  }
  syncPush(); // merged result goes back up
  return c;
}
function syncNow() {
  if (!SYNC.user) { alert('Sign in first.'); return; }
  doPush();
  syncStatus('Pushed local progress to cloud.');
}
function syncPullNow() {
  if (!SYNC.user) { alert('Sign in first.'); return; }
  syncStatus('Pulling from cloud…');
  SYNC.db.collection('users').doc(SYNC.user.uid).get().then(function (snap) {
    var dd = snap.data();
    if (!dd) { syncStatus('Cloud doc empty — nothing to pull.'); return; }
    var n = syncMerge(dd);
    syncStatus(n ? ('Pulled and merged ' + n + ' changes.') : 'Already up to date.');
  }).catch(function (e) { syncStatus('Pull failed: ' + e.message); });
}
function syncStatus(m) {
  var el = $('accSyncStatus');
  if (el) el.textContent = m;
}"""
d = d.replace(old2, new2)

nul1 = d.count('\x00')
assert nul0 == nul1, 'NUL changed %d -> %d' % (nul0, nul1)
io.open(p, 'w', encoding='utf-8', newline='').write(d)
print('patched. NUL:', nul0, '->', nul1)
