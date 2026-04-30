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
| 🔔 多通道通知 | 支持 Telegram / Discord / OneBot v11(QQ) / Bark / ServerChan / 企业微信 / Gotify / Pushover / Webhook |
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

启动容器后访问 http://localhost:37892，进入初始化向导。

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



## 🔔 通知设置

AutoBangumi 支持多种通知渠道，番剧更新时自动推送。你可以在 WebUI **设置 → 通知设置** 中配置。

### 开启通知

1. 进入 **设置 → 通知设置**
2. 打开 **启用** 开关
3. 点击 **添加通知服务**，选择需要的推送渠道

### 支持的推送渠道

| 渠道 | 类型值 | 说明 |
|------|--------|------|
| Telegram | `telegram` | Telegram Bot 推送，需 Bot Token 和 Chat ID |
| Discord | `discord` | Discord Webhook，需 Webhook URL |
| **OneBot v11 (QQ)** | `onebot` | 通过 OneBot 协议的 QQ 机器人推送 |
| Bark | `bark` | iOS 推送，需 Device Key |
| Server Chan | `server-chan` | 微信推送，需 SendKey |
| 企业微信 | `wecom` | 企业微信机器人，需 Webhook URL |
| Gotify | `gotify` | 自托管推送服务 |
| Pushover | `pushover` | 跨平台推送 |
| Webhook | `webhook` | 通用 Webhook，支持自定义 JSON 模板 |

---

### OneBot v11 (QQ) 详细配置

适用于 **LLOneBot**、**go-cqhttp**、**Lagrange.OneBot** 等 OneBot v11 兼容的 QQ 机器人。

#### 前置准备

你需要先部署一个 OneBot v11 兼容的 QQ 机器人，并确保其 HTTP API 服务正常运行。

以 **LLOneBot** 为例：

1. 在 LLOneBot 设置中启用 **HTTP 服务端**
2. 设置监听地址和端口（默认 `0.0.0.0:5700`）
3. （可选）设置 `access_token` 用于鉴权
4. 确保 QQ 号已登录且在线

#### AutoBangumi 配置

进入 **设置 → 通知设置**，添加通知服务，选择 **OneBot v11**，填写以下字段：

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| **API URL** | ✅ | OneBot HTTP API 地址 | `http://192.168.1.100:5700` |
| **Access Token** | ❌ | 与 LLOneBot 设置的 `access_token` 一致 | 留空 |
| **Target ID** | ✅ | **私聊**：填 QQ 号；**群聊**：填群号 | `123456789` |
| **Message Type** | ✅ | `private` = 私聊，`group` = 群聊 | `private` 或 `group` |

> **💡 Message Type 选择：**
> - 想给自己发通知 → 选 `private`，Target ID 填你的 **QQ 号**
> - 想发到群里 → 选 `group`，Target ID 填 **群号**

#### 番剧更新通知效果

当有新番更新时，QQ 会收到类似以下的消息：

```text
番剧名称：葬送的芙莉莲
季度：第1季
更新集数：第12集
```

如果有番剧封面图，会附带在文字上方一起发送。

#### 测试通知

配置完成后，点击通知列表右侧的 ▶ **测试** 按钮，机器人会发送一条消息到目标：

```text
AutoBangumi 通知测试成功！
Notification test successful!
```

---

### Telegram 配置

1. 在 Telegram 搜索 **@BotFather**，创建 Bot 获取 Token
2. 搜索你的 Bot，发一条消息
3. 访问 `https://api.telegram.org/bot<Token>/getUpdates` 获取 Chat ID
4. 在 AutoBangumi 通知设置中添加 Telegram，填入 Token 和 Chat ID

### Discord 配置

1. 在 Discord 频道设置 → 整合 → Webhook，创建 Webhook
2. 复制 Webhook URL
3. 在 AutoBangumi 通知设置中添加 Discord，填入 Webhook URL

### Server Chan 配置

1. 在 [Server酱](https://sct.ftqq.com/) 注册并创建 Key
2. 在 AutoBangumi 通知设置中添加 Server Chan，填入 SendKey

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
