from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import re, logging
from pandas import DataFrame
import multiprocessing as mp
#在其他核心中印不出東西 所以使用logging來記錄 或是可用終端機啟動
logging.basicConfig(filename='error.txt')
class crawl:
    def __init__(self):
        self.QQ = mp.Queue()#用來集中不同核心的資料
        
    def parse(self):
        # options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        # desired_capabilities = options.to_capabilities()
        self.browser = webdriver.Chrome( )
        self.browser.get('https://zh-tw.flightaware.com/live/airport/RCTP')
        soup = BeautifulSoup(self.browser.page_source,"html.parser")
        #裝入所有待爬取連結 且分成2群
        mission_pool = [[],[]]
        for i in urls:
            mission_pool[i% len(mission_pool)].append(url)
        #記得關掉原本瀏覽器加快速度
        self.browser.quit()

        process = []
        #啟動多核心 
        for mission in mission_pool:
            process.append(mp.Process(target=job, args = (mission,self.QQ)))
            process[-1].start()
            print('enter mission')
        
        for i in process:
            i.join()
        
        #最後將Queue中的資料取出輸出
        data = [self.QQ.get() for i in range(self.QQ.qsize())]  
        DataFrame(data).to_csv("output.csv", index=0)
            
        #分組
def job(missions, q):
    #其他核心啟動瀏覽器
    browser = webdriver.Chrome()
    #將連結一一處理 把資料放入queue中
    for link in missions:
        browser.get(link)
        #Chrome本身會占用多核心 所以會互相干涉使讀取變慢 要加等待以免抓不到資料
        WebDriverWait(browser,3, 0.2).until(ec.presence_of_element_located((By.CLASS_NAME,"RRRRRRR")))
        soup = BeautifulSoup(browser.page_source,"html.parser")
    
        q.put()
        
    browser.quit()     
if __name__ == "__main__":  
    x=crawl()
    x.parse()