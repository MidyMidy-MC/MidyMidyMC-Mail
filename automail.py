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

# #######################以下内容可修改#################################

logfile = os.environ['HOME'] + '/.znc/users/MidyMidyBot/moddata/log/#MidyMidymc_%s.log' % time.strftime('%Y%m%d', yesterday)
filterfile = 'filter.txt'

MASK = '***奇怪***'
SUBJECT = 'MidyMidyIII-%sIRC聊天记录'
ME = 'MidyMidyBot <midymidybot@outlook.com>'
TO = 'MidyMidyMC <tonychee1989@gmail.com>'
CONTENT_PREFIX = '%s聊天记录' % time.strftime('%Y年%m月%d日', yesterday)

SMTPSERVER = 'smtp-mail.outlook.com'
SMTPPORT = 587
ACCOUNT = 'midymidybot@outlook.com'
PASSWORD = 'YP2b2Mq2sN4M'

# #######################以上内容可修改#################################


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
    return msg.as_string(unixfrom=True)


def send_mail(mail):
    '''使用SMTP发送邮件'''
    r = re.compile(r'<(.*@.*)>')
    from_ = r.findall(ME)[0]
    to = r.findall(TO)[0]
    S = smtplib.SMTP(SMTPSERVER, port=SMTPPORT)
    S.starttls()
    S.login(ACCOUNT, PASSWORD)
    S.sendmail(from_, to, mail)
    S.quit()

if __name__ == '__main__':
    try:
        send_mail(make_mail(gen_content()))
        print 'Mail sent successfully!'

    except Exception as e:
        print 'Mail sent failed!'
        print e
