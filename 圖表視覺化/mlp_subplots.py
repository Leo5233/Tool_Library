# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 23:18:53 2021

@author: user
"""

import matplotlib.pyplot as plt

# 所有圖一次設參數
fig, ax = plt.subplots(3, 10, figsize=(10, 2.5),
                       subplot_kw={'xticks':[], 'yticks':[]},
                       gridspec_kw=dict(hspace=0.1, wspace=0.1))
# 一排一排繪圖
for i in range(10):
    ax[0, i].imshow(X, cmap='binary_r')
    ax[1, i].imshow(X, cmap='binary_r')
    ax[2, i].imshow(X, cmap='binary_r')

# 將所有圖拉成一直線繪圖 也可以個別圖設參數
fig2, ax2 = plt.subplots(3, 5)
for i, axi in enumerate(ax.flat):
    axi.imshow(faces.images[i], cmap='bone')
    axi.set(xticks=[], yticks=[], xlabel='')
   
# 從0開始將一張張圖放入fig
for i in range(16):
    ax = fig.add_subplot(4, 4, i + 1, xticks=[], yticks=[])
    ax.imshow(X, cmap='binary', interpolation='blackman')
    
    # text(x座標, y座標, 文字)
    ax.text(0, 7, str(digits.target[i]))