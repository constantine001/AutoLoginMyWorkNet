# -*- coding:UTF8 -*-
#POST 测试

import requests
import time


#以下为数据定义及初始化
#debugFlag = False #编代码时的debug标记，方便代码级调试
date_str = '2018-11-1'
headers = {
        'Cookie': ''
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        #'Content-Length': '1024'
    }  # headers的例子，看你的post的headers

mydata = {
    'bdBH' : '',
    'bdName' : '',
    'gcName' : '',
    'timeMin' : '',
    'timeMax' : '',
    'pbFangShi' : '',
    'page' : '1',
    'rows' : '50'
}

#封装整个操作作为函数供另一个文件调用
def PostFunc():

    response = requests.get('http://wsggzy.cn/zfcg-fw/kb/kbh_List.html')  # 你第一次的url
    
    myStructTime = time.strptime(date_str, "%Y-%m-%d")
    mytimeStamp = int(time.mktime(myStructTime))
    timeMinTemp = (mytimeStamp + 3600)*1000 #开始时间默认为1点
    timeMaxTemp = (mytimeStamp + 82800)*1000#结束时间默认为23点
    mydata['timeMin'] = str(timeMinTemp)
    mydata['timeMax'] = str(timeMaxTemp)


    response = requests.post('http://wsggzy.cn/zfcg-fw/kb/queryKBHList.do', headers = headers, data = mydata)  # 你第二次的url
    response.encoding = "utf-8"
    f = open('F:\\MyCode\\MyProject181120\\txtFile\\{}.txt'.format(date_str), 'w', encoding='UTF-8')
    f.write(response.text )
    f.close()
    #print( response.json() )
    print('{}.txt saved!'.format(date_str))
    #print( response.text )
