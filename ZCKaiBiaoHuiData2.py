# -*- coding:UTF8 -*-
#该文件为测试读取文件并输出需要代码
#20181120

import re
import time
import xlrd
import xlwt
import PostTest

#以下为数据定义及初始化
debugFlag = False #编代码时的debug标记，方便代码级调试
date_str = PostTest.date_str = '2018-12-27'
txtFilePath = 'F:\\MyCode\\MyProject181120\\txtFile\\{}.txt'.format(date_str)
excelFilePath = 'F:\\MyCode\\MyProject181120\\xlsFile\\MyZCData{}.xls'.format(date_str)

PostTest.headers['Cookie'] = '_gscu_1329143202=45905010pnpk1377; _gscbrs_1329143202=1; homeid=80621f9d-4858-4e3a-ac18-290b353eab86; JSESSIONID=W-PvS_RVv8hilvqk0mIZRF801gA7BGpWicdbaKhy59C-wPLNQDgv!-1251719136; _gscs_1329143202=t4590769163fl3y11|pv:7'

#调用PostTest.py
PostTest.PostFunc()

#以下是函数区域-------------------------------------------------------------------------------------


#筛选政采或工程标记的函数
#flag != 0 :标记政采或工程的位置
def filterBidFlag( bdBHObj ):
    bdBHObjTemp=[]
    for oneOfbdBHObj in bdBHObj:
        if oneOfbdBHObj.startswith('ZC'):
            bdBHObjTemp.append('政采')  
        if oneOfbdBHObj.startswith('GC'):
            bdBHObjTemp.append('工程')  
    return bdBHObjTemp

#筛选政采信息的函数
#20181126
def filterZC( needFilterList, ZCOrGCFlag ) :
    ZCTempList=[]
    for i in range(len(needFilterList)):
        if ( ZCOrGCFlag[i] == '政采' ) :
            ZCTempList.append( needFilterList[i] )
        else:
            pass
    return ZCTempList

#筛选工程信息的函数
#20181126
def filterGC( needFilterList, ZCOrGCFlag ) :
    GCTempList=[]
    for i in range(len(needFilterList)):
        if ( ZCOrGCFlag[i] == '工程' ) :
            GCTempList.append( needFilterList[i] )
        else:
            pass
    return GCTempList

#剔除获取到的行政地区的重复数据的函数
#并将'文山市'修改为'文山县'
def fliterxingZhengDiQuName(achieveDataOfxingZhengDiQuName):
    i=0
    TepmList = []
    while i < len(achieveDataOfxingZhengDiQuName):
        TepmList.append(achieveDataOfxingZhengDiQuName[i])
        i = i+3
    for j in range(len(TepmList)):
        if TepmList[j] == '文山市':
            TepmList[j] = '文山县'
        if TepmList[j] == '文山壮族苗族自治州':
            TepmList[j] = '州本级++++'
    return TepmList

#剔除获取到的预算价的重复数据的函数
def fliteryuSuanJia(achieveDataOfyuSuanJia):
    i=0
    TepmList = []
    while i < len(achieveDataOfyuSuanJia):
        TepmList.append(achieveDataOfyuSuanJia[i])
        i = i+2
    return TepmList

#时间格式化函数
def formatTimestamp(TimestampList):
    TimeTempList=[]
    for i in range(len(TimestampList)):
        TimeTempList.append( time.strftime("%Y-%m-%d", time.localtime( (int(TimestampList[i]))/1000 ) ) )
    return TimeTempList

#政采标段的工程类别格式化函数    
# 1-工程  2-货物  3-服务  4-其他
def formatZCgcLeiBie(achieveZCgcLeiBieList):
    ZCgcLeiBieTempList=[]
    for i in range(len(achieveZCgcLeiBieList)):
        if achieveZCgcLeiBieList[i] == '1':
            ZCgcLeiBieTempList.append('工程')
        if achieveZCgcLeiBieList[i] == '2':
            ZCgcLeiBieTempList.append('货物')
        if achieveZCgcLeiBieList[i] == '3':
            ZCgcLeiBieTempList.append('服务')
        if achieveZCgcLeiBieList[i] == '4':
            ZCgcLeiBieTempList.append('其他')
    return ZCgcLeiBieTempList
    

#以上是函数区域-------------------------------------------------------------------------------------


#政采的数据类
class ZCData:
    ZCbdBH=[]
    ZCbdName=[]
    ZCtbCount=[]
    ZCxingZhengDiQuName=[]
    ZCtbWJDiJiaoEndTime=[]
    ZCgcLeiBie=[]
    ZCyuSuanJia=[]


if __name__=="__main__":

#第1部分-数据区域---------------------
    #数据初始化区
    myZCData = ZCData()

#第2部分-读取数据---------------------
    #打开文件并读取开标会信息
    f = open(txtFilePath, 'r', encoding='UTF-8')
    str = f.read()
    f.close()

#第3部分-提取数据--------------------
    #按获取数据的顺序提取所有标段的标段编号
    #需要筛选工程或政采
    bdBHObj = re.findall(r'\"tbCount\":\d+,\"bdBH\":\"(\D+\d+)\"',str)
    #按获取数据的顺序提取所有标段的标段名称
    #需要筛选工程或政采
    bdNameObj = re.findall(r'\"tbCount\":\d+,\"bdBH\":\"\D+\d+\",\"bdName\":\"(\D*\d*\D*\d*\D*\d*\D*\d*\D*\d*\D*)\",\"huiYiLeiXingName\"',str)
    #按获取数据的顺序提取所有标段的投标人数
    #需要筛选工程或政采
    tbCountObj = re.findall(r'\"tbCount\":(\d+)',str)
    #按获取数据的顺序提取所有标段的行政地区  
    #不需要筛选工程或政采，但需要剔除重复数据
    #注意：该数据提取需要分政采、工程的开标会抓取数据
    xingZhengDiQuNameObj = re.findall(r'\"xingZhengDiQuName\":\"(\D+)\",\"fromType\"',str)
    #按获取数据的顺序提取所有标段的投标文件递交结束时间
    #获取到的是毫秒级的时间戳
    ##需要筛选工程或政采
    tbWJDiJiaoEndTimeObj = re.findall(r'\"gcLeiBie\":\"\d*\D*\",\"pbFangShi\":\d*,\"tbWJDiJiaoEndTime\":(\d+)',str)
    #按获取数据的顺序提取所有标段的工程类别  
    # 1-工程  2-货物  3-服务  4-其他  SZ-市政  FWJZ-房建
    #需要筛选工程或政采
    gcLeiBieObj = re.findall(r'\"gcLeiBie\":\"(\d*\D*)\",\"pbFangShi\"',str)
    #按获取数据的顺序提取所有标段的预算价
    #获取到的是政采开标会的重复了一次的数据
    #不需要筛选工程或政采
    yuSuanJiaObj = re.findall(r'\"isJieShouLiangHeTi\":\d*,\"yuSuanJia\":(\d*.\d*),\"isJiaoNaBaoZhengJin\":',str)

    #获取政采或工程的标记
    ZCOrGCFlag = filterBidFlag(bdBHObj) 

#第4部分-数据筛选--------------------
    #筛选政采标段编号
    myZCData.ZCbdBH = filterZC(bdBHObj,ZCOrGCFlag)
    #筛选政采标段名称
    myZCData.ZCbdName = filterZC(bdNameObj,ZCOrGCFlag)
    #筛选政采标段投标人数
    myZCData.ZCtbCount = filterZC(tbCountObj,ZCOrGCFlag)
    #筛选政采标段行政地区
    myZCData.ZCxingZhengDiQuName = fliterxingZhengDiQuName(xingZhengDiQuNameObj)
    #筛选政采标段投标文件递交结束时间
    myZCData.ZCtbWJDiJiaoEndTime = formatTimestamp( filterZC(tbWJDiJiaoEndTimeObj,ZCOrGCFlag) ) 
    #筛选政采标段工程类别
    myZCData.ZCgcLeiBie = formatZCgcLeiBie( filterZC(gcLeiBieObj,ZCOrGCFlag) )
    #筛选政采标段预算价
    myZCData.ZCyuSuanJia = fliteryuSuanJia(yuSuanJiaObj)

    #myZCData.ZCyuSuanJia.append('0.0001')#遇到价格无法读取时手动添加

#第5部分-数据写入--------------------

    
    excel = xlwt.Workbook()#新建一个excel
    sheet = excel.add_sheet('Sheet1')#添加一个sheet页


    col = 0
    for row in range(len(myZCData.ZCbdBH)):
        sheet.write(row,col,myZCData.ZCbdBH[row])
    col = 1
    for row in range(len(myZCData.ZCbdBH)):
        sheet.write(row,col,'文山项目')
    col = 2
    for row in range(len(myZCData.ZCbdBH)):
        sheet.write(row,col,'云南省')
    col = 3
    for row in range(len(myZCData.ZCbdBH)):
        sheet.write(row,col,'文山壮族苗族自治州')
    col = 4
    for row in range(len(myZCData.ZCbdBH)):
        sheet.write(row,col,myZCData.ZCxingZhengDiQuName[row])    
    col = 5
    for row in range(len(myZCData.ZCbdBH)):
        sheet.write(row,col,myZCData.ZCtbWJDiJiaoEndTime[row])  
    col = 6
    for row in range(len(myZCData.ZCbdBH)):
        sheet.write(row,col,'政府公共资源交易')   
    col = 7
    for row in range(len(myZCData.ZCbdBH)):
        sheet.write(row,col,'政府采购') 
    col = 8
    for row in range(len(myZCData.ZCbdBH)):
        sheet.write(row,col,myZCData.ZCgcLeiBie[row])
    col = 9
    for row in range(len(myZCData.ZCbdBH)):
        sheet.write(row,col,'')
    col = 10
    for row in range(len(myZCData.ZCbdBH)):
        sheet.write(row,col,myZCData.ZCbdName[row])     
    col = 11
    for row in range(len(myZCData.ZCbdBH)):
        sheet.write(row,col,float(myZCData.ZCtbCount[row]))
    col = 12
    for row in range(len(myZCData.ZCbdBH)):
        sheet.write(row,col,float(myZCData.ZCyuSuanJia[row]))
    
    excel.save(excelFilePath)#保存到当前目录下
    print('xls saved')


for i in range(len(myZCData.ZCbdBH)):
    print(myZCData.ZCxingZhengDiQuName[i])

print(len(myZCData.ZCbdBH))

