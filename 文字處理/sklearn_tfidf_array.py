# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 09:27:58 2020

@author: user
"""
import jieba
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from pandas import DataFrame
content = ["若是寶寶在第四個月的時候吃奶量突然下降變得不愛吃奶，則是要特別注意寶寶是不是到了生理性厭奶",
"所以有時候或因為輔食因素，而降低吃奶量也是在所難免，所以各位寶媽們大可以不用過分擔憂",
"寶寶不喜歡奶粉的味道或是餵奶方式不對等原因，而在這些方面，我們則是具體問題具體分析，看是要更換奶嘴，還是要換其他奶粉"]

jieba.load_userdict('dict.txt.big')
stop = []
with open('stop_words.txt','r', encoding = 'utf-8') as f:
    for i in f:
        stop += i.split()
        
def get_data(x):
    lists = jieba.cut(x)
    a=[]
    for i in lists:
        if len(i)>=2 and i not in stop:
            a.append(i)
    return ' '.join(a)
textitor =map(get_data, content)
#文字預處理

#文字轉tfidf矩陣
vectorize = CountVectorizer()
vt = vectorize.fit_transform(textitor)
transformer = TfidfTransformer().fit_transform(vt)
word = vectorize.get_feature_names()
weight = transformer.toarray()
print(DataFrame(weight, columns = word))
'''
x = sorted([ (n,i.sum()) for n, i in enumerate(weight.T)],key = lambda x : x[1], reverse = True)
for i in range(5):
    print(word[x[i][0]],x[i][1])
'''


        