# -*- coding: utf-8 -*-


import time
import xlrd
import xlwt
from xlutils.copy import copy
import os
#import codecs
import pandas as pd

testcase_statis_list = [
    {

        'env0': {
            'total': 100,
            'Executed': [1, 2, 3, 4, 5, 68, 9, 2, 3, 4, 5, 6, 7, 8],
            'Passed': [4, 6, 76, 23, 9, 6]
        }
    }
]

def Set_Excel_Statis(filepath, testcase_statis_list):
    # 打开想要更改的excel文件
    old_excel = xlrd.open_workbook(filepath, formatting_info=True)
    # 将操作文件对象拷贝，变成可写的workbook对象
    new_excel = copy(old_excel)
    # 获得第一个sheet的对象
    ws = new_excel.get_sheet(0)
    # 写入数据
    for env in testcase_statis_list:

        for k, v in env.items():
            if k == 'env0':
                ws.write(0, 0, len(env[k]['Executed']))
                ws.write(0, 1, len(env[k]['Passed']))
                ws.write(0, 2, '%.1f' % (len(env[k]['Executed'])*100/env[k]['total'])+ '%')
                ws.write(0, 3, '%.1f' % (len(env[k]['Passed'])*100/len(env[k]['Executed']))+ '%')
                ws.write(0, 4, env[k]['total'])

                #ws.write(1, 2, '第二行，第三列')
    # 另存为excel文件，并将文件命名
    new_excel.save(filepath)

    
    
    
def Generate_Html(file):
    #xd = pd.ExcelFile(file) 
    pd.set_option('display.max_colwidth',1000)#设置列的宽度，以防止出现省略号
    df = xd.parse()
    with codecs.open('example.html','w') as html_file:
        html_file.write(df.to_html(header = True,index = False))

        
        

if __name__ == '__main__':
    
    
    filepath = os.path.abspath(os.path.dirname(__file__))
    file = os.path.join(filepath, 'setexample.xls')
    Set_Excel_Statis(file, testcase_statis_list)
    Generate_Html(file)
