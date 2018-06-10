#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Arthur:Timbaland
# Date:2017-11-26

# from dateutil import parser
import MySQLdb,sys, os,time,datetime,re
from vm_tool import connect,exec_commands
from vm_tool import Logger
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# 连接mysql数据库参数字段
con = None
ip = '192.168.5.35'
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
host = ['192.168.5.30']
#底层硬重启命令
# cmd = 'xe vm-reboot force=true name-label='
cmd = ['xe vm-start force=true name-label=','xe vm-reboot force=true name-label=']
#

# 获取教室里面的虚拟机信息
query_vm = '''SELECT CONCAT(wtc.terminal_name,'-T'),room.classroom_name
from wtc_terminal wtc
INNER  JOIN wtc_classroom room on wtc.classroom_id =room.id 
WHERE wtc.remarks !=''
'''
try:
    cursor.execute(query_vm)
    result = cursor.fetchall()
    # 获取教室云桌面数量
    vm_count = len(result)
    print unicode('B901教室云桌面数量共{0}台'.format(vm_count),'utf-8')
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
set_retime = ['21:00']
#自定义每隔5天重启一次
global day
day = 0
count = 0
while True:
    now_date = datetime.datetime.now().strftime('%H:%M:%S')
    if datetime.datetime.now().strftime('%H:%M') in set_retime and (day%5) == 0:
        day +=5
        #批量重启虚拟机
        for vm_id in range(0,vm_count,1):
            # cmd = 'xe vm-shutdown force=true name-label=%s' % (vm_name[vm_id])
            recmd ='xe vm-reboot force=true name-label=%s' %(vm_name[vm_id])
            scmd = 'xe vm-start force=true name-label=%s' % (vm_name[vm_id])
            # ssh1 = connect(host=host[0])
            result = exec_commands(connect(host=host[0]), cmd=recmd)
            if re.findall(r"halted",result[1],re.M|re.I):
                exec_commands(connect(host=host[0]), cmd=scmd)
                print unicode('{0}的{1}正在开机，请等待注册\n'.format(vm_room[vm_id].encode('utf-8'), vm_name[vm_id].encode('utf-8')),'utf-8')
                continue
            print unicode('现在正在重启{0}的{1}请等待注册\n'.format(vm_room[vm_id].encode('utf-8'),vm_name[vm_id].encode('utf-8')),'utf-8')
            time.sleep(60)
        # ssh1.close()
    else:
        print  unicode('现在时间：{0}，还未到周五重启时间{1}，请等待\n'.format(now_date.encode('utf-8'),set_retime[0].encode('utf-8')),'utf-8')
        # time.sleep(10)
        # log = Logger(level='debug')

        for vm_id in range(0,vm_count,1):
            # cmd = 'xe vm-shutdown force=true name-label=%s' % (vm_name[vm_id])
            # recmd ='xe vm-reboot force=true name-label=%s' %(vm_name[vm_id])
            vm_status = 'xe vm-list  name-label=%s' %(vm_name[vm_id])
            scmd = 'xe vm-start force=true name-label=%s' % (vm_name[vm_id])
            count = count+vm_id
            try:
                if exec_commands(connect(host=host[0]),vm_status) :

                    print count
                    result = exec_commands(connect(host=host[0]),vm_status)
                    print result
                    # print re.findall(r"halted",result,re.M|re.I)
                    if re.findall(r"halted",result[1],re.M|re.I):
                        exec_commands(connect(host=host[0]), scmd)
                        print unicode('{0}classroom的{1}正在开机......\n'.format(vm_room[vm_id].encode('utf-8'), vm_name[vm_id].encode('utf-8')),'utf-8')
                # time.sleep(1)
            except Exception as f:
                print f,'exec_commands'

                #Logger('error.log', level='error').logger.error(f)
            finally:

                # log.logger.debug('debug')
                print count
                logger.info(unicode("虚拟机名称："+str(vm_name[vm_id]),'utf-8'))
                logger.info(unicode("虚拟机信息"+str(result[1])+str('\n'),'utf-8'))
                # log.logger.warning('warning')
                # log.logger.error('error')
                # log.logger.critical('critical')
                # time.sleep(1)




