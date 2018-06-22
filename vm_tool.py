#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# import json
#update:2018-06-22

import paramiko
import logging,types
from logging import handlers

#ssh 方式连接底层xenserver服务器
def connect(host):
    'this is use the paramiko connect the host,return conn'
    ssh = paramiko.SSHClient()
    username = 'root'
    password = 'xuanyuan@123'
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        #        ssh.connect(host,username='root',allow_agent=True,look_for_keys=True)
        ssh.connect(host, username=username, password=password, allow_agent=True)
        return ssh
    except Exception,e:
        print e,'ssh error'
        return e


# def command(args, outpath):
#     'this is get the command the args to return the command'
#     cmd = '%s %s' % (outpath, args)
#     print cmd
#     return cmd

#调取底层命令
def exec_commands(conn, cmd):
    'this is use the conn to excute the cmd and return the results of excute the command'
    stdin, stdout, stderr = conn.exec_command(cmd)
    results = []
    if type(stderr) is not types.NoneType :
        results.append(stderr.read())

    if type(stdout) is not types.NoneType:
        results.append(stdout.read())
    conn.close()
    return results

# def excutor(host, outpath, args):
#     conn = connect(host)
#     if not conn:
#         return [host, None]
#         # exec_commands(conn,'chmod +x %s' % outpath)
#     cmd = command(args, outpath)
#     result = exec_commands(conn, cmd)
#     print result
#     result = json.dumps(result)
#     return [host, result]

# def copy_module(conn,inpath,outpath):
#     'this is copy the module to the remote server'
#     ftp = conn.open_sftp()
#     ftp.put(inpath,outpath)
#     ftp.close()
#     return outpath


class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='D',backCount=2,fmt='%(asctime)s - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)

