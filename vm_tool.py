#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# import json

import paramiko

#ssh 方式连接底层xenserver服务器
def connect(host):
    'this is use the paramiko connect the host,return conn'
    ssh = paramiko.SSHClient()
    username = 'root'
    password = '1qaz@WSX'
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        #        ssh.connect(host,username='root',allow_agent=True,look_for_keys=True)
        ssh.connect(host, username=username, password=password, allow_agent=True)
        return ssh
    except:
        return None


# def command(args, outpath):
#     'this is get the command the args to return the command'
#     cmd = '%s %s' % (outpath, args)
#     print cmd
#     return cmd

#调取底层命令
def exec_commands(conn, cmd):
    'this is use the conn to excute the cmd and return the results of excute the command'
    stdin, stdout, stderr = conn.exec_command(cmd)
    results = stderr.read()
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