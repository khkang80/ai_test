# 📈 Trending Stocks Tracker

매일 뉴스에서 가장 이슈가 되는 상위 10개 회사를 추적하고 분석하는 프로젝트

## 🎯 주요 기능

- 실시간 금융 뉴스 수집
- 회사명 자동 추출 및 언급 빈도 분석
- 일일 상위 10개 트렌딩 회사 선정
- 데이터 시각화 및 리포트 생성
- 히스토리 추적

## 🚀 시작하기

### 설치

```bash
pip install -r requirements.txt
```

### 실행

```bash
python main.py
```

## 📊 출력

- `data/trending_companies.json`: 일일 트렌딩 회사 데이터
- `data/news_history.csv`: 뉴스 히스토리
- `reports/`: 시각화 리포트

## 🛠 기술 스택

- Python 3.8+
- Beautiful Soup / RSS 파싱
- Pandas (데이터 분석)
- Matplotlib / Plotly (시각화)
- Natural Language Processing

## 📝 라이선스

MIT License
