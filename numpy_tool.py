# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 16:19:12 2020

@author: user
"""

import numpy as np
import matplotlib.pyplot as plt
    # 等差數列 預設50份
x = np.linspace(0, 29, 30)
    # 自然指數 e**3.5
e = np.exp(3.5)
    # tan圖形轉水平 所以最大值是趨近1 最小值趨近-1
tan = np.tanh(1000)
    # 每個數字都是前面所有數字的總和 累加數列
cum = np.cumsum(x)

r= np.add.identity
a = np.array([2,3,4,5])
b = np.array([8,5,4])
c = np.array([5,4,6,8,3])
# np.ix_(n個1維array)回傳n個n維 其shape[第k個]=len(第k個) 其餘維度為1
vs = np.ix_(a,b,c)
for v in vs:
    r = np.add(r,v)
#print(r)

a= np.arange(12).reshape(3,4)
b1 = np.array([False,True,True])
b2 = np.array([True,False,True,False])
# [b1,b2]=[[1,2],[0,2]] 所以是取[1,0] 和[ 2,2]
print(a[b1,b2])
# [:,b2][b1,:] 是先取[1,2]列，再取[0,2]欄，所以是[1,0][1,2][2,0][2,2]
print(a[:,b2][b1,:])

data=np.arange(20).reshape(5,4)
print("範本\n",data, '\n')

print("np.sin()全部取sin三角函數\n",np.sin(data),'\n')
# np.argmax(axis=''/0/1) 回傳全部/每列/欄()最大值的列/欄索引\n
print(np.argmax(data,axis=1))
# axis也可用在np.max()
print(data.max(axis=1),'\n')
# np.all() 內容全為True 則回傳True, 反之則False
# data < 0本身就是個布林值陣列
print(data < 0,'\n')

# meshgrid(a, b) 會得到a複製b的列數次的二維矩陣 和b複製a的列數次的二維矩陣.T 兩個項目
# 很常np.meshgrid(np.linspace(xlim[0], xlim[1], 30), np.linspace(ylim[0], ylim[1], 30))
# 產生繪圖平面所有上座標點的x值陣列和y值陣列 常用在plt.contour(等高線圖)
mesh1, mesh2 = np.meshgrid(a, b)
# gs = mesh1.sum(1) 橫向加總每一列一個sum 成一維個數為總列數
# gs2 = mesh1.sum(0) 縱向加總 每欄一個sum 成一維個數為總欄數
# array.ravel() 和flatten()效果一樣 依序將每一列接起來成一維 但是flatten會複製一份 ravel會改掉原矩陣
ravel1, ravel2 = mesh1.ravel(), mesh2.ravel()

# np.vstack((a, b)) 將a b以垂直向連接起來(總列數相加) np.hstack((a, b)) 將a b以水平向連接起來(總欄數相加)
xy = np.vstack((ravel1, ravel2))
xy2 = np.c_[ravel1, ravel2].T # c_[a,b] = vstack([a,b]).T
sy3 = np.r_[ravel1, ravel2] # 將兩個一維array串起來


# pca.explained_variance_ratio_也可以用numpy做
# 共變異矩陣，丟入的資料每列都必須是一個特徵，因特徵原本是欄，所以要轉置
# np.linalg.eig(共變異矩陣) 會得到 特徵值 和 特徵向量 兩個資料
    # cov = np.cov(X_train_std.T)# 得到特徵數 * 特徵數 的共變異矩陣
    # eig_val, eig_vec = np.linalg.eig(cov_mat)
    # pca_ratio = [(i/sum(eig_vals)) for i in sorted(eig_val, reverse=True)]