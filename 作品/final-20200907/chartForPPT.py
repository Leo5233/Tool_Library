# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 18:10:43 2020

@author: user
"""
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import numpy as np

data=pd.read_csv("station.csv",encoding="ansi") 
fiscal=pd.read_csv("people.csv", encoding="utf8",header=None)
chinese_font = matplotlib.font_manager.FontProperties(fname="C:\Windows\Fonts\msjh.ttf")
bal=pd.read_csv("ticketPrice.csv", encoding="ansi")
data=data.fillna(method="ffill")


#預測
final=pd.DataFrame([range(292,406),[]])
final=final.T
final[1][:322-292]=119
final[1][322-292:346-292]=121
final[1][346-292:394-292]=127
final[1][394-292:]=143
pred=pd.concat([data.月份,data.站數],axis=1)
x=LinearRegression()
x.fit(pred,fiscal.iloc[1:,2])
q=x.predict(final)
final[2]=q
final2=pd.concat([data.月份, data.站數,fiscal.iloc[:-1,2]],axis=1)
final2.columns=[0,1,2]
final=pd.concat([final2,final]).reset_index()

fontsize=16

plt.figure(figsize=(12,8))
plt.grid()
ax1 = plt.gca()    #為了對圖表進行更進階的控制，使用gca來取得目前的軸
a1= ax1.plot(final[2],linewidth=2,color=[0,0.416,0.7],label="單日載客入")
ax2 = ax1.twinx()  #建立第二個y軸
a2= ax2.plot(final[0], final[1], linewidth=2,color=[0.48,0.71,0.11],label="設站數")  
plt.title("預測每日載客人數 VS 捷運站數",fontproperties=chinese_font,fontsize=fontsize)
ax1.set_xlabel("年份 ( 民國 )",fontproperties=chinese_font,fontsize=fontsize)
ax1.set_ylabel("人數",fontproperties=chinese_font,fontsize=fontsize)
ax2.set_ylabel("設站數",fontproperties=chinese_font,fontsize=fontsize)    #注意這裡是設定第二個軸的y標籤

plt.xticks([10+i*12 for i in range(0,34)],range(86,120))
ax1.tick_params(axis='x', labelsize=12, rotation=45 )

ax2.set_ylim(0,165)
ax2.tick_params(axis='y', labelsize=12 )

ax1.set_ylim(0,3220000)
ax1.set_yticks([5e5*i for i in range(1,8)])
ax1.tick_params(axis='y', labelsize=fontsize )
ax1.legend(a1+a2, [i.get_label() for i in a1+a2], prop=chinese_font,loc="upper left",fontsize="xx-large")
plt.show()
print("民國112年: {:.0f}".format(final[2][326:338].sum()*21.7*30))
print("民國114年: {:.0f}".format(final[2][346:358].sum()*21.5*30))
print("民國118年: {:.0f}".format(final[2][394:].sum()*21*30))


'''
pred=pd.concat([data.月份,data.站數],axis=1)
x=LinearRegression()
x.fit(pred,fiscal.iloc[1:,2])
print("迴歸係數: ",x.coef_)
print("截距: ",x.intercept_)
test=pd.DataFrame({"月份":[321,345,393],"站數":[121,127,143]})
q=x.predict(test)

print("民國113年 預估每日流量:",f"{q[0]:.0f}")
print("民國115年 預估每日流量:",f"{q[1]:.0f}")
print("民國119年 預估每日流量:",f"{q[2]:.0f}")
print("方差: ",x.score(pred,fiscal.iloc[1:,2]))  
'''

'''
#票價圖
a,b=[],[]
for i in range(0,19):
   a.append(fiscal.iloc[57+12*i:69+12*i,1].sum()) 
   b.append(data.iloc[57+12*i,1])
  

plt.figure(figsize=(22,12))
plt.grid()
ax1 = plt.gca()    #為了對圖表進行更進階的控制，使用gca來取得目前的軸
a1= ax1.plot((bal.時間-90)*12,bal.運輸收入/a*1e8,linewidth=2,color=[0,0.416,0.7],label="平均每人消費")
ax2 = ax1.twinx()  #建立第二個y軸
a2= ax2.plot(data.月份[63:]-63, data.站數[63:], linewidth=2,color=[0.48,0.71,0.11],label="設站數")  
plt.title("歷年每人消費 VS 捷運站數",fontproperties=chinese_font,fontsize=30)
ax1.set_xlabel("年份 ( 民國 )",fontproperties=chinese_font,fontsize=30)
ax1.set_ylabel("元",fontproperties=chinese_font,fontsize=30)
ax2.set_ylabel("設站數",fontproperties=chinese_font,fontsize=30)    #注意這裡是設定第二個軸的y標籤

plt.xticks([10+i*12 for i in range(0,18)],range(91,110))
ax1.tick_params(axis='x', labelsize=20 )

ax2.set_ylim(20,150)
ax2.tick_params(axis='y', labelsize=20 )

ax1.set_ylim(15,35)
ax1.set_yticks([5*i for i in range(3,8)])
ax1.tick_params(axis='y', labelsize=20 )
 
ax1.legend(a1+a2, [i.get_label() for i in a1+a2], prop=chinese_font,loc="upper left",fontsize="xx-large")
plt.show()
x=LinearRegression()
temp=pd.DataFrame(b)
x.fit(temp[6:],bal.運輸收入[5:-1]/a[5:-1]*1e8)
temp1=pd.DataFrame([[121],[127],[143]])
temp1=x.predict(temp1)
print("迴歸係數: ",x.coef_)
print("截距: ",x.intercept_)
print("方差: ",x.score(temp[9:],bal.運輸收入[9:]/a[9:]*1e8))
print("民國112年 預估每人消費:",f"{temp1[0]:.1f}")
print("民國114年 預估每人消費:",f"{temp1[1]:.1f}")
print("民國118年 預估每人消費:",f"{temp1[2]:.1f}")

plt.figure(figsize=(15,8))
plt.title("捷運站數和每人消費",fontproperties=chinese_font,fontsize=30)
plt.xlabel("站數",fontproperties=chinese_font,fontsize=30)
plt.ylabel("元",fontproperties=chinese_font,fontsize=30)
plt.axis([50,150,18,28])
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid()
plt.scatter(b,bal.運輸收入/a*1e8)
plt.plot(range(50,150),x.predict([[i] for i in range(50,150)]),'r')
'''

'''#收支圖
plt.subplot(2,1,1)
plt.title("歷年來運輸部分營收",fontproperties=chinese_font,fontsize=40)
plt.grid()
a1=plt.gca()
ax1=a1.plot(bal.時間,bal.運輸收入,color=[0,0,0])
plt.yticks([50,100,150,200],fontsize=20)
plt.xticks(range(90,109),fontsize=20)

plt.ylabel("億元",fontproperties=chinese_font,fontsize=30)
plt.subplot(2,1,2)
plt.title("歷年來運輸部分支出",fontproperties=chinese_font,fontsize=40)
plt.xlabel("年份 ( 民國 )",fontproperties=chinese_font,fontsize=30)
plt.ylabel("億元",fontproperties=chinese_font,fontsize=30)
plt.grid()
plt.axis([89,109,50,200])
plt.yticks([50,100,150,200],fontsize=20)
plt.xticks(range(90,109),fontsize=20)
a2=plt.gca()
ax2=a2.plot(bal.時間,bal.運輸支出,'r-')
'''

'''
plt.figure(figsize=(24,12))
plt.axis([0,291,0,144])
plt.grid()
plt.plot(data.月份,data.站數,linewidth=2,color=[0.48,0.71,0.11])
plt.title("台北捷運歷年捷運設站數量變化",fontproperties=chinese_font,fontsize=40)
plt.xlabel("年份 ( 民國 )",fontproperties=chinese_font,fontsize=30)
plt.xticks([10+i*12 for i in range(0,24)],range(86,110),fontsize=20)
plt.yticks(fontsize=20)
plt.ylabel("捷運站數量",fontproperties=chinese_font,fontsize=30)
'''

'''
#載客數和站數圖
plt.figure(figsize=(24,12))
plt.grid()
ax1 = plt.gca()    #為了對圖表進行更進階的控制，使用gca來取得目前的軸
a1= ax1.plot(fiscal.iloc[:,2],linewidth=2,color=[0,0.416,0.7],label="單日載客入")
ax2 = ax1.twinx()  #建立第二個y軸
a2= ax2.plot(data.月份, data.站數, linewidth=2,color=[0.48,0.71,0.11],label="設站數")  
plt.title("歷年載客人數 VS 捷運站數",fontproperties=chinese_font,fontsize=30)
ax1.set_xlabel("年份 ( 民國 )",fontproperties=chinese_font,fontsize=30)
ax1.set_ylabel("人數",fontproperties=chinese_font,fontsize=30)
ax2.set_ylabel("設站數",fontproperties=chinese_font,fontsize=30)    #注意這裡是設定第二個軸的y標籤

plt.xticks([10+i*12 for i in range(0,24)],range(86,110))
ax1.tick_params(axis='x', labelsize=20 )

ax2.set_ylim(0,130)
ax2.tick_params(axis='y', labelsize=20 )

ax1.set_ylim(0,2520000)
ax1.set_yticks([3.5e5*i for i in range(1,8)])
ax1.tick_params(axis='y', labelsize=20 )
 
ax1.legend(a1+a2, [i.get_label() for i in a1+a2], prop=chinese_font,loc="upper left",fontsize="xx-large")
plt.show()

 '''



'''#人次圖
plt.figure(figsize=(24,12))
plt.axis([0,291,0,2520000])
plt.grid()
plt.plot(fiscal.iloc[:,2],linewidth=2,color=[0,0.416,0.7])
plt.title("台北捷運歷年每日載客人次 ( 月結算 )",fontproperties=chinese_font,fontsize=40)
plt.xlabel("年份 ( 民國 )",fontproperties=chinese_font,fontsize=30)
plt.xticks([10+i*12 for i in range(0,24)],range(86,110),fontsize=20)
plt.yticks([3.5e5*i for i in range(1,8)],[35*i for i in range(1,8)],fontsize=20)
plt.ylabel("人數 ( 萬人 )",fontproperties=chinese_font,fontsize=30)
'''
