# -*- coding: utf-8 -*-

import configparser

config = configparser.ConfigParser()
data=config.read('config.ini')
a = config.get('a', 'b')# 取得[a] b=XXX 之中的XXX
