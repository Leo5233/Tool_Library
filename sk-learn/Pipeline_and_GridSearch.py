# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 12:42:22 2021

@author: user
"""
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

mnist = np.load('mnist_scaled.npz')

X_train, y_train, X_test, y_test = [mnist[f] for f in ['X_train', 'y_train', 
                                    'X_test', 'y_test']]
pipe_svc = make_pipeline(StandardScaler(),
                         SVC(random_state=1))

param_range = [ 0.01, 0.1, 1.0, 10.0]
# 分多次做 一次測太多種會跑超久
param_grid = [{'svc__C': param_range, 
               'svc__kernel': ['linear']},
              {'svc__C': param_range, 
               'svc__gamma': param_range, 
               'svc__kernel': ['rbf']}]

gs = GridSearchCV(estimator=pipe_svc, 
                  param_grid=param_grid, 
                  scoring='accuracy', 
                  cv=10,
                  n_jobs=-1)
gs = gs.fit(X_train[:1000], y_train[:1000])
print(gs.best_score_)
print(gs.best_params_)