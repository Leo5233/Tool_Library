# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 09:33:40 2020

@author: user
"""

import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import dash, os
import pandas as pd


logo=[[0,0.416,0.7],[0.48,0.71,0.11]]
colorbar=["rgb(0,112,189)","rgb(196,140,49)","rgb(0,134,89)","rgb(248,182,28)","rgb(243,165,168)","rgb(227,44,0)","rgb(218,225,31)","rgb(253,219,0)"]
data=pd.read_csv("allStation.csv",encoding="ansi")
data = data[(data['color_code'] != 'P') &  (data['color_code'] != 'X')]
route = ['板南線', '木柵線', '新店線', '蘆洲線','淡水線', '環狀線']
code = ['BL','BR','G','O','R','Y']
#將日期年月切開，轉換資料類型方便雙滑桿操作，完成便可刪除原本的日期欄
date = data.columns.to_list()
y_m = date[-1].split('-')
max_time = (int(y_m[0])-2015)*12 + int(y_m[1]) - 7

#取出a的色彩代號欄計算每線多少站
#變成色彩代號和站數兩欄
app = dash.Dash(__name__)
app.layout=html.Div([
    #引入自製CSS
    html.Link(rel='stylesheet', href='/assets/mycss.css'),
    #網站標題欄
    html.Div(" Taipei MRT ", className = "banner"),
    
    html.Div(
        [html.Div(
            [html.Img(id = "stack2", src='/assets/proportion.png'),
             html.Div(id='mask1',
                      style ={'background-color':'#0004',
                              'position':'absolute',
                             	'left':'43px',
                             	'top':'23px',
                             	'width':'291px',
                             	'height':'222px'})],id='stack1'),
             
          html.Div(dcc.Graph(id = "fan2"), id = 'fan'),
          
          html.Div([ 
              html.Img(id = "avg2", src='/assets/avg_history.png'),
              html.Div(id='mask2',
                      style ={'background-color':'#0004',
                              'position':'absolute',
                             	'left':'62px',
                             	'top':'23px',
                             	'width':'278px',
                             	'height':'300px'})], id = "avg1")]
          
          , className = "graph-group"),
    
    
    html.Div(
        [dcc.Slider(id = "year", 
                    min = 2015, 
                    max = int(y_m[0]), 
                    value = int(y_m[0]), 
                    step = 1, 
                    marks ={y : str(y) for y in range(2015, int(y_m[0])+1)}),
         
          dcc.Slider(id = "month", min = 1, max = 12, 
                    value = int(y_m[1]), 
                    step = 1, 
                    marks ={month : str(month) for month in range(1, 13)})],id='slider'),
    
    html.Div(dcc.Checklist(id='check',options=[{'label':i,'value':j}for i, j in zip(route, code)]
                           ,value=code)),
    html.Div(dcc.Graph(animate= True, id = "bubble"),id='chart2'),
    html.Div(" 未來規劃 ", className = "banner"),
    html.Div([html.Img(src='assets/Figure.png', id='endimg1'), html.Img(src='assets/plan.jpg', id='endimg2')], className = "graph-group" )
    
    ])


    
@app.callback(dash.dependencies.Output('mask1','style'),
              dash.dependencies.Input('year','value'),
              dash.dependencies.Input('month','value'))
def change_mask1(year, month):
    proportion = ((year-2015)*12 + month - 7) / max_time
    mask_size1 = str(int(291*proportion))+'px'
    return {'background-color':'#0004',
                              'position':'absolute',
                             	'left':'43px',
                             	'top':'23px',
                             	'width':mask_size1,
                             	'height':'222px',
                                 'z-index':100}


@app.callback(dash.dependencies.Output('mask2','style'),
              dash.dependencies.Input('year','value'),
              dash.dependencies.Input('month','value'))
def change_mask2(year, month):
    proportion = ((year-2015)*12 + month - 7) / max_time
    mask_size2 = str(int(278*proportion))+'px'
    return {'background-color':'#0004',
                              'position':'absolute',
                             	'left':'62px',
                             	'top':'23px',
                             	'width':mask_size2,
                             	'height':'300px'}

@app.callback(dash.dependencies.Output('fan2','figure'),
              dash.dependencies.Input('year','value'),
              dash.dependencies.Input('month','value'))
def fan_chart(year, month):
    col = str(year)+'-'+str(month)
    y, m =year, month
    if ((year-2015)*12 + month - 7) < 0 or ((year-2015)*12 + month - 7) > max_time:
        y, m = 2015, 7
        col='2015-7'
    data2 = data.pivot_table(index='color_code', values = col, aggfunc=['sum','count'])
    data2.columns = data2.columns.droplevel(1)
    data2 = data2.reset_index()
    
    data2['avg']= data2['sum'] / data2['count']
    data2['proportion'] = data2['sum'] / data2['sum'].sum() * 360
    data2['color'] = ["rgb(0,112,189)","rgb(196,140,49)","rgb(0,134,89)","rgb(248,182,28)","rgb(227,44,0)","rgb(253,219,0)"]
    data2['name'] = route
    data2['theta'] = [ data2.iloc[:i+1,4].sum() - data2['proportion'][i]/2 for i in range(len(data2))]
    barpolar_plots = [go.Barpolar(r= [data2['avg'][i]], 
                                  width= data2['proportion'][i], 
                                  name = data2['name'][i], 
                                  marker_color = data2['color'][i], 
                                  theta=[data2['theta'][i]],
                                    hovertemplate = "載客量: %{r:.0f}人/站<br>占比: "+'{:.2f}%'.format(data2['proportion'][i]/3.6),
                                    opacity=0.85
                                    )
                      for i in range(len(data2))]
    
    layout = go.Layout(title =  str(y) + '年' + str(m) + "月 各線單站平均載客人數 和 占全系統流量比例",
                       title_font_size = 18,
                       margin = { 'b': 90, 'r': 30, 't': 60},
                       legend = {'x':0.9,'y':0.8},
                       polar = {'angularaxis':{'ticks':'', 'showticklabels':False, 'gridcolor':'#ddd'},
                                'radialaxis':{'gridcolor':'#ccc'}}
                       )
    return {'data': barpolar_plots, 'layout': layout}

@app.callback(dash.dependencies.Output('bubble','figure'),
              dash.dependencies.Input('year','value'),
              dash.dependencies.Input('month','value'),
              dash.dependencies.Input('check','value'))
def bubble_chart(year, month, colors):
    col = str(year)+'-'+str(month)
    last_year = str(year-1)+'-'+str(month)
    y, m =year, month
    if ((year-2015)*12 + month - 7) < 12 or ((year-2015)*12 + month - 7) > max_time:
        y, m = 0, 0
    if last_year not in data.columns or col not in data.columns: 
        last_year = '2015-7'
        col = '2016-7'
    data2 = data[['station','color_code',col,last_year]].copy()
    data2['growth'] = (data2[col]-data2[last_year])/data2[last_year]*100
    data2['size'] = data2[col]**0.7/400
    data2 = data2.fillna(0)
    info = pd.DataFrame({'color_code':data2.color_code.unique(),
                         'color':["rgb(170,130,30)","rgb(0,112,189)", "rgb(0,134,89)","rgb(255,182,28)","rgb(240,44,0)","rgb(255,240,0)"],
                         'name':route})
    
    trace = []
    for i in colors:
        temp = data2[data2['color_code'] == i]
        trace.append(
            go.Scatter(
                x = temp['growth'],
                y = temp[col],
                text = temp['station'],
                mode = 'markers',
                opacity= 0.95,
                name = info['name'][info['color_code'] == i].values[0],
                hovertemplate = "%{text}站<br>載客量: %{y:.0f}人<br>成長率: %{x}%",
                marker = {'color': info['color'][info['color_code'] == i].values[0] ,
                          'size':temp['size'],
                          'line':{'width': 0.5, 'color': '#ddd'}}
                ))   
    layout = go.Layout(title=str(y) + '年' + str(m) + "月 各站載客流量和對比去年同期成長率",
                       title_font_size=18,
                       xaxis={'title':'對比去年成長率','range':(-50,30)},
                       yaxis={'title':'人次','type':'log'},
                       plot_bgcolor='#e5effa'
                       )

    return {'data':trace,'layout':layout}
    

#dev_tools_hot_reload=True 會自動更新CSS很方便
if __name__ == '__main__':
    app.run_server(host = '0.0.0.0',
                   port = int(os.environ.get('PORT', 8050)),
                   debug = False,
                   dev_tools_hot_reload=True
                   )
