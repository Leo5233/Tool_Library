# -*- coding: utf-8 -*-
import numpy as np
from sklearn.svm import SVC
import matplotlib.pyplot as plt
mnist = np.load('mnist_scaled.npz')
X_train, y_train, X_test, test_real = [mnist[f] for f in ['X_train', 'y_train', 'X_test', 'y_test']]
svm = SVC(kernel='linear', C=1.0, random_state=1)
svm.fit(X_train[:1000], y_train[:1000])
test_pre = svm.predict(X_test)
target_names = [str(i) for i in range(10)]
# --------------------------------------------------------


# 混沌矩陣的計算方式為：
# 將預測集和答案集串起來去重複
# 得到所有真正有用到的類別名names(大部分類別名都只在訓練集出現)
names = set(list(test_pre)+list(test_real))
names = [target_names[i] for i in names]

# 以下等於confusion_matrix(答案集, 預測集).T

# 用預測集/答案集的長度(兩者一樣)去跑for迴圈，每一組預測[i]答案[i]兩者都會各自對應一個類別名
# 找出類別名在names中的位置index
test_pre1 =[names.index(target_names[i]) for i in test_pre]
test_real1 =[names.index(target_names[i]) for i in test_real]
# 用names的長度製作方陣
confuse = np.zeros((len(names), len(names)), dtype=np.uint16)

for i in range(len(test_real)):
    # 預測類別index和答案類別index兩個參數便可定位方陣中的位置+1(次)
    confuse[test_pre1[i], test_real1[i]] += 1

import seaborn as sns; sns.set()
from sklearn.metrics import confusion_matrix

mat = confusion_matrix(test_real, test_pre)
#annot(annotation)標示次數 square=True(預設是長方形) cbar顯示色溫棒 fmt(format)'d'表示整數顯示數值
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=names,
            yticklabels=names)
plt.xlabel('true label')
plt.ylabel('predicted label');

