import os
import json
import sys
import time
import asyncio
import logging
from pathlib import Path
import httpx

# 从环境变量读取配置参数
alist_scan_path: str = os.getenv('ALIST_SCAN_PATH', '/')
alist_server_url = os.getenv('ALIST_SERVER_URL', 'http://192.168.1.1:5244')
alist_server_token = os.getenv('ALIST_SERVER_TOKEN',
                               'alist-xxxxx')
output_dir = os.getenv('OUTPUT_DIR', './link')
webdav_url = os.getenv('WEBDAV_URL', 'http://192.168.1.1:5244/dav')

# 日志配置
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 中文日志翻译
translated_log_messages = {
    'ERROR': '错误',
    'WARNING': '警告',
    'INFO': '信息',
    'DEBUG': '调试',
}


def translate_log_level(log_level) -> str:
    return translated_log_messages.get(log_level, log_level)


class TranslatedLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.terminator = '\n'

    def emit(self, record):
        record.levelname = translate_log_level(record.levelname)
        msg = self.format(record)
        stream = sys.stderr
        stream.write(msg)
        stream.write(self.terminator)
        self.flush()


handler = TranslatedLogHandler()
logger.addHandler(handler)


# 获取文件直链 需要支持302跳转
async def async_get_file_link(session, path):
    headers = {'Authorization': alist_server_token}
    payloads = {'path': path, 'password': ''}
    url = f'{alist_server_url}/api/fs/get'

    try:
        # 增加timeout参数
        response = await session.post(url, headers=headers, json=payloads, timeout=httpx.Timeout(30.0, connect=15.0))
        response.raise_for_status()

        if response is None:
            logger.error(f"{translate_log_level('ERROR')}: 获取文件链接时响应为空")
            return None

        data = response.json()
        if 'data' in data and 'raw_url' in data['data']:
            return data['data']['raw_url']
        else:
            logger.error(f"{translate_log_level('ERROR')}: 从服务器获取的数据不是预期的链接格式: {data}")
            return None
    except httpx.RequestError as e:
        logger.error(f"{translate_log_level('ERROR')}: 获取文件链接时发生错误: {e}")
        return None


async def async_fetch_directory_content(session, path):
    """异步从Alist服务器获取目录内容。"""
    headers = {'Authorization': alist_server_token}
    payloads = {'path': path, 'password': '', "page": 1, "per_page": 0, "refresh": False}
    url = f'{alist_server_url}/api/fs/list'
    try:
        response = await session.post(url, headers=headers, json=payloads, timeout=httpx.Timeout(15.0, connect=15.0))
        response.raise_for_status()
        data = response.json()
        if 'data' in data and 'content' in data['data'] and isinstance(data['data']['content'], list):
            return data['data']['content']
        else:
            logger.error(f"{translate_log_level('ERROR')}: 从服务器获取的数据不是预期的列表格式: {data}")
            return []
    except httpx.RequestError as e:
        logger.error(f"{translate_log_level('ERROR')}: 未能获取 {path} 的目录内容: {e}")
        return []


def generate_clean_strm_filename(file_name):
    base_name, ext = os.path.splitext(file_name)
    if ext.lower() in {'.mp4', '.mkv', '.avi', '.wmv'}:
        file_name = base_name
    return file_name + '.strm'


async def async_generate_strm_file_if_not_exists(session, file_path, alist_url):
    """异步根据视频文件路径生成.strm文件，如果已存在则跳过。"""
    clean_file_name = generate_clean_strm_filename(alist_url)
    output_file = Path(output_dir) / clean_file_name

    # 检查文件是否存在
    if output_file.exists():
        logger.info(f"{translate_log_level('INFO')}: .strm 文件已存在: {output_file}, 跳过生成.")
        print(f"{translate_log_level('INFO')}: .strm 文件已存在: {output_file}, 跳过生成.")
        return

    async with output_file.open('w') as f:
        # webdav地址
        f.write(f"{webdav_url}{alist_scan_path}{alist_url}")
    logger.info(f"{translate_log_level('INFO')}: 生成 .strm 文件: {output_file}")
    print(f"{translate_log_level('INFO')}: 生成 .strm 文件: {output_file}")


async def async_process_directory(path, alist_url_prefix=''):
    """异步递归处理目录，生成.strm文件。"""
    async with httpx.AsyncClient() as session:
        content = await async_fetch_directory_content(session, path)

        tasks = []
        for item in content:
            sub_path = os.path.join(path, item['name']) if alist_url_prefix else item['name']
            if item['is_dir']:
                # 创建子目录
                os.makedirs(Path(output_dir) / sub_path, exist_ok=True)
                print(f"{translate_log_level('INFO')}: 创建子目录: {Path(output_dir)} / {sub_path}")
                # 递归处理子目录
                await async_process_directory(sub_path, os.path.join(alist_url_prefix, item['name']))
            elif item['name'].lower().endswith(('.mp4', '.mkv', '.avi', '.wmv')):
                full_url = os.path.join(alist_url_prefix, item['name'])
                await async_generate_strm_file_if_not_exists(session, item['name'], full_url)
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    start_time = time.time()
    logger.info(f"{translate_log_level('INFO')}: 扫描目录: {alist_scan_path}")
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"{translate_log_level('INFO')}: 输出目录: {output_dir}")
    logger.info(f"{translate_log_level('INFO')}: 访问令牌: {alist_server_token}")
    logger.info(f"{translate_log_level('INFO')}: 服务器地址: {alist_server_url}")
    logger.info(f"{translate_log_level('INFO')}: 开始目录处理...")
    asyncio.run(async_process_directory(alist_scan_path))
    end_time = time.time()
    logger.info(f"{translate_log_level('INFO')}: 处理完成. 用时: {end_time - start_time} 秒.")
