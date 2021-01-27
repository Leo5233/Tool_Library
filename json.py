# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 08:45:09 2020

@author: user
"""
import pandas as pd
import json as js
import re
y = '{"工廠登記編號":"99687850","食品業者登錄字號":"H-142612538-00001-7","驗證效期":"108/01/06~110/01/05","驗證業別":"乳品加工食品業、其他、澱粉製造業、糖製造業","工廠或製造場所地址":"桃園市觀音區樹林里經建一路32號","工廠或製造場所名稱":"開元食品工業股份有限公司觀音二廠"}'
with open("192_5.json",encoding= 'utf-8-sig') as x:
    #dic_data = js.load(x) 最方便和read只能二選一
    list_2D = x.read()
list_2D = list_2D[2:-2].split('},{')
list_2D = [re.findall(':"(.*)".*:"(.*)".*:"(.*)".*:"(.*)".*:"(.*)".*:"(.*)"',i) for i in list_2D ]
one_data = js.loads(y) #只能讀一筆
pd_data = pd.read_json("192_5.json",encoding= 'utf-8-sig')