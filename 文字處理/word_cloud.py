# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 19:42:48 2020

@author: user
"""
import matplotlib.pyplot as plt
import jieba.analyse
from wordcloud import WordCloud
import requests
from bs4 import BeautifulSoup
# import jieba 並使用繁中字典
jieba.set_dictionary("dict.txt.big")
x = requests.get("https://www.inside.com.tw/tag/AI")
soup = BeautifulSoup(x.text, 'html.parser')
link = soup.find_all("a",class_="js-auto_break_title")
links = [i.get('href') for i in link][:10]
keyword =''
for url in links:
    one_article = ''
    temp = requests.get(url)
    soup = BeautifulSoup(temp.text, 'html.parser')
    article = soup.select("article p")
    
    for tex in article:
        x = tex.text.strip()
        one_article += x
    for key in jieba.analyse.extract_tags(one_article,10):
        keyword += key
        keyword += ' '
    
stopwords = ["沒有","一個","什麼","那個","他們"] 
wc = WordCloud(font_path="NotoSerifCJKtc-Black.otf", #設置字體
               background_color="white", #背景顏色
               max_words = 200 , #文字雲顯示最大詞數
               stopwords=stopwords) #停用字詞

wc.generate(keyword)

plt.imshow(wc)
plt.axis("off")
plt.figure(figsize=(20,12), dpi = 150)
plt.show()
wc.to_file('word_cloud.png')
    
