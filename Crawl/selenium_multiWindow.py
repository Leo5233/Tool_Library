from selenium import webdriver
from bs4 import BeautifulSoup
from pandas import DataFrame
#用物件寫法可以在不同子方法中操控browser較方便
class crawl:
    def __init__(self):        
        self.tag_num = 3#設定開啟分頁數
        self.group_data = []#用來集中所有資料
    def parse(self):
        # options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        # desired_capabilities = options.to_capabilities()
        self.browser = webdriver.Chrome( )
        # self.browser.get('https://zh-tw.flightaware.com/live/airport/RCTP')
        # sleep(2)
        # soup = BeautifulSoup(self.browser.page_source,"html.parser")

        # #裝入所有待爬取連結
        link_pool = []

        #開分頁 扣掉初始分頁所以-1
        for i in range(self.tag_num-1):
            self.browser.execute_script('window.open();')
        #抓取視窗控制碼    
        self.handle = self.browser.window_handles    

        for i in range(len(link_pool)):
            tag = i % self.tag_num
            #if 要剖析page_source的情況
            if tag == 0 and i !=0 or i == len(link_pool)-1:
                #tag = 0表新一輪, i != 0確保全部都已get, 或是 已經是最後一個連結
                temp = self.parse2(self.tag_num if i != len(link_pool)-1 else tag)
                #要剖析page_source的視窗數傳入parse2() ,得回傳資料放入容器中
                self.group_data.append(temp)
                
            #處理完剖析開啟新一輪切視窗get    
            self.browser.switch_to_window(self.handle[tag])
            self.browser.get(link_pool[i])
            
        self.browser.quit()
        DataFrame(self.group_data).to_csv("output.csv", index=0)
        
    def parse2(self, window):
        for i in range(window):
            self.browser.switch_to_window(self.handle[i])
            soup = BeautifulSoup(self.browser.page_source,"html.parser")
            
x=crawl()
x.parse()