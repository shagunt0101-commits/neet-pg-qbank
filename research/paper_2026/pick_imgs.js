const fs = require('fs');
const s = fs.readFileSync('F:/NEET PG/questions/bank.js', 'utf8');
const a = JSON.parse(s.slice(s.indexOf('['), s.lastIndexOf(']') + 1));
const img = a.filter(x => x.img && Array.isArray(x.imgdata) && x.imgdata.length);
console.log('total img qs:', img.length);
// pick 1 per subject: smallest total base64 (load perf), keep distribution
const byS = {};
img.forEach(x => { (byS[x.s] = byS[x.s] || []).push(x); });
const subjects = Object.keys(byS).sort((x, y) => byS[y].length - byS[x].length);
const picks = [];
const used = new Set();
for (const subj of subjects) {
  if (picks.length >= 20) break;
  const pool = byS[subj].filter(x => !used.has(x.qid));
  if (!pool.length) continue;
  pool.sort((x, y) => x.imgdata.join('').length - y.imgdata.join('').length);
  picks.push(pool[0]);
  used.add(pool[0].qid);
}
console.log('picks:', picks.length);
picks.forEach(x => console.log(x.qid, '|', x.s, '|', x.tp, '| imgs:' + x.imgdata.length, '| KB:' + Math.round(x.imgdata.join('').length * 3 / 4 / 1024)));
fs.writeFileSync('F:/NEET PG/research/paper_2026/picked.json', JSON.stringify(picks.map(x => x.qid)));
