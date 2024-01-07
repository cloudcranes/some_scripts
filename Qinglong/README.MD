# Qinglong 自动备份程序

## 概述

这个 Python 脚本用于自动备份 Qinglong 项目的文件，并将备份文件上传至 ALIST 存储服务。它利用 tar 打包目标文件并使用 API 请求将备份文件上传至指定的 ALIST 存储路径。

## 功能

- 自动备份 Qinglong 项目文件
- 将备份文件上传至 ALIST 存储

## 使用方法

1. 在 `ALIST_URL` 中填入你的 ALIST 存储服务地址
2. 在 `ALIST_UPLOAD_PATH` 中填入你的 ALIST 存储路径
3. 在 `ALIST_USER` 中填入 ALIST 登录用户名
4. 在 `ALIST_PASSWORD` 中填入 ALIST 登录密码
5. 配置定时任务使用 `cron` 来定时执行该脚本，例如 `0 2 * * *`

## 依赖项

- Python 3
- requests 库

## 配置

- `ALIST_URL`：ALIST 存储服务的 URL
- `ALIST_UPLOAD_PATH`：ALIST 存储的备份文件路径
- `ALIST_USER`：ALIST 登录用户名
- `ALIST_PASSWORD`：ALIST 登录密码

## 示例

```bash
export ALIST_URL="https://your-alist-url.com"
export ALIST_UPLOAD_PATH="/qinglong_backup"
export ALIST_USER="your_username"
export ALIST_PASSWORD="your_password"

- 排除目录名 log .git .github node_modules backups .pnpm-store
- 备份目标目录 backups
