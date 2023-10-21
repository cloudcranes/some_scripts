import requests

# 目标域名
target_domain = 'https://qyapi.weixin.qq.com'

# 企业微信应用配置
corpid = 'YOUR_CORP_ID'  # 企业ID
corpsecret = 'YOUR_CORP_SECRET'  # 应用Secret
agentid = 'YOUR_AGENT_ID'  # 应用AgentID

class CustomWeCom:
    def __init__(self, corpid, corpsecret, agentid, target_domain):
        self.CORPID = corpid
        self.CORPSECRET = corpsecret
        self.AGENTID = agentid
        self.target_domain = target_domain

    def get_access_token(self):
        url = f"{self.target_domain}/cgi-bin/gettoken?corpid={self.CORPID}&corpsecret={self.CORPSECRET}"
        response = requests.get(url)
        data = response.json()
        return data.get("access_token")

    def send_text(self, message, touser="@all"):
        access_token = self.get_access_token()
        send_url = f"{self.target_domain}/cgi-bin/message/send?access_token={access_token}"
        send_values = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {"content": message},
        }
        response = requests.post(send_url, json=send_values)
        return response.json()["errmsg"]

# 推送消息
def send_to_wecom(title, content):
    wx = CustomWeCom(corpid, corpsecret, agentid, target_domain)
    message = f"{title}\n\n{content}"
    response = wx.send_text(message)
    if response == "ok":
        print("企业微信应用推送成功！")
    else:
        print(f"企业微信应用推送失败：{response}")

# 示例用法
if __name__ == "__main__":
    title = "测试标题"
    content = "测试内容"
    send_to_wecom(title, content)
