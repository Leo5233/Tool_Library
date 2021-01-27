# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 16:16:46 2020

@author: user
"""

import threading, requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk import FreqDist
from pandas import DataFrame
import random,csv
from time import sleep

global head, final_data
head = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
final_data = []

def word_token(al, my_stopwords):
    left = []
    for word in al.split(' '): 
        temp = ''.join( [letter for letter in word.strip() if letter.isalnum()])
        if temp.lower() not in (stopwords.words('english') + my_stopwords) and len(temp) > 1 and not temp.isdigit():
            if temp.isupper():
                left.append(temp)
            else:
                left.append(temp.capitalize())
    return left
    
def word_frequence(left,rank):
    final = FreqDist(left)
    sort = sorted(list(set(final.values())), reverse = True)#次數去重複(例如多個只出現一次)排序
    count = 0
    keyword,times = [], []
    for i in sort[:rank]:#列出前幾名用次數去找對應字
        key = [k for k, v in final.items() if v == i ]
        count += len(key)#限制最大關鍵字數
        if count > rank:
            break
        if i > 3:#指挑最熱門的關鍵字
            print(key, i)
            keyword += key
            for y in range(len(key)):
                times.append(i)
    return keyword, times #裝入前rank關鍵字的串列

class turbo(threading.Thread):
    def __init__(self, year, month):
        threading.Thread.__init__(self)
        self.year = year
        self.month = month
        
    def run(self):

        website = ["new+york+times","bbc+news","cnn","daily+mail","al+jazeera"]
        check = ['new york times',"bbc news","cnn","daily mail","aljazeera"]
        my_stopwords = ['first', 'could', 'says','year', 'years','may','us','set','time','new','trumps','one','say',
                        'times','city','day','top','making','make','bbc','cnn',"two", "news",'like','wont','get',
                        'run','still','good','dont','take','days','im','gets','want','go','finds','goes','gets']
        portion = [7,11,11,4,4]
        self.month_titles = []
        for site_num in range(5):  
            temp_thread = []
            for page in range(portion[site_num]):
                sleep(0.5)
                temp_thread.append(threading.Thread(target = self.extract, args = (page, website[site_num], check[site_num])))
                temp_thread[-1].start()
        for i in temp_thread:
            i.join()
        print(len(self.month_titles))    
        text = ' '.join([ i[0] for i in self.month_titles])
        month_keyword = word_token(text, my_stopwords)
        with open(f"raw_text/{self.year}_{self.month}.csv",'w',encoding='utf-8')as w:
            csv.writer(w).writerow(month_keyword)
        month_keyword, times = word_frequence(month_keyword, 20)
        recommand0 = [j[0]+'@'+j[1] for i in month_keyword for j in self.month_titles if i.lower() in j[0].lower()]
        recommand0 = FreqDist(recommand0)
        sort_recommand = sorted(list(set(recommand0.values())), reverse = True)
        recommand = [k.split('@') for k, v in recommand0.items() if v in sort_recommand[:2]]
        if len(recommand) > 15:
            recommand = random.sample(recommand,15)#因為會照字母排序導致NYtimes永遠被排除
        final_data.append((self.year,self.month,month_keyword, times, recommand))

            
    def extract(self, page, site, site_check):        
        try:
            url = "https://www.google.com/search?q={}&tbs=cdr:1,cd_min:{}/1/{},cd_max:{}/28/{}&tbm=nws&start={}0".format(site, self.month, self.year, self.month , self.year, page)
            x = requests.get(url,headers = head)
            print(x.status_code)
        except:
            return
        soup = BeautifulSoup(x.text, 'html.parser')
        key = soup.select("div.XTjFC")
        title = soup.select("div.JheGif")
        link = soup.select("div.dbsr a")
        for i, k, m in zip(key, title, link):
            if site_check in i.text.lower():
                self.month_titles.append((k.text, m.get('href')))        

year = ["2010"]
month = [i for i in range(8,9)]
for i in year:
    all_thread = []
    for j in range(len(month)):
        sleep(0.5)
        all_thread.append(turbo(i, month[j]))
        all_thread[j].start()
    for x in all_thread:
        x.join()

DataFrame(final_data).to_csv("record.csv", index = 0, header = 0)
        

