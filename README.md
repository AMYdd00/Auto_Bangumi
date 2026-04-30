<p align="center">
    <img src="docs/public/image/icons/light-icon.svg#gh-light-mode-only" width=50%/ alt="">
    <img src="docs/public/image/icons/dark-icon.svg#gh-dark-mode-only" width=50%/ alt="">
</p>
<p align="center">
    <img title="version" src="https://img.shields.io/badge/version-3.2.6--amy-blue" alt="">
    <img title="python version" src="https://img.shields.io/badge/python-3.13-blue" alt="">
    <img title="platform" src="https://img.shields.io/badge/platform-docker%20%7C%20linux-lightgrey" alt="">
</p>

<p align="center">
  <strong>中文</strong> | <a href="README.en.md">English</a>
</p>

# AutoBangumi — Amy 自建修复版

> 基于 [EstrellaXD/Auto_Bangumi](https://github.com/EstrellaXD/Auto_Bangumi) 的自建维护分支。
> 修复了 3.2.x 版本中聚合 RSS 崩溃等问题，保持上游功能同步。

本项目是基于 RSS 的全自动追番整理下载工具。只需在 [Mikan Project](https://mikanani.me) 等网站订阅番剧，即可全自动追番。整理完成的文件命名规范，可直接被 [Plex](https://plex.tv)、[Jellyfin](https://jellyfin.org) 等媒体库识别，无需二次刮削。

---

## ✨ 特性

### 核心功能

| 功能 | 说明 |
|------|------|
| 🤖 全自动追番 | 一次配置，持续使用，无需手动干预 |
| 📡 聚合 RSS | 支持 Mikan 等多站点聚合 RSS 订阅，自动解析新番 |
| 🗂️ 智能整理 | 自动按番剧名/季度分目录，媒体库直接识别 |
| 🏷️ 自动重命名 | 去除字幕组标识，统一命名格式（`S01E01`） |
| 🔍 智能匹配 | 根据标题、别名、字幕组多渠道匹配，减少漏番 |
| 📺 TMDB 集成 | 自动获取番剧元数据，生成 TMDB 兼容格式 |
| 📅 日历视图 | 按播出日期查看订阅，集成 Bangumi 放送时间表 |
| 🔐 Passkey 登录 | 支持 WebAuthn 指纹/面容无密码登录 |
| 🧩 搜索源插件 | 支持 Mikan / DMHY / Nyaa 多种搜索源 |
| 📱 响应式 UI | PC / 移动端自适应，深色/浅色主题 |
| 🌐 国际化 | 中文 / English 双语界面 |

### 🔧 本分支修复内容

| 修复项 | 文件 | 说明 |
|--------|------|------|
| 🐛 聚合 RSS `KeyError` 崩溃 | `database/bangumi.py` | `match_list` 中 `title_index` 为空时，`re.compile("")` 匹配任意字符串导致 `KeyError`，加保护提前返回 |
| 🐛 空过滤器误杀全部种子 | `network/request_contents.py` | `filter` 配置为空列表时，`"".join()` 得空字符串，`re.search("", x)` 永远匹配 → 所有种子被过滤 |
| 🐛 `entrypoint.sh` CRLF 换行 | `entrypoint.sh` | Windows 下 PowerShell 写入 CRLF，Linux 下 `#!/bin/bash\r` 找不到解释器，容器启动失败 |
| 🚪 默认端口 | `const.py` / `Dockerfile` | `7892` → `37892`，避免端口冲突 |
| 📌 版本号 | `__version__.py` | 添加版本文件，避免 DEV 模式跳转 FastAPI docs |

---

## 🚀 一键部署（Docker）

### 方式一：Docker Compose（推荐）

创建 `docker-compose.yml`：

```yaml
services:
  Amy-AutoBangumi:
    image: "ghcr.io/AMYdd00/auto_bangumi:latest"
    container_name: Amy-AutoBangumi
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - "37892:37892"
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
      - PGID=1000
      - PUID=1000
      - UMASK=022
```

启动：

```bash
docker compose up -d
```

### 方式二：Docker CLI

```bash
docker run -d \
  --name Amy-AutoBangumi \
  -p 37892:37892 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  ghcr.io/AMYdd00/auto_bangumi:latest
```

### 方式三：从源码构建

```bash
# 克隆仓库
git clone https://github.com/AMYdd00/Auto_Bangumi.git
cd Auto_Bangumi

# 编译前端
cd webui && pnpm install && pnpm run build && cd ..

# 构建镜像
docker build -t autobangumi:custom .

# 运行
docker run -d \
  --name Amy-AutoBangumi \
  -p 37892:37892 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  autobangumi:custom
```

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `AB_WEBUI_PORT` | `37892` | WebUI 端口 |
| `AB_INTERVAL_TIME` | `900` | RSS 刷新间隔（秒） |
| `AB_RENAME_FREQ` | `60` | 重命名检查间隔（秒） |
| `AB_DOWNLOADER_HOST` | `172.17.0.1:8080` | 下载器地址 |
| `AB_DOWNLOADER_USERNAME` | `admin` | 下载器用户名 |
| `AB_DOWNLOADER_PASSWORD` | `adminadmin` | 下载器密码 |
| `AB_DOWNLOAD_PATH` | `/downloads/Bangumi` | 下载路径 |
| `AB_RSS_COLLECTOR` | `true` | 启用 RSS 收集 |
| `AB_NOT_CONTAIN` | `720\|\\d+-\\d+` | RSS 排除过滤器（\| 分隔） |
| `AB_LANGUAGE` | `zh` | 语言（zh/en） |
| `AB_RENAME` | `true` | 启用重命名 |
| `AB_METHOD` | `pn` | 重命名方法 |
| `AB_GROUP_TAG` | `false` | 文件夹保留字幕组标签 |
| `AB_EP_COMPLETE` | `false` | 季中追番补全 |
| `AB_DEBUG_MODE` | `false` | 调试模式 |
| `TZ` | `Asia/Shanghai` | 时区 |
| `PUID` / `PGID` | `1000` | 运行用户 UID/GID |
| `UMASK` | `022` | 文件权限掩码 |

---

## 📖 快速开始

### 1. 首次访问

启动容器后访问 **http://localhost:37892**，进入初始化向导。

### 2. 配置下载器

填入你的 qBittorrent 地址、用户名、密码。容器内默认使用 `172.17.0.1:8080` 访问宿主机 qBittorrent。

### 3. 添加 RSS 订阅

在「RSS」页面添加 Mikan 订阅链接：
- **单番 RSS**：Mikan 番剧页的 RSS 链接
- **聚合 RSS**：`https://mikanani.me/RSS/MyBangumi?token=你的Token`
  - 添加时**务必开启「聚合」开关**（默认为关）

### 4. 自动追番

程序会自动刷新 RSS → 匹配已有规则 → 下载新种子 → 重命名整理。全程无需手动干预。

### 5. 媒体库刮削

下载目录映射到 Plex/Jellyfin 的媒体库路径，即可自动刮削。

---

## 🖼️ 界面预览

| 页面 | 预览 |
|------|------|
| 番剧列表 | ![](docs/public/image/feature/bangumi-list.png) |
| 日历视图 | ![](docs/public/image/feature/calendar-view.png) |
| RSS 管理 | ![](docs/public/image/feature/rss-manage.png) |
| 下载器管理 | ![](docs/public/image/feature/downloader.png) |
| 设置面板 | ![](docs/public/image/feature/settings.png) |

---

## 🗂️ 文件整理格式

```
Bangumi
├── bangumi_A_title
│   ├── Season 1
│   │   ├── A S01E01.mp4
│   │   ├── A S01E02.mp4
│   │   └── ...
│   └── Season 2
│       ├── A S02E01.mp4
│       └── ...
├── bangumi_B_title
│   └── Season 1
│       ├── B S01E01.mp4
│       └── ...
```

重命名示例：
```
[Lilith-Raws] Kakkou no Iinazuke - 07 [Baha][WEB-DL][1080p][AVC AAC][CHT][MP4].mp4
→ Kakkou no Iinazuke S01E07.mp4
```

---

## ⚙️ 支持的下载器

- **qBittorrent**（WebUI）

---

## 🧪 更新日志

详见 [CHANGELOG.md](CHANGELOG.md)

### 本分支修复版本 3.2.6-amy

- 🐛 修复 `match_list` 空 `title_index` 导致的 KeyError 崩溃
- 🐛 修复 RSS 过滤器为空时所有种子被误过滤的问题
- 🐛 修复 `entrypoint.sh` CRLF 换行导致容器启动失败
- 🚪 默认端口改为 `37892`
- 📌 添加 `__version__.py` 版本文件，修复 DEV 模式跳转问题

---

## 📄 许可证

[MIT License](LICENSE)

---

<p align="center">
  <a href="https://github.com/AMYdd00/Auto_Bangumi/issues">提交 Issue</a> ·
  <a href="https://github.com/AMYdd00/Auto_Bangumi/pulls">提交 PR</a>
</p>
