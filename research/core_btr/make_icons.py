# -*- coding: utf-8 -*-
"""Generate PWA icons: accent-blue rounded background + white 'Q'."""
import os
from PIL import Image, ImageDraw, ImageFont

ACCENT = '#0891b2'
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'icons')
os.makedirs(OUT, exist_ok=True)


def icon(size, maskable=False):
    im = Image.new('RGB', (size, size), ACCENT)
    d = ImageDraw.Draw(im)
    # white rounded square (Q card), 60% of size, centered; maskable safe zone 80%
    card = int(size * 0.60)
    pad = (size - card) // 2
    d.rounded_rectangle([pad, pad, pad + card, pad + card], radius=int(card * 0.22), fill='#ffffff')
    # Q letter
    try:
        font = ImageFont.truetype('arialbd.ttf', int(card * 0.55))
    except Exception:
        font = ImageFont.load_default()
    bbox = d.textbbox((0, 0), 'Q', font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((size // 2 - tw / 2 - bbox[0], size // 2 - th / 2 - bbox[1]), 'Q',
           font=font, fill=ACCENT)
    return im


for size, maskable in [(512, False), (512, True), (192, False)]:
    im = icon(size, maskable)
    name = f'icon-{size}{"-maskable" if maskable else ""}.png'
    im.save(os.path.join(OUT, name))
    print('wrote', name, os.path.getsize(os.path.join(OUT, name)), 'bytes')
