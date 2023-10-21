# Pixiv 收藏图片下载器

这是一个用于从 Pixiv 网站下载用户收藏的图片的简单 Node.js 脚本。该脚本使用 Pixiv API 获取用户的收藏列表，并下载收藏中的图片到本地文件夹。在下载图片之前，脚本会检查本地文件夹中是否已经存在相同的图片，如果存在则跳过下载。

原作者项目链接：https://github.com/qiangmouren/pixiv-favorite-download

## 如何使用

### 1. 安装依赖

在使用之前，请确保你已经安装了 Node.js。然后，在项目文件夹中执行以下命令安装依赖：

```bash
npm install
```

### 2. 配置

在 `config.json` 文件中配置你的 Pixiv 登录信息和下载选项：

```json
{
    "cookie": "填写你的P站Cookie",
    "output": "D:/test/",
    "proxy": {
        "$mark": "如果不使用代理host请留空",
        "host": "127.0.0.1",
        "port": 7890,
        "protocol": null,
        "auth": {
            "$mark": "代理认证",
            "username": null,
            "password": null
        }
    }
}
```

### 3. 运行脚本

配置完成后，运行以下命令启动下载器：

```bash
node index.js
```

脚本将会开始下载你的 Pixiv 收藏夹中的图片到指定的文件夹。

## 注意事项

- 请确保你的 Pixiv 账号具有足够的权限来访问收藏夹中的图片。
- 脚本在下载图片之前会检查本地文件夹中是否已经存在相同的图片，如果存在则会跳过下载。

## 特殊字符处理

脚本会将图片文件名中的特殊字符替换为下划线，以确保文件名的合法性。

## 依赖

- [axios](https://www.npmjs.com/package/axios): 用于发起 HTTP 请求
- [p-queue](https://www.npmjs.com/package/p-queue): 用于管理并发请求，防止过多的请求同时发出

## License

MIT License
