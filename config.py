"""
Configuration settings for Trending Stocks Tracker
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Data directories
DATA_DIR = BASE_DIR / 'data'
REPORTS_DIR = BASE_DIR / 'reports'

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# News sources (RSS feeds)
NEWS_SOURCES = {
    'google_finance': 'https://news.google.com/rss/search?q=stock+market+when:1d&hl=ko&gl=KR&ceid=KR:ko',
    'reuters_business': 'https://www.reuters.com/business',
    'bloomberg': 'https://www.bloomberg.com/markets',
}

# Analysis settings
TOP_N_COMPANIES = 10  # 상위 N개 회사
MIN_MENTIONS = 2      # 최소 언급 횟수

# Known companies list (can be expanded)
MAJOR_COMPANIES = [
    # 한국 주요 기업
    '삼성전자', '삼성', 'Samsung',
    'SK하이닉스', 'SK',
    '현대자동차', '현대차', 'Hyundai',
    'LG전자', 'LG',
    '네이버', 'NAVER',
    '카카오', 'Kakao',
    'POSCO', '포스코',
    '기아', 'KIA',

    # 미국 주요 기업
    'Apple', '애플',
    'Microsoft', '마이크로소프트',
    'Google', 'Alphabet', '구글',
    'Amazon', '아마존',
    'Meta', 'Facebook', '메타',
    'Tesla', '테슬라',
    'NVIDIA', '엔비디아',
    'Netflix', '넷플릭스',
    'Intel', '인텔',
    'AMD',
    'Qualcomm', '퀄컴',
    'Disney', '디즈니',
    'Coca-Cola', '코카콜라',
    'McDonald', '맥도날드',
    'Nike', '나이키',
    'Boeing', '보잉',
    'JPMorgan', 'JP모건',
]

# File paths
TRENDING_FILE = DATA_DIR / 'trending_companies.json'
HISTORY_FILE = DATA_DIR / 'news_history.csv'
