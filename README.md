# AI早报生成项目
# AI早报生成系统

## 项目概述
本系统是一个自动化AI早报生成工具，能够：
1. 自动抓取最新AI相关新闻
2. 使用AI模型生成新闻摘要
3. 生成格式化的Markdown早报
4. 通过邮件或企业微信发送早报

## 安装指南

### 1. 克隆项目
```bash
git clone https://github.com/your-repo/ai-news.git
cd ai-news
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境
复制配置文件模板：
```bash
cp config/config.example.yaml config/config.yaml
```
根据实际情况修改config.yaml中的配置项

## 配置说明

### 主要配置项
- `crawler`: 爬虫配置
  - `sources`: 新闻源列表
- `generator`: 早报生成配置
  - `output_path`: 早报输出路径
- `sender`: 发送配置
  - `smtp`: 邮件发送配置
  - `wechat_work`: 企业微信配置

## 使用方法

### 运行项目
```bash
python src/main.py
```

### 定时任务
可以使用crontab设置每日定时任务：
```bash
0 8 * * * /path/to/python /path/to/project/src/main.py
```

## 项目结构
```
.
├── config/               # 配置文件
├── src/                  # 源代码
│   ├── crawler/          # 新闻爬取模块
│   ├── generator/        # 早报生成模块
│   ├── sender/           # 早报发送模块
│   ├── summarizer/       # 摘要生成模块
│   └── main.py           # 主程序
├── output/               # 输出目录
└── README.md             # 项目说明
```

## 贡献指南
欢迎提交Issue和PR

## 项目简介
基于Crawl4ai和GLM模型实现的AI早报自动生成系统，能够自动抓取新闻网站内容并生成每日早报。

## 目录结构
```
.
├── src/                  # 源代码目录
│   ├── crawler/          # 爬虫模块
│   ├── summarizer/       # 摘要生成模块  
│   ├── generator/        # 早报生成模块
│   └── sender/           # 结果发送模块
├── config/               # 配置文件目录
├── requirements.txt      # 依赖文件
└── README.md             # 项目说明
```

## 快速开始
1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 安装Playwright浏览器
```bash
playwright install
```

3. 配置项目
复制config/config.example.yaml为config/config.yaml，并根据实际情况修改配置项：

```bash
cp config/config.example.yaml config/config.yaml
```

配置文件示例：
```yaml
# 爬虫配置
crawler:
  base_url: "https://www.aibase.com/zh/news/"  # 爬取的基础URL
  max_articles: 10  # 最大爬取文章数量
  timeout: 30  # 请求超时时间（秒）
  user_agent: "Mozilla/5.0"  # 请求头User-Agent

# 智谱AI配置
zhipuai:
  api_key: "your_api_key_here"  # 智谱API密钥
  base_url: "https://open.bigmodel.cn/api/paas/v4"  # API基础URL
  model: "glm-4"  # 使用的模型
  temperature: 0.7  # 生成温度
  max_tokens: 1000  # 最大token数

# 早报生成配置
generator:
  title: "AI早报"  # 早报标题
  max_summaries: 5  # 最大摘要数量
  output_dir: "output"  # 输出目录
  output_file: "daily_report.md"  # 输出文件名

# 发送配置
sender:
  enabled: true  # 是否启用发送功能
  type: "wechat_work"  # 发送方式：wechat_work | email
  
  # 企业微信机器人配置
  wechat_work:
    enabled: true
    webhook_url: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_key_here"
  
  # SMTP邮件配置
  smtp:
    enabled: false
    host: "smtp.example.com"
    port: 465
    user: "your_email@example.com"
    password: "your_password"
    from: "your_email@example.com"
    to: "recipient@example.com"
```

4. 运行项目
```bash
python src/main.py
```

5. 查看结果
生成的早报将保存在output/daily_report.md中，并自动发送到配置的接收方式（企业微信或邮件）

## 项目结构
```
.
├── src/                  # 源代码目录
│   ├── crawler/          # 爬虫模块
│   ├── summarizer/       # 摘要生成模块
│   ├── generator/        # 早报生成模块
│   └── sender/           # 结果发送模块
├── config/               # 配置文件目录
│   ├── config.yaml       # 主配置文件
│   └── logging_config.yaml # 日志配置
├── output/               # 输出目录
├── logs/                 # 日志目录
├── requirements.txt      # 依赖文件
└── README.md             # 项目说明
```

## 日志配置
