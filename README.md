# AI早报生成系统

## 项目概述
本系统是一个自动化AI早报生成工具，能够：
1. 自动抓取最新AI相关新闻
2. 使用AI模型生成新闻摘要
3. 生成格式化的Markdown早报
4. 通过邮件或企业微信发送早报
5. 保存原始文章的标题、正文和链接到Markdown文件

## 主要功能
- **新闻抓取**：从AIBase网站抓取最新AI相关新闻
- **摘要生成**：使用智谱AI模型生成新闻摘要
- **早报生成**：将摘要整理成格式化的Markdown早报
- **多渠道发送**：支持邮件和企业微信发送
- **原始文章保存**：自动保存原始文章内容，便于追溯和审核

## 安装指南

### 1. 克隆项目
```bash
git clone https://github.com/StanleyChanH/AI-NewsGlance.git
cd AI-NewsGlance
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. Ubuntu系统依赖安装
```bash
# 以下步骤仅适用于Ubuntu系统
sudo apt-get install -y \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libasound2 \
    libatspi2.0-0
```

### 4. 安装Playwright浏览器
```bash
playwright install
```

### 5. 配置环境
复制配置文件模板：
```bash
cp config/config.example.yaml config/config.yaml
```
根据实际情况修改config.yaml中的配置项

## 发送功能配置

### 邮件发送配置
```yaml
smtp:
  enabled: true
  host: "smtp.qq.com"
  port: 465
  user: "your_email@qq.com"
  password: "your_email_password"
  from: "your_email@qq.com"
  to: "recipient@example.com"
```

### 企业微信机器人配置
```yaml
wechat_work:
  enabled: true
  webhook_url: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_key"
```

## 使用示例

### 运行程序
```bash
python src/main.py
```

### 查看输出
- 早报文件：output/daily_report.md
- 原始文章：output/raw_articles/

## 代码质量保障
项目采用以下工具保证代码质量：
- **代码格式化**: Black, isort
- **静态检查**: flake8, mypy

## 项目结构
```
.
├── config/               # 配置文件
│   ├── config.yaml       # 主配置文件
│   ├── config.example.yaml # 配置示例
│   └── logging_config.yaml # 日志配置
├── src/                  # 源代码
│   ├── crawler/          # 新闻爬取模块
│   ├── generator/        # 早报生成模块
│   ├── sender/           # 早报发送模块
│   ├── summarizer/       # 摘要生成模块
│   └── main.py           # 主程序
├── output/               # 输出目录
│   ├── raw_articles/     # 原始文章Markdown文件
├── .github/              # GitHub配置
│   ├── ISSUE_TEMPLATE/   # Issue模板
│   └── PULL_REQUEST_TEMPLATE.md # PR模板
├── .gitignore            # Git忽略规则
├── .flake8               # flake8配置
├── .mypy.ini             # mypy配置
├── requirements.txt      # Python依赖
├── README.md             # 项目说明
└── CONTRIBUTING.md       # 贡献指南
```

## 贡献指南
请阅读[CONTRIBUTING.md](CONTRIBUTING.md)了解如何为项目做贡献

## 开发规范
1. 遵循PEP 8代码风格
2. 使用类型注解
3. 提交信息遵循Conventional Commits规范

## 许可证
[MIT License](LICENSE)
