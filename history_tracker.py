"""
시계열 분석 및 히스토리 추적 모듈
"""
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import config


class HistoryTracker:
    """히스토리 추적 클래스"""

    def __init__(self, history_file: Path = None):
        """
        Args:
            history_file: 히스토리 파일 경로
        """
        self.history_file = history_file or (config.DATA_DIR / 'history.json')
        self.history = self._load_history()

    def _load_history(self) -> List[Dict]:
        """히스토리 로드"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _save_history(self):
        """히스토리 저장"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def add_snapshot(self, data: Dict):
        """
        현재 스냅샷 추가

        Args:
            data: 저장할 데이터
        """
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'data': data
        }

        self.history.append(snapshot)
        self._save_history()

        print(f"✅ 히스토리 저장: {len(self.history)}개 스냅샷")

    def get_history(self, days: int = 30) -> List[Dict]:
        """
        최근 N일 히스토리 가져오기

        Args:
            days: 조회할 일수

        Returns:
            히스토리 리스트
        """
        return self.history[-days:]

    def get_company_trend(self, company: str, days: int = 7) -> pd.DataFrame:
        """
        특정 회사의 트렌드 분석

        Args:
            company: 회사명
            days: 분석 기간

        Returns:
            트렌드 데이터프레임
        """
        recent = self.get_history(days)

        trend_data = []
        for snapshot in recent:
            date = snapshot['date']
            companies = snapshot['data'].get('top_companies', [])

            # 해당 회사 찾기
            company_data = next((c for c in companies if c.get('name') == company), None)

            if company_data:
                trend_data.append({
                    'date': date,
                    'rank': company_data.get('rank', None),
                    'mentions': company_data.get('mentions', 0),
                    'sentiment_score': company_data.get('sentiment_score', 0),
                    'stock_price': company_data.get('stock_price'),
                    'stock_change': company_data.get('stock_change', 0),
                })
            else:
                # 순위권 밖
                trend_data.append({
                    'date': date,
                    'rank': None,
                    'mentions': 0,
                    'sentiment_score': 0,
                    'stock_price': None,
                    'stock_change': 0,
                })

        return pd.DataFrame(trend_data)

    def get_trending_changes(self) -> Dict:
        """
        트렌드 변화 분석 (이전 대비)

        Returns:
            변화 분석 결과
        """
        if len(self.history) < 2:
            return {'message': '비교할 데이터가 부족합니다.'}

        previous = self.history[-2]['data'].get('top_companies', [])
        current = self.history[-1]['data'].get('top_companies', [])

        # 이전 순위 맵
        prev_ranks = {c.get('name'): c.get('rank') for c in previous}
        curr_ranks = {c.get('name'): c.get('rank') for c in current}

        # 변화 분석
        new_entries = []  # 새로 진입
        dropped = []      # 순위권 밖
        rising = []       # 순위 상승
        falling = []      # 순위 하락

        for company, curr_rank in curr_ranks.items():
            prev_rank = prev_ranks.get(company)

            if prev_rank is None:
                new_entries.append({'name': company, 'rank': curr_rank})
            elif prev_rank > curr_rank:
                rising.append({
                    'name': company,
                    'from': prev_rank,
                    'to': curr_rank,
                    'change': prev_rank - curr_rank
                })
            elif prev_rank < curr_rank:
                falling.append({
                    'name': company,
                    'from': prev_rank,
                    'to': curr_rank,
                    'change': curr_rank - prev_rank
                })

        for company, prev_rank in prev_ranks.items():
            if company not in curr_ranks:
                dropped.append({'name': company, 'rank': prev_rank})

        return {
            'new_entries': new_entries,
            'dropped': dropped,
            'rising': sorted(rising, key=lambda x: x['change'], reverse=True),
            'falling': sorted(falling, key=lambda x: x['change'], reverse=True),
        }

    def get_summary_stats(self) -> Dict:
        """
        전체 통계 요약

        Returns:
            통계 딕셔너리
        """
        if not self.history:
            return {'message': '데이터가 없습니다.'}

        # 가장 자주 등장한 회사
        all_companies = {}
        for snapshot in self.history:
            companies = snapshot['data'].get('top_companies', [])
            for company in companies:
                name = company.get('name')
                if name:
                    if name not in all_companies:
                        all_companies[name] = {
                            'appearances': 0,
                            'total_mentions': 0,
                            'avg_rank': 0,
                            'ranks': []
                        }
                    all_companies[name]['appearances'] += 1
                    all_companies[name]['total_mentions'] += company.get('mentions', 0)
                    all_companies[name]['ranks'].append(company.get('rank', 0))

        # 평균 순위 계산
        for company in all_companies.values():
            if company['ranks']:
                company['avg_rank'] = sum(company['ranks']) / len(company['ranks'])

        # 상위 등장 빈도 회사
        top_frequent = sorted(
            all_companies.items(),
            key=lambda x: x[1]['appearances'],
            reverse=True
        )[:10]

        return {
            'total_snapshots': len(self.history),
            'total_companies': len(all_companies),
            'most_frequent': [
                {
                    'name': name,
                    'appearances': data['appearances'],
                    'avg_rank': round(data['avg_rank'], 1),
                    'total_mentions': data['total_mentions']
                }
                for name, data in top_frequent
            ]
        }

    def export_to_csv(self, output_file: Path = None):
        """
        히스토리를 CSV로 내보내기

        Args:
            output_file: 출력 파일 경로
        """
        output_file = output_file or (config.DATA_DIR / 'history.csv')

        rows = []
        for snapshot in self.history:
            date = snapshot['date']
            companies = snapshot['data'].get('top_companies', [])

            for company in companies:
                rows.append({
                    'date': date,
                    'rank': company.get('rank'),
                    'company': company.get('name'),
                    'mentions': company.get('mentions'),
                    'sentiment': company.get('sentiment'),
                    'sentiment_score': company.get('sentiment_score'),
                    'stock_price': company.get('stock_price'),
                    'stock_change': company.get('stock_change'),
                })

        df = pd.DataFrame(rows)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')

        print(f"✅ CSV 내보내기: {output_file}")
        return output_file
