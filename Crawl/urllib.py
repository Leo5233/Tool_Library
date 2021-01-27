# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 22:49:23 2020

@author: user
"""

from urllib.parse import urlparse
import requests
url = "https://www.google.com/search?q=news&rlz=1C1WPZB_enTW722TW722&oq=news&aqs=chrome..69i57j0i433j0l2j0i131i433j69i60l3.2199j0j7&sourceid=chrome&ie=UTF-8"
info = urlparse(url)
print(info)
"""
會產生網址剖析結果，輸出資料用info.參數，參數有：
scheme(通訊協定)、netloc(網域)、path(環境變數)、params(參數)、query(檢索屬性)、fragment()
"""
a = requests.get(url)
wod = a.text.splitlines()