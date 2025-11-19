# 📈 Trending Stocks Tracker

매일 뉴스에서 가장 이슈가 되는 상위 10개 회사를 추적하고 분석하는 AI 기반 주식 분석 도구

## 🎯 주요 기능

### 핵심 기능
- 🔍 **실시간 금융 뉴스 수집** - RSS 피드를 통한 자동 뉴스 수집
- 🏢 **회사명 자동 추출** - 뉴스에서 언급된 회사 자동 감지 및 분석
- 🏆 **상위 10개 트렌딩 회사 선정** - 언급 빈도 기반 트렌딩 회사 추출
- 📊 **데이터 시각화** - 차트 및 HTML 리포트 자동 생성

### 고급 기능 ✨
- 💰 **실시간 주가 데이터 연동** - Yahoo Finance API를 통한 주가 정보 통합
- 🎭 **AI 감성 분석** - 뉴스의 긍정/부정/중립 감성 자동 분석
- 📈 **시계열 분석** - 시간에 따른 트렌드 변화 추적
- 🌐 **웹 대시보드** - Streamlit 기반 인터랙티브 대시보드
- 📜 **히스토리 추적** - 과거 데이터 저장 및 트렌드 비교
- 📊 **기술적 분석** - RSI, MACD, 이동평균 등 기술적 지표 계산
- 🎯 **매수/매도 의견** - 알고리즘 기반 투자 신호 생성

## 🚀 시작하기

### 설치

```bash
pip install -r requirements.txt
```

### 실행 방법

#### 1. 기본 데모 (샘플 데이터)
```bash
python3 demo.py
```

#### 2. 향상된 데모 (주가 + 감성 분석)
```bash
python3 demo_enhanced.py
```

#### 3. 완전판 데모 (기술적 분석 + 매매 의견 포함) ⭐ 추천!
```bash
python3 demo_complete.py
```

#### 4. 웹 대시보드
```bash
streamlit run dashboard.py
```

#### 5. 실제 뉴스 수집
```bash
python3 main.py
```

## 📊 출력 파일

- `data/trending_companies.json` - 기본 트렌딩 회사 데이터
- `data/trending_companies_enhanced.json` - 주가 + 감성 분석 데이터
- `data/trending_companies_complete.json` - 기술적 분석 + 매매 의견 포함
- `data/history.json` - 시계열 히스토리 데이터
- `data/history.csv` - CSV 형식 히스토리
- `reports/trending_companies.png` - 시각화 차트
- `reports/trending_report.html` - HTML 리포트

## 🛠 기술 스택

### 백엔드
- Python 3.11+
- Beautiful Soup 4 (XML/RSS 파싱)
- Pandas (데이터 분석)
- Requests (HTTP 클라이언트)

### 데이터 분석
- 자연어 처리 기반 회사명 추출
- 키워드 기반 감성 분석
- 시계열 데이터 분석
- 기술적 분석 (RSI, MACD, 볼린저 밴드, 이동평균)
- 매수/매도 신호 생성 알고리즘

### 시각화
- Matplotlib (차트 생성)
- Streamlit (웹 대시보드)
- HTML/CSS (리포트)

### 데이터 소스
- Yahoo Finance API (주가 데이터)
- RSS 뉴스 피드 (뉴스 수집)

## 📂 프로젝트 구조

```
ai_test/
├── config.py              # 설정 및 회사 리스트
├── news_collector.py      # 뉴스 수집 모듈
├── company_analyzer.py    # 회사명 분석 모듈
├── sentiment_analyzer.py  # 감성 분석 모듈
├── stock_data.py         # 주가 데이터 수집 모듈
├── technical_analysis.py  # 기술적 분석 모듈 (NEW!)
├── history_tracker.py    # 히스토리 추적 모듈
├── visualizer.py         # 시각화 모듈
├── main.py               # 메인 실행 파일
├── demo.py               # 기본 데모
├── demo_enhanced.py      # 향상된 데모
├── demo_complete.py      # 완전판 데모 (매매 의견 포함)
├── dashboard.py          # 웹 대시보드
├── requirements.txt      # 의존성 패키지
└── README.md            # 문서
```

## 💡 활용 사례

1. **투자 인사이트** - 어떤 회사가 뉴스에 많이 언급되는지 파악
2. **트렌드 추적** - 시간에 따른 회사별 관심도 변화 모니터링
3. **감성 분석** - 특정 회사에 대한 뉴스 감성 파악
4. **주가 상관관계** - 뉴스 언급과 주가 변동의 관계 분석
5. **경쟁사 분석** - 산업별 회사들의 미디어 노출도 비교
6. **기술적 매매 신호** - RSI, MACD 등을 활용한 매수/매도 타이밍 포착
7. **종합 투자 판단** - 뉴스 감성 + 기술적 분석을 결합한 투자 의견

## 🔧 향후 개발 계획

- [ ] 실시간 뉴스 API 연동 (NewsAPI, Alpha Vantage)
- [ ] 고급 NLP 모델 적용 (BERT, GPT)
- [ ] 주가 예측 모델 추가
- [ ] 알림 시스템 (이메일, Slack)
- [ ] 모바일 앱 개발
- [ ] 다국어 지원

## 📝 라이선스

MIT License

## 🤝 기여

이슈와 PR을 환영합니다!

---
Made with 💚 by Creative AI Team
