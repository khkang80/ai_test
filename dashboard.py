#!/usr/bin/env python3
"""
Trending Stocks Tracker - Web Dashboard
Streamlit을 사용한 인터랙티브 웹 대시보드
"""
import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import pandas as pd

import config
from company_analyzer import CompanyAnalyzer
from sentiment_analyzer import SentimentAnalyzer
from stock_data import StockDataCollector


# 페이지 설정
st.set_page_config(
    page_title="Trending Stocks Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_data():
    """저장된 데이터 로드"""
    data_file = config.DATA_DIR / 'trending_companies_enhanced.json'
    if data_file.exists():
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def generate_sample_news():
    """샘플 뉴스 데이터"""
    return [
        {
            'title': '삼성전자, AI 반도체 시장 점유율 30% 돌파',
            'description': '삼성전자가 인공지능 반도체 시장에서 30% 점유율을 달성하며 업계 1위로 올라섰다.',
            'published': '2025-11-19'
        },
        {
            'title': 'Apple, 새로운 Vision Pro 2 발표 예정',
            'description': 'Apple이 다음 달 Vision Pro 2를 공개할 예정이라고 밝혔다.',
            'published': '2025-11-19'
        },
        {
            'title': 'Tesla 주가 급등, 전기차 판매 호조',
            'description': 'Tesla의 3분기 전기차 판매가 예상을 크게 상회하며 주가가 15% 상승했다.',
            'published': '2025-11-19'
        },
        {
            'title': 'NVIDIA, 신형 GPU 출시로 주가 사상 최고치',
            'description': 'NVIDIA가 차세대 Blackwell GPU를 출시하며 주가가 사상 최고치를 경신했다.',
            'published': '2025-11-19'
        },
        {
            'title': '네이버, 하이퍼클로바X 글로벌 진출',
            'description': '네이버가 자체 개발한 AI를 동남아시아에 출시한다.',
            'published': '2025-11-19'
        },
    ]


def main():
    # 헤더
    st.title("📈 Trending Stocks Tracker")
    st.markdown("### 뉴스 기반 트렌딩 회사 분석 대시보드")
    st.markdown("---")

    # 사이드바
    with st.sidebar:
        st.header("⚙️ 설정")

        if st.button("🔄 데이터 새로고침", use_container_width=True):
            st.rerun()

        st.markdown("---")
        st.markdown("### 📊 통계")

        data = load_data()
        if data:
            st.metric("분석 일자", data.get('date', 'N/A'))
            st.metric("분석 회사 수", len(data.get('top_companies', [])))

            sentiment_summary = data.get('sentiment_summary', {})
            st.metric("긍정 뉴스", f"{sentiment_summary.get('positive_percent', 0)}%")
            st.metric("평균 감성 점수", f"{sentiment_summary.get('average_score', 0):.2f}")

    # 메인 컨텐츠
    data = load_data()

    if not data:
        st.warning("⚠️ 데이터가 없습니다. demo_enhanced.py를 먼저 실행하세요.")
        st.code("python3 demo_enhanced.py")
        return

    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["📊 트렌딩 회사", "🎭 감성 분석", "📰 뉴스"])

    # 탭 1: 트렌딩 회사
    with tab1:
        st.header("🏆 상위 10개 트렌딩 회사")

        companies = data.get('top_companies', [])

        # 테이블 데이터 준비
        table_data = []
        for company in companies:
            sentiment_emoji = company.get('sentiment_emoji', '➡️')
            stock_change = company.get('stock_change', 0) or 0
            stock_emoji = '📈' if stock_change > 0 else '📉' if stock_change < 0 else '➡️'

            table_data.append({
                '순위': company.get('rank', 0),
                '회사명': company.get('name', ''),
                '언급': f"{company.get('mentions', 0)}회",
                '감성': f"{sentiment_emoji} {company.get('sentiment', 'neutral')}",
                '감성점수': f"{company.get('sentiment_score', 0):.2f}",
                '주가': f"{company.get('stock_price', 'N/A')}",
                '변동': f"{stock_emoji} {stock_change:.2f}%" if company.get('stock_price') else 'N/A',
            })

        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 상위 3개 회사 상세 정보
        st.markdown("---")
        st.subheader("🔍 상위 3개 회사 상세 정보")

        cols = st.columns(3)
        for idx, company in enumerate(companies[:3]):
            with cols[idx]:
                st.markdown(f"### {idx+1}. {company.get('name', '')}")
                st.metric("언급 횟수", f"{company.get('mentions', 0)}회")

                sentiment = company.get('sentiment', 'neutral')
                sentiment_emoji = company.get('sentiment_emoji', '➡️')
                st.metric("감성", f"{sentiment_emoji} {sentiment}")

                stock_price = company.get('stock_price')
                if stock_price:
                    currency = company.get('stock_currency', '')
                    st.metric("주가", f"{stock_price:,.2f} {currency}")

                    stock_change = company.get('stock_change', 0) or 0
                    st.metric("변동률", f"{stock_change:+.2f}%")

    # 탭 2: 감성 분석
    with tab2:
        st.header("🎭 전체 감성 분석")

        sentiment_summary = data.get('sentiment_summary', {})

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("총 뉴스 수", sentiment_summary.get('total', 0))
        with col2:
            st.metric("긍정 뉴스",
                     f"{sentiment_summary.get('positive', 0)}개",
                     delta=f"{sentiment_summary.get('positive_percent', 0):.1f}%")
        with col3:
            st.metric("부정 뉴스",
                     f"{sentiment_summary.get('negative', 0)}개",
                     delta=f"-{sentiment_summary.get('negative_percent', 0):.1f}%",
                     delta_color="inverse")
        with col4:
            st.metric("중립 뉴스", f"{sentiment_summary.get('neutral', 0)}개")

        # 감성 분포 차트
        st.markdown("---")
        st.subheader("📊 감성 분포")

        sentiment_data = pd.DataFrame({
            '감성': ['긍정', '부정', '중립'],
            '개수': [
                sentiment_summary.get('positive', 0),
                sentiment_summary.get('negative', 0),
                sentiment_summary.get('neutral', 0)
            ],
            '비율': [
                sentiment_summary.get('positive_percent', 0),
                sentiment_summary.get('negative_percent', 0),
                sentiment_summary.get('neutral_percent', 0)
            ]
        })

        st.bar_chart(sentiment_data.set_index('감성')['개수'])

        # 회사별 감성
        st.markdown("---")
        st.subheader("🏢 회사별 감성 분석")

        companies = data.get('top_companies', [])
        company_sentiment = pd.DataFrame([
            {
                '회사명': c.get('name', ''),
                '감성': c.get('sentiment', 'neutral'),
                '감성 점수': c.get('sentiment_score', 0),
                '이모지': c.get('sentiment_emoji', '➡️')
            }
            for c in companies
        ])

        st.dataframe(company_sentiment, use_container_width=True, hide_index=True)

    # 탭 3: 뉴스
    with tab3:
        st.header("📰 최근 뉴스")

        companies = data.get('top_companies', [])

        # 회사 선택
        company_names = [c.get('name', '') for c in companies]
        selected_company = st.selectbox("회사 선택", ['전체'] + company_names)

        # 뉴스 표시
        if selected_company == '전체':
            for company in companies[:5]:
                with st.expander(f"{company.get('name', '')} ({company.get('mentions', 0)}개 언급)"):
                    for article in company.get('articles', []):
                        st.markdown(f"**{article.get('title', '')}**")
                        st.caption(article.get('published', ''))
                        st.markdown("---")
        else:
            selected_data = next((c for c in companies if c.get('name') == selected_company), None)
            if selected_data:
                st.subheader(f"{selected_company} 관련 뉴스")

                for article in selected_data.get('articles', []):
                    with st.container():
                        st.markdown(f"### {article.get('title', '')}")
                        st.caption(f"📅 {article.get('published', '')}")
                        if article.get('link'):
                            st.markdown(f"[뉴스 읽기]({article.get('link')})")
                        st.markdown("---")

    # 푸터
    st.markdown("---")
    st.caption("💡 Trending Stocks Tracker - 뉴스 기반 투자 인사이트")
    st.caption(f"마지막 업데이트: {data.get('timestamp', 'N/A')}")


if __name__ == '__main__':
    main()
