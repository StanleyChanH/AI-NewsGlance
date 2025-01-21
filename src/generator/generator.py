from datetime import datetime
from typing import List, Dict
from pathlib import Path

class Generator:
    def __init__(self):
        self.template = """# AI早报 - {date}

{content}

---

> 本早报由AI自动生成，数据来源：{source}
"""

    def generate_daily_report(self, summaries: List[str]) -> str:
        """生成每日早报"""
        date_str = datetime.now().strftime("%Y年%m月%d日")
        content = "\n\n".join(
            f"## {i+1}. {summary}" 
            for i, summary in enumerate(summaries)
        )
        
        return self.template.format(
            date=date_str,
            content=content,
            source="AIBase"
        )

    def save_report(self, report: str, file_path: str) -> bool:
        """保存早报到文件"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(report)
            return True
        except Exception as e:
            print(f"保存早报失败: {e}")
            return False
