#!/bin/env python
# -*- coding: utf-8 -*-
#Function:备份wtc数据库到制定目录
#Arthor:Timbaland
# dbbackup.py
# !/usr/bin/python
# coding:utf-8
#date:2017-11-25
import subprocess
import time
import os
import sys
import sendEmail
import getip
import logging

# create logger
# print len(sys.argv)
logger = logging.getLogger("dbbackup")
logger.setLevel(logging.DEBUG)
# create console handler and set level to error
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create file handler and set level to debug
fh = logging.FileHandler("dbbackup.log")
fh.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add ch and fh to logger
logger.addHandler(ch)
logger.addHandler(fh)

def backup(user='root', password='123456', host='172.25.1.13', dbname='hj21_backend'):
    start_time = time.clock()
    ip = getip.get_ip_address('eth0')
    today = time.strftime("%Y%m%d", time.localtime())
    backup_dir = '/data/dbbackup/%s' % today
    if not os.path.isdir(backup_dir):
        os.makedirs(backup_dir)
    os.chdir(backup_dir)
    cmd = "/usr/local/mysql/bin/mysqldump --opt -u%s -p%s -h%s %s | gzip > %s-%s.sql.gz" \
          % (user, password, host, dbname, today, ip, dbname)
    logger.debug(dbname + ':' + cmd)
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    content = result.stdout.read()
    # if content:
    #     logger.error(dbname + ':' + content)
    #     # subject = "%s - %s backup error" % (ip, dbname)
    #     # sendEmail.send_mail(mail_to_list, subject, content)
    end_time = time.clock()
    use_time = end_time - start_time
    logger.debug(dbname + " backup use: %s" % use_time)


# def help():
#     print '''Usage: %s dbname''' % sys.argv[0]
#     # sys.exit(1)
def del_log():
    cmd = "find /data/dbbackup/*  -mtime +30  -exec rm -rf {} \; "
    logger.debug(cmd)
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

if __name__ == "__main__":

    del_log()
    backup()