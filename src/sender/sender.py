import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests
import yaml
import json
from typing import Optional
from pathlib import Path

class Sender:
    def __init__(self, config_path: Path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
    def send_email(self, content: str, subject: str = "AI早报") -> bool:
        """通过SMTP发送邮件"""
        try:
            smtp_config = self.config['smtp']
            msg = MIMEText(content, 'html', 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = smtp_config['from']
            msg['To'] = smtp_config['to']
            
            with smtplib.SMTP_SSL(smtp_config['host'], smtp_config['port']) as server:
                server.login(smtp_config['user'], smtp_config['password'])
                server.sendmail(smtp_config['from'], smtp_config['to'], msg.as_string())
            return True
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return False

    def send_wechat_work(self, content: str) -> bool:
        """通过企业微信机器人发送消息"""
        try:
            webhook_url = self.config['wechat_work']['webhook_url']
            headers = {'Content-Type': 'application/json'}
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "content": content
                }
            }
            response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
            return response.status_code == 200
        except Exception as e:
            print(f"企业微信发送失败: {e}")
            return False

    def send(self, content: str, subject: Optional[str] = None) -> bool:
        """根据配置选择发送方式"""
        if self.config.get('wechat_work', {}).get('enabled', False):
            return self.send_wechat_work(content)
        elif self.config.get('smtp', {}).get('enabled', False):
            return self.send_email(content, subject)
        else:
            print("未配置任何发送方式")
            return False
