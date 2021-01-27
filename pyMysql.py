# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 18:23:20 2021

@author: user
"""

import pymysql
# 可以是password/passwd database/db
x = pymysql.connect(host="localhost",
                            user="my",
                            password="root",
                            database="python_test",
                            charset="utf8")#不是utf-8
a = x.cursor()
a.execute("SELECT * FROM CUSTOMER;")
# 用for迴圈輸出或fetchall()都可以 每筆一個tuple
data = a.fetchall()
# a.description為欄位的詳細資料 (欄位名稱, 資料類型編號, ?, 最小長度, 最大長度, ? ,非空)
print(a.description)
# for i in a:
#     print(i)

'''
# 如果要執行多行語法要用""" 包起來""" 但一次只能放一個指令(分號)
sql = """
UPDATE my_class SET ms_math = 60 WHERE ms_math <= 60;
"""
a.execute(sql)
x.commit()# 不是a.commit()
'''

# 將python的資料放進去sql查詢中可用.format()或是LIKE '%s';" % 變數

# 最後兩個都要close() 且要注意順序
a.close()
x.close()