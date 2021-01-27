# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 09:56:11 2020

@author: user
"""
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk.stem import LancasterStemmer

def word_frequence(al,rank):
    lst = LancasterStemmer()
    left =[ lst.stem(word.lower()) for word in word_tokenize(al) 
           if word.lower() not in stopwords.words('english') and len(word) > 2]
    final = FreqDist(left)
    sort = sorted(list(set(final.values())))
    sort = [i for i in sort[::-1]]
    for i in sort[:rank]:#列出前幾名
        print([v for v, k in final.items() if k == i ], i)
