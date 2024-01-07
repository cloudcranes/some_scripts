#!/usr/bin/env python3
# coding: utf-8
'''
功能：自动备份qinglong基本文件
cron: 0 2 * * *
new Env('qinglong备份');
'''
import logging
import os
import sys
import tarfile
import time
import requests
import json
from urllib.parse import quote

# 全局变量
# alist 地址url 示例 http://192.168.1.2:5244
ALIST_URL = ""
# alist 备份文件保存目录 示例 /qinglong_backup
ALIST_UPLOAD_PATH = "
# alist 账号 示例 admin
ALIST_USER = ""
# alist 密码 示例 password
ALIST_PASSWORD = ""

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
try:
    from SendNotify import send
except:
    logger.info("无推送文件")

def env(key):
    return os.environ.get(key)

QLBK_EXCLUDE_NAMES = ['log', '.git', '.github',
                      'node_modules', 'backups', '.pnpm-store']  # 排除目录名
if env("QLBK_EXCLUDE_NAMES"):
    QLBK_EXCLUDE_NAMES = env("QLBK_EXCLUDE_NAMES")
    logger.info(f'检测到设置变量 {QLBK_EXCLUDE_NAMES}')

QLBK_BACKUPS_PATH = 'backups'  # 备份目标目录
if env("QLBK_BACKUPS_PATH"):
    QLBK_BACKUPS_PATH = str(env("QLBK_BACKUPS_PATH"))
    logger.info(f'检测到设置变量 {QLBK_BACKUPS_PATH}')

QLBK_MAX_FLIES = 5  # 最大备份保留数量默认5个
if env("QLBK_MAX_FLIES"):
    QLBK_MAX_FLIES = int(env("QLBK_MAX_FLIES"))
    logger.info(f'检测到设置变量 {QLBK_MAX_FLIES}')


def start():
    """开始备份"""
    logger.info('将所需备份目录文件进行压缩...')
    retval = os.getcwd()
    mkdir(QLBK_BACKUPS_PATH)
    now_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    files_name = f'{QLBK_BACKUPS_PATH}/qinglong_{now_time}.tar.gz'
    logger.info(f'创建备份文件: {retval}/{files_name}')
    backup_success = make_targz(files_name, retval)
    message_up_time = time.strftime("%Y年%m月%d日 %H时%M分%S秒", time.localtime())
    text = f'备份完成时间:\n{message_up_time}\n'

    if backup_success:
        text += f'已备份:\n{run_path}{QLBK_BACKUPS_PATH}/qinglong_{now_time}.tar.gz\n'
        logger.info('---------------------备份完成---------------------')
    else:
        text += '备份压缩失败,请检查日志\n'
        sys.exit(1)

    # 调用 file_upload 函数上传备份文件
    upload_success = file_upload(files_name)  # 使用备份文件的完整路径进行上传
    if upload_success:
        text += '备份文件上传成功'
        logger.info('备份文件上传成功')
    else:
        text += '备份文件上传失败'
        logger.info('备份文件上传失败')

    try:
        send('【qinglong自动备份】', text)
    except:
        logger.info("通知发送失败")
    sys.exit(0)


def make_targz(output_filename, retval):
    """
    压缩为 tar.gz
    :param output_filename: 压缩文件名
    :param retval: 备份目录
    :return: bool
    """
    try:
        tar = tarfile.open(output_filename, "w:gz")
        os.chdir(retval)
        path = os.listdir(os.getcwd())
        for p in path:
            if os.path.isdir(p):
                if p not in QLBK_EXCLUDE_NAMES:
                    pathfile = os.path.join(retval, p)
                    tar.add(pathfile)
        tar.close()
        return True
    except Exception as e:
        logger.info(f'压缩失败: {str(e)}')
        return False


def mkdir(path):
    """创建备份目录"""
    folder = os.path.exists(path)
    if not folder:
        logger.info(f'第一次备份,创建备份目录: {QLBK_BACKUPS_PATH}')
        os.makedirs(path)
    else:
        backup_files = f'{run_path}{path}'
        files_all = os.listdir(backup_files)
        logger.info(f'当前备份文件 {len(files_all)}/{QLBK_MAX_FLIES}')
        files_num = len(files_all)
        if files_num > QLBK_MAX_FLIES:
            logger.info(f'达到最大备份数量 {QLBK_MAX_FLIES} 个')
            check_files(files_all, files_num, backup_files, QLBK_MAX_FLIES)


def fileremove(filename):
    """删除旧的备份文件"""
    if os.path.exists(filename):
        os.remove(filename)
        logger.info('已删除本地旧的备份文件: %s' % filename)
    else:
        pass


def check_files(files_all, files_num, backup_files, QLBK_MAX_FLIES):
    """检查旧的备份文件"""
    create_time = []
    file_name = []
    for names in files_all:
        if names.endswith(".tar.gz"):
            filename = os.path.join(backup_files, names)
            file_name.append(filename)
            create_time.append(os.path.getctime(filename))
    dit = dict(zip(create_time, file_name))
    dit = sorted(dit.items(), key=lambda d: d[-2], reverse=False)
    for i in range(files_num - QLBK_MAX_FLIES):
        file_location = dit[i][1]
        fileremove(file_location)


def token_get():
    """获取 token"""
    url = f"{ALIST_URL}/api/auth/login"

    payload = json.dumps({
       "username": ALIST_USER,
       "password": ALIST_PASSWORD
    })
    headers = {
       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
       'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        token = response.json().get('data', {}).get('token')
        logger.info(f"成功获取 token: {token}")
        return token
    else:
        logger.error(f"获取 token 失败: {response.text}")
        return None


def file_upload(file_path):
    """文件上传"""
    url = f"{ALIST_URL}/api/fs/put"
    file_name_1, file_ext = os.path.splitext(os.path.basename(file_path))
    file_alist_path = f"{ALIST_UPLOAD_PATH}/{file_name_1}{file_ext}"
    encoded_path = quote(file_alist_path, safe='')

    # 获取 token
    auth_token = token_get()
    if not auth_token:
        logger.error("无法上传文件，获取认证 token 失败")
        return False

    headers = {
       'Authorization': auth_token,
       'File-Path': encoded_path,  # 添加上传文件的路径
       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
       'Content-Type': 'application/x-zip-compressed'
    }

    try:
        file_size_bytes = os.path.getsize(file_path)  # 获取文件大小（字节）
        file_size_kb = math.ceil(file_size_bytes / 1024)  # 将文件大小转换为KB并向上取整
        file_size_kb_str = str(file_size_kb)  # 以字符串形式表示文件大小（KB）
        headers['Content-Length'] = file_size_kb_str  # 设置 Content-Length

        with open(file_path, 'rb') as file:
            files = {
                'file': (file_name_1, file)
            }

            response = requests.put(url, headers=headers, files=files)

            if response.status_code == 200:
                logger.info(f"文件上传成功 {response.text}")
                return True
            else:
                logger.error(f"文件上传失败: {response.text}")
                return False
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}\n{response.text}")
        return False


if __name__ == '__main__':
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logger.info('---------' + str(nowtime) + ' 备份程序开始执行------------')
    if os.path.exists('/ql/data/'):
        logger.info('检测到data目录，切换运行目录至 /ql/data/')
        run_path = '/ql/data/'
    else:
        run_path = '/ql/'
    os.chdir(run_path)
    start()
    sys.exit(0)
