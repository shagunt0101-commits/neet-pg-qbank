const fs = require('fs');
const s = fs.readFileSync('F:/NEET PG/questions/test_2026.js', 'utf8');
const a = JSON.parse(s.slice(s.indexOf('['), s.lastIndexOf(']') + 1));
console.log('bytes:', s.length, '| qs:', a.length, '| qids:', a[0].qid, '...', a[199].qid);
console.log('all 4 opts:', a.every(x => x.o.length === 4), '| a 0-3:', a.every(x => x.a >= 0 && x.a <= 3));
const imgs = a.filter(x => x.img);
console.log('image qs:', imgs.length, '| all have imgdata:', imgs.length && imgs.every(x => Array.isArray(x.imgdata) && x.imgdata.length));
const order = a.map(x => x.s); const uniq = [...new Set(order)];
console.log('subjects:', uniq.length, '| first:', order.slice(0, 11).join(','), '| last:', order.slice(189).join(','));
console.log('fix checks:',
  'heat-stable:', a[70].ex.includes('heat-stable'),
  '| 1.8%:', a[81].ex.includes('1.8%'),
  '| 19.5:', a[149].ex.includes('19.5'),
  '| 40mL/kg:', a[155].q.includes('40 mL/kg'),
  '| first-tri:', a[121].q.includes('first trimester'),
  '| 12mmHg:', a[152].ex.includes('12 mmHg'),
  '| high-risk:', a[118].ex.includes('high-risk'),
  '| domperidone-12wk:', a[55].ex.includes('12 weeks'),
  '| ISPAD-now:', a[153].ex.includes('added now'),
  '| TTTS:', a[148].ex.includes('not present here'));
