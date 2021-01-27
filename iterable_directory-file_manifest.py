# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 13:02:08 2020

@author: user
"""
import os

path = "./烘焙"
def find_dir(main_path):
# 函數功能: 遞迴顯示指定路徑下的所有檔案及資料夾名稱
    for inner_file in os.listdir(main_path):
        full_path = os.path.join(main_path,inner_file)
        if os.path.isdir(full_path):#如果是資料夾
            print('資料夾:',full_path)
            find_dir(full_path)#再找內部
        else:
            print('檔案:',full_path)
find_dir(path)