import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.colors as c
#*為個人偏好

#------color_palette(['#afc235',#123587'....]) 此function可辨識各種顏色數值轉換成tuple 可搭配palplot繪出自製色票
#預設多彩色系 color_palette
#()內第一項可放deep, muted, pastel, bright, dark, 和 colorblind(無紅綠) 不同明暗但只有10色循環 第二項為數量
#其他模式 'hls' 數量不限， *'husl'修正過各色相亮度問題
#sn.palplot(sn.color_palette('dark',16))

#------hls_palette 則是明亮全色相去均分，數量沒有限制，但有個缺點是藍紫色系偏暗
#sn.palplot(sn.hls_palette(16(數量), l=0.6(亮度), s=0.8(飽和度)))

#------*paired 一深一淺組色6組共12色
#sns.palplot(sns.color_palette("Paired", 12))

#------Set1 9色基本高彩度色 *Set2-平衡中間色系但只有8色 *Dark2為Set2加深版 *Set3-平衡淡色系-12色
#sns.palplot(sns.color_palette("Set3", 12))

#sns.choose_colorbrewer_palette("sequential")
# data_type: {‘sequential’, ‘diverging’, ‘qualitative’}
#sns.choose_colorbrewer_palette("qualitative",as_cmap=1)

#------sn.xkcd_palette則是處理顏色英文名稱 可將名稱轉換成對應tuple 若要取用某色可用sn.xkcd_rgb['顏色名稱']
#colors = ["windows blue", "amber", "greyish", "faded green", "dusty purple"]
#b= sns.xkcd_palette(colors)

#---------因為離散型主要是色相差距大 亮度飽和度相近 但色相本身很難讓人直覺連想到數值高低 強調數值時最好用不同深淺單、雙色系
#單色系 可不限數量 'Oranges' 'Blues' 'Purples' 'Reds' 'Greens' 'Greys'
#sns.palplot(sns.color_palette("Blues"))
#多色系 字尾可加_r(順序反轉) _d(dark) 
#近似雙色系(淺到深 兩色可前後互換) 綠藍GnBu BuGn 藍紫BuPu PuBu 紫紅PuRd 黃綠YiGn
#120度三色系 黃橙紅YiOrRd  黃橙棕YiOrBr 黃綠藍YiGnBu 紫藍綠PuBuGn
#紅藍RdBu 棕水綠BrBG 紅黃綠RdYlGn 紅黃藍*RdYlBu 紅灰*RdGy 紫棕PuOr 紫綠*PRGn 粉紅綠*PiYG
#sns.palplot(sns.color_palette("RdPu",10))

#其他內建名稱"rocket", "mako", "flare","crest" ,*"coolwarm" "cubehelix" "viridis" "icefire" "vlag" *"Spectral

#----------自製雙色系色票 
#sns.diverging_palette(色相1 0-360, 色相2 0-360, 兩端飽和度0-190, 兩端亮度0-100, 色票數量, sep中間色的範圍, center='dark'中間色改黑色)
#sns.palplot(sns.diverging_palette(100, 280, s=90, l=40, n=7 ,sep=10))

#sns.cubehelix_palette(start=0~1(0和1為黃微綠 0.5為對比色紫微藍), rot=(從dark=0 到 light=1 要色相環轉多少圈 當圈數很多時會形成離散形色票 ) 
                    #, dark和light=0~1 (本身會生成從最暗到最亮的漸層，但若不需要極端深淺色，可用dark和light值來指定擷取亮度範圍 超過0或1會多取出全黑全白 要搭配rot來指定範圍內轉出那些色
                    #, n_colors=色票數量 將這段dark和light指定範圍切分成多少份
sns.palplot(sns.cubehelix_palette(start=0, rot=2, dark=0.25, light =0.75, n_colors=12))

#要將此cubehelix物件放入繪圖的palette屬性時，可簡寫成xxx.replot(palette = "ch:r=.5, l=.8")

#---------其他單色系 light_palette 和 dark_palette
#sns.palplot(sns.light_palette("seagreen"))
#sns.palplot(sns.dark_palette("#69d"))

#------------將RGB轉#FFFFFF形式 如果是有透明度要加 keep_alpha = True
#hex_color = c.to_hex((0.5,0.7,0.6,0.7),keep_alpha=True)
#將#ffffff轉回RGB 有透明度要用to_rgba 若是to_rgb會自動捨棄最後一個色板
#rgb_color = c.to_rgba(hex_color)
#一次轉多色
#rgb_color_array = c.to_rgba_array([hex_color,hex_color])

#----------將色票以長條圖秀出來
# cop = [[0, 147, 146],[114, 170, 161],[177, 199, 179],[241, 234, 200],[229, 185, 173],[217, 137, 148],[208, 88, 126]]
# cop = [(color[0]/ 255, color[1]/ 255, color[2]/ 255) for color in cop ]
# plt.bar(width =1, x = [i for i in range(len(cop))], height = [sum(i) for i in cop], color =cop)

