"""
주가 데이터 수집 모듈
실시간 주가 정보를 가져옵니다.
"""
import requests
from typing import Dict, Optional
from datetime import datetime


class StockDataCollector:
    """주가 데이터 수집 클래스"""

    # 회사명 -> Ticker 심볼 매핑
    TICKER_MAP = {
        # 한국 기업
        '삼성전자': '005930.KS',
        'SK하이닉스': '000660.KS',
        '현대자동차': '005380.KS',
        'LG전자': '066570.KS',
        '네이버': '035420.KS',
        '카카오': '035720.KS',
        'POSCO': '005490.KS',
        '포스코': '005490.KS',
        '기아': '000270.KS',

        # 미국 기업
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Alphabet': 'GOOGL',
        'Amazon': 'AMZN',
        'Meta': 'META',
        'Tesla': 'TSLA',
        'NVIDIA': 'NVDA',
        'Netflix': 'NFLX',
        'Intel': 'INTC',
        'AMD': 'AMD',
        'Qualcomm': 'QCOM',
        'Disney': 'DIS',
        'Coca-Cola': 'KO',
        'Nike': 'NKE',
        'Boeing': 'BA',
        'JPMorgan': 'JPM',
    }

    def __init__(self):
        """초기화"""
        self.cache = {}  # 간단한 캐시

    def get_ticker(self, company_name: str) -> Optional[str]:
        """
        회사명으로 Ticker 심볼 가져오기

        Args:
            company_name: 회사명

        Returns:
            Ticker 심볼 또는 None
        """
        return self.TICKER_MAP.get(company_name)

    def get_stock_info(self, company_name: str) -> Optional[Dict]:
        """
        주가 정보 가져오기 (Yahoo Finance API 사용)

        Args:
            company_name: 회사명

        Returns:
            주가 정보 딕셔너리
        """
        ticker = self.get_ticker(company_name)
        if not ticker:
            return None

        # 캐시 확인
        if ticker in self.cache:
            return self.cache[ticker]

        try:
            # Yahoo Finance API (간단한 버전)
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            params = {
                'range': '1d',
                'interval': '1d'
            }

            response = requests.get(url, params=params, timeout=5, headers={
                'User-Agent': 'Mozilla/5.0'
            })

            if response.status_code != 200:
                return self._get_mock_data(company_name, ticker)

            data = response.json()

            # 데이터 파싱
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                result = data['chart']['result'][0]
                meta = result.get('meta', {})

                current_price = meta.get('regularMarketPrice', 0)
                previous_close = meta.get('chartPreviousClose', current_price)
                change = current_price - previous_close if current_price and previous_close else 0
                change_percent = (change / previous_close * 100) if previous_close else 0

                stock_info = {
                    'company': company_name,
                    'ticker': ticker,
                    'price': round(current_price, 2),
                    'change': round(change, 2),
                    'change_percent': round(change_percent, 2),
                    'currency': meta.get('currency', 'USD'),
                    'market_cap': meta.get('marketCap', 'N/A'),
                    'timestamp': datetime.now().isoformat(),
                }

                self.cache[ticker] = stock_info
                return stock_info
            else:
                return self._get_mock_data(company_name, ticker)

        except Exception as e:
            print(f"주가 데이터 수집 오류 ({company_name}): {e}")
            return self._get_mock_data(company_name, ticker)

    def _get_mock_data(self, company_name: str, ticker: str) -> Dict:
        """
        모의 데이터 생성 (API 실패 시)

        Args:
            company_name: 회사명
            ticker: 티커 심볼

        Returns:
            모의 주가 정보
        """
        import random

        # 회사별 대략적인 주가 범위
        price_ranges = {
            'AAPL': (150, 200),
            'MSFT': (350, 420),
            'TSLA': (200, 300),
            'NVDA': (400, 600),
            '005930.KS': (60000, 80000),  # 삼성전자
            '035420.KS': (150000, 200000),  # 네이버
        }

        price_range = price_ranges.get(ticker, (100, 500))
        base_price = random.uniform(*price_range)
        change_percent = random.uniform(-5, 5)
        change = base_price * (change_percent / 100)

        return {
            'company': company_name,
            'ticker': ticker,
            'price': round(base_price, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'currency': 'KRW' if ticker.endswith('.KS') else 'USD',
            'market_cap': 'N/A',
            'timestamp': datetime.now().isoformat(),
            'is_mock': True,
        }

    def get_multiple_stocks(self, companies: list) -> Dict[str, Dict]:
        """
        여러 회사의 주가 정보 가져오기

        Args:
            companies: 회사명 리스트

        Returns:
            회사명을 키로 하는 주가 정보 딕셔너리
        """
        results = {}
        for company in companies:
            info = self.get_stock_info(company)
            if info:
                results[company] = info
        return results
