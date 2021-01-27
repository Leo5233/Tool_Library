import seaborn as sns
import numpy as np
import random
from matplotlib import pyplot as plt
#Y = ((R*299)+(G*587)+(B*114))/1000肉眼知覺亮度
'''
color=[]
num =15
fade = 0#0-1
bright=4#0-10
for i in range(num):
    c1_min = bright
    c1_max = 15
    c1_min = int( c1_min+(c1_max-c1_min)*fade/2)
    c1_max = int( c1_max-(c1_max-c1_min)*fade/2)
    c1 = random.randint(c1_min, c1_max)
    c2 = random.randint(0,15)
    r=hex(c1)[2:] + hex(c2)[2:]
    c1 = random.randint(c1_min, c1_max)
    g= hex(c1)[2:] + hex(c2)[2:]
    if (g[0]+r[0]).isalpha():
        c1 = random.randint(bright,c1_max)
    else:
        c1 = random.randint(c1_min, c1_max)
    b= hex(c1)[2:] + hex(c2)[2:]
    x=[r,g,b]
    random.shuffle(x)
    color.append('#'+''.join(x))
a=sorted(color)
sns.palplot(sns.color_palette(a))
'''

def rgb_hsl(color):
    try:
        temp = max(color)/ (min(color)+0.1)
        sature = 360/(1+3**(-(temp-1)**0.42+0.7))-120
        hue_angle = [360,120,240] if min(color) == color[1] else [0,120,240]
        hue_temp = [i-min(color) for i in color]
        hue = sorted(hue_temp, reverse = True)
        hue_value = (hue_temp[hue_temp.index(hue[0])]*hue_angle[hue_temp.index(hue[0])] + hue_temp[hue_temp.index(hue[1])]*hue_angle[hue_temp.index(hue[1])]) / (hue[0]+hue[1]) /360*240
        light = (max(color)+min(color))/510*240
        print(hue_value, sature, light)
    except:
        print('data type is wrong')
   
rgb_hsl((254,0,1))