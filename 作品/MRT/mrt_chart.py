import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

def update_data(csv):
    #不含新北投和小碧潭的其他色
    colorbar=[[0.0, 0.44, 0.74],[0.77, 0.55, 0.19],[0.0, 0.53, 0.35],[0.97, 0.71, 0.11],[0.89, 0.17, 0.0],[0.99, 0.86, 0.0]]
    #stack為每條線總人數
    stack = csv.pivot_table(index=['color_code'],aggfunc='sum')
    #avg為每條線有幾站 values要選環狀線出現後的欄位
    avg = csv.pivot_table(index=['color_code'], values = ['2020-7'],aggfunc='count')
    #將每條線站數加到stack
    stack['count'] = avg['2020-7']
    #其時不建議將資料作為欄，但因為原始資料就長這樣，所以要將columns取出，另外也將pivot後的index取出
    coco = stack.index.tolist()
    date =stack.columns.tolist()
    
    chart = []
    for i in coco:
        #排除新北投和小碧潭
        if i != 'P' and i != 'X':
            #最後面一欄是新加入的'count'
            for j in date[:-1]:
                #因為欄名格式是YYYY-M 所以要切開轉換成數字
                time = j.split('-')
                time = (int(time[0])-2015) * 12 + int(time[1]) - 7
                #最後有時間、color_code、該色該月總人數、該線站數、此線佔該月總比例 float是因為seaborn畫圖指定格式
                chart.append([time, i, 
                              float(stack[j][i]), 
                              stack['count'][i], 
                             float(stack[j][i]/stack[j].sum())
                             ])
    
    chart = pd.DataFrame(chart, columns = ['date','color_code','traffic','station_num','proportion'])
    #再新增一欄該月該線平均每站載客人數
    chart['avg_traffic'] = chart['traffic'] / chart['station_num']
    #照日期排序方便繪圖
    chart.sort_values('date',ascending=True)
    plt.figure(figsize=(12,8),dpi=72)
    
    sns.set_style("darkgrid",{"font.sans-serif":'Microsoft JhengHei'})
    avg = sns.relplot(data=chart, x='date', y='avg_traffic', hue='color_code', palette=colorbar,kind='line')
    avg.set(title="各線每月每站平均載客人次",xlabel="時間",ylabel="人次", xticks=[ i for i in chart['date'] if i % 12 == 6])
    avg.set_xticklabels([ (i+7) // 12 + 2015 for i in chart['date'] if i % 12 == 6],color='#777')
    #labelsize為字型大小
    plt.tick_params(axis='x',labelsize =10,rotation=45)
    #將seaborn自動加入的圖示標題改掉
    plt.xlim(0,chart['date'].max())
    avg.legend.set_title("")
    avg.savefig('assets/avg_history.png')
    plt.clf()
    temp = [ chart['proportion'][chart['color_code'] == color] for color in chart['color_code'].unique() ]
    #stackplot沒有x=, y= ，且預設會有邊線，要取消要edgecolor設成透明
    strip = plt.stackplot( range(chart['date'].max()+1), temp, colors=colorbar, edgecolor='#0000')
    plt.title("各路線載客占全系統比例")
    plt.xlabel("時間")
    plt.ylabel("百分比")
    plt.yticks([0,0.2,0.4,0.6,0.8,1],[0,20,40,60,80,100])
    plt.xticks([ i for i in chart['date'] if i % 12 == 6], [(i+7) // 12 + 2015 for i in chart['date'] if i % 12 == 6], color='#777')
    plt.tick_params(axis='x',labelsize =10,rotation=45)
    plt.ylim(0,1)
    plt.xlim(0,chart['date'].max())
    #不加這個標題會被切掉
    plt.tight_layout()
    plt.savefig('assets/proportion.png')