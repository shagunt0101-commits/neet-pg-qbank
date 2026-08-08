# -*- coding: utf-8 -*-
"""Audit prep: regenerate fresh chunks from bank.js + extract embedded images to files."""
import io, json, os, re, base64, sys

BANK_PATH = 'questions/bank.js'
OUT_DIR = 'research/audit'
IMG_DIR = os.path.join(OUT_DIR, 'imgs')
CHUNK_SIZE = 200

def load_bank():
    src = io.open(BANK_PATH, encoding='utf-8').read()
    m = re.search(r'window\.QUESTIONS\s*=\s*(\[.*\])\s*;', src, re.S)
    if not m:
        print('Cannot parse bank.js', file=sys.stderr)
        sys.exit(1)
    return json.loads(m.group(1))

def main():
    bank = load_bank()
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)
    # chunks: strip imgdata (huge), keep img flag
    for ci in range(0, len(bank), CHUNK_SIZE):
        chunk = []
        for j, q in enumerate(bank[ci:ci+CHUNK_SIZE]):
            item = {k: v for k, v in q.items() if k != 'imgdata'}
            item['idx'] = ci + j
            chunk.append(item)
        with io.open(os.path.join(OUT_DIR, 'chunk_%d.json' % (ci // CHUNK_SIZE)), 'w', encoding='utf-8') as f:
            json.dump(chunk, f, ensure_ascii=False, indent=0)
    # extract images
    n_img = 0
    for i, q in enumerate(bank):
        if q.get('img') and q.get('imgdata'):
            for k, d in enumerate(q['imgdata']):
                try:
                    raw = base64.b64decode(d)
                except Exception:
                    continue
                fn = os.path.join(IMG_DIR, 'q%04d_%d.jpg' % (i, k))
                with open(fn, 'wb') as f:
                    f.write(raw)
                n_img += 1
    print('chunks written to', OUT_DIR)
    print('images extracted:', n_img)

if __name__ == '__main__':
    main()
