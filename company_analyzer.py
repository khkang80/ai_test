"""
회사명 추출 및 분석 모듈
뉴스에서 회사명을 추출하고 언급 빈도를 분석합니다.
"""
import re
from typing import List, Dict, Tuple
from collections import Counter
import config


class CompanyAnalyzer:
    """회사명 분석 클래스"""

    def __init__(self, companies_list: List[str] = None):
        """
        Args:
            companies_list: 추적할 회사명 리스트
        """
        self.companies = companies_list or config.MAJOR_COMPANIES
        self.company_mentions = Counter()
        self.company_articles = {}  # 회사별 관련 기사

    def extract_companies(self, text: str) -> List[str]:
        """
        텍스트에서 회사명 추출

        Args:
            text: 분석할 텍스트

        Returns:
            발견된 회사명 리스트
        """
        found_companies = []
        text_lower = text.lower()

        for company in self.companies:
            # 대소문자 구분 없이 검색
            if company.lower() in text_lower:
                found_companies.append(company)

        return found_companies

    def normalize_company_name(self, company: str) -> str:
        """
        회사명을 정규화 (동일 회사의 다른 표기 통합)

        Args:
            company: 회사명

        Returns:
            정규화된 회사명
        """
        # 동일 회사 매핑
        mappings = {
            '삼성': '삼성전자',
            'Samsung': '삼성전자',
            '현대차': '현대자동차',
            'Hyundai': '현대자동차',
            'Google': 'Alphabet',
            '구글': 'Alphabet',
            'Facebook': 'Meta',
            '애플': 'Apple',
            '마이크로소프트': 'Microsoft',
            '아마존': 'Amazon',
            '테슬라': 'Tesla',
            '엔비디아': 'NVIDIA',
            '넷플릭스': 'Netflix',
            '인텔': 'Intel',
            '퀄컴': 'Qualcomm',
        }

        return mappings.get(company, company)

    def analyze_articles(self, articles: List[Dict]) -> Dict[str, int]:
        """
        기사들에서 회사 언급 빈도 분석

        Args:
            articles: 뉴스 기사 리스트

        Returns:
            회사별 언급 횟수 딕셔너리
        """
        print("\n🔍 회사명 분석 시작...")

        for article in articles:
            # 제목과 설명 합치기
            text = f"{article.get('title', '')} {article.get('description', '')}"

            # 회사명 추출
            companies = self.extract_companies(text)

            for company in companies:
                # 정규화
                normalized = self.normalize_company_name(company)

                # 카운트
                self.company_mentions[normalized] += 1

                # 관련 기사 저장
                if normalized not in self.company_articles:
                    self.company_articles[normalized] = []

                self.company_articles[normalized].append({
                    'title': article.get('title', ''),
                    'link': article.get('link', ''),
                    'published': article.get('published', ''),
                })

        print(f"✅ {len(self.company_mentions)}개 회사 발견")

        return dict(self.company_mentions)

    def get_top_companies(self, n: int = 10) -> List[Tuple[str, int]]:
        """
        상위 N개 회사 반환

        Args:
            n: 반환할 회사 수

        Returns:
            (회사명, 언급횟수) 튜플 리스트
        """
        return self.company_mentions.most_common(n)

    def get_company_details(self, company: str) -> Dict:
        """
        특정 회사의 상세 정보 반환

        Args:
            company: 회사명

        Returns:
            회사 상세 정보
        """
        return {
            'name': company,
            'mentions': self.company_mentions.get(company, 0),
            'articles': self.company_articles.get(company, [])[:5]  # 최근 5개 기사
        }
