# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
fu = requests.get("要抓取的網路檔案連結")
with open("路徑和檔名",'wb') as data:#抓取並存檔
    data.write(fu.content)