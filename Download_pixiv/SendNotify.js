const axios = require('axios');

function sendEnterpriseWechatNotification(message) {
  const corpID = 'YOUR_CORP_ID'; // 企业微信的CorpID
  const agentID = 'YOUR_AGENT_ID'; // 企业微信的应用AgentID
  const chatID = 'YOUR_CHAT_ID'; // 企业微信群聊的ChatID
  const appSecret = 'YOUR_APP_SECRET'; // 企业微信应用的Secret

  const url = `https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token=ACCESS_TOKEN`;

  axios.get(`https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=${corpID}&corpsecret=${appSecret}`)
  .then(response => {
    const accessToken = response.data.access_token;
    const apiUrl = url.replace('ACCESS_TOKEN', accessToken);

    return axios.post(apiUrl, {
      chatid: chatID,
      msgtype: 'text',
      text: {
        content: message,
      },
    });
  })
  .then(response => {
    console.log('企业微信消息发送成功:', response.data);
  })
  .catch(error => {
    console.error('企业微信消息发送失败:', error);
  });
}

module.exports = {
  sendEnterpriseWechatNotification,
};
