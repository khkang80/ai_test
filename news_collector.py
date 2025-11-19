"""
뉴스 수집 모듈
RSS 피드 및 웹 스크래핑을 통해 금융 뉴스를 수집합니다.
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import time
import xml.etree.ElementTree as ET


class NewsCollector:
    """뉴스 수집 클래스"""

    def __init__(self, sources: Dict[str, str]):
        """
        Args:
            sources: 뉴스 소스 딕셔너리 {name: url}
        """
        self.sources = sources
        self.articles = []

    def collect_from_rss(self, url: str) -> List[Dict]:
        """
        RSS 피드에서 뉴스 수집 (XML 파싱 사용)

        Args:
            url: RSS 피드 URL

        Returns:
            뉴스 기사 리스트
        """
        articles = []
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()

            # BeautifulSoup로 XML 파싱
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')[:50]  # 최근 50개 기사

            for item in items:
                title = item.find('title')
                description = item.find('description')
                link = item.find('link')
                pubDate = item.find('pubDate')

                article = {
                    'title': title.text if title else '',
                    'description': description.text if description else '',
                    'link': link.text if link else '',
                    'published': pubDate.text if pubDate else '',
                    'source': 'Google News',
                }
                articles.append(article)

        except Exception as e:
            print(f"RSS 수집 오류 ({url}): {e}")

        return articles

    def collect_from_google_news(self, query: str = "stock market") -> List[Dict]:
        """
        Google News RSS에서 뉴스 수집

        Args:
            query: 검색 쿼리

        Returns:
            뉴스 기사 리스트
        """
        articles = []

        # 한국 주식 시장 뉴스
        kr_url = f'https://news.google.com/rss/search?q={query}+한국+주식&hl=ko&gl=KR&ceid=KR:ko'
        articles.extend(self.collect_from_rss(kr_url))

        time.sleep(1)  # Rate limiting

        # 글로벌 주식 시장 뉴스
        global_url = f'https://news.google.com/rss/search?q={query}&hl=en&gl=US&ceid=US:en'
        articles.extend(self.collect_from_rss(global_url))

        return articles

    def collect_all(self) -> List[Dict]:
        """
        모든 소스에서 뉴스 수집

        Returns:
            전체 뉴스 기사 리스트
        """
        all_articles = []

        print("📰 뉴스 수집 시작...")

        # Google News에서 수집
        print("  - Google News 수집 중...")
        all_articles.extend(self.collect_from_google_news("stock market"))
        time.sleep(1)

        all_articles.extend(self.collect_from_google_news("기업 실적"))
        time.sleep(1)

        all_articles.extend(self.collect_from_google_news("주가 급등"))

        self.articles = all_articles
        print(f"✅ 총 {len(all_articles)}개 뉴스 수집 완료")

        return all_articles

    def get_articles(self) -> List[Dict]:
        """수집된 기사 반환"""
        return self.articles
