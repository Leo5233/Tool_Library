#硬邊無漸層縮放 輸入圖像矩陣和放大倍率
import numpy as np
def hard_resize(img, scale):
    w,h = img.shape[0], img.shape[1]
    w = int(w*scale)
    h = int(h*scale)
    img2 = np.zeros((w, h),dtype = np.uint8)
    for x in range(w):
        for y in range(h):
            img2[x,y] = img[int(x/scale),int(y/scale)]
    return img2[:w, :h]
