# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from pyexcel_ods import get_data
import pandas as pd
data = get_data("ODS檔的路徑")
content= pd.DataFrame(data['工作表名稱'])