#!/usr/bin/env python3
# coding: utf-8
'''
功能：WPS打卡活动
cron: 10 9 * * *
new Env('WPS打卡活动');
'''

# 需要参数：wps_sid 
# 获取方式 wps主页或者微信小程序【我的WPS超级会员】
# 抓取域名 *.wps.cn

import json
import requests
import os
from SendNotify import send

def get_userinfo(account):
    url = "https://account.wps.cn/p/auth/check"
    headers = {
        'Cookie': f'wps_sid={account};csrf=1234567890',
        'X-CSRFToken': "1234567890",
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.47(0x18002f28) NetType/WIFI Language/zh_CN"
    }
    msg = ''
    response = requests.post(url=url, headers=headers)
    # print(response.text)  # 打印响应内容，以便调试
    if response.status_code == 200:
        response_data = response.json()
        account_name = response_data.get('nickname', 'Unknown')
        print(f"账号【{account_name}】 绑定手机：{response_data.get('loginmode', 'Unknown')}")
        msg = f"账号【{account_name}】 绑定手机：{response_data.get('loginmode', 'Unknown')}\n"
        return msg, account_name
    else:
        print('运行失败: 未收到有效响应')
        return '运行失败: 未收到有效响应', 'Unknown'


def clock_in(account):
    url = "https://personal-bus.wps.cn/activity/clock_in/v1/info?client_type=1&page_index=0&page_size=2"
    headers = {
        'Cookie': f'wps_sid={account};csrf=1234567890',
        'X-CSRFToken': "1234567890",
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.47(0x18002f28) NetType/WIFI Language/zh_CN"
    }
    login_msg, account_name = get_userinfo(account)
    msg = ''
    msg += login_msg
    response = requests.get(url=url, headers=headers)
    # print(response.text)  # 打印响应内容，以便调试
    response_data = response.json()
    if response.status_code == 200:
        reward_list = response_data.get('data', {}).get('reward_list', {}).get('list', [])
        if reward_list:
            reward_info = reward_list[0]
            reward_sku_name = reward_info.get('sku_name', None)
            if not reward_sku_name:
                reward_sku_name = reward_info.get('mb_name', '未知')
            print(f"账号【{account_name}】 {reward_sku_name}")
            msg += f"账号【{account_name}】 {reward_sku_name}\n"
            print(f"账号【{account_name}】 持续打卡天数：{response_data['data']['continuous_days']}")
            msg += f"账号【{account_name}】 持续打卡天数：{response_data['data']['continuous_days']}"
        else:
            print(f"账号【{account_name}】今日已成功打卡，但未获得奖励")
            msg += f"账号【{account_name}】今日已成功打卡，但未获得奖励\n"
    else:
        print('运行失败: 未收到有效响应')
        return '', '账号 运行失败: 未收到有效响应'
    return msg, account_name


if __name__ == "__main__":
    # 获取环境变量中的cookies
    cookies = cookies = os.environ.get("wps_ck")
    # 将cookies分割成账号列表
    accounts = cookies.replace('&', '\n').split('\n')
    print(f"检测到{len(accounts)}个ck记录\n开始运行【WPS 每周打卡】")

    msg = ""

    for account in accounts:
        # 调用打卡函数
        clock_msg, name = clock_in(account)
        msg += str(clock_msg) + '\n'  # 将元组转换为字符串

    # 发送通知
    # send("【WPS 每周打卡】", msg)