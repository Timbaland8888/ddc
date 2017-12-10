#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time,datetime

from Tkinter import *

root = Tk()
root.title("云桌面重启设置")
# root.geometry('183x160')
Label(root,text='时：').grid(row=2)
Label(root,text='分：').grid(row=3)
photo = PhotoImage(file='bg.gif')
Label(root,image=photo).grid(row=2,column=3,rowspan=2)
Entry(root,show=None,background = 'red').grid(row=2,column=1)
Entry(root,show=None,background = 'red').grid(row=3,column=1)
Button(text="确定",width=10).grid(row=4,columnspan=3,pady=5)
root.mainloop()