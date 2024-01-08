#!/usr/bin/python3
# -- coding: utf-8 --
# cron "30 7 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('科技玩家签到')

import requests, json, re,os
from SendNotify import send


# 青龙变量 kjwj_username 配置用户名（一般是邮箱）  kjwj_password 配置用户名对应的密码 和上面的username对应上 多账号&隔开
kjwj_username = os.getenv("kjwj_username").split('&')
kjwj_password = os.getenv("kjwj_password").split('&')

log_messages = ""

for i in range(len(kjwj_username)):
    url = 'https://www.kejiwanjia.net/wp-json/jwt-auth/v1/token'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
        'Origin': 'https://www.kejiwanjia.net',
        'Referer': 'https://www.kejiwanjia.net'
    }
    data = {
        'username': f'{kjwj_username[i]}',
        'password': f'{kjwj_password[i]}'
    }
    html = requests.post(url=url, headers=headers, data=data)
    result = json.loads(html.text)
    # print(json.dumps(result, indent=2))
    name = result['name']
    token = result['token']
    check_url = 'https://www.kejiwanjia.net/wp-json/b2/v1/getUserMission'
    sign_url = 'https://www.kejiwanjia.net/wp-json/b2/v1/userMission'
    sign_headers = {
        'Host': 'www.kejiwanjia.net',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'authorization': 'Bearer ' + f'{token}',
        'cookie': f'b2_token={token};',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
    }
    html_1 = requests.post(url=check_url, headers=sign_headers)
    imfo_1 = json.loads(html_1.text)
    if imfo_1['mission']['credit'] == 0:
        log_messages += f"开始检查第[{i+1}]个帐号 {name} 签到\n还未签到 开始签到\n"
        html_2 = requests.post(url=sign_url, headers=sign_headers)
        imfo_2 = json.loads(html_2.text)
        log_messages += f"签到成功 获得 {str(imfo_2)} 积分\n总积分：{str(imfo_1['mission']['my_credit'])}"
    else:
        log_messages += f"帐号[{i + 1}] {name}\n今天已经签到 \n获得 {str(imfo_1['mission']['credit'])} 积分\n总积分：{str(imfo_1['mission']['my_credit'])}"
print(log_messages)
send('科技玩家 签到', log_messages)
