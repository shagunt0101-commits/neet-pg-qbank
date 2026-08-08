// Inject image-based questions into test_2026.js at fixed slots (every 10th, from Q20).
// Reuses real bank questions with embedded base64 imgdata (no image files exist for new stems).
const fs = require('fs');
const pf = 'F:/NEET PG/questions/test_2026.js';
const bf = 'F:/NEET PG/questions/bank.js';
const ps = fs.readFileSync(pf, 'utf8');
const paper = JSON.parse(ps.slice(ps.indexOf('['), ps.lastIndexOf(']') + 1));
const bs = fs.readFileSync(bf, 'utf8');
const bank = JSON.parse(bs.slice(bs.indexOf('['), bs.lastIndexOf(']') + 1));
const byId = {}; bank.forEach(x => { byId[x.qid] = x; });

// chosen bank image questions, one per slot (order = slot order)
const PICK = ['q1212', 'q2239', 'q1823', 'q1818', 'q2731', 'q1582', 'q1138', 'q2010', 'q2523', 'q2167',
  'q1158', 'q1708', 'q1852', 'q1533', 'q1187', 'q2658', 'q1937', 'q1204', 'q971', 'q990'];
const SLOTS = [19, 29, 39, 49, 59, 69, 79, 89, 99, 109, 119, 129, 139, 149, 159, 169, 179, 189, 194, 199];

if (PICK.length !== SLOTS.length) throw new Error('pick/slot mismatch');
SLOTS.forEach((slot, i) => {
  const src = byId[PICK[i]];
  if (!src) throw new Error('missing bank qid ' + PICK[i]);
  const old = paper[slot];
  // keep paper identity: qid, exam/year/src, but swap content + image
  paper[slot] = {
    qid: old.qid, e: 'NEET PG', y: '2026', src: 'paper2026',
    q: src.q, o: src.o.slice(), a: src.a, ex: src.ex, tp: src.tp, s: src.s,
    img: true, imgdata: src.imgdata,
  };
  console.log('slot', slot, '<-', PICK[i], '(' + src.s + ')', 'replaced', old.tp);
});

fs.writeFileSync(pf, 'window.TEST_2026 = ' + JSON.stringify(paper) + ';\n');
console.log('written', paper.length, 'questions;', paper.filter(x => x.img).length, 'with images');
