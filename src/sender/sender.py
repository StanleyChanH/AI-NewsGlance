import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import re
import requests
import yaml
import json
from typing import Optional, List
from pathlib import Path
from email.mime.base import MIMEBase
from email import encoders

class Sender:
    def __init__(self, config_path: Path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
    def send_email(self, content: str, subject: str = "AI早报", attachments: List[Path] = []) -> bool:
        """通过SMTP发送邮件"""
        try:
            smtp_config = self.config['sender']['smtp']
            
            # 创建多部分消息
            msg = MIMEMultipart()
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = smtp_config['from']
            msg['To'] = smtp_config['to']
            
            # 处理主内容
            lines = content.split('\n')
            filtered_content = []
            max_content_length = 4000  # 预留空间给markdown格式
            
            # 添加标题样式
            filtered_content.append("## 🌟 AI早报")
            filtered_content.append("---")
            
            # 添加主内容（保留所有内容）
            for line in lines:
                if len('\n'.join(filtered_content)) + len(line) < max_content_length:
                    # 添加emoji和格式优化
                    if line.startswith("# "):
                        filtered_content.append(f"## 📰 {line[2:]}")
                    elif line.startswith("## "):
                        filtered_content.append(f"### 🔍 {line[3:]}")
                    elif line.startswith("- "):
                        filtered_content.append(f"• {line[2:]}")
                    else:
                        filtered_content.append(line)
                else:
                    filtered_content.append("...（内容过长已截断）")
                    break
            
            # 添加附录（从raw_articles获取所有文章）
            raw_articles_dir = Path("output/raw_articles")
            if raw_articles_dir.exists():
                # 获取所有原始文章文件并按文件名排序
                article_files = sorted(raw_articles_dir.glob("*.md"), key=lambda f: f.name)
                
                # 初始化appendix
                appendix = ["\n## 📚 附录"]
                appendix.append("---")
                remaining_length = max_content_length - len('\n'.join(filtered_content))
                
                for article_file in article_files:
                    try:
                        with open(article_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # 使用正则表达式匹配标题和链接
                            # 匹配一级标题和链接
                            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
                            link_match = re.search(r'\[.+?\]\((https?://.+?)\)', content)
                            
                            if title_match and link_match:
                                title = title_match.group(1)
                                link = link_match.group(1)
                                formatted_entry = f"[{title}]({link})"
                                if len('\n'.join(appendix)) + len(formatted_entry) + 1 < remaining_length:
                                    appendix.append(formatted_entry)
                                else:
                                    break
                    except Exception as e:
                        print(f"读取原始文章文件{article_file}失败: {e}")
                        continue
                
                if len('\n'.join(filtered_content)) + len('\n'.join(appendix)) < max_content_length:
                    filtered_content.extend(appendix)
                else:
                    filtered_content.append("\n...（内容过长已截断）")
            
            # 将markdown转换为HTML并添加样式
            import markdown
            # 在附录内容前添加换行
            content_with_breaks = '\n'.join(filtered_content).replace('\n## 📚 附录', '\n\n## 📚 附录')
            html_content = markdown.markdown(content_with_breaks)
            
            # 添加CSS样式
            styled_html = f"""
            <html>
                <head>
                    <style>
                        body {{
                            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            max-width: 800px;
                            margin: 20px auto;
                            padding: 0 20px;
                        }}
                        h1, h2, h3 {{
                            color: #2c3e50;
                            margin-top: 1.5em;
                            margin-bottom: 0.5em;
                        }}
                        h2 {{
                            color: #2980b9;
                            border-bottom: 2px solid #eee;
                            padding-bottom: 0.3em;
                        }}
                        a {{
                            color: #3498db;
                            text-decoration: none;
                        }}
                        a:hover {{
                            text-decoration: underline;
                        }}
                        code {{
                            background: #f5f5f5;
                            padding: 2px 5px;
                            border-radius: 3px;
                            font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
                        }}
                        blockquote {{
                            border-left: 4px solid #ddd;
                            padding-left: 15px;
                            color: #666;
                            margin: 1.5em 0;
                        }}
                        .article-list {{
                            margin: 20px 0;
                            padding-left: 20px;
                        }}
                        .article-list li {{
                            margin: 10px 0;
                            padding: 8px;
                            background: #f8f9fa;
                            border-radius: 4px;
                        }}
                        .emoji {{
                            margin-right: 8px;
                        }}
                        hr {{
                            border: 0;
                            height: 1px;
                            background: #ddd;
                            margin: 2em 0;
                        }}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
            </html>
            """
            
            # 添加正文
            msg.attach(MIMEText(styled_html, 'html', 'utf-8'))
            
            # 添加附件
            for attachment in attachments:
                part = MIMEBase('application', 'octet-stream')
                with open(attachment, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={attachment.name}'
                )
                msg.attach(part)
            
            # 测试SMTP连接
            print("正在连接SMTP服务器...")
            with smtplib.SMTP_SSL(smtp_config['host'], smtp_config['port']) as server:
                print("SMTP连接成功")
                print("正在登录邮箱...")
                server.login(smtp_config['user'], smtp_config['password'])
                print("邮箱登录成功")
                print("正在发送邮件...")
                server.sendmail(smtp_config['from'], smtp_config['to'], msg.as_string())
                print("邮件发送成功")
            return True
        except smtplib.SMTPException as e:
            # 对于非关键错误（如-1），仅记录警告
            if getattr(e, 'smtp_code', -1) == -1:
                print(f"SMTP警告: {e}")
                print(f"服务器响应: {e.args}")
                return True
            else:
                print(f"SMTP错误: {e}")
                print(f"错误代码: {e.smtp_code}")
                print(f"错误消息: {e.smtp_error.decode() if hasattr(e, 'smtp_error') else str(e)}")
                print(f"服务器响应: {e.args}")
                return False
        except Exception as e:
            import traceback
            print(f"邮件发送失败: {e}")
            print("完整错误堆栈:")
            traceback.print_exc()
            return False

    def send_wechat_work(self, content: str, attachments: List[Path] = []) -> bool:
        """通过企业微信机器人发送消息"""
        try:
            webhook_url = self.config['sender']['wechat_work']['webhook_url']
            headers = {'Content-Type': 'application/json'}
            
            # 处理主内容
            lines = content.split('\n')
            filtered_content = []
            max_content_length = 4000  # 预留空间给markdown格式
            
            # 添加标题样式
            filtered_content.append("## 🌟 AI早报")
            filtered_content.append("---")
            
            # 添加主内容（保留所有内容）
            for line in lines:
                if len('\n'.join(filtered_content)) + len(line) < max_content_length:
                    # 添加emoji和格式优化
                    if line.startswith("# "):
                        filtered_content.append(f"## 📰 {line[2:]}")
                    elif line.startswith("## "):
                        filtered_content.append(f"### 🔍 {line[3:]}")
                    elif line.startswith("- "):
                        filtered_content.append(f"• {line[2:]}")
                    else:
                        filtered_content.append(line)
                else:
                    filtered_content.append("...（内容过长已截断）")
                    break
            
            # 添加附录（从raw_articles获取所有文章）
            raw_articles_dir = Path("output/raw_articles")
            if raw_articles_dir.exists():
                # 获取所有原始文章文件
                article_files = list(raw_articles_dir.glob("*.md"))
                
                # 初始化appendix
                appendix = ["\n## 📚 附录"]
                appendix.append("---")
                remaining_length = max_content_length - len('\n'.join(filtered_content))
                
                for article_file in article_files:
                                try:
                                    with open(article_file, 'r', encoding='utf-8') as f:
                                        content = f.read()
                                        # 使用正则表达式匹配标题和链接
                                        # 匹配一级标题和链接
                                        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
                                        link_match = re.search(r'\[.+?\]\((https?://.+?)\)', content)
                                        
                                        if title_match and link_match:
                                            title = title_match.group(1)
                                            link = link_match.group(1)
                                            formatted_entry = f"[{title}]({link})"
                                            if len('\n'.join(appendix)) + len(formatted_entry) + 1 < remaining_length:
                                                appendix.append(formatted_entry)
                                            else:
                                                break
                                except Exception as e:
                                    print(f"读取原始文章文件{article_file}失败: {e}")
                                    continue
                
                if len('\n'.join(filtered_content)) + len('\n'.join(appendix)) < max_content_length:
                    filtered_content.extend(appendix)
                else:
                    filtered_content.append("\n...（内容过长已截断）")
            
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "content": '\n'.join(filtered_content)
                }
            }
            print(f"发送数据: {data}")  # 调试信息
            response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
            print(f"响应状态码: {response.status_code}")  # 调试信息
            print(f"响应内容: {response.text}")  # 调试信息
            return response.status_code == 200
        except Exception as e:
            print(f"企业微信发送失败: {str(e)}")
            if hasattr(e, 'response'):
                print(f"错误响应: {e.response.text}")
            return False

    def send(self, content: str, subject: Optional[str] = None, attachments: List[Path] = []) -> bool:
        """根据配置选择发送方式"""
        results = []
        
        # 支持同时使用多个发送方式
        for sender_type in self.config['sender']['types']:
            if sender_type == "wechat_work":
                if not self.config['sender']['wechat_work']['enabled']:
                    print("企业微信发送方式未启用")
                    continue
                results.append(self.send_wechat_work(content, attachments))
            elif sender_type == "smtp":
                if not self.config['sender']['smtp']['enabled']:
                    print("SMTP发送方式未启用")
                    continue
                results.append(self.send_email(content, subject, attachments))
            else:
                print(f"未知的发送方式: {sender_type}")
                continue
                
        # 只要有一个发送成功就返回True
        return any(results)
