import numpy as np
import cv2
import collections
import timeit

def posterization(frame: np.ndarray, step = 4):
    if 1 < step and step <= 256:
        look_up_table = np.zeros((256, 1), dtype = 'uint8')
        split = int(256 / (step - 1))
        up = int(256 / step)
        for i in range(256):
            if np.trunc(i / up) * split >= 255:
                look_up_table[i][0] = 255
            else:
                look_up_table[i][0] = np.trunc(i / up) * split
        return cv2.LUT(frame, look_up_table)
    else:
        return frame

def calcColor(mask: np.ndarray):
    # 各色をカウントする
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
    thresh = 5
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
    return img

def calcColor_llist(mask: np.ndarray):
    # 各色をカウントする
    mask_llist = collections.deque()
    # for i in range(len(mask)):
    #     for j in range(len(mask[0])):
    #         mask_llist.append(mask[i][j])
    mask_llist = [mask[i][j] for i in range(len(mask)) for j in range(len(mask[0]))]
    count = collections.Counter(map(tuple, mask_llist))
    score_sorted = sorted(count.items(), key=lambda x: -x[1])

    flag1 = False
    flag2 = False
    flag3 = False

    # pop_list = []

    # 色の取捨選択のための閾値
    thresh = 10
    # 色の取捨選択(RGBだから3色ごとに色の近さを計測)
    # 隣の色との近さを計測
    # 厳密に隣の色を計測する必要はないので20px離れたところを計測する
    for i in range(0, len(score_sorted)-1, 20):
        if abs(int(score_sorted[i][0][0]) - int(score_sorted[i+1][0][0])) >= 0 and abs(int(score_sorted[i][0][0]) - int(score_sorted[i+1][0][0])) <= thresh:
            flag1 = True
        if abs(int(score_sorted[i][0][1]) - int(score_sorted[i+1][0][1])) >= 0 and abs(int(score_sorted[i][0][1]) - int(score_sorted[i+1][0][1])) <= thresh:
            flag2 = True
        if abs(int(score_sorted[i][0][2]) - int(score_sorted[i+1][0][2])) >= 0 and abs(int(score_sorted[i][0][2]) - int(score_sorted[i+1][0][2])) <= thresh:
            flag3 = True
        
        if flag1 == True and flag2 == True and flag3 ==True:
            mask_llist.pop(i)

        flag1 = False
        flag2 = False
        flag3 = False

    # for i in sorted(set(pop_list), reverse=True):
    #     score_sorted.pop(i)

    print(score_sorted[0:4])
    img = np.full((50, 200, 3), 128, dtype=np.uint8)
    cv2.rectangle(img, (0, 0), (50, 50), (int(score_sorted[0][0][0]),int(score_sorted[0][0][1]),int(score_sorted[0][0][2])), -1)
    cv2.rectangle(img, (50, 0), (100, 50),  (int(score_sorted[1][0][0]),int(score_sorted[1][0][1]),int(score_sorted[1][0][2])), -1)
    cv2.rectangle(img, (100, 0), (150, 50),  (int(score_sorted[2][0][0]),int(score_sorted[2][0][1]),int(score_sorted[2][0][2])),-1)
    cv2.rectangle(img, (150, 0), (200, 50),  (int(score_sorted[3][0][0]),int(score_sorted[3][0][1]),int(score_sorted[3][0][2])),-1)
    return img

mask = cv2.imread("art/paypay2.png")
mask = posterization(mask, step=4)
img = calcColor_llist(mask)
cv2.imwrite("colorpalette.jpg", img)
