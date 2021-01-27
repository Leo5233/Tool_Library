# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 11:38:16 2020

@author: user
"""
import random

out_fig = ['()','  ','||']
eye = ['`´','--','¬¬','@@','><','°°','ﾟﾟ','＞＜','••','｀｀','´`','^^','･･','˘˘','ˇˇ','☉☉','。。','￣￣','✖✖','≖≖','◔◔','ಠಠ','≧≦','ఠ్ఠఠ్ఠ']
eyebrow = ['^^','˘˘','ˇˇ','´`','  ','  ']
mouth = ['_','ー','﹏','ᴗ','₃','‿','^','ω','д','▽','ʍ','w','ν']
hand = ['~~','＼/','\/','ヾﾉ','  ','ヾゞ','~♥','＼♡','╭╭']
blush = ['-','๑','｡',' ','*','●','〃']

for i in range(30):
    eb = str(random.choice(eyebrow))
    out = str(random.choice(out_fig))
    ey = str(random.choice(eye))
    mo = str(random.choice(mouth))
    han = str(random.choice(hand))
    blu = str(random.choice(blush))

    print(han[0],out[0],blu,eb[0],ey[0],mo,ey[1],eb[1],blu,out[1],han[1], sep = '')
    print()
    