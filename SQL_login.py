# -*- coding: utf-8 -*-
import pymysql
from time import sleep
# mysql要先用control panel啟用才能聯
conn = pymysql.connect(host='localhost', 
                       user='my',
                       password='root',
                       database='test',
                       charset='utf8')

a = conn.cursor()
user_id, psw = 0, 0
def create_account():
    user_id = input("請輸入帳號: ")
    sql = f"""SELECT em_userid from EMPLOYEE WHERE EM_userid = "{user_id}" """
    a.execute(sql)
    data = a.fetchall()
    if data:
        print("帳號已存在，請輸入其他帳號")
        return create_account()
    else:
        name = input("請輸入姓名: ")
        while True:
            psw = input("請輸入密碼: ")
            if psw == input("請再次輸入密碼: "):
                sql = f"""INSERT INTO EMPLOYEE(em_name, em_userid, em_psw) VALUES("{name}", "{user_id}","{psw}");"""
                a.execute(sql)
                conn.commit()
                print("新帳戶註冊成功!")
                break
            else:
                print("兩次輸入不一樣，請重新輸入")
        return

def login():
    global user_id, psw
    user_id = input("請輸入帳號: ")
    sql = f"""SELECT em_userid from EMPLOYEE WHERE EM_userid = "{user_id}" """
    a.execute(sql)
    data = a.fetchone()
    if data:
        psw = input("請輸入密碼: ")
        sql = f"""SELECT * from EMPLOYEE WHERE EM_userid = "{user_id}" AND EM_psw = "{psw}"; """
        a.execute(sql)
        data = a.fetchone()
        if data:
            print("登入成功")
            return user_id, psw
        else:
            print("密碼不正確!")
    else:
        print("帳號不存在!")
    return 0,0

def query(user_id, psw):
        sql = f"""SELECT * from EMPLOYEE WHERE EM_userid = "{user_id}" AND EM_psw = "{psw}"; """
        a.execute(sql)
        data = a.fetchone()
        print("您的資料如下: ")
        print(data)

def delete(user_id, psw):
    if input("確定要刪除資料嗎，請輸入Y(是)/N(否): ").upper() == 'Y':
        sql = f"""DELETE from EMPLOYEE WHERE EM_userid = "{user_id}" AND EM_psw = "{psw}"; """
        a.execute(sql)
        conn.commit()
        print("刪除成功!")
        return 1
    else:
        print("要求取消")
        return 0


def change(user_id, psw):
    while True:
        psw2 = input("請輸入新密碼: ")
        if psw2 == psw:
            print("新密碼不得和原本的一樣")
        elif psw2 == input("請再次輸入密碼: "):
            sql = f"""UPDATE EMPLOYEE SET EM_psw = "{psw2}" WHERE EM_userid = "{user_id}" AND EM_psw = "{psw}";"""
            a.execute(sql)
            conn.commit()
            print("修改成功!")
            break
        else:
            print("兩次輸入不一樣，請重新輸入")
        
while True:
    num = input(
        """1 新增帳號
2 登入
3 結束
請輸入數字: """)
    if num == '3': 
        break
    elif num == '1':
        create_account()
    elif num == '2':
        user_id, psw = login()
        while user_id and psw:
            sleep(1)
            num = input("1 查詢資料\n2 刪除資料\n3 修改密碼\n4 登出\n請輸入數字: ")
            if num == '4': 
                print("已登出")
                break
            elif num == '1':
                query(user_id, psw)
            elif num == '2':
                result = delete(user_id, psw)
                if result: break
            elif num == '3':
                change(user_id, psw)
            else:
                print("輸入格式不正確，請輸入數字")
    else:
        print("輸入格式不正確，請輸入數字")
    sleep(1)
print("感謝使用")
a.close()
conn.close()