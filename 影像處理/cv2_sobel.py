# -*- coding: utf-8 -*-
import cv2
import numpy as np
img = cv2.imread('lenacolor.png',0)
# 找水平邊緣用的kernel
kernel = np.array([[-1,-2, -1], [0,0,0], [1,2,1]],dtype=np.int8)
w, h = img.shape

o1 = np.zeros((w,h), dtype=np.uint8)
o2 = np.zeros((w,h), dtype=np.uint8)
a = 3
q = 202
b = 5
for x in range(w-a+1):
    for y in range(h-a+1):
        temp = np.sum(img[x:x+a, y:y+a] * kernel)
        temp2 = np.sum(img[x:x+a, y:y+a] * kernel.T)
        if temp >=0 and temp <=255:
            o1[x+1,y+1] = temp
        elif temp < 0:
            o1[x+1,y+1] = 0
        elif temp > 255:
            o1[x+1,y+1] = 255
        o2[x+1,y+1] = abs(temp2) if abs(temp2) <= 255 else 255

# ddepth=-1 則是運算後原始值(含負值) 將>255 的像素通通設定255 <0通通設為0
# dx=0, dy=1 是尋找水平向的邊緣
img2 = cv2.Sobel(img, ddepth=-1, dx=0, dy=1)

# dx=1, dy=0 是尋找垂直向的邊緣
# ddepth=cv2.CV_64F 則是先保留運算後原始值(含負值)不做更動
# 搭配上convertScaleAbs則是將負值變號 若原本<-255變號後會>255 則取255
img3 = cv2.Sobel(img, ddepth=cv2.CV_64F, dx=1, dy=0)
img3 = cv2.convertScaleAbs(img3)

cv2.imshow('o1', o1)
cv2.imshow('img2', img2)
cv2.imshow('o2', o2)
cv2.imshow('img3', img3)
cv2.waitKey()
cv2.destroyAllWindows()

# o = cv2.imread('sobel4.bmp', cv2.IMREAD_GRAYSCALE)
# #sobel dx dy皆=1 是找出角落點 所以一次sobel只能找水平或垂直其中一種邊緣
# 純黑白若有長條水平/垂直邊要用ddepth=cv2.CV_64F 不然會自動捨棄負值(黑到白的部分)少一側的邊 
# 所以要轉f64容納負值再轉絕對值，因此要分兩次(水平、垂直)做再加在一起
# sobelx = cv2.Sobel(o, ddepth=cv2.CV_64F, dx=1, dy=0)
# sobelx = np.absolute(sobelx)
# sobely = cv2.Sobel(o, ddepth=cv2.CV_64F, dx=0, dy=1)
# sobely = np.absolute(sobely) # 也可以用cv2.convertScaleAbs(sobely)
# sobel_final = cv2.addWeighted(sobelx, 1, sobely, 1, 0)
# cv2.imshow('o', o)
# cv2.imshow('x', sobel_final)
# cv2.waitKey()
# cv2.destroyAllWindows()