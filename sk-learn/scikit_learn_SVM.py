# -*- coding: utf-8 -*-

from sklearn.datasets import make_circles
from sklearn.datasets import make_blobs, make_moons
from sklearn.svm import SVC
import numpy as np
import matplotlib.pyplot as plt
# --------make_circles
# 產生同心圓的資料 會產生所有點的座標值(n,2)和所有點的分類值(內外圓兩類) 參數(共幾筆, factor內圓直徑為外圓直徑的比例, noise散亂程度, random_state每個數字代表一種固定的隨機值
# X, y = make_circles(100, factor=.5, shuffle=False, noise=.1, random_state=3)

# --------make_blobs
# 產生團塊型的資料 會產生所有點的座標值(n,2)和所有點的分類值(n團n類) 參數(samples共幾筆, centers群數 random_state每個數字代表一種固定的隨機值 cluster_std組內標準差
# X, y = make_blobs(n_samples=1000, centers=2, random_state=0, cluster_std=0.60)
# --------make_moons 拋物線型資料

x = range(4)
y = range(4)
x, y = np.meshgrid(x, y)
z = [[0, 0, 0, 1],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 0]]

fig = plt.figure(figsize=(14,6))
fig.add_subplot(121)#122為熱圖
plt.contour(x, y, z)
# 雖然z是深度但是繪製出來的圖會順時針轉90度 因為模型分類常需要搭配contour所以模型產生的矩陣已設定成可直接拿來繪圖不用調整
X, y = make_blobs(n_samples=500, cluster_std=.1, random_state=2)
model = SVC(kernel='linear', C=1e4)
model.fit(X, y)
    #kernel ‘linear’, ‘poly’, ‘rbf’圓形, ‘sigmoid’S型, ‘precomputed’ 
    # C 出錯懲罰分數：預設為1e1 越小容錯率越高 越高則訓練結果越精準 但可能overfitting
    # random_state ：資料洗牌時的種子值，int值
    # gamma ： ‘rbf’,‘poly’ 和‘sigmoid’的核函式引數。預設是’auto’，則會選擇1/n_features
    # coef0 ：核函式的常數項。對於‘poly’和 ‘sigmoid’有用。
    # degree ：poly函式專用的維度，預設是3，選擇其他核函式時會被忽略。
    # probability ：是否採用概率估計？.預設為False
    # shrinking ：是否採用shrinking heuristic方法，預設為true
    # tol ：停止訓練的誤差值大小，預設為1e-3
    # cache_size ：核函式cache快取大小，預設為200
    # class_weight ：每種分類的權重，字典形式傳遞。設定第幾類的引數C為weight*C(C-SVC中的C)
    # verbose ：允許詳細輸出
    # max_iter ：最大迭代次數。-1為無限制。
    # decision_function_shape ：‘ovo’, ‘ovr’ or None, default=None3
print(model.support_vectors_)#支持向量
x_pre = np.array([[-1.31725387,-9.16537877],[ 0.84314555,-1.54509609],[ 0.80158651,-1.51628628]])
dot = model.predict(x_pre)
print(model.coef_)


# 繪圖
    # x = np.linspace(xlim[0], xlim[1], 30)
    # y = np.linspace(ylim[0], ylim[1], 30)
    # X, Y = np.meshgrid(x, y)
    # meshgrid產生的座標xy值矩陣，每列皆x,y值兩欄 n*2的形狀
    # xy = np.vstack([X.ravel(), Y.ravel()]).T # 也可以用np.c_[a,b]
    # 繪圖用矩陣P = model.decision_function(xy)
    # P = P.reshape(X/Y.shape)將一長串還原成原平面形狀
    # levels=[-1, 0, 1]就是決定向量和兩側界線
    # plt.contour(X, Y, xy, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])