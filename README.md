# AI早报生成系统

## 项目概述
本系统是一个自动化AI早报生成工具，能够：
1. 自动抓取最新AI相关新闻
2. 使用AI模型生成新闻摘要
3. 生成格式化的Markdown早报
4. 通过邮件或企业微信发送早报

## 工程化特性
- 模块化架构，易于维护和扩展
- 完善的代码质量保障体系
- 清晰的文档和贡献指南

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

### 3. 配置环境
复制配置文件模板：
```bash
cp config/config.example.yaml config/config.yaml
```
根据实际情况修改config.yaml中的配置项

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
