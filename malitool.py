#!/usr/bin/python3
# 从管道读取数据发送
# author：ruanzq
# GitHub：ruanzq.github.com
import smtplib,sys,fcntl,os
from email.mime.text import MIMEText
from email.header import Header
content = None

HOST = "smtp.qq.com"

PORT = "465"

CODE = ""

RECEIVE = []

ME = ""

def readOnPipe():
    """从管道读取数据"""
    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK)
    return sys.stdin.read()

def writeLetter(content):
    """组装邮件"""
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header("linux server msg",'utf-8')
    msg['From'] = Header(ME, 'utf-8')
    msg['To'] =  Header(RECEIVE[0], 'utf-8')
    return msg

try:
    letter = writeLetter(readOnPipe())
    smtp = smtplib.SMTP_SSL(HOST,PORT)
    smtp.login(ME,CODE)
    smtp.sendmail(ME,RECEIVE,letter.as_string())
except TypeError as e:
    print("nothing input")
except Exception as e:
    print(e)
    print("failed")