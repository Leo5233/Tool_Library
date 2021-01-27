from selenium import webdriver
from bs4 import BeautifulSoup
import tkinter as tk
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests, os

# 類別名 出錯關閉browser與否 訊息輸出
def waiting( name, end, message):
    try:
        WebDriverWait(browser, 6, 0.3).until(
            EC.presence_of_element_located((By.CLASS_NAME, name)))# 不加就讀不到
    except:
        if end == True:
            print(message)
            browser.quit()

class aaa:
    # 由於每次都是依序輸入關鍵字、編號、圖數，所以設一個開關sw每次按下按鈕都依序012012...
    # 還有關鍵字kw 計數num
    kw, num, sw = 0, 0, 0
    def do(self):
        if  self.sw == 0:
            self.sw = 1
            self.kw = kwbox.get()
            # ig將關鍵字輸入搜尋欄 確定
            browser.find_element_by_class_name("XTCLo").send_keys(self.kw)
            waiting("yCE8d",0,"選單沒出來")
                
            x = BeautifulSoup(browser.page_source, "html.parser")
            self.ig = x.find_all('a',class_="yCE8d")# 粉絲頁連結
            title = x.find_all("span",class_="Ap253")# 粉絲頁名稱
            temp = []
            for i in range(len(title)):
                # 在畫布框架組中生成文字為 _1: xxx換行 的Label物件
                # 將第n個label定位在第n列
                tex = "{: 2}: {}".format(i+1, title[i].text) + '\n'
                temp.append(tk.Label(frame_texts, text=tex))
                temp[-1].grid(row=i, column=0, sticky='news')
            # 隨卷軸滾動會改變frame內的顯示內容.update_idletasks()使卷軸不要回捲
            frame_texts.update_idletasks()
            # 設定畫布捲動的範圍
            canvas.config(scrollregion=canvas.bbox("all"))
            info.configure(text = "請輸入要抓取的IG編號: ")

        elif self.sw == 1:
            self.num = int(kwbox.get())
            self.sw = 2
            # 用關鍵字建資料夾
            os.mkdir(self.kw)
            browser.get("https://www.instagram.com" + self.ig[self.num-1]["href"])
            waiting("FFVAD", 1, "選單沒出來")
            info.configure(text="請輸入所需要的圖片數量:")

        else:
            self.num = int(kwbox.get())
            count, available = 0, 0
            error = 0            
            pic_urls = []
            # 因為IG改版之後沒辦法讀取太多圖 最多到42張之後，就會把之前的圖的標籤語法從page_source中拿掉
            # 所以要每次下拉就將新讀到的圖片url放入pic_urls中(過濾重複)
            while True:
                browser.find_element_by_tag_name('body').send_keys(Keys.END)
                sleep(1)
                x2 = BeautifulSoup(browser.page_source, "html.parser")
                pic = x2.find_all('img', class_="FFVAD")
                
                for i in pic:
                    # IG圖片的src有防抓所以網址無效 必須抓srcset 裡面有該圖各種尺寸的版本其格式為url..空格150px,url..空格200px,....
                    # 所以用' '找index 之前的字元全取便是完整的第一個url
                    temp = i["srcset"]
                    temp = temp[:temp.index(' ')]
                    if temp not in pic_urls:#去重複
                        pic_urls.append(temp)
                
                # 數量達標就break
                if len(pic_urls) >= self.num: 
                    break
                #available會紀錄上一輪的圖片連結數量 如果上一輪和此輪數量相同表示沒讀到新的
                elif len(pic_urls) == available: 
                    print(len(pic_urls), available)
                    # 連續2次沒讀到判定是頁面捲到底了
                    if error == 1:
                        tk.messagebox.showinfo("提示", "網站圖片數量不夠")
                        break
                    # 如果是第一次沒讀到 錯誤次數+1
                    else:
                        error = 1
                # 如果有正確讀到新的圖連結 表示沒發生錯誤或只偶然發生一次(可能browser跑太慢)，error重新計算
                else:
                    error = 0
                # 紀錄本次的圖連結數 供下次比較
                available = len(pic_urls) 
            
            # 存圖
            for i in pic_urls:
                with open(f'{self.kw}/{count+1}.jpg', 'wb') as save:
                    save.write(requests.get(i, headers=my_header).content)
                count += 1
                if count == self.num: break
                info.configure(text="已下載完成，請輸入搜尋關鍵字或關閉視窗: ")
                self.sw = 0

# 給圖片request用的header
my_header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
browser = webdriver.Chrome()
browser.get("https://www.instagram.com/")
waiting("_2hvTZ",1,"連線超時")
# 輸入帳密登入
browser.find_elements_by_class_name("_2hvTZ")[0].send_keys('vspk5@yahoo.com.tw')
browser.find_elements_by_class_name("_2hvTZ")[1].send_keys('zpqmlaqwe123')
browser.find_element_by_class_name("L3NKy").click()
# 如果有出現儲存帳密和開啟通知的頁面出現要點擊略過
waiting("cmbtv",0,"這次沒有儲存帳密資料頁面")# 和前一頁有同樣的btn class所以必須找該頁獨有的其他東西來偵測
browser.find_element_by_class_name("yWX7d").click()
waiting("HoLwm",0,"這次沒有開啟通知提醒")
browser.find_element_by_class_name("HoLwm").click()
waiting("XTCLo",1,"連入個人IG內頁超時")

root = tk.Tk()
step = aaa()
# 產生TK視窗上而下依序為提示字、輸入框和確定鈕、框架
info = tk.Label(root, text="請輸入搜尋關鍵字或關閉視窗: ")
info.grid(row=0, column=0, sticky=tk.W)
kwbox = tk.Entry(root, width=20)
kwbox.grid(row=1, column=0, sticky='w')
enter = tk.Button(root, text="確定", command=step.do)
enter.grid(row=1, column=1, pady=(5, 0), sticky='nw')# pady為邊框

# 生成一個框架(需定位) frame物件可以用來放置其他物件
frame_canvas = tk.Frame(root)
frame_canvas.grid(row=2, column=0)
#此三行為去除frame的周圍多於空白
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
frame_canvas.grid_propagate(False)
frame_canvas.config(width=200, height=400)

# frame內建立一個畫布擴張至和frame一樣大(sticky='news') 相對於frame相對定位
# 但此時的frame還沒設定大小
canvas = tk.Canvas(frame_canvas)
canvas.grid(row=0, column=0, sticky="news")

# 卷軸要設command但frame物件沒有yview 所以一定要有canvas 
vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
# 卷軸定位通常都是row=0, column=最右欄, sticky='ns'
vsb.grid(row=0, column=1, sticky='ns')
# 讓卷軸移動幅度可以對上內容移動篇幅
canvas.configure(yscrollcommand=vsb.set)

# 畫布內再生成一個frame
frame_texts = tk.Frame(canvas)
# 因為要用Label來存IG粉絲頁名稱，而Label又必須放在frame物件內
# 而卷軸須要一個frame物件裝卷軸和一個canvas來設command
# 但卷軸不能控制frame物件所以 最後是frame裡有卷軸和canvas, canvas再生成frame裝入被卷軸控制的東西
# 最後透過create_window使畫布和frame綁在一起捲動(不然frame不會動)
canvas.create_window((0, 0), window=frame_texts, anchor='nw')
root.mainloop()
browser.quit()

