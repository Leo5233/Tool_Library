from selenium import webdriver
from selenium.webdriver.support.ui import Select

# 開啟Chrome瀏覽器需下載chrome的webdriver並放在和py檔同的目錄內，注意版本要和瀏覽器版本一致
browser = webdriver.Chrome()
browser.get("http://tieba.baidu.com/f/search/adv")

# 選定網頁中的下拉式選單(<select name="sm">標籤內的name屬性)
aim = browser.find_element_by_css_selector("select[name='sm']")
#aim = browser.find_element_by_id#("如果select標籤有id屬性的話可用這個")

# 抓取下拉框中所有選項<option>標籤，並印出所有選項文字
alloption = Select(aim).options#為放有weblist物件的list
for i in alloption:
    print("元素對應的選項：%s"% i.text)

print("-----------------------分隔符---------------------------")
# 抓取選單中目前網頁顯示(選中)的選項
selected = Select(aim).all_selected_options#預設就是很多option物件的list，即使只有一個選中也要用for 迴圈才能讀文字
for i in selected:
    print("當前選中的選項(預設項)：%s" % i.text)

#也可以用select_by_value選但是要重新讀進一次all_selected_option
Select(aim).select_by_value("2")#需查看原始碼中option標籤的value為何，這個select_by動作只會傳值給內部屬性，本身不是物件沒有屬性
selected = Select(aim).all_selected_options
for i in selected:
    print("當前選中的選項(重抓)：%s" % i.text)

#print(browser.page_source)#page_source就是原始碼但經過排版，可以丟進beautifulSoup
browser.quit()