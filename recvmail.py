#!/usr/bin/python
#coding: utf-8

import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  
  
sender = 'shiweifu@126.com'  
receiver = 'shiweifu@gmail.com'  
subject = 'python email test'  
smtpserver = 'smtp.126.com'  
username = 'shiweifu@126.com'  
password = ''  
  
msg = MIMEText('你好','plain','utf-8')#中文需参数‘utf-8’，单字节字符不需要  
msg['Subject'] = Header(subject, 'utf-8')
msg['']  
  
smtp = smtplib.SMTP()  
smtp.connect(smtpserver)  
smtp.login(username, password)  
smtp.sendmail(sender, receiver, msg.as_string()) 

