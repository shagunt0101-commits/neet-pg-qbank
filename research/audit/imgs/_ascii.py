from PIL import Image
import numpy as np
import sys
f = sys.argv[1]
im = Image.open(f).convert('L')
a = np.array(im)
chars = ' .:*#@'
scale_x = max(1, a.shape[1] // 120)
scale_y = max(1, a.shape[0] // 96)
for y0 in range(0, a.shape[0], scale_y):
    line = []
    for x0 in range(0, a.shape[1], scale_x):
        v = a[y0:y0+scale_y, x0:x0+scale_x].mean()
        line.append(chars[min(5, int((255-v)/255*5.99))])
    print(''.join(line))