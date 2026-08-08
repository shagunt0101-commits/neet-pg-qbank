from PIL import Image
import os

def montage(files, out):
    ims = [Image.open(os.path.join('research/audit/imgs', f + '.jpg')) for f in files]
    cols = 4
    cellw = max(i.width for i in ims)
    cellh = max(i.height for i in ims)
    rows = (len(ims) + cols - 1) // cols
    c = Image.new('RGB', (cellw * cols + (cols + 1) * 4, cellh * rows + (rows + 1) * 4), 'white')
    for idx, im in enumerate(ims):
        r, cc = divmod(idx, cols)
        c.paste(im, (4 + cc * (cellw + 4), 4 + r * (cellh + 4)))
    c.save(out)
    return c.size

d = 'research/audit/imgs'
imgs = [f[:7] for f in os.listdir(d) if f.startswith('q1971_') and f.endswith('.jpg')]
imgs.sort()
print(imgs)
full = [f for f in imgs if os.path.getsize(os.path.join(d, f + '.jpg')) > 4000]
tiny = [f for f in imgs if os.path.getsize(os.path.join(d, f + '.jpg')) <= 4000]
print('full sized:', montage(full, 'research/audit/mont_full.png'))
print('tiny:', montage(tiny, 'research/audit/mont_tiny.png'))