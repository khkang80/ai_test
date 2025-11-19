#!/usr/bin/env python3
"""
Trending Stocks Tracker - Complete Demo
뉴스 분석 + 감성 분석 + 주가 데이터 + 기술적 분석 + 매수/매도 의견
"""
import json
from datetime import datetime
from pathlib import Path

import config
from company_analyzer import CompanyAnalyzer
from sentiment_analyzer import SentimentAnalyzer
from stock_data import StockDataCollector
from technical_analysis import TechnicalAnalyzer
from visualizer import Visualizer


def generate_sample_news():
    """샘플 뉴스 데이터 생성"""
    return [
        {
            'title': '삼성전자, AI 반도체 시장 점유율 30% 돌파',
            'description': '삼성전자가 인공지능 반도체 시장에서 30% 점유율을 달성하며 업계 1위로 올라섰다. 실적 호조세 지속 전망.',
            'link': 'https://example.com/news1',
            'published': '2025-11-19',
            'source': 'Tech News'
        },
        {
            'title': 'Apple, 새로운 Vision Pro 2 발표 예정',
            'description': 'Apple이 다음 달 Vision Pro 2를 공개할 예정이라고 밝혔다. 혁신적인 기능으로 시장 선도 기대.',
            'link': 'https://example.com/news2',
            'published': '2025-11-19',
            'source': 'Apple Insider'
        },
        {
            'title': 'Tesla 주가 급등, 전기차 판매 호조',
            'description': 'Tesla의 3분기 전기차 판매가 예상을 크게 상회하며 주가가 15% 상승했다.',
            'link': 'https://example.com/news3',
            'published': '2025-11-19',
            'source': 'Finance Daily'
        },
        {
            'title': '네이버, 하이퍼클로바X 글로벌 진출',
            'description': '네이버가 자체 개발한 AI 하이퍼클로바X를 동남아시아에 출시한다. 성장세 지속 예상.',
            'link': 'https://example.com/news4',
            'published': '2025-11-19',
            'source': 'Korea Business'
        },
        {
            'title': 'NVIDIA, 신형 GPU 출시로 주가 사상 최고치',
            'description': 'NVIDIA가 차세대 Blackwell GPU를 출시하며 주가가 사상 최고치를 경신했다.',
            'link': 'https://example.com/news5',
            'published': '2025-11-19',
            'source': 'Tech Crunch'
        },
        {
            'title': '카카오, 메타버스 플랫폼 투자 확대',
            'description': '카카오가 메타버스 사업에 1조원 규모의 투자를 발표했다.',
            'link': 'https://example.com/news6',
            'published': '2025-11-19',
            'source': 'Business Korea'
        },
        {
            'title': 'Microsoft, AI 챗봇 기능 강화',
            'description': 'Microsoft가 Copilot AI에 새로운 기능을 추가하며 경쟁력을 높였다.',
            'link': 'https://example.com/news7',
            'published': '2025-11-19',
            'source': 'Windows Central'
        },
        {
            'title': '현대자동차, 수소차 양산 본격화',
            'description': '현대자동차가 수소 전기차의 대량 생산을 시작한다고 발표했다.',
            'link': 'https://example.com/news8',
            'published': '2025-11-19',
            'source': 'Auto News'
        },
        {
            'title': 'Amazon 실적 부진 우려, 주가 하락',
            'description': 'Amazon의 클라우드 서비스 성장률이 둔화되며 투자자들의 우려가 커지고 있다.',
            'link': 'https://example.com/news9',
            'published': '2025-11-19',
            'source': 'Cloud Computing'
        },
        {
            'title': '삼성전자, 갤럭시 S25 사전 예약 시작',
            'description': '삼성전자가 신제품 갤럭시 S25의 사전 예약을 개시했다. 폭발적인 반응 예상.',
            'link': 'https://example.com/news10',
            'published': '2025-11-19',
            'source': 'Mobile News'
        },
        {
            'title': 'Tesla, 자율주행 기술 획기적 발전',
            'description': 'Tesla의 완전자율주행(FSD) 기술이 큰 진전을 이뤘다.',
            'link': 'https://example.com/news11',
            'published': '2025-11-19',
            'source': 'Auto Tech'
        },
        {
            'title': 'Apple, 인도 시장 공략 강화',
            'description': 'Apple이 인도에 새로운 제조 공장을 설립할 계획이다.',
            'link': 'https://example.com/news12',
            'published': '2025-11-19',
            'source': 'Global Business'
        },
        {
            'title': 'NVIDIA, 데이터센터 부문 성장세',
            'description': 'NVIDIA의 데이터센터 GPU 매출이 전분기 대비 50% 증가했다.',
            'link': 'https://example.com/news13',
            'published': '2025-11-19',
            'source': 'Data Center Weekly'
        },
    ]


def main():
    """메인 실행 함수"""

    print("=" * 80)
    print("📈 Trending Stocks Tracker - COMPLETE EDITION")
    print("   뉴스 분석 + 감성 분석 + 주가 데이터 + 기술적 분석 + 매수/매도 의견")
    print("=" * 80)
    print(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 1. 샘플 뉴스 생성
    print("📰 샘플 뉴스 데이터 생성...")
    articles = generate_sample_news()
    print(f"✅ 총 {len(articles)}개 샘플 뉴스 생성 완료\n")

    # 2. 감성 분석
    print("🎭 뉴스 감성 분석 중...")
    sentiment_analyzer = SentimentAnalyzer()
    articles_with_sentiment = sentiment_analyzer.analyze_articles(articles)
    sentiment_summary = sentiment_analyzer.get_sentiment_summary(articles_with_sentiment)

    print(f"✅ 감성 분석 완료:")
    print(f"   긍정: {sentiment_summary['positive']}개 ({sentiment_summary['positive_percent']}%)")
    print(f"   부정: {sentiment_summary['negative']}개 ({sentiment_summary['negative_percent']}%)")
    print(f"   평균 감성 점수: {sentiment_summary['average_score']}\n")

    # 3. 회사명 분석
    analyzer = CompanyAnalyzer()
    analyzer.analyze_articles(articles_with_sentiment)

    # 4. 상위 10개 회사 추출
    top_companies = analyzer.get_top_companies(config.TOP_N_COMPANIES)

    if not top_companies:
        print("❌ 발견된 회사가 없습니다.")
        return

    # 5. 주가 데이터 수집
    print("💰 주가 데이터 수집 중...")
    stock_collector = StockDataCollector()
    company_names = [company for company, _ in top_companies]
    stock_data = stock_collector.get_multiple_stocks(company_names)
    print(f"✅ {len(stock_data)}개 회사 주가 데이터 수집 완료\n")

    # 6. 기술적 분석 및 매매 신호 생성
    print("📊 기술적 분석 및 매수/매도 신호 생성 중...")
    tech_analyzer = TechnicalAnalyzer()
    technical_data = {}

    for company_name in company_names:
        ticker = stock_collector.get_ticker(company_name)
        if ticker:
            analysis = tech_analyzer.analyze_stock(ticker, company_name)
            technical_data[company_name] = analysis

    print(f"✅ {len(technical_data)}개 회사 기술적 분석 완료\n")

    print("\n" + "=" * 80)
    print("🏆 오늘의 상위 10개 트렌딩 회사 (종합 투자 분석)")
    print("=" * 80)
    print("\n⚠️  면책 조항: 본 분석은 참고용이며, 투자 권유가 아닙니다. 투자 결정은 본인 책임입니다.\n")

    # 7. 상세 정보 수집 및 표시
    companies_details = []
    for idx, (company, count) in enumerate(top_companies, 1):
        details = analyzer.get_company_details(company)

        # 회사 관련 기사의 감성 분석
        company_sentiment = sentiment_analyzer.get_company_sentiment(
            details['articles']
        )

        # 주가 정보
        stock_info = stock_data.get(company, {})

        # 기술적 분석
        tech_info = technical_data.get(company, {})

        # 통합 정보
        enhanced_details = {
            **details,
            'rank': idx,
            'sentiment': company_sentiment,
            'stock': stock_info,
            'technical': tech_info,
        }
        companies_details.append(enhanced_details)

        # 콘솔 출력
        print(f"\n{'='*80}")
        print(f"#{idx:2d} {company:20s} - {count} mentions")
        print(f"{'='*80}")

        # 감성 분석
        sentiment_emoji = company_sentiment.get('emoji', '➡️')
        print(f"📰 뉴스 감성: {sentiment_emoji} {company_sentiment['overall_sentiment']:10s} "
              f"(점수: {company_sentiment['summary']['average_score']:+.2f})")

        # 주가 정보
        stock_price = stock_info.get('price', 'N/A')
        if stock_price != 'N/A':
            stock_change = stock_info.get('change_percent', 0)
            stock_emoji = '📈' if stock_change > 0 else '📉' if stock_change < 0 else '➡️'
            currency = stock_info.get('currency', '')
            is_mock = ' (모의)' if stock_info.get('is_mock') else ''
            print(f"💰 현재 주가: {stock_emoji} {stock_price:,.2f} {currency} "
                  f"({stock_change:+.2f}%){is_mock}")
        else:
            print(f"💰 현재 주가: 데이터 없음")

        # 기술적 분석 및 매매 의견
        if tech_info and 'recommendation' in tech_info:
            rec = tech_info['recommendation']
            emoji = tech_info.get('emoji', '➡️')
            confidence = tech_info.get('confidence', 0)
            analysis_text = tech_info.get('analysis', '')

            print(f"\n🎯 투자 의견: {emoji} {rec:15s} (신뢰도: {confidence:.1f}%)")
            print(f"📌 분석: {analysis_text}")

            indicators = tech_info.get('indicators', {})
            print(f"\n📊 기술적 지표:")
            print(f"   • RSI(14):  {indicators.get('RSI', 'N/A')}")
            print(f"   • SMA(20):  {indicators.get('SMA20', 'N/A')}")
            print(f"   • SMA(50):  {indicators.get('SMA50', 'N/A')}")
            print(f"   • MACD:     {indicators.get('MACD', 'N/A')}")

            # 종합 평가
            print(f"\n💡 종합 평가:")
            news_score = company_sentiment['summary']['average_score']
            if news_score > 0.3 and rec in ['BUY', 'STRONG_BUY']:
                print(f"   ✓ 긍정적 뉴스 + 매수 신호 = 긍정적 전망")
            elif news_score < -0.3 and rec in ['SELL', 'STRONG_SELL']:
                print(f"   ✗ 부정적 뉴스 + 매도 신호 = 부정적 전망")
            elif news_score > 0 and rec in ['SELL', 'STRONG_SELL']:
                print(f"   ⚠ 긍정적 뉴스이나 기술적으로 매도 신호 = 주의 필요")
            elif news_score < 0 and rec in ['BUY', 'STRONG_BUY']:
                print(f"   ⚠ 부정적 뉴스이나 기술적으로 매수 신호 = 신중한 검토 필요")
            else:
                print(f"   ➡ 중립적 관점 = 추가 분석 권장")

        else:
            print(f"\n🎯 투자 의견: 분석 데이터 부족")

    # 8. 데이터 저장
    output_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'timestamp': datetime.now().isoformat(),
        'mode': 'complete',
        'sentiment_summary': sentiment_summary,
        'disclaimer': '본 분석은 참고용이며 투자 권유가 아닙니다.',
        'top_companies': [
            {
                'rank': d['rank'],
                'name': d['name'],
                'mentions': d['mentions'],
                'sentiment': d['sentiment']['overall_sentiment'],
                'sentiment_score': d['sentiment']['summary']['average_score'],
                'stock_price': d['stock'].get('price'),
                'stock_change': d['stock'].get('change_percent'),
                'recommendation': d['technical'].get('recommendation', 'N/A'),
                'confidence': d['technical'].get('confidence', 0),
                'technical_analysis': d['technical'].get('analysis', ''),
                'articles': d['articles'][:3]
            }
            for d in companies_details
        ]
    }

    output_file = config.DATA_DIR / 'trending_companies_complete.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n\n{'='*80}")
    print("✅ 분석 완료!")
    print(f"{'='*80}")
    print(f"💾 데이터 저장: {output_file}")
    print("\n📋 제공 기능:")
    print("   ✓ 뉴스 트렌드 분석")
    print("   ✓ AI 감성 분석")
    print("   ✓ 실시간 주가 데이터")
    print("   ✓ 기술적 분석 (RSI, MACD, 이동평균)")
    print("   ✓ 매수/매도 투자 의견")
    print("   ✓ 종합 투자 인사이트")
    print("\n⚠️  투자 시 유의사항:")
    print("   • 본 분석은 알고리즘 기반 참고 자료입니다")
    print("   • 실제 투자 결정은 본인의 책임입니다")
    print("   • 과거 데이터가 미래 수익을 보장하지 않습니다")
    print("   • 분산 투자 및 리스크 관리가 중요합니다")


if __name__ == '__main__':
    main()
