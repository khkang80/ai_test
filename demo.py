#!/usr/bin/env python3
"""
Trending Stocks Tracker - Demo with Sample Data
실제 뉴스 대신 샘플 데이터로 프로그램 기능을 시연합니다.
"""
import json
from datetime import datetime
from pathlib import Path

import config
from company_analyzer import CompanyAnalyzer
from visualizer import Visualizer


def generate_sample_news():
    """샘플 뉴스 데이터 생성"""
    return [
        {
            'title': '삼성전자, AI 반도체 시장 점유율 30% 돌파',
            'description': '삼성전자가 인공지능 반도체 시장에서 30% 점유율을 달성하며 업계 1위로 올라섰다.',
            'link': 'https://example.com/news1',
            'published': '2025-11-19',
            'source': 'Tech News'
        },
        {
            'title': 'Apple, 새로운 Vision Pro 2 발표 예정',
            'description': 'Apple이 다음 달 Vision Pro 2를 공개할 예정이라고 밝혔다.',
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
            'description': '네이버가 자체 개발한 AI 하이퍼클로바X를 동남아시아에 출시한다.',
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
            'title': 'Amazon, 클라우드 서비스 매출 증가',
            'description': 'Amazon Web Services의 분기 매출이 전년 대비 25% 증가했다.',
            'link': 'https://example.com/news9',
            'published': '2025-11-19',
            'source': 'Cloud Computing'
        },
        {
            'title': '삼성전자, 갤럭시 S25 사전 예약 시작',
            'description': '삼성전자가 신제품 갤럭시 S25의 사전 예약을 개시했다.',
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
        {
            'title': 'SK하이닉스, HBM3E 본격 양산',
            'description': 'SK하이닉스가 차세대 고대역폭 메모리 HBM3E 양산을 시작했다.',
            'link': 'https://example.com/news14',
            'published': '2025-11-19',
            'source': 'Semiconductor Today'
        },
        {
            'title': 'Meta, AI 모델 Llama 4 공개',
            'description': 'Meta가 차세대 AI 언어 모델 Llama 4를 오픈소스로 공개했다.',
            'link': 'https://example.com/news15',
            'published': '2025-11-19',
            'source': 'AI News'
        },
        {
            'title': 'LG전자, 가전 로봇 라인업 확대',
            'description': 'LG전자가 AI 기반 가전 로봇 신제품을 대거 출시한다.',
            'link': 'https://example.com/news16',
            'published': '2025-11-19',
            'source': 'Home Appliance'
        },
        {
            'title': 'Intel, 차세대 프로세서 발표',
            'description': 'Intel이 Arrow Lake 프로세서를 정식 발표했다.',
            'link': 'https://example.com/news17',
            'published': '2025-11-19',
            'source': 'CPU World'
        },
        {
            'title': '네이버, AI 검색 기능 업그레이드',
            'description': '네이버가 AI 기반 검색 엔진을 대폭 개선했다.',
            'link': 'https://example.com/news18',
            'published': '2025-11-19',
            'source': 'Internet News'
        },
        {
            'title': 'Microsoft, 클라우드 게임 서비스 확장',
            'description': 'Microsoft가 Xbox Cloud Gaming을 50개국으로 확대한다.',
            'link': 'https://example.com/news19',
            'published': '2025-11-19',
            'source': 'Gaming News'
        },
        {
            'title': '카카오, 모빌리티 사업 성장',
            'description': '카카오모빌리티의 이용자 수가 2천만을 돌파했다.',
            'link': 'https://example.com/news20',
            'published': '2025-11-19',
            'source': 'Mobility Today'
        },
    ]


def main():
    """메인 실행 함수"""

    print("=" * 60)
    print("📈 Trending Stocks Tracker - DEMO MODE")
    print("=" * 60)
    print(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 1. 샘플 뉴스 생성
    print("📰 샘플 뉴스 데이터 생성...")
    articles = generate_sample_news()
    print(f"✅ 총 {len(articles)}개 샘플 뉴스 생성 완료\n")

    # 2. 회사명 분석
    analyzer = CompanyAnalyzer()
    analyzer.analyze_articles(articles)

    # 3. 상위 10개 회사 추출
    top_companies = analyzer.get_top_companies(config.TOP_N_COMPANIES)

    if not top_companies:
        print("❌ 발견된 회사가 없습니다.")
        return

    print("\n" + "=" * 60)
    print("🏆 오늘의 상위 10개 트렌딩 회사")
    print("=" * 60)

    for idx, (company, count) in enumerate(top_companies, 1):
        print(f"{idx:2d}. {company:20s} - {count:3d} mentions")

    # 4. 상세 정보 수집
    companies_details = []
    for company, count in top_companies:
        details = analyzer.get_company_details(company)
        companies_details.append(details)

    # 5. 데이터 저장
    output_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'timestamp': datetime.now().isoformat(),
        'mode': 'demo',
        'top_companies': [
            {
                'rank': idx,
                'name': company,
                'mentions': count,
                'articles': analyzer.company_articles.get(company, [])[:3]
            }
            for idx, (company, count) in enumerate(top_companies, 1)
        ]
    }

    with open(config.TRENDING_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n💾 데이터 저장: {config.TRENDING_FILE}")

    # 6. 시각화
    visualizer = Visualizer()
    chart_path = visualizer.plot_top_companies(top_companies)
    report_path = visualizer.create_report(companies_details)

    print("\n" + "=" * 60)
    print("✅ 분석 완료!")
    print("=" * 60)
    print(f"📊 차트: {chart_path}")
    print(f"📄 리포트: {report_path}")
    print(f"💾 데이터: {config.TRENDING_FILE}")
    print("\n💡 데모 모드로 실행되었습니다.")
    print("   실제 뉴스 데이터를 사용하려면 뉴스 API를 설정하세요.")


if __name__ == '__main__':
    main()
