import cv2
import glob

files = glob.glob("realPlate/*.jpg")
img = cv2.imread(files[0])  #讀取要辨識的圖形
# img = cv2.imread('realPlate/resizejpg001.jpg')  #讀取要辨識的圖形
detector = cv2.CascadeClassifier('haar_carplate.xml')  #讀取Haar模型
signs = detector.detectMultiScale(img, minSize=(76, 20), scaleFactor=1.1, minNeighbors=4)  #辨識
if len(signs) > 0 :  #有偵測到車牌
    for (x, y, w, h) in signs:  #逐一框選出車牌  
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        print(signs)
else:
    print('沒有偵測到車牌！')

cv2.imshow('Frame', img)  #顯示圖形
cv2.waitKey(0)
cv2.destroyAllWindows()