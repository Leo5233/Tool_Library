# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 14:56:49 2020

@author: user
"""

from tkinter import *
from pandas import read_csv
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib import font_manager
import tkinter.ttk as ttk

chinese_font = font_manager.FontProperties(fname="C:\Windows\Fonts\msjh.ttf")
data=read_csv("allStation.csv",encoding="ansi")
data2=read_csv("allStation.csv",encoding="ansi")
colorbar=[[0,112,189],[196,140,49],[0,134,89],[248,182,28],[243,165,168],[227,44,0],[218,225,31],[253,219,0]]
colorpie=[[0,112,189],[196,140,49],[0,134,89],[248,182,28],[227,44,0],[253,219,0]]
a=data.groupby(['1']).count()
a=DataFrame([a.index.tolist(),a['0']]).T

def xxx():
    total=[]
    try:
        tag = str(int(comboYear.get())-89) + comboMonth.get()
        for i in a[0]:
            total.append(data[tag][data['1']==i].sum())    
    except:
        return
    a[2]=total
    
    plt.figure(figsize=(7,5))
    barfont=plt.bar(x=range(8),height=list(a[2]/a[1]),width=0.6,color=[[i[j]/255 for j in range(3) ]for i in colorbar])
    plt.title("{}年{}月 各線平均每站載客人次".format(comboYear.get(),comboMonth.get()),FontProperties=chinese_font,fontsize=15)
    plt.xticks(range(8),["板南線","文湖線","松山新店線","中和新蘆線","新北投線","淡水信義線","小碧潭線","環狀線"],FontProperties=chinese_font)
    plt.yticks([2e5,4e5,6e5,8e5])
    for x,y in enumerate(list(a[2]/a[1])):
        plt.text(x,y,f'{y:.0f}',ha='center')
    
    plt.savefig("bar.png")
    plt.show()
    
    z=[i for i in range(len(a)) if a.iloc[i,0]=="P" or a.iloc[i,0]=="X"]
    apie=a.drop(z)
    plt.title("{}年{}月 各線載客量占全系統比例".format(comboYear.get(),comboMonth.get()),FontProperties=chinese_font,fontsize=15)
    piefont=plt.pie(apie[2],labels=["板南線","文湖線","松山新店線","中和新蘆線","淡水信義線","環狀線"],colors=[[i[j]/255 for j in range(3) ]for i in colorpie],autopct="%1.1f%%",explode=[0.02 for i in range(6)])
    for i in piefont[1]:
        i.set_fontproperties(chinese_font)
    plt.savefig("pie.png")
    plt.close()
    
    p1 = PhotoImage(file="bar.png")
    p2 = PhotoImage(file="pie.png")
    picbar.configure(image=p1,width=470,height=320)
    picpie.configure(image=p2,width=460,height=320)
    window.mainloop()

    
window=Tk()
window.geometry('1100x700')
yearLable = Label(window,text='民國(年): ')
yearLable.grid(row=0,column=0)


comboYear = ttk.Combobox(window, value = [104,105,106,107,108,109], width = 4)
comboYear.grid(row=0,column=1)

monthLable = Label(window,text='月份: ')
monthLable.grid(row=1,column=0)

temp=[f'{i:02}' for i in range(1,13)]
comboMonth = ttk.Combobox(window, value = temp, width = 4)
comboMonth.place(x=60,y=22)

picbar = Label(window)#
picbar.grid(row=4,column=3)

picpie = Label(window)#
picpie.grid(row=4,column=2)

bbar = Button(window ,command = xxx, text="顯示圖表")
bbar.grid(row=2,column=1)

p3 = PhotoImage(file="totalChart1.png")
p4 = PhotoImage(file="totalChart2.png")
picall1 = Label(window, image=p4)
picall1.grid(row=3,column=2)
picall2 = Label(window, image=p3)
picall2.grid(row=3,column=3)
window.mainloop()#維持最新狀態
