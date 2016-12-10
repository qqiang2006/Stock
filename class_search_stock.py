#coding=utf8
__author__ = 'lihuixian'
import json, urllib
from urllib import urlencode
from PIL import Image,ImageTk
import sys
import io
import string
reload(sys)
sys.setdefaultencoding("utf8")
#股票查询函数
class Stock:
    def __init__(self):
        self.back_result = ''
        self.appkey="1495baff799edb1d926cf3374f53ff1c"
        self.url=url = "http://web.juhe.cn:8080/finance/stock/hs"
    #修改程序调用API的注册参数函数
    def modify_appkey_url(self,value1,value2):
        self.appkey=value1
        self.url=value2
    def search_stock(self,ID):
        # 自动判定股票代码属于哪个交易所
        ret =int(ID[0])
        if ret == 0:
            stock_num = "%s%s" % ("sz", ID)
        else:
            stock_num = "%s%s" % ("sh", ID)
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
                min_pic=pic["minurl"]
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
                back_all=back_name + "\r\n""\r\n" +back_price +"\r\n""\r\n" +back_rate +"\r\n""\r\n" +back_change
            else:
                back_all= "%s:%s" % (res["error_code"],res["reason"])
        else:
            back_all="request api error"
        self.back_result = [back_all , min_pic]
        return self.back_result
    #处理股票k线图返回
    def stock_pic(self,url_pic):
        image_bytes = urllib.urlopen(url_pic).read()
        # 返回<_io.BytesIO object at 0x10eafcdd0>
        data_stream = io.BytesIO(image_bytes)
        # 返回图片对象<PIL.GifImagePlugin.GifImageFile image mode=P size=545x300 at 0x108DB6710>
        pil_image = Image.open(data_stream)
        # 返回 pyimage1
        tk_image = ImageTk.PhotoImage(pil_image)
        return tk_image

if __name__ == '__main__':
    stock_A=Stock()
    ID=raw_input("请输入股票代码：")
    result=stock_A.search_stock(ID)
    print type(stock_A.back_result)
    print stock_A.back_result[0]
