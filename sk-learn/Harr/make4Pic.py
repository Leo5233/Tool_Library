from PIL import Image
import glob

path = 'Haar-Training_carPlate/training/positive/'
fp = open(path + 'info.txt', 'r')
lines = fp.readlines()  #讀取所有文字
#lines = ["rawdata/bmpraw001.bmp 1 44 109 106 30"]
count =  len(glob.glob("carPlate/*.bmp")) #圖片數也就是最大舊圖片編號，新產生的圖片編號繼續遞增
if len(lines)>count:
    print("新圖片已產生過!")
else:    
    rettext = '' #用來裝所有的每行標框紀錄
    print('開始產生新圖片！')    
    for line in lines:
        data = line.split(' ')
        img = Image.open(path + data[0])  #讀入圖形檔
        x = int(data[2])  #標框左上點X坐標
        y = int(data[3])  #標框左上點Y坐標
        w = int(data[4])  #標框寬
        h = int(data[5])  #標框高
        reduceW = 30  #減少的的寬度
        reduceH = int(reduceW*0.75)  #減少的的高度 長寬4:3因為原圖尺寸是300X255
        multi = float(300/(300-reduceW))  #原圖與新圖比例
        neww = int(w*multi)  #新圖的寬
        newh = int(h*multi)  #新圖的高
        # 因為手拉框線在圖中的位置可能很靠邊，為避免切到所以要判斷框線和圖片邊界的空間夠不夠
        # 沒意外的話會生成4張複製圖
        if (x-reduceW)>5 and (y-reduceH)>5:  #手拉框線左上側還有空間才移除左上角
            count += 1  #編號加1,此數值會做為檔名用
            newimg = img.crop((reduceW, reduceH, 300, 225))  #擷取縮減後圖形(左上座標, 右下座標)
            newimg = newimg.resize((300, 225), Image.ANTIALIAS)  #放大回原尺寸
            newimg.save(path + 'rawdata/bmpraw{:0>3d}.bmp'.format(count), 'bmp')  #存檔
            newx = int((x-reduceW)*multi)  #新圖的框框左上點X坐標
            newy = int((y-reduceH)*multi)  #新圖的框框左上點Y坐標            
            rettext = rettext+'rawdata/bmpraw{:0>3d}.bmp'.format(count)+' '+'1'+' '+str(newx)+' '+str(newy)+' '+str(neww)+' '+str(newh)+'\n'  #記錄新圖資料
        #移除右上角圖
        if (x+w)<(300-reduceW-5) and y>(reduceW+5):
            count += 1
            newimg = img.crop((0, reduceH, (300-reduceW), 225))
            newimg = newimg.resize((300, 225), Image.ANTIALIAS)
            newimg.save(path + 'rawdata/bmpraw{:0>3d}.bmp'.format(count), 'bmp')
            newx = int(x*multi)
            newy = int((y-reduceH)*multi)
            rettext = rettext+'rawdata/bmpraw{:0>3d}.bmp'.format(count)+' '+'1'+' '+str(newx)+' '+str(newy)+' '+str(neww)+' '+str(newh)+'\n'
        #移除左下角圖
        if (x-reduceW)>5 and (y+h)<(225-reduceH-5):
            count += 1
            newimg = img.crop((reduceW, 0, 300, 225-reduceH))
            newimg = newimg.resize((300, 225), Image.ANTIALIAS)
            newimg.save(path + 'rawdata/bmpraw{:0>3d}.bmp'.format(count), 'bmp')
            newx = int((x-reduceW)*multi)
            newy = int(y*multi)
            rettext = rettext+'rawdata/bmpraw{:0>3d}.bmp'.format(count)+' '+'1'+' '+str(newx)+' '+str(newy)+' '+str(neww)+' '+str(newh)+'\n'
        #移除右下角圖
        if (x+w)<(300-reduceW-5) and (y+h)<(225-reduceH-5):
            count += 1
            newimg = img.crop((0, 0, (300-reduceW), 225-reduceH))
            newimg = newimg.resize((300, 225), Image.ANTIALIAS)
            newimg.save(path + 'rawdata/bmpraw{:0>3d}.bmp'.format(count), 'bmp')
            newx = int(x*multi)
            newy = int(y*multi)
            rettext = rettext+'rawdata/bmpraw{:0>3d}.bmp'.format(count)+' '+'1'+' '+str(newx)+' '+str(newy)+' '+str(neww)+' '+str(newh)+'\n'

    fp.close()
    
    fpmake = open(path + 'Info.txt', 'a')  #以新增資料方式開啟檔案
    fpmake.write(rettext)  #寫入檔案
    fpmake.close()
    print('產生新圖片結束！')