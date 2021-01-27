# -*- coding: utf-8 -*-
import random
def randomtree(obj, psw=''):
    global answer
    if len(obj) > 1:
    # 如果陣列中數量>=2 就再分支
        obj_l, obj_r = [], []
        psw_l = psw + '0' # 左分支編碼+'0'
        psw_r = psw + '1' # 右分支編碼+'1'
        for i in obj:
            # 隨機產生布林 F為左分支 T為右分支
            sw = random.getrandbits(1)
            if sw and len(obj_l) != 0 or len(obj_r) == 0:
            # 為避免全為T或F(尤其最後一層分支只剩2個可說是必發生) 要加上條件使左右分支不會沒分到
                obj_r.append(i)
            else:
                obj_l.append(i)
        # 遞迴下一層
        randomtree(obj_r, psw_r)
        randomtree(obj_l, psw_l)
    else:
        # 只剩一個表示為葉節點 放進全域變數answer中
        answer.append((obj[0], psw))

def sortPair(obj1, obj2):
# 用來排序分支加總值，但相對應的分支結構也必須同樣排序，所以要兩個綁在一起排序後再拆開
    temp = [(i, j) for i, j in zip(obj1, obj2)]
    temp = sorted(temp, key=lambda x:x[0])
    return [i[0] for i in temp], [i[1] for i in temp]

"""
Huffman原理是將一段文字每個字元去計算出現次數，得到一串頻率數字，每個數字視為一個分支(最底層)
將其升冪排序，將最小的兩個合併相加，再排序...每次兩個值合併等於是將兩個分支合併，接者網上一層
如此反覆，最後會聚集到只剩一個後結束，最底層的每個數字都獲得的一條路線，途中的每個節點，向左為0
向右為1，於是可將數字轉換成0和1的編碼，且因為是由最小的開始合併，大的數字(最常出現的字元)
會最後才合併，所以編碼比較短，達到容量壓縮的效果。但若是有出現頻率一樣多的字元，每次產生的編碼
都會不一樣 """
def huffmanTree(total, layer):
# 要有兩個陣列 一個用來存分支加總值 另一個存分支內部的結構(未合併為整數、合併後為[[數字, 編碼], [..)
    if len(total) >1: #如果還有2個以上的值，表示還可以再合併
        temp = [] # 用來存放新合併後的結構
        obj, layer_ = sortPair(total, layer) # 同步排序分支加總值和分支結構
        # obj[0][1]為最小的兩個
        if isinstance(layer_[0], int): 
            temp.append([obj[0], '0'])
            # 類型是整數表示沒有合併過 被合併之後會是[數值, '0']
        else:
            temp += [[i[0], i[1]+'0'] for i in layer_[0]]
            # 類型非整數表示為含有許多值的分支 將分支內的每個值的編碼後面加'0'
            
        # obj[1]為最小的兩個中比較大的 
        if isinstance(layer_[1], int):
            temp.append([obj[1], '1'])
            # 類型是整數表示沒有合併過 被合併之後會是[數值, '1']
        else:
            temp += [[i[0], i[1]+'1'] for i in layer_[1]]
            # 類型非整數表示為含有許多值的分支 將分支內的每個值的編碼後面加'1'
            
        obj.append(obj.pop(0) + obj.pop(0)) # obj要加入兩最小數相加的新值，舊的兩個數要拿掉
        del layer_[:2] # 要將最小兩數相對應的分支結構拿掉
        layer_.append(temp) # 並加入對應兩最小數相加的新值的新分支結構，拿掉比加入的多，所以總長度會越來越短
        return huffmanTree(obj, layer_) # 將新的分支總值陣列和新的結構陣列放入下一層
    else:       
        return [[i, j[::-1]] for i, j in layer[0]]
        # 已經不能再合併表示已完成，此時要把最終的分支(root，包含所有原始的值和編碼)的編碼反轉
        # 因為是由下往上合併，但編碼的邏輯是要由上往下的順序

obj = [45,13,12,16,9,5]
answer = []
randomtree(obj)
ansForHuff = huffmanTree(obj, obj)