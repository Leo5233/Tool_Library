# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('housing.data.txt', header=None, sep='\s+')# 正則表示 一個以上的任意空白(含tab)
df.columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
X = df.iloc[:,:-1].values #最後一欄是解答不要取 加上.values轉換成nparray
y = df['MEDV'].values  #解答欄 
X_train, X_test, y_train, y_test =  train_test_split(X, y, test_size=.3,random_state = 1)

# 不同資料的標準化數值會不同 所以要先fit 再標準化 第一次是fit_transform 之後就只要transfrom
sc = StandardScaler()
X_train_std = sc.fit_transform(X_train)
X_test_std = sc.transform(X_test)

pca = PCA(n_components=4) # 取前4個 不給的話預設為全取 第一次可不給列出全部特徵的解釋量 選好特徵數再回頭改
X_train_pca = pca.fit_transform(X_train_std)
X_test_pca = pca.transform(X_test_std)
# class_ = pca.components_每種特徵都成為一筆代表性資料可繪圖看看
# projected = pca.inverse_transform(X_test_pca) # 將降維資料再次升維(但數值已簡化)可繪製簡化版特徵圖
print(pca.explained_variance_ratio_)

# pca.explained_variance_ratio_是個包含每個特徵的比例的list 其總和為1
    # plt.bar(range(1, 5), pca.explained_variance_ratio_, alpha=0.5, align='center')
    # plt.step(range(1, 5), np.cumsum(pca.explained_variance_ratio_), where='mid')
    # plt.ylabel('Explained variance ratio')
    # plt.xlabel('Principal components')
    # plt.show()

plt.scatter(X_test_pca[:, 0], X_test_pca[:, 1])
plt.xlabel('PC 1')
plt.ylabel('PC 2')
plt.show()

# pca.explained_variance_ratio_也可以用numpy做
# 共變異矩陣，丟入的資料每列都必須是一個特徵，因特徵原本是欄，所以要轉置
# np.linalg.eig(共變異矩陣) 會得到 特徵值 和 特徵向量 兩個資料
cov_mat = np.cov(X_train_std.T)# 得到特徵數 * 特徵數 的共變異矩陣
eigen_vals, eigen_vecs = np.linalg.eig(cov_mat)
var_exp = [(i/sum(eigen_vals)) for i in sorted(eigen_vals, reverse=True)]

# 繪圖
plt.bar(range(1, 14), var_exp, alpha=0.5, align='edge',label='individual explained variance')
plt.step(range(1, 14), np.cumsum(var_exp), where='post',label='cumulative explained variance')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal component index')
plt.legend(loc='best')
plt.show()
