# -*- coding: utf-8 -*-
import cv2
# 視訊鏡頭要加上cv2.CAP_DSHOW
catch = cv2.VideoCapture(0,cv2.CAP_DSHOW)# 數字表示攝像頭ID 也可捕捉檔案
# cap = cv2.VideoCapture('video.avi')
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')# avi要用這種編碼才能讀

# 要寫入檔案 必須要將output的解析度設置成和input一樣
# 所以加上cap.get(3,4)影片長寬 參數依序為 檔名 編碼 fps 解析度長寬
# 3.寬度=cap.get(cv2.CAP_PROP_FRAME_WIDTH) 4.高度=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
output= cv2.VideoWriter('output.avi',fourcc, 20,(int(catch.get(3)),int(catch.get(4))))
# 可將視訊當成不斷的高速傳送圖片
while(catch.isOpened()):
    # ret為狀態T表示成功
    ret, img = catch.read()
    if ret==True:
        img = cv2.Canny(img,100,200)
        output.write(img)        
        cv2.imshow('frame',img)
        
        #單位是1/1000秒 所以fps29= wait(33)
        if cv2.waitKey(3) == 27:#27為ESC鍵
            break
    else:
        break
catch.release()
output.release()
cv2.destroyAllWindows()



