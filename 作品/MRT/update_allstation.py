# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 10:15:22 2020

@author: user
"""

import pandas as pd
import datetime as d
import requests
from pyexcel_ods import get_data
from os import remove
from mrt_chart import update_data

now = d.date.today()
#抓取資料起始時間點
year = 2020
month = 9
links = []
times = []
for i in range(year, now.year+1):
    #將起始點到現在回推2個月的年月份抓出並形成對應url
    for j in range(month if i== year else 1, now.month-1 if i == now.year else 13):
        links.append("https://web.metro.taipei/RidershipPerStation/" + str(i) + f"{j:02}" + "_cht.ods")
        times.append(f"{i}-{j}")

#將這些url一一存檔(ODS)
csv = pd.read_csv('allStation.csv', encoding='ansi',header=0)

for i,j in zip(links,times):
    with open(i[-14:], 'wb') as file:
        file.write(requests.get(i).content)
        
    ods = get_data(i[-14:])
    content= pd.DataFrame(ods['出站資料'])
    #只處理數字的部分不要標頭和欄名
    content = content.iloc[1:,1:]
    #算出每一欄的人數總和
    content = [content[index].sum() for index in content.columns]
    #第一欄為日期(要回推兩個月且只要年月)
    csv[j] = content
    #用完後將資料砍掉
    remove(i[-14:])    

csv.to_csv('allStation.csv', encoding='ansi',header=1,index=0)
update_data(csv)


