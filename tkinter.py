# -*- coding: utf-8 -*-
# 如果物件需要接受回傳值，則定位要分另外一行，不需要接收值的物件可直接在產生時將.pack()接在後面

import tkinter as tk
n = 1
def add():
    global n
    varStr.set(f"加數字: {n}")
    n += 1

def show_radio():
    varStr.set("選中的是"+varStr2.get())

def show_checkbox():
    temp = "你選了:"
    for i in range(len(booleanList)):
        if booleanList[i].get() == 1:#不要忘記.get()
            temp += option[i]+','
    varStr.set(temp)
    
def entry_get():
    # tk.INSERT 和tk.END好像沒差?
    if entry.get():
        str_box.insert(tk.INSERT, "您輸入的文字為: "+entry.get()+'\n')
    else:
        str_box.insert(tk.END, "結束\n"+entry.get()+'\n')
    # 隨卷軸滾動會改變frame內的顯示內容.update_idletasks()使卷軸不要回捲
    frame_texts.update_idletasks()
    # 設定畫布捲動的範圍
    canvas.config(scrollregion=canvas.bbox("all"))
    
root = tk.Tk()
root.geometry("500x500")
root.title("fuckfuckfuck")

# Label有字體 字大小 背景色 字色 可以挑
label = tk.Label(root, text="標籤一", font=("微軟正黑體", 12),
                 bg="#77d8f2", fg="#6ab")
label.pack()

# 有動態字串可用.get() .set()來獲取/修改元件中的文字 
# 另外也有tk.IntVar() tk.Double()
# btn的文字要用textvarible
varStr = tk.StringVar()
btn = tk.Button(root, textvariable=varStr, command=add)
varStr.set('加數字')
btn.pack()

# Radiolist
# 每個選項都要定位且要給text(顯示)和value(傳入)和command
varStr2 = tk.StringVar()#被選中的radio會將其value傳給variable屬性的動態文字物件 最後再用get()將值取出
radio = tk.Radiobutton(root, text='飯', value='飯',
                       variable=varStr2, command=show_radio)
radio2 = tk.Radiobutton(root, text='麵', value='麵',
                        variable=varStr2, command=show_radio)
radio.pack()
radio2.pack()
radio.select()#決定預設是選取哪一個

# Checkboxlist
# 大量選項用迴圈+list生成比較方便
booleanList = []
option = ['a','b','c']
for i in range(len(option)):
    #因為checkbox的回傳值為0和1(有勾選沒勾選) 所以是一個會隨狀態變動的整數 用IntVar()
    booleanList.append( tk.IntVar())
    temp = tk.Checkbutton(root, text=option[i],
                          variable=booleanList[i], command=show_checkbox)
    temp.pack()#每個選項都要定位
    
# Entry輸入框 Text文字方塊
entry = tk.Entry(root)
enter = tk.Button(root, text='確定', command=entry_get).pack()
entry.pack()

frame = tk.Frame(root)
frame.pack()
#此三行為去除frame的周圍多於空白
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_propagate(False)
frame.config(width=200, height=200)

# frame內建立一個畫布擴張至和frame一樣大(sticky='news') 相對於frame相對定位
# 但此時的frame還沒設定大小
canvas = tk.Canvas(frame)
canvas.grid(row=0, column=0, sticky="news")

# 卷軸要設command但frame物件沒有yview 所以一定要有canvas 
vsb = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
# 卷軸定位通常都是row=0, column=最右欄, sticky='ns'
vsb.grid(row=0, column=1, sticky='ns')
# 讓卷軸移動幅度可以對上內容移動篇幅
canvas.configure(yscrollcommand=vsb.set)

# 畫布內再生成一個frame
frame_texts = tk.Frame(canvas)
# 卷軸須要一個frame物件裝卷軸和一個canvas來設command
# 但卷軸不能控制frame物件所以 最後是frame裡有卷軸和canvas, canvas再生成frame裝入被卷軸控制的東西
# 最後透過create_window使畫布和frame綁在一起捲動(不然frame不會動)
canvas.create_window((0, 0), window=frame_texts, anchor='nw')
str_box = tk.Text(frame_texts)
str_box.pack()

root.mainloop()
