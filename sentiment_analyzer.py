"""
감성 분석 모듈
뉴스 기사의 감성(긍정/부정/중립)을 분석합니다.
"""
from typing import Dict, List


class SentimentAnalyzer:
    """감성 분석 클래스"""

    # 긍정 키워드
    POSITIVE_KEYWORDS = [
        # 한국어
        '상승', '급등', '호조', '성장', '증가', '최고', '사상', '돌파', '성공',
        '확대', '강세', '개선', '긍정', '발전', '혁신', '선도', '1위', '우수',
        '수익', '이익', '흑자', '실적', '호실적', '신기록', '최대', '최고치',
        '선정', '수상', '획득', '달성', '개발', '출시', '투자', '확장',

        # 영어
        'surge', 'soar', 'jump', 'rise', 'gain', 'growth', 'increase',
        'strong', 'positive', 'success', 'best', 'record', 'high', 'profit',
        'revenue', 'beat', 'exceed', 'outperform', 'bullish', 'upgrade',
        'innovation', 'breakthrough', 'launch', 'expansion', 'award',
    ]

    # 부정 키워드
    NEGATIVE_KEYWORDS = [
        # 한국어
        '하락', '급락', '부진', '감소', '하락세', '악화', '우려', '위기', '손실',
        '적자', '폭락', '추락', '실망', '부정', '문제', '리스크', '타격', '침체',
        '하향', '축소', '철수', '중단', '취소', '지연', '실패', '경고',

        # 영어
        'fall', 'drop', 'decline', 'plunge', 'loss', 'negative', 'weak',
        'concern', 'risk', 'crisis', 'failure', 'disappointing', 'bearish',
        'downgrade', 'miss', 'underperform', 'warning', 'cut', 'reduce',
        'suspend', 'delay', 'cancel', 'struggle', 'crash', 'slump',
    ]

    # 중립/객관 키워드
    NEUTRAL_KEYWORDS = [
        '발표', '예정', '계획', '진행', '검토', '논의', '보도', '전망',
        'announce', 'plan', 'schedule', 'report', 'consider', 'discuss',
    ]

    def __init__(self):
        """초기화"""
        pass

    def analyze_text(self, text: str) -> Dict:
        """
        텍스트의 감성 분석

        Args:
            text: 분석할 텍스트

        Returns:
            감성 분석 결과 {'sentiment': str, 'score': float, 'confidence': float}
        """
        text_lower = text.lower()

        # 키워드 카운트
        positive_count = sum(1 for keyword in self.POSITIVE_KEYWORDS if keyword in text_lower)
        negative_count = sum(1 for keyword in self.NEGATIVE_KEYWORDS if keyword in text_lower)
        neutral_count = sum(1 for keyword in self.NEUTRAL_KEYWORDS if keyword in text_lower)

        total_keywords = positive_count + negative_count + neutral_count

        # 점수 계산 (-1 ~ 1)
        if total_keywords == 0:
            score = 0
            sentiment = 'neutral'
            confidence = 0.3  # 낮은 신뢰도
        else:
            score = (positive_count - negative_count) / max(total_keywords, 1)
            confidence = min(total_keywords / 5, 1.0)  # 최대 1.0

            # 감성 분류
            if score > 0.2:
                sentiment = 'positive'
            elif score < -0.2:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'

        return {
            'sentiment': sentiment,
            'score': round(score, 3),
            'confidence': round(confidence, 3),
            'keywords': {
                'positive': positive_count,
                'negative': negative_count,
                'neutral': neutral_count,
            }
        }

    def analyze_article(self, article: Dict) -> Dict:
        """
        뉴스 기사 감성 분석

        Args:
            article: 뉴스 기사 딕셔너리

        Returns:
            감성 분석이 포함된 기사 딕셔너리
        """
        # 제목과 설명 합치기
        text = f"{article.get('title', '')} {article.get('description', '')}"

        # 감성 분석
        sentiment = self.analyze_text(text)

        # 기사에 감성 정보 추가
        article_with_sentiment = article.copy()
        article_with_sentiment['sentiment'] = sentiment

        return article_with_sentiment

    def analyze_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        여러 뉴스 기사 감성 분석

        Args:
            articles: 뉴스 기사 리스트

        Returns:
            감성 분석이 포함된 기사 리스트
        """
        return [self.analyze_article(article) for article in articles]

    def get_sentiment_summary(self, articles: List[Dict]) -> Dict:
        """
        기사들의 전체 감성 요약

        Args:
            articles: 감성 분석된 기사 리스트

        Returns:
            감성 요약 통계
        """
        if not articles:
            return {
                'total': 0,
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'average_score': 0,
            }

        sentiments = [a.get('sentiment', {}) for a in articles if 'sentiment' in a]

        positive = sum(1 for s in sentiments if s.get('sentiment') == 'positive')
        negative = sum(1 for s in sentiments if s.get('sentiment') == 'negative')
        neutral = sum(1 for s in sentiments if s.get('sentiment') == 'neutral')

        avg_score = sum(s.get('score', 0) for s in sentiments) / len(sentiments) if sentiments else 0

        return {
            'total': len(articles),
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'positive_percent': round(positive / len(articles) * 100, 1) if articles else 0,
            'negative_percent': round(negative / len(articles) * 100, 1) if articles else 0,
            'neutral_percent': round(neutral / len(articles) * 100, 1) if articles else 0,
            'average_score': round(avg_score, 3),
        }

    def get_company_sentiment(self, company_articles: List[Dict]) -> Dict:
        """
        특정 회사에 대한 감성 분석

        Args:
            company_articles: 회사 관련 기사 리스트

        Returns:
            회사 감성 요약
        """
        analyzed = self.analyze_articles(company_articles)
        summary = self.get_sentiment_summary(analyzed)

        # 전체 감성 판단
        if summary['average_score'] > 0.2:
            overall = 'positive'
            emoji = '📈'
        elif summary['average_score'] < -0.2:
            overall = 'negative'
            emoji = '📉'
        else:
            overall = 'neutral'
            emoji = '➡️'

        return {
            'overall_sentiment': overall,
            'emoji': emoji,
            'summary': summary,
            'analyzed_articles': analyzed,
        }
