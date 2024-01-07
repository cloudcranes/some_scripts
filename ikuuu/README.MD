# ikuuu签到脚本说明

## 概述

该 Python 脚本用于进行 ikuuu 签到，适用于特定网站的签到功能。脚本通过指定的 CK 登录账号，自动完成登录、签到操作，并通过 SendNotify 库发送签到通知。

## 功能

- 自动完成 ikuuu 的登录和签到功能
- 支持多个 CK 账号进行签到

## 使用方法

1. 确保安装了 Python 3、requests 库以及 SendNotify 库
2. 将脚本中的 `IKUUU_URL` 设置为 ikuuu 网站的 URL
3. 在环境变量中设置名为 `ikuuu` 的 CK 记录，多个 CK 使用 `&` 分隔
4. 运行脚本

## 注意事项

- 在运行脚本之前，请确保已正确配置环境变量 `ikuuu` 包含有效的 CK 记录
- 如果需要根据具体需求处理用户信息，请修改 `get_user_info` 函数

## 示例

```bash
# ck格式 邮箱#密码
export ikuuu="ck1@domain#123456&ck2@domain#123456"

python3 ikuuu_checkin.py
