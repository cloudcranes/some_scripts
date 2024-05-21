# AList strm File Generator

这是一个Python脚本，旨在扫描特定目录并依据指定的视频文件类型（例如 `.mp4`, `.mkv`, `.avi`, `.wmv`）生成对应的 `.strm` 文件。这些 `.strm` 文件内嵌指向 [AList](https://alist.nn.ci/) 服务器上存储文件的直接链接，便于诸如 Kodi 之类的媒体中心软件直接播放。

## 环境配置

本脚本依赖以下环境变量进行配置：

- **`ALIST_SCAN_PATH`**: 扫描起始目录路径，默认为 `/`。
- **`ALIST_SERVER_URL`**: AList 服务器的基础 URL，默认为 `http://127.0.0.1:5244`。
- **`ALIST_SERVER_TOKEN`**: 访问 AList 服务器所需的认证令牌。
- **`OUTPUT_DIR`**: 输出 `.strm` 文件的目标目录，默认为 `./link`。
- **`WEBDAV_URL`**: 可选项，WebDAV 服务的 URL。

未明确配置时，脚本将以默认值执行。

## 核心功能

1. **异步获取文件链接** - 使用 `async_get_file_link` 函数通过 AList API 获取单个文件的直接下载链接。
2. **目录内容检索** - `async_fetch_directory_content` 函数递归地获取目录下的所有文件及子目录信息。
3. **生成 `.strm` 文件** - `async_generate_strm_file_if_not_exists` 确保每个支持的视频文件都有一个对应的 `.strm` 文件，避免重复生成。
4. **目录遍历处理** - `async_process_directory` 作为主逻辑，负责递归处理目录结构，确保所有符合条件的文件都被处理。

## 快速启动

1. **安装依赖**：确保已安装 `aiohttp`, `asyncio`, `pathlib` 等必要库。
2. **配置环境**：根据需要设置环境变量。
3. **执行脚本**：在命令行中运行 `python main.py`。

脚本运行过程中，详细日志会记录到控制台，展示扫描进度、文件处理情况及总耗时。

## 注意事项

- 确认 AList 服务器的 URL、访问令牌及目标扫描目录正确无误。
- 输出目录将在运行前自动创建，如不存在。

## 许可与贡献

本项目遵循 [MIT License](LICENSE)。

## 作者信息

[[cloudcranes](https://github.com/cloudcranes)]
