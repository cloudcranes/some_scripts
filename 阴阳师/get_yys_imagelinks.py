import os
import requests
from bs4 import BeautifulSoup
import re

def extract_filename_from_url(img_url):
    # 使用正则表达式从图片链接中提取特定部分作为文件名
    filename = re.search(r'/(\d+/\d+)/', img_url)
    if filename:
        # 将斜杠替换为下划线
        return filename.group(1).replace('/', '_')
    else:
        return "unknown_filename"

def is_image_already_downloaded(file_path):
    return os.path.exists(file_path)

def download_images(image_urls, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for img_url in image_urls:
        try:
            # 提取文件名并将斜杠替换为下划线
            file_name = extract_filename_from_url(img_url)
            file_path = os.path.join(save_folder, f"{file_name}.jpg")
            
            if is_image_already_downloaded(file_path):
                print(f'{file_name}.jpg 已经存在，跳过下载')
            else:
                response = requests.get(img_url, headers=headers)
                if response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f'{file_name}.jpg 下载成功')
                else:
                    print(f'{img_url} 下载失败  原因：{response.status_code}')
        except Exception as e:
            print(f'{img_url} 下载失败  原因：{str(e)}')

def main():
    url = "https://yys.163.com/media/picture.html"
    response = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(response, 'html.parser')
    wallpaper = soup.find_all('div', {'class': 'tab-cont'})  
    pc = wallpaper[0].find_all('div', {'class': 'mask'})  

    pc_list = []  
    for div in pc:
        a = div.find_all('a')
        if len(a) == 6:
            img_url = re.findall('href="(.*?)" target', str(a[2]))[0]  
            pc_list.append(img_url)

    save_folder = "./yys原画"
    download_images(pc_list, save_folder)

if __name__ == "__main__":
    main()
