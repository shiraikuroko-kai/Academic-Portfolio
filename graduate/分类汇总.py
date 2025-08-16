import pandas as pd
import numpy as np
#读取excel二次分类数据
'''df = pd.read_excel( r'data/1.xlsx')      
pp=df.groupby('dm_text').agg({'dm_text':'count'})'''


#读取csv数据
df = pd.read_csv( r'BV1bZ4y1j7yi副本.csv')      
'''pp=df.groupby('dm_userId').agg({'dm_text':'count'})
dd=pp.groupby('dm_text').agg({'dm_text':'count'})
writer = pd.ExcelWriter(r"1.xlsx") #新建xlsx
sheet1 = pd.DataFrame(pp) #进行转成DF格式
sheet1.to_excel(writer,sheet_name='发送弹幕汇总') #写入到xlsx表 的名叫 '省份汇总'的sheet中
writer.save()'''
#writer = pd.ExcelWriter(r"11.xlsx") #新建xlsx文件
#sheet1 = pd.DataFrame(dd) #进行转成DF格式
#sheet1.to_excel(writer,sheet_name='发送弹幕汇总') #写入到xlsx表 的名叫 '省份汇总'的sheet中
#writer.save()
pp=df.groupby('出现时间').agg({'出现时间':'count'})
writer = pd.ExcelWriter(r"3.xlsx") #新建xlsx
sheet1 = pd.DataFrame(pp) #进行转成DF格式
sheet1.to_excel(writer,sheet_name='sheet1') 
writer.save()

#数据简述
#print(pp.describe())
#print(dd.describe())
print(pp)
#print(dd)


'''
BV1bZ4y1j7yi 1
BV1c741187gr 2
BV1fk4y1d7qn 3
BV1ia4y1x7n5 4
BV1kJ411r7cX 5
BV1m7411F7si 6
BV1v741117Dn 7
BV1X7411t7jL 8
BV11Q4y1N7Ry 9
BV15V411o7VR 10
'''
