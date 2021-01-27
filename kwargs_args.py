# -*- coding: utf-8 -*-

def a(b, *args, **kwargs):
    for i in args:
        print(i)
        
    # kwargs 為字典{a:na, b:nb, c...}
    for k, v in kwargs.items():
        print(f'{k}:{v}')
        
a(1,3,2,6, o=3, e=8)

# *字典=*list(字典)=*list(key值) key1, key2,..
diction = {'k1':10, 'k2':11}
print('*diction',*diction)

# **只可以用在 字典當參數時
a(1, **diction)
