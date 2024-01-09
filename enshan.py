#!/usr/bin/python3
# -- coding: utf-8 -- 
# cron "0 0 2 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('恩山签到')
import requests,re,os
from SendNotify import send

def login():
    url = "https://www.right.com.cn/forum/home.php?mod=spacecp&ac=credit&showcredit=1"

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36",
    "Cookie": enshanck
    }

    session = requests.session()
    response = session.get(url=url, headers=headers)
    try:
        coin = re.findall("恩山币: </em>(.*?) &nbsp;", response.text)[0]
        point = re.findall("<em>积分: </em>(.*?)<span", response.text)[0]
        res = f"恩山币：{coin}\n积分：{point}"
        print(res)
        return res
    except Exception as e:
        res = str(e)
        return res

if __name__ == "__main__":
    msg = ""  # 初始化日志信息变量
    #配置恩山的cookie 到配置文件config.sh export enshanck=''
    enshanck = os.environ.get("enshanck")
    accounts = enshanck.split('\n')
    print(f"检测到{len(accounts)}个ck记录\n开始 恩山无线论坛 签到\n")
    msg += f"检测到{len(accounts)}个ck记录\n开始 恩山无线论坛 签到\n"

    for account in accounts:
        login_msg = login()
        msg += login_msg + "\n"
    send('恩山无线论坛', msg)
