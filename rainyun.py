#!/usr/bin/env python3
# coding: utf-8
'''
功能：雨云服务器签到
cron: 0 2 * * *
new Env('Rainyun签到');
'''

import requests
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
import logging
import json
from SendNotify import send

# 忽略 不验证ssl的提示
import warnings
warnings.filterwarnings('ignore')

rainyun_host = "api.rainyun.com"
rainyun_api_host = "api.v2.rainyun.com"

class RainYun():
    def __init__(self, account) -> None:
        # 认证信息
        user = account.split('#')[0]
        pwd = account.split('#')[1]
        self.user = user.lower()
        self.pwd = pwd
        self.json_data = json.dumps({
            "field": self.user,
            "password": self.pwd
            })
        # 日志输出
        self.logger = logging.getLogger(self.user)
        formatter = logging.Formatter(datefmt='%Y/%m/%d %H:%M:%S',
                                      fmt="%(asctime)s 雨云 %(levelname)s: 用户<%(name)s> %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        # 签到结果初始化
        self.signin_result = False
        # 请求设置
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
            "Origin": f'https://{rainyun_host}',
            "Referer": f'https://{rainyun_host}'
        })
        self.login_url = f'https://{rainyun_api_host}/user/login'
        self.signin_url = f'https://{rainyun_api_host}/user/reward/tasks'
        self.logout_url = f'https://{rainyun_api_host}/user/logout'
        self.query_url = f'https://{rainyun_api_host}/user/'
        # 忽略 .cc ssl错误
        self.session.verify = False

    def login(self) -> None:
        """登录"""
        res = self.session.post(
            url=self.login_url, headers={"Content-Type": "application/json"}, data=self.json_data)
        if res.text.find("200") > -1:
            self.msg += f"{self.user}: 登录成功\n"
            self.logger.info("登录成功")
            self.session.headers.update({
                "X-CSRF-Token": res.cookies.get("X-CSRF-Token", "")
            })
        else:
            self.msg += f"{self.user}: 登录失败，响应信息：{res.text}\n"
            self.logger.error(f"登录失败，响应信息：{res.text}")

    def signin(self) -> None:
        """签到"""
        res = self.session.post(url=self.signin_url, headers={"Content-Type": "application/json"}, data=json.dumps({
            "task_name": "每日签到",
            "verifyCode": ""
        }))
        self.signin_date = datetime.utcnow()
        if res.text.find("200") > -1:
            self.msg += f"{self.user}: 成功签到并领取积分\n"
            self.logger.info("成功签到并领取积分")
            self.signin_result = True
        else:
            self.msg += f"{self.user}: 签到失败，响应信息：{res.text}\n"
            self.logger.error(f"签到失败，响应信息：{res.text}")
            self.signin_result = False

    def logout(self) -> None:
        res = self.session.post(url=self.logout_url)
        if res.text.find("200") > -1:
            self.msg += f"{self.user}: 已退出登录\n"
            self.logger.info('已退出登录')
        else:
            self.msg += f"{self.user}: 退出登录时出了些问题，响应信息：{res.text}\n"
            self.logger.warning(f"退出登录时出了些问题，响应信息：{res.text}")

    def query(self) -> None:
        res = self.session.get(url=self.query_url)
        self.points = None
        if res.text.find("200") > -1:
            data = res.json()["data"]
            if "points" in data:
                self.points = data["points"]
                self.msg += f"{self.user}: 积分查询成功为 {repr(self.points)}\n"
                self.logger.info("积分查询成功为 " + repr(self.points))
            else:
                self.msg += f"{self.user}: 未获取到积分信息\n"
                self.logger.warning("未获取到积分信息")
        else:
            self.msg += f"{self.user}: 积分信息失败，响应信息：{res.text}\n"
            self.logger.error(f"积分信息失败，响应信息：{res.text}")

if __name__ == '__main__':
    msg = ""  # 初始化日志信息变量
    rainyun_ck = os.environ.get("rainyun_ck")
    accounts = rainyun_ck.replace('&', '\n').split('\n')
    print(f"检测到{len(accounts)}个ck记录\n开始 RainYun服务器 签到\n")
    msg += f"检测到{len(accounts)}个ck记录\n开始 RainYun服务器 签到\n"

    for account in accounts:
        ry = RainYun(account)  # 实例
        ry.msg = ""  # 为每个账户初始化日志信息
        ry.login()  # 登录
        ry.signin()  # 签到
        ry.query()  # 查询积分
        ry.logout()  # 登出
        msg += ry.msg  # 将当前账户的日志信息追加到全局 msg 变量中

    try:
        send('Rainyun服务器', msg)  # 发送整合后的日志信息
    except Exception as e:
        print(f"发送通知时出现异常：{e}")
