# 职场嘴替 - 飞书Bot MVP

帮你在职场沟通中找到自己的"嘴替"，不再因为不会回消息而内耗。

## 功能特性

- 🧪 **22道趣味测试** - 测出你的职场人设
- 🎭 **6种鲜明人设** - 和事佬·沙僧、整顿侠·半泽直树、太极王·甄嬛、通透派·余华、捧哏王·岳云鹏、毒舌君·小S
- 💬 **三档回复** - 温和版/标准版/火力版
- 🆘 **请外援** - 临时呼叫其他人设
- 📝 **多种输入** - 文字/截图/转发对话

## 快速开始

### 1. 安装依赖

```bash
cd zhichang-zuiti
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入你的配置
```

### 3. 启动服务

```bash
python -m app.main
```

### 4. 配置飞书Bot

1. 在飞书开放平台创建机器人应用
2. 配置事件订阅地址：`http://你的域名/webhook`
3. 配置卡片回调地址：`http://你的域名/callback`
4. 订阅消息事件：`im.message.receive_v1`

### 5. 本地调试（使用ngrok）

```bash
ngrok http 8080
# 将ngrok提供的地址配置到飞书开放平台
```

## 项目结构

```
zhichang-zuiti/
├── app/
│   ├── main.py              # 主入口
│   ├── config.py            # 配置管理
│   ├── models/
│   │   └── user.py          # 数据模型
│   ├── services/
│   │   ├── database.py      # 数据库服务
│   │   └── llm.py           # LLM服务
│   ├── handlers/
│   │   └── feishu.py        # 飞书事件处理
│   ├── cards/
│   │   └── builder.py       # 消息卡片构建
│   ├── quiz/
│   │   └── questions.py     # 测试题数据
│   └── prompts/             # 人设Prompt文件
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## 六大人设

| 人设 | 代表人物 | 核心策略 |
|------|----------|----------|
| 🕊️ 和事佬 | 沙僧 | 附和即安全，谁也不得罪 |
| 🔥 整顿侠 | 半泽直树 | 以牙还牙，加倍奉还 |
| 🌀 太极王 | 甄嬛 | 话术即权力，示弱即布局 |
| 🧊 通透派 | 余华 | 幽默是最后的武器 |
| 🎭 捧哏王 | 岳云鹏 | 糊弄即智慧，自嘲即铠甲 |
| 💀 毒舌君 | 小S | 犀利即尊重，吐槽即正义 |

## API文档

启动后访问：`http://localhost:8080/docs`

## 相关文档

- [PRD文档](../职场嘴替-PRD-v2.md)
- [交互设计](../飞书Bot交互设计-v2.md)
- [测试题设计](../职场人格测试设计_v4.md)

## License

MIT
