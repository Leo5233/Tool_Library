# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import tkinter as tk

def wait(class_name, message):
    try:
        WebDriverWait(browser, 10, 0.25).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    except:
        print(message)

class aaa:
    sw = 0
    keyword = ''
    num = 0
    def do(self):
        if self.sw == 0:
            self.shoplist = ""
            self.keyword = kwbox.get()#讀入文字框的輸入字
            key_url = browser.current_url.find('@')   
            browser.get(f"https://www.google.com.tw/maps/search/{self.keyword}/"+browser.current_url[key_url:])#將關鍵字合到url中
            wait("cards-rating-score","地圖找關鍵字發生錯誤")
            soup = BeautifulSoup(browser.page_source,'html.parser')
            self.shops = soup.select("h3.section-result-title span")#左邊列表店名、星等、地址、電話
            self.star = soup.select('span.cards-rating-score')
            self.address = soup.select("div.section-result-details-container")
            self.tel = soup.select('span.section-result-phone-number')
            if len(self.shops) == 0: #沒讀到東西時給予信息並關閉瀏覽器
                message.configure(text = f"這附近沒有{self.keyword}, 程式結束")
                browser.quit()
                return
            
            for k, i in enumerate(range(len(self.star))):#將所有資訊放進shoplist中並給予編號
                self.shoplist += f'{k+1}.'
                self.shoplist += self.shops[i].text[:10]
                self.shoplist += self.star[i].text+'  '
                self.shoplist += self.address[i*3].text[7:]+'\n\n'
                
            self.sw += 1#開關打開 讓下次按查詢鈕跑else
            kw.configure(text = "請輸入店家編號:")#改輸入框訊息
            message.configure(text = self.shoplist)#顯示訊息
        else:
            if not kwbox.get().isdigit() or int(kwbox.get())>len(self.shops):#要確認輸入框內是整數且編號不超過資料筆數
                message.configure(text = "請輸入列表中的數字\n\n"+self.shoplist)
                return
            self.shoplist = ""#確認文字框資訊沒問題再清空
            self.num = int(kwbox.get())-1#讀取文字框內的數字
            browser.find_elements_by_class_name("section-result")[self.num].click()#選特定店家編號    
            wait("section-back-to-list-button","找特定店家發生錯誤")
            self.shoplist += self.shops[self.num].text[:10]#只顯示選定店家訊息
            self.shoplist += self.star[self.num].text+'\n'
            self.shoplist += self.address[self.num*3].text[7:]+'\n'
            self.shoplist += ''.join([a for a in self.tel[self.num].text if a.isdigit()])+'\n'#電話只取數字
            if "cX2WmPgCkHi__section-info-hour-text" in browser.page_source:#如果有營業時間的話也放進去
                self.shoplist += browser.find_element_by_class_name("cX2WmPgCkHi__section-info-hour-text").text
            
            browser.find_element_by_class_name("iRxY3GoUYUY__button").click()#按下導航鈕
            wait("section-categorical-shortcut-button-icon","導航發生錯誤")#因為收合面板鈕一直都在，要偵測別的物件
            browser.find_elements_by_class_name("widget-pane-toggle-button")[3].click()#收合面板
            sleep(1)
            browser.save_screenshot("map.png")#螢幕截圖
            message.configure(text = self.shoplist)#顯示店家訊息
            self.sw -= 1#切回下個地點的搜尋
            map_ = tk.PhotoImage(file="map.png")
            pic.configure(image = map_)#讀入並顯示圖片
            kw.configure(text = "請輸入地點關鍵字:")
            root.mainloop()#更新同檔名圖片必加
    
    def end(self):
        browser.quit()
        message.configure(text = "程式結束，謝謝")
          
browser = webdriver.Chrome()
browser.get("https://www.google.com.tw/maps")#進入地圖
wait("section-categorical-shortcut-button-icon","定位發生錯誤")
browser.find_elements_by_class_name("widget-mylocation-button")[0].click()#按下右下定位鈕
         
step = aaa()
root = tk.Tk()
kw = tk.Label(root, text="請輸入地點關鍵字:")
kw.grid(row = 0, column = 0, sticky = tk.W)

kwbox = tk.Entry(root, width = 20)
kwbox.grid(row = 1, column = 0, sticky = tk.W)

enter = tk.Button(root, text = "查詢", command=step.do)#
enter.grid(row = 1, column = 1, sticky = tk.W)

end = tk.Button(root, text = "結束", command=step.end)#按下結束鈕關閉瀏覽器
end.grid(row = 0, column = 1, sticky = tk.W)

message = tk.Label(root, justify = 'left')
message.grid(row = 2, column = 0, sticky = tk.W)

pic = tk.Label(root)
pic.grid(row = 2, column = 1)

root.mainloop()