# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 18:51:56 2020

@author: USER
"""
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import dash, os, datetime

import pandas as pd
from seaborn import color_palette
#從今天算起前一個月的日期
now = datetime.date.today()
now -= datetime.timedelta(days = 30.25)

#製作長條圖所需的色票 且需轉成"rgb(r,b b)"的格式才能使用
color1 = color_palette('husl',n_colors=20)
color1 = ['rgb({},{},{})'.format(i[0]*255,i[1]*255,i[2]*255) for i in color1]

recommand = pd.read_csv("history_links.csv", header=None, encoding='ansi')
keywords = pd.read_csv("history_keyword.csv", header=None)

#預設為__main__但被呼叫時不會執行，改成__name__比較保險
app = dash.Dash(__name__)
app.layout=html.Div([
    #引入自製CSS
    html.Link(rel='stylesheet',
            href='/assets/mycss.css'),
    #網站標題欄
    html.Div("  INTERNATIONAL NEWS fOR YOU", id = "banner"),
    #推薦新聞欄標
    html.Div("  The News We Recommend for You", className = "chapter"),
    #推薦新聞表格
    html.Div(html.Table(id = "newslist"),id ="recommend_table"),
    
    #本月關鍵字欄標
    html.Div("  Popular Keywords This Month", className = "chapter"),
    
    #大圖表區塊每月字詞圖表+時間滑桿*2年和月
    html.Div(
         #左邊關鍵字勾選欄 和 提示選用字圖片
        [html.Div([dcc.Checklist( id ="keyword-checklist",options=[{'label':'', 'value':''}],value = [''], labelStyle = {'display':'block'})
                   ,html.Div(html.Img(src = "/assets/hint.png", width ='125px', height='92px', style=dict(padding = '10px')))], id = 'hint'),
            #右邊為滑桿和長條圖
            html.Div([dcc.Slider(id = "month-word-year", min = 2010, max = recommand[0].max(), value = now.year, step = 1, marks ={year : str(year) for year in range(2010, 2021)}),
                  dcc.Slider(id = "month-word-month", min = 1, max = 12, value = now.month, step = 1, marks ={month : str(month) for month in range(1, 13)}),
                  dcc.Graph(id = "month-word-frequence")], id = "graph1"),
        ], id ='chart1'),
    
    #趨勢字詞下拉選單記得要開啟multi屬性
    html.Div(dcc.Dropdown( id = "drop-down",value = [],multi=True) 
             ,style ={'height':'30px'}),  
    
    #大區塊二 左邊為字詞搜尋連結鈕 右邊為趨勢變化圖
    html.Div([html.Div(id = 'search_button'),
                html.Div(dcc.Graph(id = "history-word-frequence"))], id ="chart2")
    ])

#更新勾選選單 將滑桿年月輸入轉成對應的當月字
@app.callback(dash.dependencies.Output("keyword-checklist", 'options'),
    dash.dependencies.Input("month-word-year", 'value'),
    dash.dependencies.Input("month-word-month", 'value'))
def update_words(year, month):
    time = (year-2010)*12 + month -1
    month_word = keywords[2][keywords[4]== time]
    return [{'label':i, 'value':i} for i in month_word]

#將滑桿年月輸入抓出對應的當月字 製作成長條圖
@app.callback(dash.dependencies.Output("month-word-frequence", 'figure'),
    dash.dependencies.Input("month-word-year", 'value'),
    dash.dependencies.Input("month-word-month", 'value'))
def update_month_chart(year, month):
    #將年月合併成一個值
    time = (year-2010)*12 + month -1
    #keyword[4]為年月合併值欄 keyword[2]為關鍵字 keyword[3]為次數
    month_word = keywords[2][keywords[4]== time]
    fre = keywords[3][keywords[4]== time]
    layout = dict(xaxis ={'title':'words'}, yaxis = {'title':'times'},plot_bgcolor = '#f2f2f2',margin=dict(l=50,r=0,b=50,t=60))
    return {'data':[go.Bar(x = month_word, y = fre, width = 0.6, marker_color=color1[:len(month_word)]  )], 'layout':layout}

#推薦新聞更新 將滑桿年月輸入轉成對應的當月新聞標題和連結
@app.callback(dash.dependencies.Output("newslist", 'children'),
    dash.dependencies.Input("month-word-year", 'value'),
    dash.dependencies.Input("month-word-month", 'value'))
def update_link(year, month):
    time = (year-2010)*12 + month -1
    titles = recommand[2][recommand[4]== time]
    links = recommand[3][recommand[4]== time]
    #每一列一個標題連結 所以每列Tr只有一欄Td，欄內有一個連結a，連結的文字為新聞標題
    return [html.Tr(html.Td(html.A(i,href=j,target = '_blank'))) for i, j in zip(titles, links)]
        

#更新選取下拉選單 = 勾選選框的選項(即使勾選框隨月份換選項，以勾選的值仍會保留，相同的字再出現會顯示已勾選，所以不會重複)
@app.callback(dash.dependencies.Output('drop-down', 'options'),
    dash.dependencies.Input("keyword-checklist", 'value'))
def update_drop_down(word):
    return [{'label':i, 'value':i} for i in word if i != '']

#趨勢圖
@app.callback(dash.dependencies.Output('history-word-frequence', 'figure'),
              dash.dependencies.Input('drop-down', 'value'))
def update_historychart(words):
    #keyword[4]為年月合併值欄 keyword[2]為關鍵字 keyword[3]為次數
    filter_ = keywords[[2,3,4]][(keywords[2].isin(words))]
    filter_ = filter_.sort_values(4)
    timelim = filter_[4].max()
    fre, time , date= [],[],[]
    print(timelim)
    for word in words:
        temp1 = list(filter_[3][filter_[2] == word])
        temp2 = list(filter_[4][filter_[2] == word])
        #取最大時間timelim用range不包含所以要+1
        try:#第一次沒有下拉選單值會出錯 
            fre.append([ temp1[temp2.index(i)] if i in temp2 else 0 for i in range(timelim+1)])
        except:#但又不想隨便給個關鍵字 給全0頻率讓圖表初始一條線
            fre.append([0 for i in range(timelim)])
        time.append([i for i in range(timelim+1)])
        date.append([str(i//12+2010)+'/'+str(i%12+1) for i in range(timelim+1)])
    #日期放入text屬性中才可以引入hovertemplate內部使用 
    fig = [ go.Scatter(x = x, y = y, name = words[z], mode = 'lines', line={'width':1},opacity = 0.8, text = t, hovertemplate='<b>times:</b>%{y}<br>'+'<b>date:</b>%{text}') 
           for x, y, z, t in zip(time, fre, range(len(words)), date)]
    #記一下刻度標、margin、背景色的用法
    return {'data':fig, 'layout':dict(title = "Attention On Each Topic", 
                                      titlefont= dict(size=30, color='#333'),
                                      plot_bgcolor = '#f2f2f2',
                                      margin=dict(l=80,r=50,b=80,t=70),
                                      
                                      #變化幅度很大的極端值要用非等距的y軸刻度
                                      yaxis = {'title':'frequence',"showline":False,
                                               'tickvals':[5,10,15,20,40,60,120,180],
                                               'ticktext':['1.5%','3%','4.5%','6%','12%','18%','36%','54%' ]
                                               },
                                      xaxis = {'title':'time','showline':True,'showticklabel':True,'ticklen': 4,
                                               'tickvals':[i for i in range(130) if i % 12 ==0],
                                               'ticktext':[str(i//12+2010)+'/1' for i in range(130) if i % 12 ==0 ]
                                               })
            }

#搜尋按鈕表單 有圖片、morenews
@app.callback(dash.dependencies.Output('search_button', 'children'),
              dash.dependencies.Input('drop-down', 'value'))
def update_search(value):
    #morenews跳到google新聞頁 圖片跳到維基百科搜尋頁 所有的A都要 target = '_blank'在新分頁開啟
    more = ["https://www.google.com/search?q=","&tbm=nws"]
    what = "https://zh.wikipedia.org/wiki/"
    #因為只有連結要設hover所以要給class名稱,Dash中是用className
    return [html.H2("Find More Information")]+[html.Table(
                [html.Tr([html.Td(i), 
                html.Td(html.A(html.Img(src = "/assets/260.png"),href= what+i, target = '_blank'), className="symbol"),
                html.Td(html.A('more news', href = more[0]+i+more[1], target = '_blank'), className="morenews")
             ]) for i in value]
    )]

#dev_tools_hot_reload=True 會自動更新CSS很方便
if __name__ == '__main__':
    app.run_server(host = '0.0.0.0',
                   port = int(os.environ.get('PORT', 8050)),
                   debug = False,
                   dev_tools_hot_reload=True
                   )