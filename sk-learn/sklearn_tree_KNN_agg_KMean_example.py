# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 21:14:54 2020

@author: user
"""

from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn import metrics, cluster, tree
from sklearn.datasets import load_iris
import pandas as pd
import numpy as np

data=load_iris()
clf = neighbors.KNeighborsClassifier()
clf2 = cluster.KMeans(n_clusters=3)
clf3 = tree.DecisionTreeClassifier()
clf4 = cluster.AgglomerativeClustering(n_clusters = 3)

x1 = data.data[[i for i in range(0,150,2)]]
y1 = data.target[[i for i in range(0,150,2)]]
x2=data.data[[i for i in range(1,150,2)]]
y2=data.target[[i for i in range(1,150,2)]]


mode1 = clf.fit(x1, y1)
mode2 = clf2.fit(x1)
mode3 = clf3.fit(x1, y1)
mode4 = clf4.fit(x1)

pred1 = mode1.predict(x2)
pred2 = mode2.labels_
pred3 = mode3.predict(x2)
pred4 = mode4.labels_

print("KNN: ",metrics.accuracy_score(y2, pred1))
print("Tree: ",metrics.accuracy_score(y2, pred3))

y1= pd.DataFrame(y1)#silhouette_score必須使用轉置矩陣

print("KMean: ",metrics.silhouette_score(y1, pred2))
print("agglomerative: ",metrics.silhouette_score(y1, pred4))

