# -*- coding: utf-8 -*-

# s=size直徑 c=color線色 facecolors=點色
plt.scatter(x, y, s=300, linewidth=1, color='r', facecolors='white',alpha=.5)

# explode為扇形外推值要測試 autopct='%{文字格式}%'看要幾位小數 wedgeprops={'width':內圓直徑佔外圓比例}可挖空成環狀
labels = plt.pie(list, labels=['a','b','c'], 
                colors=['w','k','r'], 
                shadow=True, explode=[.1,.2,.1], 
                autopct='%1.2f%%',
                startangle=20,
                counterclock=True,
                wedgeprops={'width':0.5})

# 可用for i in labels:
#         i.set_fontproperties(....)

# align='center/edge'代表X軸刻度在棒狀的左下角或正中央
plt.bar(x=xlist, height=ylist, width=1, tick_label=['a','b','c'], align='edge')
# 長條圖要每根棒加字可用for i, y in enumerate(ylist):
#     plt.text(i, y, '顯示文字', ha="center") ha為文字對齊方式

# 填滿兩條線的色塊 所以要有兩個Ylist
plt.fill_between(xfit, yfit - d, yfit + d, edgecolor='none',
                      color='#AAAAAA', alpha=0.4)

# 堆疊圖色塊(不重疊)
plt.stackplot(xlist, ylist1, ylist2, ...., colors=['r', 'b', 'k'])

# 階梯折線圖 常搭配np.cumsum()繪製階梯狀累加線圖 where='pre/mid/post'階梯升起在刻度的左/中/右端
plt.step(range(1, 14), np.cumsum(var_exp), where='post',label='cumulative explained variance')

# 可調子圖的邊框 和長寬比 參數要測試
plt.subplots_adjust(left = 0.1, bottom = 0.2, right = 0.9, top = 0.9, wspace = 0.4, hspace = 0.1)

# 繪製3D圖
from mpl_toolkits import mplot3d
ax = plt.subplot(projection='3d')
ax.scatter3D(X, Y, Z, c=y, s=50, cmap='autumn')
ax.view_init(elev=45, azim=0)# elev上下視角轉動 azim水平視角轉定
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('r')

# 互動式 需在Jupiter上執行
from ipywidgets import interact, fixed

def plot_3D(elev=30, azim=30, X=X, y=y):
    ax = plt.subplot(projection='3d')
    ax.scatter3D(X[:, 0], X[:, 1], r, c=y, s=50, cmap='autumn')

interact(plot_3D, elev=[-180, 180], azip=(-180, 180),
          X=fixed(X), y=fixed(y))

#不顯示XY軸
ax.axis('off')