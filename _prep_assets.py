# 빌런 스프라이트 시트의 흰 배경(테두리 연결 영역만)을 투명 처리하는 전처리 스크립트
import numpy as np
from PIL import Image

SRC = "빌런 모델.png"
DST = "빌런_투명.png"

img = Image.open(SRC).convert("RGBA")
arr = np.array(img)
h, w = arr.shape[:2]
r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]

# 흰색 후보: 세 채널 모두 밝고 채도 낮음
white = (r > 235) & (g > 235) & (b > 235)

# 테두리에 연결된 흰색만 배경으로 간주 (내부 흰 디테일 보존)
visited = np.zeros((h, w), dtype=bool)
stack = []
for x in range(w):
    if white[0, x]:
        stack.append((0, x))
    if white[h - 1, x]:
        stack.append((h - 1, x))
for y in range(h):
    if white[y, 0]:
        stack.append((y, 0))
    if white[y, w - 1]:
        stack.append((y, w - 1))

# 반복 BFS (numpy dilation으로 가속)
bg = np.zeros((h, w), dtype=bool)
for (y, x) in stack:
    bg[y, x] = True
while True:
    grown = bg.copy()
    grown[1:, :] |= bg[:-1, :]
    grown[:-1, :] |= bg[1:, :]
    grown[:, 1:] |= bg[:, :-1]
    grown[:, :-1] |= bg[:, 1:]
    grown &= white  # 흰색 영역 안에서만 확장
    if np.array_equal(grown, bg):
        break
    bg = grown

# 배경은 완전 투명
arr[bg, 3] = 0

# 디프린지: 배경과 인접한 밝은 잔여 픽셀의 alpha를 밝기에 따라 감쇠 (흰 테두리 제거)
edge = np.zeros((h, w), dtype=bool)
edge[1:, :] |= bg[:-1, :]
edge[:-1, :] |= bg[1:, :]
edge[:, 1:] |= bg[:, :-1]
edge[:, :-1] |= bg[:, 1:]
edge &= ~bg
bright = (r.astype(int) + g + b) / 3.0
fringe = edge & (bright > 215)
fade = np.clip((255 - bright) * 3, 0, 255).astype(np.uint8)
arr[..., 3] = np.where(fringe, np.minimum(arr[..., 3], fade), arr[..., 3])

Image.fromarray(arr).save(DST)
removed = int(bg.sum())
print(f"OK {DST}  size={img.size}  removed_bg_px={removed} ({removed*100//(h*w)}%)")
