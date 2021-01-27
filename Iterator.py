# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 12:31:07 2020

@author: user
"""
#此為Iterator(含有__iter__和__next__)必定iterable
#__iter__會被執行2次因為有return self
class my:
    def __iter__(self):
        self.num = 0
        return self
    def __next__(self):
        if self.num <= 10:
            z = self.num
            self.num += 1
            return z
        else:
            raise StopIteration

print('\n my:')            
for i in iter(my()):
    print(i)

#此非Iterator但是iterable因為含有__getitem__
#__getitem__會自體循環將return放入自身 要多給一個參數空間
class b:
    def __getitem__(self, key=0):
        if key <= 10:
            return key
        else:
            raise StopIteration

print('\n b:')
for i in b():
    print(i)
    
#此為Generator同時也是Iterator(含有__iter__和yield)必定iterable 
#可以在__iter__ return self +__next__ 或是直接在__iter__內用yield  
class a:
    n = 0
    def __iter__(self):
        while self.n <=10:
            yield self.n
            self.n += 1

print('\n a:')            
for i in iter(a()):
    print(i)
