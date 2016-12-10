#coding=utf8
__author__ = 'lihuixian'
import ntplib
import time
from Tkinter import *
from class_search_stock import *

#初始化Stock实例
stock1=Stock()
#统一响应button按钮点击command
def data_pic(ID):
	tmp = stock1.search_stock(ID)
	back_pic = stock1.stock_pic(tmp[1])
	image_label = Label(root, image=back_pic)
	image_label.image = back_pic
	image_label.grid(row=2, column=2, columnspan=2, sticky='E')
	return tmp[0]

# GUI主体
root = Tk()
root.title("股票查询")
# 输入框
stock_id = StringVar()
raw_id = Entry(root, textvariable=stock_id)
raw_id.grid(row=0, columnspan=1, sticky='W')
# 查询按钮
action = Button(root, text="search", command=lambda: var.set(data_pic(ID=stock_id.get())))
action.grid(row=0, column=1, sticky='W')
# 实时刷新选项
F5 = Checkbutton(root, text="实时刷新数据")
F5.grid(row=1, column=0)
# Ntp服务器时间
def tick():
	global live_time
	# 从运行程序的计算机上面获取当前的系统时间
	'''ntpclient = ntplib.NTPClient()
	repose = ntpclient.request('s2m.time.edu.cn')
	live_time_new = time.ctime(repose.tx_time)
	'''
	live_time_new = time.asctime(time.localtime())
	# 如果时间发生变化，代码自动更新显示的系统时间
	if live_time_new != live_time:
		live_time = live_time_new
		clock.config(text=live_time_new)
	clock.after(200, tick)
live_time = ''
clock = Label(root, bg='green')
clock.grid(row=0, column=3,sticky='W')
tick()

# 查询结果返回框
var = StringVar()
result = Message(root, textvariable=var)
result.grid(row=2, column=0, columnspan=1, sticky='W')
# 退出按钮
quit = Button(root, text="exit", command=quit)
quit.grid(row=0, column=2, sticky='W')
root.mainloop()
