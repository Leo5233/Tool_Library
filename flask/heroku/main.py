# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 09:33:37 2020

@author: user
"""

from flask import Flask
from flask import render_template
import pandas as pd
from flask import request
#需要先開啟mysql 連線
import pymysql

a = 0

app = Flask(__name__)
    # 雙大括{{ }}告訴 HTML 5 檔案這是一個 Jinja2 的函數/變數，才能使用url_for(資料夾名, filename=)
    # <link rel="icon" href="{{ url_for('static', filename='img/aygz.ico')}}">引入icon圖
@app.route("/")#'/'代表根目錄 user只有連到此目錄時才有效果
def home():
    return render_template("home.html") 
    # 方式一：return """<h1>賴田捕手第 20 天</h1>""" 直接把原始碼return
    # 方式二：return 'Hello World'
    # 將原始碼打在一個html檔中，用render_template回傳，預設會自動抓取自建templates資料夾中html檔

    # 模板中自定義區塊{% block XXX %}{% endblock %}
    # 在要套用模板的html中加入 {% extends "檔名" %}
@app.route("/test")# 127.0.0.1:5000/test 每個分頁都要一個@app
def test():
    return render_template("home2.html")#dir的檔案路徑，和url要分清楚

    # {% for i in data/range(1,n)%}{% endfor %}
    # {% macro func(a, b,...)-%}{%- endmacro %}
    # {% set 變數=(("a","b"...))%}
    # {% if a==False %}{% endif %}
    # {{myfunction()}}
o = pd.read_csv('history_keyword.csv',header=None)
o.columns=['year', 'month', 'keyword', 'frequency', 'time']
@app.route("/test2")# 127.0.0.1:5000/test2
def test2():
    data = [list(o.iloc[i]) for i in range(len(o))]
    return render_template("home3.html", mydata=data)#mydata是在html語法中自訂的名稱

def get_db(sql):
    conn = pymysql.connect(host="localhost", user="my", password="root", database="csv_db 8", charset="utf8")
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

# 一個input頁面 和一個output頁面
@app.route("/input")# 127.0.0.1:5000/test2
def test3():
    return render_template("input.html")#mydata是在html語法中自訂的名稱
# 這裡的method表示允許的request方式 request.form是user提交的<form>資料 是一個字典 可用data['key值']
@app.route("/select_records", methods=['POST'])# 非POST會顯示405
def get_data():
    command = []
    if request.method == 'POST':
        for k, v in request.form.items():
            command.append( f"{k} = {v}".upper())# 要注意是單引號還雙引
        sql = "SELECT * FROM history_keyword WHERE " + " AND ".join(command) + ";"
    data = get_db(sql)
    
    return render_template("secret.html", mydata=data)
app.run()