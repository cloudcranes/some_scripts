#!/usr/bin/python3
# -- coding: utf-8 --
# cron "30 7 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('科技玩家签到')
# 青龙变量 kjwj_info（邮箱#密码）多账号换行或者&隔开

import requests, json, re,os
from SendNotify import send

# 科技玩家网址
kjwj_host = "www.kejiwanjia.net"

def login(account):
    login_url = f'https://{kjwj_host}/wp-json/jwt-auth/v1/token'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
        'Origin': f'https://{kjwj_host}',
        'Referer': f'https://{kjwj_host}'
    }
    data = {
        'username': account.split('#')[0],
        'password': account.split('#')[1]
    }
    
    try:
        account_email = account.split('#')[0]
        print(f"======= 账号[{account_email}] 登录信息 =======")
        print('进行登录...')
        response = json.loads(requests.post(url=login_url, headers=headers, data=data).text)
        name = response['name']
        print(f'账户名：{name}')
        token = response['token']
        return name, token, f"======= 账号[{account_email}] 登录信息 =======\n进行登录...\n账户名：{response['name']}\n"
    except Exception as e:
        error_msg = f"登录失败: {e}\n"
        return None, None, error_msg

def checkin(name, token):
    log_messages = ""

    check_url = f'https://{kjwj_host}/wp-json/b2/v1/getUserMission'
    sign_url = f'https://{kjwj_host}/wp-json/b2/v1/userMission'
    sign_headers = {
        'Host': kjwj_host,
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': 'Bearer ' + f'{token}',
        'Cookie': f'b2_token={token};',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
    }

    try:
        imfo_1 = json.loads(requests.post(url=check_url, headers=sign_headers).text)
        if imfo_1['mission']['credit'] == 0:
            log_messages += f"开始检查第[{i+1}]个帐号 {name} 签到\n还未签到 开始签到\n"
            imfo_2 = json.loads(requests.post(url=sign_url, headers=sign_headers).text)
            log_messages += f"签到成功 获得 {str(imfo_2)} 积分\n总积分：{str(imfo_1['mission']['my_credit'])}"
        else:
            log_messages += f"帐号[{i + 1}] {name}\n今天已经签到 \n获得 {str(imfo_1['mission']['credit'])} 积分\n总积分：{str(imfo_1['mission']['my_credit'])}"
        print(log_messages)
        return log_messages    
    except Exception as e:
        print('签到失败:', e)
        return '签到失败'        




if __name__ == "__main__":
    msg = ""  # 初始化日志信息变量

    # 青龙变量 kjwj_info（邮箱#密码）多账号&隔开
    kjwj_info = os.environ.get("kjwj_info")
    accounts = kjwj_info.replace('&', '\n')。split('\n')
    print(f"检测到{len(accounts)}个ck记录\n开始 科技玩家 签到\n")
    msg += f"检测到{len(accounts)}个ck记录\n开始 科技玩家 签到\n"

    for i,account in enumerate(accounts):
        name, token, login_msg = login(account)
        if name is not None:
            msg += login_msg + "\n"
            checkin_msg = checkin(name, token)
            msg += checkin_msg + "\n"

    send("科技玩家 签到", msg)
