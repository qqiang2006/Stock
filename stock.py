#coding=utf8
__author__ = 'lihuixian'
import json, urllib
from urllib import urlencode
import sys
import io
import string
import sqlite3
reload(sys)
sys.setdefaultencoding("utf8")
#股票查询函数
class Stock:
    def __init__(self):
        self.min_pic=''
        self.back_all = ''
        self.appkey="1495baff799edb1d926cf3374f53ff1c"
        self.url=url = "http://web.juhe.cn:8080/finance/stock/hs"
    #修改程序调用API的注册参数函数
    def modify_appkey_url(self,value1,value2):
        self.appkey=value1
        self.url=value2
    def search_stock(self,ID):
        #判断输入格式为数字时
        # 自动判定股票代码属于哪个交易所
        if ID[0] in  ['6','0','3','9']:
            ret =int(ID[0])
            if ret in [0, 3]:
                stock_num = "%s%s" % ("sz", ID)
            else:
                stock_num = "%s%s" % ("sh", ID)
        #判断输入为中文时
        else:
            #打开股市列表数据库
            data_base_stock = sqlite3.connect('/home/lihuixian/Desktop/stock.db')
            cu = data_base_stock.cursor()
            #模糊查询股市ID
            cu.execute("select stock_ID from stock_list where stock_name like '%"+ID+"%'")
            stock_num_list = cu.fetchall()
            stock_num =list(stock_num_list)[0][0]
        params = {
            "gid" : stock_num, #股票编号，上海股市以sh开头，深圳股市以sz开头如：sh601009
            "key" : self.appkey, #APP Key
        }
        params = urlencode(params)
        f = urllib.urlopen("%s?%s" % (self.url, params))
        content = f.read()
        res = json.loads(content)
        if res:
            error_code = res["error_code"]
            if error_code == 0:
                #成功请求
                first_result = res["result"]
                second_result = first_result[0]
                mid_result =second_result["data"]
                stock_name =mid_result["name"]
                #股票涨跌幅
                rate = mid_result["increPer"]
                price_change=mid_result["increase"]
                pic=second_result["gopicture"]
                #分时曲线图
                self.min_pic=pic["minurl"]
                #股票名称
                back_name= "股票名称为: " +stock_name
                #股票价格
                final_result =mid_result["nowPri"]
                back_price="股票最新价格为: " + final_result
                if string.atof(rate) > 0:
                    back_rate= "股票涨幅为:" + rate
                else:
                    back_rate="股票跌幅为: " + rate
                if string.atof(price_change) >0:
                    back_change="股票升值:" + price_change + "元"
                else:
                    back_change="股票贬值:" + price_change + "元"
                #股票查询结果
                self                                                                                                    .back_all=back_name + "\r\n""\r\n" +back_price +"\r\n""\r\n" +back_rate +"\r\n""\r\n" +back_change
            else:
                self.back_all= "%s:%s" % (res["error_code"],res["reason"])
        else:
            self.back_all="request api error"
        return self.back_all

if __name__ == '__main__':
    stock_A=Stock()
    # ID=raw_input("请输入股票代码：")
    i=1	
    while i<=len(sys.argv)-1:
	print "----------------------------"
	result=stock_A.search_stock(sys.argv[i])
	#print "----------------------------"
	print(stock_A.back_all)
	print "----------------------------"
	i+=1
    #result = stock_A.search_stock("000725")
    # print stock_A.min_pic
    #print(stock_A.back_all)
    # result = stock_A.search_stock("华天科技")
    # print "----------------------------"
    # print(stock_A.back_all)
    # print "----------------------------"
