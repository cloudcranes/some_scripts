#!/usr/bin/python3
# -- coding: utf-8 --
# -------------------
# @Author: cloudcranes
# @Time: 2024/06/03 16:54
# const $ = new Env("活力伊利")

import json
from datetime import datetime
from os import environ
from sys import stdout
from time import time
from hashlib import md5 as md5Encode
from SendNotify import send
import requests

现在 = datetime.now()
# ck获取 https://msmarket.msx.digitalyili.com下access-token
# ck格式 access-token#备注
hlylck = environ.get('hlylck') if environ.get('hlylck') else True


def print_now(content):
    print(content)
    msg.append(content)
    stdout.flush()


class hlyl:
    def __init__(self, ck):
        self.hlylck = ck
        self.host = 'https://msmarket.msx.digitalyili.com'
        self.headers = {
            'Host': 'msmarket.msx.digitalyili.com',
            'Referer': 'https://servicewechat.com/wx06af0ef532292cd3/459/page-frame.html',
            'content-type': 'application/json',
            'access-token': self.hlylck
        }
        self.main()

    def timestamp(self):
        return round(time() * 1000)

    def md5(self):
        m = md5Encode(str.encode(encoding='utf-8'))
        return m.hexdigest()

    def sign(self):
        url = self.host + '/gateway/api/member/daily/sign'
        data = {}
        try:
            res = requests.post(url, headers=self.headers, data=json.dumps(data), timeout=30)
            if res.json()['error'] == "null":
                if 'dailySign' in res.json()['data']:
                    res = res.json()['data']['dailySign']
                    print_now(f"签到成功")
                    for r in res:
                        print_now(f"获得{res['bonusPoint']}积分，成长积分{res['bonusGrowth']}")
                else:
                    print_now(f"{res.json()['error']}")
            else:
                print_now(f"{res.text}")
        except:
            print_now('签到出错了')

    def sign_check(self):
        self.user_info()
        url = self.host + '/gateway/api/member/sign/status'
        try:
            res = requests.get(url, headers=self.headers, timeout=30)
            if res.json()['status']:
                res = res.json()['data']
                if res['signed']:
                    print_now(f"今天已经签到过了")
                    print_now(f"已签到{res['signedDays']}/{res['taskDays']}天，月签天数：{res['monthSignDays']}天")
                else:
                    print_now('今天未签到')
                    self.sign()
                    print_now(f"周任务天数：{res['taskDays']}天，已签到{res['signedDays']}天，月签天数：{res['monthSignDays']}天")
            else:
                print_now(f"{res.text}")
        except:
            print_now('查询签到奖励出错')

    def user_info(self):
        url = self.host + '/gateway/api/auth/account/user/info'
        try:
            res = requests.get(url, headers=self.headers, timeout=30)
            if res.json()['status']:
                res = res.json()['data']
                print_now(f"用户名：{res['mobile']}")
            else:
                print_now(f"{res.text}")
        except:
            print_now('查询用户信息出错')

    def check_points(self):
        url = self.host + '/gateway/api/member/point'
        try:
            res = requests.get(url, headers=self.headers, timeout=30)
            if res.json()['status']:
                print_now(f"积分：{res.json()['data']}")
            else:
                print_now(f"{res.text}")
        except:
            print_now('查询积分出错')

    def lucky_draw(self):
        url = self.host + '/gateway/api/upgrade/lottery/luckDraw?activityId=1796131190130262018'
        while True:
            try:
                res = requests.get(url, headers=self.headers, timeout=30)
                if res.json()['status']:
                    res = res.json()['data']
                    print_now(f"抽奖成功，获得{res['name']}")
                else:
                    print_now(f"{res.json()['error']['msg']}")
                    break
            except:
                print_now('抽奖出错')
                break

    def main(self):
        self.sign_check()
        self.lucky_draw()
        self.check_points()


if __name__ == '__main__':
    ckArr = []
    for ck in hlylck.split('&'):
        if len(ck) > 10:
            ckArr.append(ck)
    print('共' + str(len(ckArr)) + '个账户')
    c = 0
    u = []
    msg = []
    for i in ckArr:
        c += 1
        print(f"\n****************** 开始账号 {i.split('#')[1]} ******************\n")
        msg.append(f"\n******** 账号 {i.split('#')[1]} ********\n")
        hlyl(i.split('#')[0])
    print("\n****************** 结束 ******************\n")
    print('\n'.join(msg))
    send('活力伊利', '\n'.join(msg))
    exit(0)
