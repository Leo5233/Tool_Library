# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 10:50:45 2021

@author: user
"""
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

def visualize_classifier(estimator, X, y, boundaries=True,
                   xlim=None, ylim=None, ax=None, cmap='rainbow'):
    ax = ax or plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    # fit the estimator
    estimator.fit(X, y)
    xx, yy = np.meshgrid(np.linspace(*xlim, num=200),
                         np.linspace(*ylim, num=200))
    # 將版面座標點丟入模型，得到圖面上每一點類別值預測
    Z = estimator.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    n_classes = len(np.unique(y))
    # 劃出色塊 原本有4類 因為np.arange不含尾所以要+1 且分界界定level為[0, 1]時 其界線定義為1>= x >0只能分一類 界線外的不會畫出來
    # 所以要分n類 要n+1條線 且因為界線不包頭 類別值0無法被定義 所以全部要-1(0屬於 -1<x<=0)
    # zorder類似CSS的z-index 因為有散布圖、線圖、色塊等重疊 看要不要排順序
    contours = ax.contourf(xx, yy, Z, alpha=0.3,
                           levels=np.arange(n_classes+1)-1,
                           cmap='rainbow',
                           zorder=1)

    ax.set(xlim=xlim, ylim=ylim)
    # print('node',estimator.tree_.node_count) estimator.tree_.node_count總節點數
    # print('left',estimator.tree_.children_left).children_left 每個節點的左分支的ID 沒有分支(葉節點)則是-1
    # print('right',estimator.tree_.children_right) 同上只是改右邊 因每個節點都有 所以是個list長度為.node_count總節點數
    # print('feature',estimator.tree_.feature) 該節點用來分類的資料index ，0 表示以data[0] -2表示到底了
    # 類似畫線分地遊戲 每個節點都是一段線段
    def plot_boundaries(i, xlim, ylim):
        if i >= 0: # i 為分支ID如果=-1表示已經到分支末端 其他狀況都會>=0
            tree = estimator.tree_
            # tree.feature[i] == 0 表示以data[0]作為該節點的決策條件 也就是x值大小 所以會畫出一條垂直線
            if tree.feature[i] == 0:
                #plot((x分界值,x分界值),(y軸最小,最大)) 因為x值一樣 所以是垂直線
                ax.plot([tree.threshold[i], tree.threshold[i]], ylim, '-k', zorder=2)
                # 保留ylim
                # 該節點的左分支==0 X軸範圍剩上述垂直線左側範圍
                plot_boundaries(tree.children_left[i],
                                [xlim[0], tree.threshold[i]], ylim)
                # 該節點的右分支==0 X軸範圍剩上述垂直線右側範圍
                plot_boundaries(tree.children_right[i],
                                [tree.threshold[i], xlim[1]], ylim)

            # tree.feature[i] == 1 表示以data[1]作為該節點的決策條件 也就是y值大小 所以會畫出一條水平線
            elif tree.feature[i] == 1:
                #plot((x軸最小,最大),(y分界值,y分界值)) 因為y值一樣 所以是水平橫線
                ax.plot(xlim, [tree.threshold[i], tree.threshold[i]], '-k', zorder=2)
                # 保留xlim
                # 該節點的左分支==0  y軸範圍剩上述水平線以下
                plot_boundaries(tree.children_left[i], xlim,
                                [ylim[0], tree.threshold[i]])
                # 該節點的右分支==0  y軸範圍剩上述水平線以上
                plot_boundaries(tree.children_right[i], xlim,
                                [tree.threshold[i], ylim[1]])
  
    if boundaries:
        plot_boundaries(0, xlim, ylim)
        
X, y = make_blobs(n_samples=300, centers=4,
                  random_state=3, cluster_std=1.0)
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='rainbow')

# 決策樹
# tree = DecisionTreeClassifier()
# visualize_classifier(DecisionTreeClassifier(), X, y)

# 隨機森林
model = RandomForestClassifier(n_estimators=1000, random_state=0, max_depth=1)
visualize_classifier(model, X, y, boundaries=False)