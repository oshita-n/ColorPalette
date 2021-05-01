import numpy as np
import cv2
import collections

mask = cv2.imread("abema.jpg")
mask_arr = []
for i in range(len(mask)):
    for j in range(len(mask[0])):
        mask_arr.append(mask[i][j])
count = collections.Counter(map(tuple, mask_arr))
score_sorted = sorted(count.items(), key=lambda x: -x[1])

flag1 = False
flag2 = False
flag3 = False

pop_list = []

# 色の取捨選択のための閾値
thresh = 30
# 色の取捨選択
for i in range(len(score_sorted)-1):
    if abs(int(score_sorted[i][0][0]) - int(score_sorted[i+1][0][0])) >= 0 and abs(int(score_sorted[i][0][0]) - int(score_sorted[i+1][0][0])) <= thresh:
        flag1 = True
    if abs(int(score_sorted[i][0][1]) - int(score_sorted[i+1][0][1])) >= 0 and abs(int(score_sorted[i][0][1]) - int(score_sorted[i+1][0][1])) <= thresh:
        flag2 = True
    if abs(int(score_sorted[i][0][2]) - int(score_sorted[i+1][0][2])) >= 0 and abs(int(score_sorted[i][0][2]) - int(score_sorted[i+1][0][2])) <= thresh:
        flag3 = True
    
    if flag1 == True and flag2 == True and flag3 ==True:
        pop_list.append(i)

    flag1 = False
    flag2 = False
    flag3 = False

for i in sorted(set(pop_list), reverse=True):
    score_sorted.pop(i)

print(score_sorted[0:4])
img = np.full((50, 200, 3), 128, dtype=np.uint8)
cv2.rectangle(img, (0, 0), (50, 50), (int(score_sorted[0][0][0]),int(score_sorted[0][0][1]),int(score_sorted[0][0][2])), -1)
cv2.rectangle(img, (50, 0), (100, 50),  (int(score_sorted[1][0][0]),int(score_sorted[1][0][1]),int(score_sorted[1][0][2])), -1)
cv2.rectangle(img, (100, 0), (150, 50),  (int(score_sorted[2][0][0]),int(score_sorted[2][0][1]),int(score_sorted[2][0][2])),-1)
cv2.rectangle(img, (150, 0), (200, 50),  (int(score_sorted[3][0][0]),int(score_sorted[3][0][1]),int(score_sorted[3][0][2])),-1)

cv2.imwrite("colorpalette.jpg", img)