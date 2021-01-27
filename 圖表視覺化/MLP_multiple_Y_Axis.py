# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 16:42:15 2020

@author: user
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
chinese_font = matplotlib.font_manager.FontProperties(fname="C:\Windows\Fonts\msjh.ttf")
x=np.sort(np.random.rand(1,16))*10
y1=np.sort(np.random.rand(1,16))*10
y2=np.sort(np.random.rand(1,16))*100
y3=np.sort(np.random.rand(1,16))*50

#設定圖表大小和解析度要在所有軸之前
#plt.figure(figsize=(12,8), dpi = 100) 
axis1 = plt.gca()    #為了對圖表進行更進階的控制，使用gca來取得目前的軸
axis2 = axis1.twinx()  #建立第二個y軸 並以軸作圖axis.plot而非plt.plot(永遠只有一個y軸)
axis3 = axis1.twinx() #第三軸
axis3.spines["right"].set_position(("axes", 1.2))#地3Y軸會重疊所以要位移

#axis3.set_frame_on(False) 可隱藏刻度主軸線

#X軸刻度顯示值一定要用xticks()設定,但字型大小要用tick_params的labelsize設定
plt.xticks(range(11))
axis1.tick_params(axis='x', labelsize=20 ,rotation=30)#用來旋轉刻度
axis1.set_xlabel("共用X軸",fontproperties=chinese_font,fontsize=20)

#標籤一律用set_x/ylabel() 不可用x/label() 其中,labelpad設定刻度和軸標題距離，loc設定位置xlabel 要用左右 ylabel用頂底
axis1.set_ylabel("Y軸1",fontproperties=chinese_font,fontsize=20,)
axis2.set_ylabel("Y軸2",fontproperties=chinese_font,fontsize=20, labelpad=-10, loc="bottom")    #注意這裡是設定第二個軸的y標籤
axis3.set_ylabel("Y軸3",fontproperties=chinese_font,fontsize=20, labelpad=-10, loc="bottom",rotation=0)    #注意這裡是設定第二個軸的y標籤rotation=0轉水平

#雙Y軸刻度只能給值(才有互相比較的意義)，所以set_yticks()只給位置list即可
#一個軸的定義要給最大最小值、刻度值、字型大小和顏色
axis1.set_ylim(0,10)
axis1.set_yticks(range(2,11,2))
axis1.tick_params(axis='y', labelsize=20 ,colors='b')

axis2.set_ylim(0,100)
axis2.set_yticks([20,40,60,80,100])
axis2.tick_params(axis='y', labelsize=20 ,colors='r',rotation = 20)

axis3.set_ylim(0,51)
axis3.set_yticks([10,20,30,40,50])
axis3.tick_params(axis='y', labelsize=20 ,colors='g')

#設定好再畫圖比較保險
lab1= axis1.plot(x[0],y1[0],label="AAA")
lab2= axis2.plot(x[0], y2[0],'r',label="BBB")  
lab3= axis3.plot(x[0], y3[0],'g',label="CCC")  

#lab為[Line2D物件] 也可以用ax1.lines + ax2.lines + ax3.lines
#legend的第一項其實是handles屬性 第二個為labels 屬性
#plt.legend(handles =lab1+lab2+lab3, labels = [i.get_label() for i in lab1+lab2+lab3]
axis1.legend(lab1+lab2+lab3, [i.get_label() for i in lab1+lab2+lab3], prop=chinese_font,loc="upper left")
plt.show()
#多Y軸一定要用show()來顯示不然圖會存在lab物件中