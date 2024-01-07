import json
import requests
import os
from SendNotify import send

# 全局变量定义
IKUUU_URL = 'https://ikuuu.me'

def login(account, header):
    login_url = f'{IKUUU_URL}/auth/login'
    data = {
        'email': account.split('#')[0],
        'passwd': account.split('#')[1]
    }

    session = requests.session()

    try:
        account_email = account.split('#')[0]
        print(f"======= 账号[{account_email}] 登录信息 =======")
        print('进行登录...')
        response = json.loads(session.post(url=login_url, headers=header, data=data).text)
        print(response['msg'])
        return session, f"======= 账号[{account_email}] 登录信息 =======\n进行登录...\n{response['msg']}\n"  # 返回包含登录信息的字符串
    except Exception as e:
        error_msg = f"登录失败: {e}\n"
        return None, error_msg

def checkin(session, header):
    check_url = f'{IKUUU_URL}/user/checkin'

    try:
        result = json.loads(session.post(url=check_url, headers=header).text)
        print(result['msg'])
        return result['msg']
    except Exception as e:
        print('签到失败:', e)
        return '签到失败'

def get_user_info(session, header):
    info_url = f'{IKUUU_URL}/user/profile'

    try:
        info_html = session.get(url=info_url, headers=header).text
        # 可以根据需要处理用户信息的部分
    except Exception as e:
        print('获取用户信息失败:', e)

if __name__ == "__main__":
    ikuuu_ck = os.environ.get("ikuuu")
    accounts = ikuuu_ck.split('&')
    print(f"检测到{len(accounts)}个ck记录\n开始ikuuu签到\n")

    header = {
        'origin': IKUUU_URL,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    msg = ""  # 初始化日志信息变量

    for account in accounts:
        session, login_msg = login(account, header)
        if session:
            msg += login_msg + "\n"
            get_user_info(session, header)
            checkin_msg = checkin(session, header)
            msg += checkin_msg + "\n"

    send("ikuuu签到通知", msg)  # 发送日志信息
