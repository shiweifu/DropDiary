#!/usr/bin/python
#coding: utf-8

import poplib
import json
import os.path
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import time
import dropbox
import tempfile

config = {}

# def get_temp_file_with_str(s):
#   p = tempfile.tempfile()
#   with open()


def save_to_file(fn, content):
  f = open(fn, "w")
  f.write(content)
  f.flush()
  f.close()

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def file_exist(p):
  return os.path.isfile(p)

def parse_msg(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            return parse_msg(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            # print('%sText: %s' % ('  ' * indent, content + '...'))
            return content
        elif content_type=='text/html':
            pass
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))


def conver_time_to_str(s):
  return time.strftime("%Y%m%d", s)

def init():
  global config
  config = json.load(open("./conf/config.json"))


def main():
  global config
  init()
  user      = config["pop3_user"]
  password  = config["pop3_password"]
  pop3_host = config["pop3_host"]
  to_email  = config["to_email"]

  server = poplib.POP3(pop3_host)
  #server.set_debuglevel(1)
  print(server.getwelcome())
  # 认证:
  server.user(user)
  server.pass_(password)
  print('Messages: %s. Size: %s' % server.stat())
  resp, mails, octets = server.list()
  # 获取最新一封邮件, 注意索引号从1开始:
  resp, lines, octets = server.retr(len(mails))
  # 解析邮件:
  msg = Parser().parsestr(b'\r\n'.join(lines).decode())
  if(msg.get("from").find(to_email) < 0):
    return

  msg_time = time.strptime(msg.get("date"), "%a, %d %b %Y %H:%M:%S +0800")
  filename = conver_time_to_str(msg_time)

  content = parse_msg(msg).split("\r\n\r\n")[0]

  print("content:\n%s\n\n" % content)
  server.dele(len(mails))
  server.quit()

  save_path = "%s/%s.txt" % (config["save_path"], filename)

  if(file_exist(save_path)):
    content += "\r\n"
    pass

  access_token = config["dropbox_token"]
  client = dropbox.client.DropboxClient(access_token)
  if(client == None):
    save_to_file(save_path, content)
    print("can't drop, save to file: %s" % save_path)
    return

  with tempfile.TemporaryFile() as fp:
    fp.write(str.encode(content))
    fp.seek(0)
    client.put_file('/20141005.txt', fp)
    print("done.")

if __name__ == '__main__':
  main()