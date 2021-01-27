import cv2
import glob

files = glob.glob("realPlate/*.jpg")
for file in files:
    print('圖片檔案：' + file)
    img = cv2.imread(file)
    detector = cv2.CascadeClassifier('haar_carplate.xml')
    signs = detector.detectMultiScale(img, minSize=(76, 20), scaleFactor=1.1, minNeighbors=4)
    if len(signs) > 0 :
        for (x, y, w, h) in signs:          
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)  
            print(signs)
    else:
        print('沒有偵測到車牌！')
    
    cv2.imshow('Frame', img)
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()
    if key == 113 or key==81:  #按q鍵結束
        break