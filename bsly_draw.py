import json
import requests
import os
from SendNotify import send

def draw(account):
    # 抽奖接口URL
    url = 'https://pepcoinbhhpre.pepcoinbypepsico.com.cn/mp/draw'
    headers = {
        'token': account.split('#')[0],
        'User-Agent': account.split('#')[1],
        'Referer': 'https://servicewechat.com/wx1a72addb7ee74f67/126/page-frame.html'
    }
    try:
        # 解析账号信息
        account_name = account.split('#')[2]
        print(f"======= 账号[{account_name}] =======")
        print('开始抽奖...')
        
        draw_msg = ''  # 初始化抽奖信息变量
        
        while True:
            # 发送抽奖请求
            response_text = requests.get(url=url, headers=headers).text
            print("返回数据:", response_text)  
            response = json.loads(response_text)
            
            # 根据抽奖结果处理消息
            if response['code'] == 0:
                draw_msg += f"账号[{account_name}] 抽奖成功：获得{response['data']['name']}\n提示：{response['data']['remark']}\n"
                print(draw_msg)
            elif response['code'] == 500:
                draw_msg += f"账号[{account_name}] {response['msg']}\n"
                print(draw_msg)
                break
            else:
                draw_msg += f"账号[{account_name}] 抽奖失败：{response['msg']}\n"
                print(draw_msg)
                break
        
        return account_name, draw_msg
        
    except Exception as e:
        print('运行失败:', e)
        return '运行失败', ''

if __name__ == "__main__":
    cookies = os.environ.get("bsly")
    accounts = cookies.replace('&', '\n').split('\n')
    print(f"检测到{len(accounts)}个ck记录\n开始运行【百事乐元】")

    msg = ""  

    for account in accounts:
        name, draw_msg = draw(account)
        msg += draw_msg + '\n'

    send("【百事乐元】", msg)
