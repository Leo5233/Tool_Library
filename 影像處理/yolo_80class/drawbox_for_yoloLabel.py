import glob
import cv2

files = glob.glob("*.txt")
for f in files:
    with open(f) as data:
        text = data.readlines()
    img = cv2.imread(f.split('.')[0]+'.png',1)
    h, w, _ = img.shape
    for i in text:
        co = i.split(' ')
        x, y = int(float(co[1])*w), int(float(co[2])*h)
        xw, yw = int(float(co[3])*w), int(float(co[4])*h)
        cv2.rectangle(img, (x-xw, y-yw), (x+xw, y+yw), (0, 0, 255), 1)

    cv2.imshow("img", img)
    cv2.waitKey()
    cv2.destroyAllWindows()
        