# 카드뒤집기 캐릭터 시트(1024x1024)를 8x6 격자로 잘라 개별 타일 PNG로 저장하는 스크립트
import os
from PIL import Image
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'assets', 'characters.png')
OUT = os.path.join(BASE, 'assets', 'cards')
os.makedirs(OUT, exist_ok=True)

im = Image.open(SRC).convert('RGB')
W, H = im.size
COLS, ROWS = 8, 6
cw, ch = W / COLS, H / ROWS
INSET = 0.05  # 각 셀 가장자리 5% 잘라 옆 캐릭터 침범 제거


def ink_density(box):
    a = np.asarray(im.crop(box)).astype(int)
    mx = a.max(2); mn = a.min(2)
    return (((mx - mn) > 60) | (mx < 90)).mean()


idx = 0
saved = []
for r in range(ROWS):
    for c in range(COLS):
        x0, y0 = c * cw, r * ch
        x1, y1 = (c + 1) * cw, (r + 1) * ch
        if ink_density((x0, y0, x1, y1)) < 0.06:  # 빈 칸 건너뛰기
            continue
        ix = (x1 - x0) * INSET
        iy = (y1 - y0) * INSET
        crop = im.crop((round(x0 + ix), round(y0 + iy), round(x1 - ix), round(y1 - iy)))
        idx += 1
        crop.save(os.path.join(OUT, f'card{idx:02d}.png'))
        saved.append(crop)

# 검증용 컨택트시트
n = len(saved)
ccols = 8
crows = (n + ccols - 1) // ccols
tw, th = 120, 150
sheet = Image.new('RGB', (ccols * tw, crows * th), (255, 255, 255))
for i, t in enumerate(saved):
    tt = t.copy(); tt.thumbnail((tw - 8, th - 8))
    px = (i % ccols) * tw + (tw - tt.width) // 2
    py = (i // ccols) * th + (th - tt.height) // 2
    sheet.paste(tt, (px, py))
sheet.save(os.path.join(BASE, 'assets', '_contact.png'))
print(f'saved {n} tiles')
