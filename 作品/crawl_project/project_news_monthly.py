# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 16:16:46 2020

@author: user
"""

import threading, requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk import FreqDist
import time, sched
import random, csv, datetime


global head, final_data, final_data2 ,count
head = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
#要輸出月關鍵字 和月連結 兩份csv用的list
final_data, final_data2 = [],[]

#傳入空白分隔字串 和 停用字list
def word_token(al, my_stopwords):
    #收入所有篩選過字詞的list
    left = []
    for word in al.split(' '): 
        #切分出每個單字 去掉空白(\n) 和夾在中間的符號
        temp = ''.join( [letter for letter in word.strip() if letter.isalnum()])
        #轉小寫和停用字比對 如果非停用字且長度在2字母以上 轉開頭大寫放入list中
        if temp.lower() not in (stopwords.words('english') + my_stopwords) and len(temp) > 1 and not temp.isdigit():
            if temp.isupper():
                left.append(temp)
            else:
                left.append(temp.capitalize())
    return left

#傳入字串list和所需關鍵字數上限
def word_frequence(left,rank):
    #將字詞list轉成{字:次數}
    final = FreqDist(left)
    #sort為次數去重複(例如多個只出現一次)排序
    sort = sorted(list(set(final.values())), reverse = True)
    count = 0#全域變數計算這個月有幾個關鍵字排名
    keyword,times = [], []
    for i in sort[:rank]:#列出次數的前幾名去找對應字 用value找key
        key = [k for k, v in final.items() if v == i ]
        count += len(key)#一個次數可能會有很多字，如果這個次數(i)的字數加上去會超過rank則跳出迴圈不加入
        if count > rank:
            break
        if i > 3:#若不會超過字數，且屬於最熱門(至少出現三次)的關鍵字
            print(key, i)
            #將字和次數別傳入keyword 和times (各為一維list)
            keyword += key
            for y in range(len(key)):
                times.append(i)
    return keyword, times 

#繼承threading.Thread的物件
class turbo(threading.Thread):
    #傳入上個月的年、月
    def __init__(self, year, month):
        threading.Thread.__init__(self)
        self.year = year
        self.month = month
        
    def run(self):
        website = ["new+york+times","bbc+news","cnn","daily+mail","al+jazeera"]#放在url內的關鍵字
        check = ['new york times',"bbc news","cnn","daily mail","aljazeera"]#google新聞搜尋的網站名稱對照詞，避免抓錯
        my_stopwords = ['first', 'could', 'says','year', 'years','may','us','set','time','new','trumps','one','say',
                        'times','city','day','top','making','make','bbc','cnn',"two", "news",'like','wont','get',
                        'run','still','good','dont','take','days','im','gets','want','go','finds','goes','gets']
        portion = [7,11,11,4,4]#根據每家新聞網社群流量推算出來的比例，使抽樣能近似母體
        self.month_titles = []#用來存所有當月新聞(標題, 連結)
        for site_num in range(5):#五家新聞網  
            temp_thread = []
            for page in range(portion[site_num]):#從portion取出抓取分頁數 每種新聞網的每一個分頁都開一個thread 
                #thread跳到extract function 傳入該新聞網抓取頁數、url關鍵字、比對用網站名稱
                temp_thread.append(threading.Thread(target = self.extract, args = (page, website[site_num], check[site_num])))
                temp_thread[-1].start()#這個好用
                
        #等全部thread都完成extract function再接下去
        for i in temp_thread:
            i.join()
        print(len(self.month_titles))#列出這個月抓到多少個標題 
        
        text = ' '.join([ i[0] for i in self.month_titles])#i[0]為標題 text 為空白分隔
        month_keyword = word_token(text, my_stopwords)#取的切分過濾好的list
        #儲存所有原始標題字詞
        with open(f"raw_text/{self.year}_{self.month}.csv",'w',encoding='utf-8',newline='')as w:
            csv.writer(w).writerow(month_keyword)
        #最多取20個關鍵字 從次數最高開始取 且關鍵字和次數各一個list
        month_keyword, times = word_frequence(month_keyword, 20)
        #對比每個當月關鍵字和連結新聞標題 ，如果關鍵字有在標題中(小寫對比) 回傳標題@連結 如果一個標題包含很多關鍵字就會被加入很多次
        recommand0 = [j[0]+'@'+j[1] for i in month_keyword for j in self.month_titles if i.lower() in j[0].lower()]
        #因為必須是字串list不能是tuple，要用方便切割的符號@串起來 所以標題@連結也可計算次數
        recommand0 = FreqDist(recommand0)
        #一樣由大到小 將次數取出去重複排列成查詢用list
        sort_recommand = sorted(list(set(recommand0.values())), reverse = True)
        #如果出現次數為前兩名(第一名至少會有包含2個關鍵字) 將對應的標題@連結拆開送入recommand
        recommand = [k.split('@') for k, v in recommand0.items() if v in sort_recommand[:2]]
        if len(recommand) > 15:#最多只給15個推薦連結 不到15個就全給
            recommand = random.sample(recommand,15)#因為會照字母排序導致NYtimes永遠被排除(www.nytimes n在較後面) 要隨機取
        for i in range(len(times)):#因csv不能放list所以要將keyword和times(兩個長度相等)拆解成 (年 月 字 次 總月數)
            final_data.append((self.year,self.month,month_keyword[i], times[i],  (self.year-2010)*12+ self.month-1))
        for i in range(len(recommand)):#(年 月 標題 連結 總月數)
            final_data2.append([self.year,self.month,recommand[i][0], recommand[i][1], (self.year-2010)*12 + self.month-1])
        #更新累加至兩個csv檔
        with open("history_keyword.csv",'a',encoding='utf-8',newline='')as w1:
            csv.writer(w1).writerows(final_data)
        with open("history_links.csv",'a',encoding='ansi',newline='')as w2:
            csv.writer(w2).writerows(final_data2)
    #該網站頁數, url用字串, 網站名稱比對用字串 
    def extract(self, page, site, site_check):        
        try:
            url = "https://www.google.com/search?q={}&tbs=cdr:1,cd_min:{}/1/{},cd_max:{}/28/{}&tbm=nws&start={}0".format(site, self.month, self.year, self.month , self.year, page)
            x = requests.get(url,headers = head)
            print(x.status_code)#429表示被ban
        except:
            return
        soup = BeautifulSoup(x.text, 'html.parser')
        key = soup.select("div.XTjFC")
        title = soup.select("div.JheGif")
        link = soup.select("div.dbsr a")
        for i, k, m in zip(key, title, link):
            if site_check in i.text.lower():#確定該標題是屬於該網站
                #標題要去除標點
                temp =''.join([letter for letter in k.text if letter not in ['\n',',','.','‘','’','"']])
                #不分網站放入(標題, 連結)
                self.month_titles.append((temp, m.get('href')))        

def monthly_catch():                
    date = datetime.date.today()
    date -= datetime.timedelta(days = 30.25)
    #抓取今天回推一個月的日期 將年月送入turbo
    x = turbo(date.year, date.month)
    x.start()
    x.join()
    #因為final_data, final_data2 是全域變數在下次抓取前要記得清空
    final_data, final_data2 = [],[]
    #s.enter(261360, 0, monthly_catch)

s = sched.scheduler(time.time, time.sleep)
s.enter(5, 0, monthly_catch)#首次停五秒(可改) 執行monthly_catch()
s.run()