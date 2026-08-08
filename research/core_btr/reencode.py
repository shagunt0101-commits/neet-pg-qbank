# -*- coding: utf-8 -*-
"""Convert embedded JPEG imgdata to WebP q80 (full-res) to shrink core_btr.js.

Input:  with_imgs.json   (same dir; 7158 Qs, 1807 with imgdata)
Output: with_imgs_webp.json (intermediate, gitignored)
        questions/core_btr.js  (regenerated, ~66 MB instead of 357 MB)
"""
import json
import os
import io
import base64
import random
from PIL import Image

QUALITY = 80
SRC = 'with_imgs.json'


def to_webp_b64(jpeg_b64):
    raw = base64.b64decode(jpeg_b64)
    im = Image.open(io.BytesIO(raw))
    im = im.convert('RGB')  # strip alpha/palette; all source imgs are JPEG
    buf = io.BytesIO()
    im.save(buf, 'WEBP', quality=QUALITY, method=6)
    return base64.b64encode(buf.getvalue()).decode()


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, SRC), encoding='utf-8') as f:
        data = json.load(f)

    n_q = n_img = n_err = 0
    webp_total = jpeg_total = 0
    for q in data:
        n_q += 1
        if not q.get('imgdata'):
            continue
        n_img += 1
        try:
            new_b64 = [to_webp_b64(d) for d in q['imgdata']]
            webp_total += sum(len(b) for b in new_b64)
            jpeg_total += sum(len(d) for d in q['imgdata'])
            q['imgdata'] = new_b64
        except Exception:
            n_err += 1  # keep original JPEG string; HTML fallback handles it

    with open(os.path.join(base, 'with_imgs_webp.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    js_out = os.path.join(base, '..', '..', 'questions', 'core_btr.js')
    with open(js_out, 'w', encoding='utf-8') as f:
        f.write('window.CORE_BTR = ' + json.dumps(data, ensure_ascii=False) + ';\n')

    print(f'questions={n_q} img_qs={n_img} errors={n_err}')
    print(f'imgdata bytes: {jpeg_total:,} -> {webp_total:,} ({100*webp_total/jpeg_total:.1f}%)')
    print(f'core_btr.js: {os.path.getsize(js_out)/1e6:.1f} MB')

    # self-check: decoded images are WEBP
    # self-check: decoded images are WEBP (base64 of RIFF header starts 'UklG')
    imgs = [d for q in data for d in q.get('imgdata', []) if d and d[0] == 'U']
    random.seed(42)
    for d in random.sample(imgs, min(10, len(imgs))):
        im = Image.open(io.BytesIO(base64.b64decode(d)))
        assert im.format == 'WEBP', im.format
    print('self-check: 10 random imgdata decode as WEBP — OK')


if __name__ == '__main__':
    main()
