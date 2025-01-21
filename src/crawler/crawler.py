import asyncio
import json
from typing import List, Dict, Optional
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import requests
from bs4 import BeautifulSoup
import re

class Crawler:
    def __init__(self, base_url: str, max_articles: int = 10):
        self.base_url = base_url
        self.max_articles = max_articles

    def get_article_numbers(self) -> List[int]:
        """获取文章编号列表"""
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

                return json.loads(result.extracted_content)
        except Exception as e:
            print(f"爬取文章 {article_num} 时发生错误: {e}")
            return None
