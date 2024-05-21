import os
import json
import asyncio
import logging
import time
from pathlib import Path
from typing import Any
import aiofiles
import aiohttp

# 保持环境变量读取不变
alist_scan_path: str = os.getenv('ALIST_SCAN_PATH', '/')
alist_server_url = os.getenv('ALIST_SERVER_URL', 'http://127.0.0.1:5244')
alist_server_token = os.getenv('ALIST_SERVER_TOKEN',
                               'alist-ec9cff6a-69f1-4f8a-8c56-a7bb5cb4d628Bj0uXjbNRuBcstx68jPONME02B6XWNAjXHTTJ6Z1zjg0p4aO5LEpsjvdwkGJzUJd')
output_dir = os.getenv('OUTPUT_DIR', './link')
webdav_url = os.getenv('WEBDAV_URL', 'http://192.168.1.1:5244/dav')
# 支持的文件类型
supported_file_types = ['.mp4', '.mkv', '.avi', '.wmv']
# 请求超时配置
timeout = aiohttp.ClientTimeout(total=30.0, connect=15.0)

# 日志配置
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# 使用aiohttp替换httpx
async def async_get_file_link(session, path):
    logger.info(f"正在获取文件链接: {path}")
    headers = {'Authorization': alist_server_token}
    payloads = {'path': path, 'password': '', 'page': 1, 'per_page': 0, 'refresh': False}
    url = f'{alist_server_url}/api/fs/get'

    try:
        response = await session.post(url, headers=headers, json=payloads, timeout=timeout)
        if response.status != 200:
            raise aiohttp.HttpProcessingError(message=f"Unexpected status {response.status}", code=response.status)

        data = await response.json()
        if 'data' in data and 'raw_url' in data['data']:
            return data['data']['raw_url']
        else:
            logger.error(f"从服务器获取的数据不是预期的链接格式: {data}")
            return None
    except aiohttp.ClientError as e:
        logger.error(f"获取文件链接时发生错误: {e}")
        return None


async def async_fetch_directory_content(session: aiohttp.ClientSession, path: str) -> list[Any]:
    headers = {'Authorization': alist_server_token}
    payloads = {'path': path, 'password': '', "page": 1, "per_page": 0, "refresh": False}
    url = f'{alist_server_url}/api/fs/list'

    try:
        response = await session.post(url, headers=headers, json=payloads, timeout=timeout)
        response.raise_for_status()  # 引发HTTP错误，如果响应状态不是200

        data = await response.json()
        # logger.debug(f"接收到的服务器响应: {data}")

        if 'data' not in data or 'content' not in data['data']:
            logger.error(f"从服务器获取的数据不是预期的格式: {data}")
            return []

        content = data['data']['content']
        if not isinstance(content, list):
            logger.error(f"从服务器获取的数据'content'不是预期的列表格式: {data}")
            return []

        return content
    except aiohttp.ClientError as e:
        logger.error(f"未能获取 {path} 的目录内容: {e}")
        return []


def generate_clean_strm_filename(file_name):
    base_name, ext = os.path.splitext(file_name)
    if ext.lower() in supported_file_types:
        file_name = base_name
    return file_name + '.strm'


async def async_generate_strm_file_if_not_exists(session, file_path, alist_url):
    clean_file_name = generate_clean_strm_filename(alist_url)
    output_file = Path(output_dir) / clean_file_name

    # 检查文件是否存在，同时避免路径遍历攻击
    if output_file.is_file():
        logger.info(f".strm 文件已存在: {output_file}, 跳过生成.")
        return

    file_link = await async_get_file_link(session, alist_url)
    logger.info(f"获取文件链接: {file_link}")

    async with aiofiles.open(output_file, 'w') as f:
        await f.write(f"{file_link}")

    logger.info(f"生成 .strm 文件: {output_file}")


async def async_process_directory(path, alist_url_prefix=''):
    async with aiohttp.ClientSession() as session:
        content = await async_fetch_directory_content(session, path)

        tasks = []
        for item in content:
            sub_path = os.path.join(path, item['name']) if alist_url_prefix else item['name']
            if item['is_dir']:
                # 创建子目录，加入路径合法性检查
                output_sub_path = Path(output_dir) / sub_path
                if output_sub_path.is_dir() or output_sub_path.parent.is_dir():
                    os.makedirs(output_sub_path, exist_ok=True)
                    logger.info(f"创建子目录: {output_sub_path}")
                    await async_process_directory(sub_path, os.path.join(alist_url_prefix, item['name']))
            elif any(item['name'].lower().endswith(ext) for ext in supported_file_types):
                full_url = os.path.join(alist_url_prefix, item['name'])
                await async_generate_strm_file_if_not_exists(session, item['name'], full_url)
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    start_time = time.time()
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"扫描目录: {alist_scan_path}")
    logger.info(f"输出目录: {output_dir}")
    logger.info(f"访问令牌已设置")
    logger.info(f"服务器地址: {alist_server_url}")
    logger.info(f"开始目录处理...")
    asyncio.run(async_process_directory(alist_scan_path))
    end_time = time.time()
    logger.info(f"处理完成. 用时: {end_time - start_time} 秒.")
