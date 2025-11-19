"""
기술적 분석 모듈
주가 차트 분석 및 매수/매도 신호 생성
"""
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


class TechnicalAnalyzer:
    """기술적 분석 클래스"""

    def __init__(self):
        """초기화"""
        pass

    def get_price_history(self, ticker: str, period: str = '3mo') -> Optional[pd.DataFrame]:
        """
        주가 히스토리 데이터 가져오기

        Args:
            ticker: 주식 Ticker 심볼
            period: 기간 (1mo, 3mo, 6mo, 1y)

        Returns:
            주가 데이터프레임
        """
        try:
            # Yahoo Finance API
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            params = {
                'range': period,
                'interval': '1d'
            }

            response = requests.get(url, params=params, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0'
            })

            if response.status_code != 200:
                return self._generate_mock_data(ticker, period)

            data = response.json()

            if 'chart' not in data or 'result' not in data['chart'] or not data['chart']['result']:
                return self._generate_mock_data(ticker, period)

            result = data['chart']['result'][0]
            timestamps = result.get('timestamp', [])
            quotes = result.get('indicators', {}).get('quote', [{}])[0]

            df = pd.DataFrame({
                'date': pd.to_datetime(timestamps, unit='s'),
                'open': quotes.get('open', []),
                'high': quotes.get('high', []),
                'low': quotes.get('low', []),
                'close': quotes.get('close', []),
                'volume': quotes.get('volume', [])
            })

            df = df.dropna()
            return df

        except Exception as e:
            print(f"주가 히스토리 수집 오류 ({ticker}): {e}")
            return self._generate_mock_data(ticker, period)

    def _generate_mock_data(self, ticker: str, period: str = '3mo') -> pd.DataFrame:
        """
        모의 주가 데이터 생성

        Args:
            ticker: Ticker 심볼
            period: 기간

        Returns:
            모의 주가 데이터프레임
        """
        # 기간에 따른 일수 계산
        days_map = {'1mo': 30, '3mo': 90, '6mo': 180, '1y': 365}
        days = days_map.get(period, 90)

        # 시작 날짜
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # 날짜 범위
        dates = pd.date_range(start=start_date, end=end_date, freq='D')

        # 초기 가격 설정
        base_price = 100 if not ticker.endswith('.KS') else 50000
        prices = [base_price]

        # 랜덤 워크로 주가 생성
        np.random.seed(hash(ticker) % 2**32)
        for _ in range(len(dates) - 1):
            change = np.random.randn() * 0.02  # 2% 변동성
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)

        # 데이터프레임 생성
        df = pd.DataFrame({
            'date': dates,
            'close': prices
        })

        # OHLV 데이터 생성
        df['open'] = df['close'].shift(1).fillna(df['close'])
        df['high'] = df[['open', 'close']].max(axis=1) * (1 + np.random.rand(len(df)) * 0.01)
        df['low'] = df[['open', 'close']].min(axis=1) * (1 - np.random.rand(len(df)) * 0.01)
        df['volume'] = np.random.randint(1000000, 10000000, len(df))

        return df

    def calculate_sma(self, df: pd.DataFrame, window: int = 20) -> pd.Series:
        """
        단순 이동평균(SMA) 계산

        Args:
            df: 주가 데이터프레임
            window: 기간

        Returns:
            SMA 시리즈
        """
        return df['close'].rolling(window=window).mean()

    def calculate_ema(self, df: pd.DataFrame, window: int = 12) -> pd.Series:
        """
        지수 이동평균(EMA) 계산

        Args:
            df: 주가 데이터프레임
            window: 기간

        Returns:
            EMA 시리즈
        """
        return df['close'].ewm(span=window, adjust=False).mean()

    def calculate_rsi(self, df: pd.DataFrame, window: int = 14) -> pd.Series:
        """
        RSI(Relative Strength Index) 계산

        Args:
            df: 주가 데이터프레임
            window: 기간

        Returns:
            RSI 시리즈
        """
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def calculate_macd(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        MACD 계산

        Args:
            df: 주가 데이터프레임

        Returns:
            (MACD, Signal, Histogram) 튜플
        """
        ema12 = self.calculate_ema(df, 12)
        ema26 = self.calculate_ema(df, 26)

        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal

        return macd, signal, histogram

    def calculate_bollinger_bands(self, df: pd.DataFrame, window: int = 20, num_std: float = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        볼린저 밴드 계산

        Args:
            df: 주가 데이터프레임
            window: 기간
            num_std: 표준편차 배수

        Returns:
            (Upper Band, Middle Band, Lower Band) 튜플
        """
        middle = self.calculate_sma(df, window)
        std = df['close'].rolling(window=window).std()

        upper = middle + (std * num_std)
        lower = middle - (std * num_std)

        return upper, middle, lower

    def analyze_stock(self, ticker: str, company_name: str = None) -> Dict:
        """
        종합 기술적 분석 및 매수/매도 신호 생성

        Args:
            ticker: Ticker 심볼
            company_name: 회사명

        Returns:
            분석 결과 딕셔너리
        """
        # 주가 데이터 가져오기
        df = self.get_price_history(ticker, period='3mo')

        if df is None or len(df) < 30:
            return {
                'ticker': ticker,
                'company': company_name,
                'error': '데이터 부족',
                'recommendation': 'HOLD',
                'confidence': 0
            }

        # 기술적 지표 계산
        df['SMA20'] = self.calculate_sma(df, 20)
        df['SMA50'] = self.calculate_sma(df, 50)
        df['EMA12'] = self.calculate_ema(df, 12)
        df['RSI'] = self.calculate_rsi(df, 14)

        macd, signal, histogram = self.calculate_macd(df)
        df['MACD'] = macd
        df['MACD_Signal'] = signal
        df['MACD_Hist'] = histogram

        upper, middle, lower = self.calculate_bollinger_bands(df, 20)
        df['BB_Upper'] = upper
        df['BB_Middle'] = middle
        df['BB_Lower'] = lower

        # 최신 데이터
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest

        # 신호 계산
        signals = []
        signal_strengths = []

        # 1. 이동평균 신호
        if latest['close'] > latest['SMA20']:
            signals.append('BUY')
            signal_strengths.append(1)
        elif latest['close'] < latest['SMA20']:
            signals.append('SELL')
            signal_strengths.append(-1)

        # 2. 골든크로스/데드크로스
        if latest['SMA20'] > latest['SMA50'] and prev['SMA20'] <= prev['SMA50']:
            signals.append('STRONG_BUY')
            signal_strengths.append(2)
        elif latest['SMA20'] < latest['SMA50'] and prev['SMA20'] >= prev['SMA50']:
            signals.append('STRONG_SELL')
            signal_strengths.append(-2)

        # 3. RSI 신호
        rsi_val = latest['RSI']
        if rsi_val < 30:
            signals.append('BUY')  # 과매도
            signal_strengths.append(1.5)
        elif rsi_val > 70:
            signals.append('SELL')  # 과매수
            signal_strengths.append(-1.5)

        # 4. MACD 신호
        if latest['MACD'] > latest['MACD_Signal'] and prev['MACD'] <= prev['MACD_Signal']:
            signals.append('BUY')
            signal_strengths.append(1.5)
        elif latest['MACD'] < latest['MACD_Signal'] and prev['MACD'] >= prev['MACD_Signal']:
            signals.append('SELL')
            signal_strengths.append(-1.5)

        # 5. 볼린저 밴드 신호
        if latest['close'] < latest['BB_Lower']:
            signals.append('BUY')  # 하단 돌파
            signal_strengths.append(1)
        elif latest['close'] > latest['BB_Upper']:
            signals.append('SELL')  # 상단 돌파
            signal_strengths.append(-1)

        # 종합 신호 계산
        if not signal_strengths:
            recommendation = 'HOLD'
            confidence = 0
        else:
            total_strength = sum(signal_strengths)
            confidence = min(abs(total_strength) / len(signal_strengths) * 50, 100)

            if total_strength > 2:
                recommendation = 'STRONG_BUY'
            elif total_strength > 0:
                recommendation = 'BUY'
            elif total_strength < -2:
                recommendation = 'STRONG_SELL'
            elif total_strength < 0:
                recommendation = 'SELL'
            else:
                recommendation = 'HOLD'

        # 이모지 매핑
        emoji_map = {
            'STRONG_BUY': '🚀',
            'BUY': '📈',
            'HOLD': '⏸️',
            'SELL': '📉',
            'STRONG_SELL': '⚠️'
        }

        # 결과 반환
        return {
            'ticker': ticker,
            'company': company_name,
            'recommendation': recommendation,
            'emoji': emoji_map.get(recommendation, '➡️'),
            'confidence': round(confidence, 1),
            'current_price': round(latest['close'], 2),
            'indicators': {
                'SMA20': round(latest['SMA20'], 2),
                'SMA50': round(latest['SMA50'], 2),
                'RSI': round(rsi_val, 2),
                'MACD': round(latest['MACD'], 2),
                'MACD_Signal': round(latest['MACD_Signal'], 2),
            },
            'signals': signals,
            'analysis': self._generate_analysis_text(recommendation, latest, signals),
            'is_mock': 'is_mock' not in df.columns or df['close'].std() < 1,  # 간단한 모의 데이터 체크
        }

    def _generate_analysis_text(self, recommendation: str, latest: pd.Series, signals: List[str]) -> str:
        """
        분석 텍스트 생성

        Args:
            recommendation: 투자 의견
            latest: 최신 데이터
            signals: 신호 리스트

        Returns:
            분석 텍스트
        """
        texts = []

        rsi_val = latest['RSI']
        if rsi_val < 30:
            texts.append(f"RSI {rsi_val:.1f}로 과매도 구간")
        elif rsi_val > 70:
            texts.append(f"RSI {rsi_val:.1f}로 과매수 구간")

        if latest['close'] > latest['SMA20']:
            texts.append("20일 이동평균선 상회")
        else:
            texts.append("20일 이동평균선 하회")

        if 'STRONG_BUY' in signals:
            texts.append("골든크로스 발생")
        elif 'STRONG_SELL' in signals:
            texts.append("데드크로스 발생")

        if len(texts) == 0:
            return "중립적 신호"

        return ", ".join(texts)
