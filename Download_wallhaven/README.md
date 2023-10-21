# Wallhaven壁纸下载器

这是一个用于从Wallhaven网站下载壁纸图片的简单Python脚本。该脚本会从Wallhaven的最新壁纸页面获取图片链接，然后下载这些图片到本地文件夹，并发送通知。

## 如何使用

### 1. 安装依赖

在使用之前，请确保你已经安装了Python。然后，使用以下命令安装依赖：

```bash
pip install requests parsel
```

### 2. 配置

在脚本中找到以下代码段：

```python
# 定义保存路径，包括日期分类
save_folder = os.path.join('/ql/data/downloads/local-website/img', current_date)
```

将`save_folder`变量的值修改为你希望保存壁纸图片的本地文件夹路径。

### 3. 运行脚本

在项目文件夹中运行以下命令：

```bash
python main.py
```

脚本将会开始从Wallhaven的最新壁纸页面获取图片链接，并下载这些图片到指定的本地文件夹。

## 注意事项

- 请确保你的网络连接正常，以便从Wallhaven网站获取壁纸图片。
- 脚本会将图片保存到指定的本地文件夹，确保你有权限在该文件夹下写入文件。
- 如果需要发送通知，请确保你的系统环境支持通知功能，并且配置了通知库。

## 依赖

- [requests](https://pypi.org/project/requests/): 用于发起 HTTP 请求
- [parsel](https://pypi.org/project/parsel/): 用于进行 HTML 解析

## License

这个项目采用 MIT 许可证。详细信息请参阅 [LICENSE](LICENSE) 文件。
