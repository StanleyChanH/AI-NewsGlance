# 贡献指南

欢迎为AI早报生成系统做贡献！在提交贡献之前，请仔细阅读以下指南。

## 开发环境设置

1. 克隆仓库
```bash
git clone https://github.com/StanleyChanH/AI-NewsGlance.git
cd ai-news
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements-dev.txt
pre-commit install
```

## 代码风格

- 遵循PEP 8规范
- 使用Black进行代码格式化
- 使用isort进行import排序
- 使用mypy进行类型检查
- 使用flake8进行静态检查

## 提交规范

1. 创建功能分支
```bash
git checkout -b feature/your-feature-name
```

2. 提交信息遵循Conventional Commits规范
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

常用type：
- feat: 新功能
- fix: bug修复
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

示例：
```
feat(crawler): add new news source

- add support for aibase.com
- update crawler config
```

## 测试要求

- 新功能必须包含单元测试
- 测试覆盖率应保持在90%以上
- 使用pytest编写测试
- 测试文件应放在tests目录下，与src目录结构保持一致

## Pull Request流程

1. Fork主仓库
2. 创建功能分支
3. 提交代码变更
4. 确保所有测试通过
5. 提交Pull Request
6. 等待代码审查
7. 根据反馈进行修改
8. PR合并后删除功能分支

## 代码审查标准

- 代码符合项目规范
- 包含必要的测试
- 文档及时更新
- 代码可读性高
- 功能实现完整
- 性能优化合理

## 问题报告

请在GitHub Issues中报告问题，并包含以下信息：
- 问题描述
- 重现步骤
- 预期行为
- 实际行为
- 环境信息
- 相关日志

感谢您的贡献！
