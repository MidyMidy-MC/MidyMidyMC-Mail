#!/usr/bin/env python2
# coding:utf-8
# AutoMail by TonyChyi
# Send filted irc log 1 day ago!

import time
import re
import email
import smtplib
import os

yesterday = time.localtime(time.time() - 86400)
today = time.localtime(time.time())

########################以下内容可修改#################################

logfile = os.environ['HOME'] + '#MidyMidymc_%s.log' % time.strftime('%Y%m%d', yesterday)
filterfile = 'filter.txt'

MASK = '***奇怪***'
SUBJECT = 'MidyMidyIII-%sIRC聊天记录'
ME = 'mc_bot <no-replay@MidyMidyMC>'
TO = 'leo_song <leo_songwei@outlook.com>'
CONTENT_PREFIX = '%s聊天记录' % time.strftime('%Y年%m月%d日', yesterday)

########################以上内容可修改#################################


def gen_content():
    '''邮件正文生成'''
    mail = '%s\n\n' % CONTENT_PREFIX
    for line in open(logfile):
        if re.search(r'\*\*\*', line):
            continue

        line = re.sub(r'\x03[0-9]{2}|\x0f', '', line)
        mail += filter(line)
    return mail


def filter(msg):
    '''奇怪的词语过滤'''
    for line in open('filter.txt', 'r'):
        if line != '':
            msg = re.sub(line.replace('\n', ''), MASK, msg)

    return msg


def make_mail(payload):
    '''生成邮件'''
    msg = email.Message.Message()
    msg['To'] = TO
    msg['From'] = ME
    msg['Date'] = time.strftime('%Y-%m-%d', today)
    msg['Subject'] = SUBJECT % time.strftime('%Y年%m月%d日', yesterday)
    msg['Content-Type'] = 'text/plain; charset=utf-8'
    msg['Content-Transfer-Encoding'] = '8bit'
    msg.set_payload(payload)
    return msg.as_string()


def send_mail(mail):
    '''使用SMTP发送邮件'''
    S = smtplib.SMTP('localhost')
    S.send(mail)
    S.quit()

if __name__ == '__main__':
    send_mail(make_mail(gen_content()))
