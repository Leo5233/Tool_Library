# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 20:04:28 2020

@author: USER
"""

import os 
import struct
import numpy as np
import gzip
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics


def load_mnist(path, kind='train'):
    #讀入圖片集和分類集
    labels_path = os.path.join(path, f'{kind}-labels-idx1-ubyte')
    images_path = os.path.join(path, f'{kind}-images-idx3-ubyte')

    #讀取分類集0-9
    with open(labels_path,'rb') as lbpath:
        #前8Byte是檔案資訊，以pop的方式讀取而非index所以剩下的資料會變少
        temp = lbpath.read(8)
        #將位元資料還原，依資料類型指定不同格式'II'為2個整數 一個I佔4byte !><=為位元順序會影響編碼結果

        magic,n = struct.unpack('!II',temp)#在此呈現magic未知 n為圖片數量
        #剩下的資料是'b'1byte的數字也就是1 byte即一筆資料共60000筆
        #將去除8Byte檔案資訊的剩餘檔案用numpy.lbpath讀入 因為是0-9設uint8
        labels = np.fromfile(lbpath, dtype= np.uint8)

    #讀取圖片集        
    with open(images_path, 'rb') as imgpath:
        #將位元資料還原，依資料類型指定不同格式'IIII'為4個整數 一個I佔4byte 共讀入16byte
        #!><=為位元順序會影響編碼結果 num, rows, cols 分別為圖片數、列數、欄數
        magic,num, rows, cols = struct.unpack("!IIII", imgpath.read(16))
        
        #剩下的資料類型不明，但無論如何做knn要將矩陣拉平
        images = np.fromfile(imgpath, dtype = np.uint8).reshape(len(labels), 784)
        #大多會進行標準化將0-255轉換成-1~1
        images = ((images/255.) - .5)*2
    
    return images, labels

#這裡是將所有的.gz檔解壓縮    
# for z in os.listdir('./'):
#     if z.endswith('ubyte.gz'):
#         with gzip.GzipFile(z,mode='rb') as decompressed, open('dfhdhg', 'wb') as outfile:
#             outfile.write(decompressed.read())

#X為圖片 Y為標籤分類 train:60000筆 test:10000筆
X_train, y_train = load_mnist('', kind='train')
X_test, y_test = load_mnist('', kind='t10k')

'''
fig, ax = plt.subplots(nrows = 2, ncols= 5, sharex= True, sharey= True)
#產生2*5張小圖 為了方便用for迴圈跑，因此將subplot的二維index拉平
ax = ax.flatten()
for i in range(10):
    #將0-9每個數字第[0]張圖(列) 從拉平狀態還原成矩陣 單純展示用 也可以是第[1][2]....
    img = X_train[y_train== i][1].reshape(28,28)
    ax[i].imshow(img, cmap='Greys')

ax[0].set_xticks([])
ax[0].set_yticks([])
plt.tight_layout()
plt.savefig('1231234.png', dpi=300)
plt.show()
'''

#將讀取的訓練測試集存成壓縮檔 np.savez_compressed(檔名.npz, 自訂區塊名=ndarray,....)
#np.savez_compressed('mnist_scaled.npz', X_train=X_train, y_rain = y_train,X_test = X_test, y_test = y_test)
#mnist = np.load('mnist_scaled.npz')
#之後要在使用時 可用容器['自訂區塊名'] 來使用
#X_train,y_train, X_test,y_test = [mnist[f] for f in ['X_train', 'y_rain', 'X_test', 'y_test']]


knn = KNeighborsClassifier(n_neighbors = 5, p = 2, metric= 'minkowski')
#因為60000張圖跑不動所以取1000來做訓練
y_train_pred = knn.fit(X_train[:100],y_train[:100])
#回傳同測試集數量的預測集
y_test_pred = knn.predict(X_test)


#列出前25
num = 35
plt.figure(figsize=(15,15*num/20))
# for i in range(num):
#     #這裡用的是subplot和剛剛的subplots不一樣
#     #要給予欄數、列數、第幾張圖
#     ax2 = plt.subplot(int(num/5),5,i+1)
#     ax2.imshow(np.reshape(X_test[i],(28,28)),cmap='binary')
#     title = "label= " +str((y_test[i])) + ",predict="+str(y_test_pred[i])
#     ax2.set_title(title,fontsize=10)
#     #連句用;隔開
#     ax2.set_xticks([]);ax2.set_yticks([])
import math
f, ax2 = plt.subplots(nrows = int(math.ceil(num/5)), ncols=5, sharex=False, sharey= False,figsize=(15,15*num/20))
ax2 = ax2.flatten()
for i in range(num):
    #這裡用的是subplot和剛剛的subplots不一樣
    #要給予欄數、列數、第幾張圖
    
    ax2[i].imshow(np.reshape(X_test[i],(28,28)),cmap='binary')
    title = "label= " +str((y_test[i])) + ",predict="+str(y_test_pred[i])
    ax2[i].set_title(title,fontsize=10)
    #連句用;隔開
    ax2[i].set_xticks([]);ax2[i].set_yticks([])

#準確率 訓練集100:0.6232 500:0.7953
print(metrics.accuracy_score(y_test, y_test_pred))

plt.show()
    

