import sys
import asyncio
import yaml
from pathlib import Path
from typing import List

# 将项目根目录添加到PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from src.crawler import Crawler
from src.summarizer import Summarizer
from src.generator import Generator
from src.sender import Sender

async def main():
    # 加载配置
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 初始化各模块
    crawler = Crawler(
        base_url=config['crawler']['base_url'],
        max_articles=config['crawler']['max_articles']
    )
    
    summarizer = Summarizer(
        api_key=config['zhipuai']['api_key'],
        base_url=config['zhipuai']['base_url'],
        model=config['zhipuai']['model'],
        temperature=config['zhipuai']['temperature'],
        max_tokens=config['zhipuai']['max_tokens']
    )
    
    generator = Generator()

    # 获取文章编号
    article_numbers = crawler.get_article_numbers()
    if not article_numbers:
        print("未获取到文章编号")
        return

    # 爬取并处理文章
    summaries = []
    attachments: List[Path] = []
    for num in article_numbers:
        article = await crawler.crawl_article(num)
        if article:
            summary = summarizer.summarize_article(article)
            if summary:
                summaries.append(summary)
                # 收集原始文章文件
                raw_article_path = Path(__file__).parent.parent / "output" / "raw_articles"
                attachments.extend(list(raw_article_path.glob(f"article_{num}_*.md")))

    # 生成并保存早报
    if summaries:
        report = generator.generate_daily_report(summaries)
        output_path = Path(__file__).parent.parent / "output" / "daily_report.md"
        output_path.parent.mkdir(exist_ok=True)
        if generator.save_report(report, str(output_path)):
            print(f"早报已成功保存至: {output_path}")
            
            # 发送早报
            sender = Sender(config_path)
            if config.get('sender', {}).get('enabled', False):
                if sender.send(report, config['generator']['title'], attachments):
                    print("早报发送成功")
                else:
                    print("早报发送失败")
        else:
            print("早报保存失败")
    else:
        print("未生成有效摘要")

if __name__ == "__main__":
    asyncio.run(main())
