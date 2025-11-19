#!/usr/bin/env python3
"""
Trending Stocks Tracker - Main Entry Point
매일 뉴스에서 가장 이슈가 되는 상위 10개 회사를 추적합니다.
"""
import json
from datetime import datetime
from pathlib import Path

import config
from news_collector import NewsCollector
from company_analyzer import CompanyAnalyzer
from visualizer import Visualizer


def main():
    """메인 실행 함수"""

    print("=" * 60)
    print("📈 Trending Stocks Tracker")
    print("=" * 60)
    print(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 1. 뉴스 수집
    collector = NewsCollector(config.NEWS_SOURCES)
    articles = collector.collect_all()

    if not articles:
        print("❌ 수집된 뉴스가 없습니다.")
        return

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
    print("\n리포트를 브라우저로 열어보세요!")


if __name__ == '__main__':
    main()
