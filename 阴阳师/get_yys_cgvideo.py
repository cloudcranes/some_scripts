import os
import requests
from bs4 import BeautifulSoup
import time

# 创建保存视频的文件夹
os.makedirs("H:\\Download", exist_ok=True)

# 用于保存已下载视频的信息的文本文件
downloaded_videos_file = "H:\\Download\\downloaded_videos.txt"

# 如果已下载视频信息的文件存在，从文件中读取已下载视频的名称
downloaded_video_names = set()
if os.path.exists(downloaded_videos_file):
    with open(downloaded_videos_file, "r") as file:
        downloaded_video_names = set(file.read().splitlines())

# 发送GET请求获取网页内容
url = "https://yys.163.com/media/video.html"
response = requests.get(url)

# 使用Beautiful Soup解析HTML
soup = BeautifulSoup(response.content, "html.parser")

# 找到所有class为"tab-cont"的div元素，这里包含了视频信息
video_containers = soup.find_all(class_="tab-cont")

# 定义要下载的视频数量（设置为0表示下载全部视频，或者设置为一个具体的数字表示下载的视频数量）
num_videos_to_download = 0  # 设置为0表示下载全部视频，或者设置为一个具体的数字表示下载的视频数量

# 提取视频信息并下载
downloaded_videos = 0
for idx, container in enumerate(video_containers):
    videos = container.find_all(class_="item2")
    for video in videos:
        video_link = video.find(class_="item")["data-src"]
        video_title = video.find(class_="title").text.strip()

        # 检查视频名称是否已经下载过，如果是则跳过下载
        if video_title in downloaded_video_names:
            print(f"视频已下载过，跳过：{video_title}")
            continue

        # 下载视频文件
        response = requests.get(video_link, stream=True)
        video_filename = f"E:\\Download\\{video_title}.mp4"

        with open(video_filename, "wb") as video_file:
            for chunk in response.iter_content(chunk_size=8192):
                video_file.write(chunk)

        print(f"已下载视频：{video_filename}")
        downloaded_videos += 1

        # 将下载过的视频名称添加到集合中，并保存到文件中
        downloaded_video_names.add(video_title)
        with open(downloaded_videos_file, "a") as file:
            file.write(video_title + "\n")

        # 如果设置了下载数量，并且已下载的视频数量达到指定数量，则停止下载
        if num_videos_to_download > 0 and downloaded_videos >= num_videos_to_download:
            break

        # 每个视频下载间隔2秒
        time.sleep(2)

print("所有视频下载完成。")
