import asyncio
import json
from typing import List, Dict, Optional
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
from datetime import datetime

class Crawler:
    def __init__(self, base_url: str, max_articles: int = 10):
        self.base_url = base_url
        self.max_articles = max_articles
        self.output_dir = Path("output/raw_articles")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_article_numbers(self) -> List[int]:
        """获取文章编号列表"""
        # 清空raw_articles目录
        raw_articles_dir = Path("output/raw_articles")
        if raw_articles_dir.exists():
            for file in raw_articles_dir.glob("*"):
                try:
                    file.unlink()
                except Exception as e:
                    print(f"删除文件{file}失败: {e}")

        try:
            first_num = self._get_first_article_number()
            if first_num is None:
                return []
            
            return list(range(first_num, first_num - self.max_articles, -1))
        except Exception as e:
            print(f"获取文章编号失败: {e}")
            return []

    def _get_first_article_number(self) -> Optional[int]:
        """获取第一条文章的编号"""
        try:
            response = requests.get(self.base_url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    match = re.search(r'/zh/news/(\d+)', href)
                    if match:
                        return int(match.group(1))
            return None
        except Exception as e:
            print(f"获取首篇文章编号失败: {e}")
            return None

    async def crawl_article(self, article_num: int) -> Optional[Dict]:
        """爬取单篇文章内容"""
        # 配置Playwright浏览器路径
        import os
        from playwright.async_api import async_playwright
        
        playwright_browser_path = os.path.join(
            os.getenv('LOCALAPPDATA'),
            'ms-playwright',
            'chromium-1148',
            'chrome-win',
            'chrome.exe'
        )
        
        article_url = f"{self.base_url}{article_num}"
        schema = {
            "name": "AIbase News Article",
            "baseSelector": "div.pb-32",
            "fields": [
                {"name": "title", "selector": "h1", "type": "text"},
                {"name": "publication_date", "selector": "div.flex.flex-col > div.flex.flex-wrap > span:nth-child(6)", "type": "text"},
                {"name": "content", "selector": "div.post-content", "type": "text"},
            ],
        }

        try:
            extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
            async with AsyncWebCrawler(
                verbose=True,
                browser_executable_path=playwright_browser_path
            ) as crawler:
                result = await crawler.arun(
                    url=article_url,
                    extraction_strategy=extraction_strategy,
                    bypass_cache=True,
                )

                if not result.success:
                    print(f"爬取文章 {article_num} 失败")
                    return None

                print(f"原始提取内容: {result.extracted_content}")  # 添加调试信息
                
                try:
                    extracted_data = json.loads(result.extracted_content)
                    if not isinstance(extracted_data, list):
                        print(f"文章 {article_num} 数据格式错误: 期望列表类型，得到 {type(extracted_data)}")
                        return None
                        
                    if len(extracted_data) == 0:
                        print(f"文章 {article_num} 无有效数据: 提取结果为空列表")
                        return None
                        
                    # 取列表中的第一个元素
                    first_item = extracted_data[0]
                    if not isinstance(first_item, dict):
                        print(f"文章 {article_num} 数据格式错误: 期望字典类型，得到 {type(first_item)}")
                        return None
                        
                    article_data = {
                        'title': first_item.get('title', '无标题'),
                        'publication_date': first_item.get('publication_date', '未知日期'),
                        'content': first_item.get('content', '无内容')
                    }
                    
                    print(f"解析后的文章数据: {article_data}")  # 添加调试信息
                except json.JSONDecodeError as e:
                    print(f"文章 {article_num} JSON解析失败: {e}")
                    return None
                self._save_raw_article(article_num, article_data, article_url)
                return article_data
        except Exception as e:
            print(f"爬取文章 {article_num} 时发生错误: {e}")
            return None

    def _save_raw_article(self, article_num: int, article_data: Dict, article_url: str):
        """保存原始文章到Markdown文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"article_{article_num}_{timestamp}.md"
        
        markdown_content = f"""# {article_data['title']}

**发布日期**: {article_data['publication_date']}

**原文链接**: [{article_url}]({article_url})

## 正文

{article_data['content']}
"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)
