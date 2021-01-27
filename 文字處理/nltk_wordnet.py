# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 12:12:36 2020

@author: user
"""
from nltk.corpus import wordnet as wn
x= wn.synset("power.n.04")
print(wn.synset('energy.n.05').lemma_names())#近似詞
print(wn.synset('energy.n.05').definition())#解釋
print(wn.synset('energy.n.05').hypernyms())#上位詞
print(wn.synset('energy.n.05').hyponyms())#下位詞
print()
temp = wn.synset('energy.n.05').hypernym_paths()#上位路徑
for i in temp[0]:
    print(i)
print()     
print(wn.synset('energy.n.05').min_depth())#該詞層數
print(wn.synset('energy.n.05').lowest_common_hypernyms(x))#最低共同上位詞
print(wn.synset('energy.n.05').path_similarity(x))#相似度

