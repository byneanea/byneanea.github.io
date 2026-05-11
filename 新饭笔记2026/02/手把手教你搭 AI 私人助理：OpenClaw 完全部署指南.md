---
总结:
---
原创 新饭的日常笔记 *2026年2月26日 11:33*

\> 综合 20+ 篇技术文档交叉验证 · 版本：OpenClaw 2026.2.x

\## 先说结论

OpenClaw 是什么？一句话：\*\*装在你自己机器上、24 小时不停的 AI 助手\*\*。

它不是网页 AI，不是月订阅服务，是真正跑在你设备里的"私人 AI 员工"——你发一句话，它帮你浏览网页、整理文件、写代码、定时执行任务，还能接入微信、飞书、钉钉、Telegram。

两周 GitHub 15 万 Star，史上增长最快开源项目之一。

\## 一、它到底由哪几部分组成？

OpenClaw 有四个核心模块，搞清楚它们，部署就不懵了。

| 模块 | 干什么的 |

|------|---------|

| \*\*核心引擎\*\* | AI 大脑，负责理解你的指令、调度任务，需要接入大模型 API |

| \*\*Skills 技能库\*\* | 像插件一样的功能包，目前有 1715+ 个，覆盖 31 个分类 |

| \*\*ClawHub\*\* | Skills 的应用市场，一键搜索、安装、更新技能 |

| \*\*Gateway 网关\*\* | 负责和消息平台（飞书/Telegram 等）通信，默认端口 18789 |

\*\*类比理解\*\*：核心引擎是大脑，Skills 是双手，Gateway 是嘴巴，ClawHub 是技能学校。

\## 二、部署方式怎么选？

目前有 8 种主流方案，按需选择：

| 方案 | 难度 | 费用 | 最适合谁 | 耗时 |

|------|------|------|---------|------|

| 一键脚本 | ⭐ 最简单 | 免费（只付 API） | 快速体验 | 5 分钟 |

| npm 安装 | ⭐⭐ | 免费（只付 API） | 开发者 | 5 分钟 |

| Mac Mini 本地 | ⭐⭐⭐ | 硬件 800~2000 美元 | 极客 · 零月租 | 30 分钟 |

| Docker 容器 | ⭐⭐⭐ | 免费（只付 API） | 安全优先 | 15 分钟 |

| \*\*阿里云轻量\*\* | ⭐⭐ | \*\*68 元/年起\*\* | 国内用户首选 | 10 分钟 |

| \*\*腾讯云 Lighthouse\*\* | ⭐⭐ | \*\*99 元/年起\*\* | 国内用户 | 10 分钟 |

| DigitalOcean | ⭐ | 5~12 美元/月 | 海外用户 | 5 分钟 |

| Railway/Render | ⭐⭐ | 0~7 美元/月 | 开发者云端 | 10 分钟 |

\> \*\*最低硬件要求\*\*：2 核 CPU · 2GB 内存 · 10GB 磁盘 · Node.js ≥ 22

\*\*选方案建议\*\*：

\- 国内用户 → 阿里云轻量（性价比最高）

\- 有 Mac Mini 闲置或重隐私 → 本地部署

\- 只是试试 → 一键脚本

\## 三、四种方案手把手教学

\### ▎方案一：本地一键安装（5 分钟搞定）

适合：Mac / Linux / Windows（需先装好 WSL2）

\*\*第一步：安装\*\*

\`\`\`bash

\# 推荐：官方一键脚本

curl -fsSL https://openclaw.ai/install.sh | bash

\`\`\`

或者用 npm：

\`\`\`bash

npm install -g openclaw@latest

\`\`\`

\*\*第二步：启动配置向导\*\*

\`\`\`bash

openclaw onboard --install-daemon

\`\`\`

向导会一步步问你：

1\. 选哪个 AI 模型（Claude / GPT / 本地 Ollama）

2\. 填入 API Key

3\. 选消息渠道（Telegram / 飞书等）

4\. 安装后台守护进程（让它后台一直跑）

\### ▎方案二：Mac Mini 本地部署（零月租，极客方案）

\*\*硬件怎么选？\*\*

| 预算 | 推荐型号 | 可运行模型 |

|------|---------|----------|

| ~800 美元 | Mac Mini M4（24GB） | 7B / 13B 模型 |

| ~2000 美元 | Mac Mini M4 Pro（64GB） | 32B 模型，如 Qwen2.5-Coder-32B |

\*\*装本地 AI 模型（免费，零 API 费用）\*\*

\`\`\`bash

\# 第一步：安装 Ollama

brew install ollama

ollama serve

\# 第二步：下载模型（约 20GB，耐心等待）

ollama pull qwen2.5-coder:32b

\`\`\`

\*\*配置 OpenClaw 使用本地模型\*\*，编辑 \`~/.openclaw/openclaw.json\`：

\`\`\`json

{

"agent": {

"model": "ollama/qwen2.5-coder:32b",

"providers": {

"ollama": { "baseUrl": "http://localhost:11434/v1" }

}

}

}

\`\`\`

\*\*让 Mac Mini 24 小时不睡眠\*\*

\`\`\`bash

sudo pmset -a sleep 0 displaysleep 0 disksleep 0

\`\`\`

\### ▎方案三：阿里云轻量服务器（国内用户首选，68 元/年）

\*\*为什么推荐？\*\*

\- 有官方预装镜像，买了直接能用

\- 国内网络访问稳定

\- 已预置 Node.js 22 + Python 3.9，省去环境配置

\*\*费用\*\*：68 元/年（2 核 2G · 200Mbps · 40GB 磁盘）

\*\*第一步：创建服务器\*\*

\> 阿里云控制台 → 轻量应用服务器 → 应用镜像 → 搜索「OpenClaw」→ 选官方镜像 v2026.2.12 → 购买

\*\*第二步：放通端口（必做！）\*\*

\> 实例详情页 → 防火墙 → 一键放通

自动放行：22（SSH）· 80（网页）· \*\*18789（OpenClaw 控制面板）\*\*

\*\*第三步：配置百炼 API Key\*\*

去 \[阿里云百炼控制台\](https://bailian.console.aliyun.com) → 密钥管理 → 创建 API-Key，Key 只显示一次，务必保存好。

SSH 连接服务器后，编辑配置文件：

\`\`\`bash

nano ~/.openclaw/openclaw.json

\`\`\`

填入以下内容：

\`\`\`json

{

"model": {

"provider": "dashscope",

"dashscope": {

"apiKey": "你的AccessKey Secret",

"accessKeyId": "你的AccessKey ID",

"baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",

"defaultModel": "qwen-max"

}

}

}

\`\`\`

\*\*第四步：加速 Skills 安装（解决下载慢）\*\*

\`\`\`bash

openclaw config set registry.mirror "https://clawhub-mirror.aliyuncs.com"

\`\`\`

\*\*第五步：打开控制面板\*\*

\`\`\`bash

\# 查看你的访问 Token

cat ~/.openclaw/openclaw.json | grep token

\`\`\`

浏览器访问：

\`\`\`

http://你的服务器公网IP:18789/?token=查到的token值

\`\`\`

\### ▎方案四：腾讯云 Lighthouse（99 元/年）

\*\*费用\*\*：99 元/年（2 核 2G · 50Mbps · 50GB 磁盘）

\*\*亮点\*\*：原生支持 QQ / 企业微信 / 钉钉 / 飞书

\*\*启动向导\*\*

\`\`\`bash

openclaw onboard

\# 选择 QuickStart 模式，最快部署

\`\`\`

\*\*配置公网访问\*\*，编辑 \`~/.openclaw/openclaw.json\`：

\`\`\`json

{

"gateway": {

"mode": "remote",

"bind": "lan"

}

}

\`\`\`

\*\*接入飞书（四步走）\*\*

1\. 飞书应用管理后台 → 添加应用能力 → 选择「机器人」

2\. 开通「消息与群组」权限

3\. 配置事件和回调 → 使用长连接 → 添加消息事件

4\. 执行 \`openclaw configure\` → 选 Channels → 填入飞书 App ID 和 Secret

\## 四、接哪个 AI 模型？

| 模型 | 特点 | 适合场景 |

|------|------|---------|

| \*\*Kimi（月之暗面）\*\* | 中文强，长上下文 | 日常中文对话 |

| \*\*阿里云百炼 Qwen\*\* | 国内访问快，成本低 | 国内部署首选 |

| \*\*Claude 4 Sonnet\*\* | 代码能力顶级 | 写代码、分析 |

| \*\*GPT-4.1\*\* | 通用能力最强 | 综合任务 |

| \*\*本地 Ollama\*\* | 零费用，数据不出门 | 隐私优先 |

\*\*Kimi 配置示例\*\*，编辑 \`~/.openclaw/openclaw.json\`：

\`\`\`json

{

"agents": {

"defaults": {

"model": { "primary": "moonshot/kimi-k2.5" }

}

},

"models": {

"mode": "merge",

"providers": {

"moonshot": {

"baseUrl": "https://api.moonshot.cn/v1",

"apiKey": "你的Kimi API Key",

"api": "openai-completions",

"models": \[{ "id": "kimi-k2.5", "name": "Kimi K2.5" }\]

},

"kimi-code": {

"baseUrl": "https://api.kimi.com/coding/v1",

"apiKey": "你的Kimi Code API Key",

"api": "openai-completions",

"models": \[{ "id": "kimi-for-coding", "name": "Kimi For Coding" }\]

}

}

}

}

\`\`\`

\## 五、烧钱警报：Token 费用怎么控制？

OpenClaw 软件本身免费，\*\*你的真实成本来自 AI 模型的 API 调用费\*\*。

\*\*真实翻车案例\*\*：

\- 有人因为没关心跳检测（每 30 分钟问一次 AI"你在吗？"），一晚上烧掉 \*\*18.75 美元\*\*

\- 有人单日待机消耗 \*\*5000 万 Token\*\*（约 11 美元）

\*\*成本从哪来？\*\*

| 来源 | 占比 |

|------|------|

| 对话历史越堆越长 | 40~50% |

| Skills 执行结果存储 | 20~30% |

| 系统提示词 | 10~15% |

| 定时心跳任务 | 持续消耗 |\*\*四招省钱（实测从 150 美元/月降到 35 美元/月）\*\*

| 方法 | 怎么做 |

|------|-------|

| 定期重置对话 | 清理历史上下文 |

| 按任务选模型 | 简单问题用 Gemini Flash，复杂任务才用 Claude |

| 限制上下文长度 | 设置 max\_tokens 上限 |

| 简单任务走本地模型 | Ollama 不花 API 钱 |

\## 六、安全红线，必须知道

\*\*已发生的真实安全事故\*\*：

\- \*\*CVE-2026-25253\*\*（危险等级 8.8/10）：跨站劫持可导致远程控制你的机器，已在 v2026.1.29 修复

\- \*\*923 个实例裸奔公网\*\*：安全研究员扫描发现近千台服务器零密码暴露，API Key 直接被盗

\- \*\*假 VS Code 插件\*\*："ClawdBot Agent" 插件被植入木马

\- \*\*诈骗 Skills\*\*：通过钓鱼技能骗走 1600 万美元加密货币

\*\*怎么保护自己？5 条必做\*\*：

1\. \*\*保持最新版本\*\*（最重要，修复 CVE 漏洞）

2\. \*\*开启 Token 认证\*\*（禁止 \`auth: "none"\` 模式）

3\. \*\*开启 Docker 沙箱隔离\*\*（只读文件系统 + 非 root 运行）

4\. \*\*在 API 平台设置月度支出上限\*\*（防止超支）

5\. \*\*定期运行安全审计\*\*：

\`\`\`bash

openclaw security audit --deep

\`\`\`

\## 七、遇到问题怎么快速排查？

| 问题现象 | 可能原因 | 解决方法 |

|---------|---------|---------|

| Skills 安装一直转圈 | 从境外下载太慢 | 配置阿里云镜像加速 |

| 打不开控制面板 | 防火墙没放行 | 检查 18789 端口是否开放 |

| 调用 AI 报错 | API Key 填错 | 核查 baseUrl 和 apiKey |

| 飞书收不到回复 | 应用权限缺失 | 检查飞书应用权限配置 |

| 本地模型响应很慢 | 内存不够用 | 换更小的模型，或升级内存 |

\## 参考资源

\- 官方文档：https://docs.openclaw.ai

\- GitHub 开源仓库：https://github.com/openclaw/openclaw

\- ClawHub 技能市场：https://clawhub.com

\- 阿里云部署专题：https://www.aliyun.com/activity/ecs/clawdbot

\---> \*\*免责声明\*\*：本文基于公开技术文档整理，部署前请仔细阅读官方安全指南，自行承担使用风险。

\> 版本：2026 年 2 月 | 整理：Iceman

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

  

继续滑动看下一个

新饭的日常笔记

向上滑动看下一个

## 链接

- ↔ [[3月19日 肉身效能与 Impossible 实验：纳瓦尔的 AI 时代生存范式]]
- ↔ [[3月23日 AI时代，普通人撕碎的6行诗]]
- ↔ [[20260211_2月11日AI个人画像与性格分析]]
- ↔ [[3月2日 文明新契约：“人类与AI的三法则”，从阿西莫夫谈起]]
- ↔ [[2月18日 读“AI文明前史”—“涌现”]]
- ↔ [[2月19日 AI前线风云人物演义：奥特曼VS梁文锋]]
- ↔ [[2月22日 面对咄咄逼人的AI，人类的生存空间在哪里？]]
- ↔ [[2月23日 谁是下一个安德？——超级平台阴影下的“人类当量”终结者]]
