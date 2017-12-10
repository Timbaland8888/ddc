#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Arthur:Timbaland
# Date:2017-11-26

# from dateutil import parser
import MySQLdb,sys, os,time,datetime,re
from vm_tool import connect,exec_commands
# 连接mysql数据库参数字段
con = None
ip = '172.25.1.13'
user = 'root'
password = '123456'
dbname = 'hj21_backend'
port = 3306
charset = 'utf8'
db = MySQLdb.connect(host=ip, user=user, passwd=password, db=dbname, port=port, charset=charset)
cursor = db.cursor()
vm_name = []
vm_room = []
#服务器清单
host = ['172.25.1.5','172.25.1.4','172.25.1.3','172.25.1.2','172.25.1.1']
#底层硬重启命令
# cmd = 'xe vm-reboot force=true name-label='
cmd = ['xe vm-start force=true name-label=','xe vm-reboot force=true name-label=']
#

# 获取教室里面的虚拟机信息
query_vm = '''SELECT CONCAT(wtc.terminal_name,'-V'),room.classroom_name
from wtc_terminal wtc
INNER  JOIN wtc_classroom room on wtc.classroom_id =room.id
'''
try:
    cursor.execute(query_vm)
    result = cursor.fetchall()
    # 获取教室云桌面数量
    vm_count = len(result)
    print 'A、B、C、D教室云桌面数量共{0}台'.format(vm_count)
    # print len(cursor.fetchall())
    # cursor.execute(query_vm)
    for vm_id in range(0,vm_count,1):
        # print result[vm_id][0]
        # print result[vm_id][1]
        vm_name.append(result[vm_id][0])
        vm_room.append(result[vm_id][1])

    # print type(cursor.fetchall()[0])

    db.commit()

except ValueError:
    db.roolback
    print 'error'
# 关闭游标和mysql数据库连接
cursor.close()
db.close()
#获取当前时间
now_date = datetime.datetime.now().strftime('%H:%M')
# print now_date
# cure_date = datetime.datetime.strptime(now_date,'%Y-%m-%d %H:%M:%S')
# print now_date
#自定义重启时间
set_retime = ['12:58','22:00']

while True:
    now_date = datetime.datetime.now().strftime('%H:%M:%S')
    if datetime.datetime.now().strftime('%H:%M') in set_retime:

        #批量重启虚拟机
        for vm_id in range(0,vm_count,1):
            # cmd = 'xe vm-shutdown force=true name-label=%s' % (vm_name[vm_id])
            recmd ='xe vm-reboot force=true name-label=%s' %(vm_name[vm_id])
            scmd = 'xe vm-start force=true name-label=%s' % (vm_name[vm_id])
            result=exec_commands(connect(host=host[0]), cmd=recmd)
            if re.findall(r"halted",result,re.M|re.I):
                exec_commands(connect(host=host[1]), cmd=scmd)
                print '{0}的{1}正在开机，请等待注册\n'.format(vm_room[vm_id].encode('utf-8'), vm_name[vm_id].encode('utf-8'))
                continue
            print '现在正在重启{0}的{1}请等待注册\n'.format(vm_room[vm_id].encode('utf-8'),vm_name[vm_id].encode('utf-8'))
            time.sleep(5)
    else:
        print  '现在时间：{0}，还未到重启时间{1}，{2}，请等待\n'.format(now_date.encode('utf-8'),\
                set_retime[0].encode('utf-8'), set_retime[1].encode('utf-8'))
        time.sleep(5)