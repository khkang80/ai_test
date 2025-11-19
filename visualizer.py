"""
데이터 시각화 모듈
트렌딩 회사 데이터를 시각화합니다.
"""
import matplotlib.pyplot as plt
import matplotlib
from typing import List, Tuple
from pathlib import Path
import config

# 한글 폰트 설정 (Linux 환경)
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['axes.unicode_minus'] = False


class Visualizer:
    """시각화 클래스"""

    def __init__(self, output_dir: Path = None):
        """
        Args:
            output_dir: 출력 디렉토리
        """
        self.output_dir = output_dir or config.REPORTS_DIR
        self.output_dir.mkdir(exist_ok=True)

    def plot_top_companies(self, companies: List[Tuple[str, int]],
                          title: str = "Top 10 Trending Companies") -> str:
        """
        상위 회사 바 차트 생성

        Args:
            companies: (회사명, 언급횟수) 튜플 리스트
            title: 차트 제목

        Returns:
            저장된 파일 경로
        """
        if not companies:
            print("표시할 데이터가 없습니다.")
            return ""

        # 데이터 분리
        names = [c[0] for c in companies]
        counts = [c[1] for c in companies]

        # 차트 생성
        plt.figure(figsize=(12, 8))
        bars = plt.barh(names, counts, color='steelblue')

        # 막대 위에 숫자 표시
        for i, (bar, count) in enumerate(zip(bars, counts)):
            plt.text(count + 0.5, i, str(count),
                    va='center', fontweight='bold')

        plt.xlabel('Mentions Count', fontsize=12, fontweight='bold')
        plt.title(title, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()

        # 저장
        output_path = self.output_dir / 'trending_companies.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"📊 차트 저장: {output_path}")
        return str(output_path)

    def create_report(self, companies_data: List[dict]) -> str:
        """
        HTML 리포트 생성

        Args:
            companies_data: 회사 상세 정보 리스트

        Returns:
            저장된 파일 경로
        """
        from datetime import datetime

        html = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Trending Companies Report</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                .company {{
                    background: white;
                    margin: 20px 0;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .company h2 {{
                    color: #3498db;
                    margin-top: 0;
                }}
                .mentions {{
                    background: #3498db;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                    display: inline-block;
                    font-weight: bold;
                }}
                .articles {{
                    margin-top: 15px;
                }}
                .article {{
                    padding: 10px;
                    margin: 5px 0;
                    background: #f8f9fa;
                    border-left: 3px solid #3498db;
                }}
                .article a {{
                    color: #2c3e50;
                    text-decoration: none;
                    font-weight: 500;
                }}
                .article a:hover {{
                    color: #3498db;
                    text-decoration: underline;
                }}
                .timestamp {{
                    color: #7f8c8d;
                    font-size: 0.9em;
                    margin-top: 20px;
                }}
                .rank {{
                    background: #e74c3c;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 50%;
                    display: inline-block;
                    width: 30px;
                    height: 30px;
                    text-align: center;
                    line-height: 30px;
                    font-weight: bold;
                    margin-right: 10px;
                }}
            </style>
        </head>
        <body>
            <h1>📈 Today's Trending Companies</h1>
            <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        """

        for idx, company in enumerate(companies_data, 1):
            html += f"""
            <div class="company">
                <h2>
                    <span class="rank">{idx}</span>
                    {company['name']}
                    <span class="mentions">{company['mentions']} mentions</span>
                </h2>
                <div class="articles">
                    <h3>Recent Articles:</h3>
            """

            for article in company['articles'][:5]:
                html += f"""
                    <div class="article">
                        <a href="{article.get('link', '#')}" target="_blank">
                            {article.get('title', 'No title')}
                        </a>
                        <div style="font-size: 0.85em; color: #7f8c8d; margin-top: 5px;">
                            {article.get('published', '')}
                        </div>
                    </div>
                """

            html += """
                </div>
            </div>
            """

        html += """
        </body>
        </html>
        """

        output_path = self.output_dir / 'trending_report.html'
        output_path.write_text(html, encoding='utf-8')

        print(f"📄 리포트 저장: {output_path}")
        return str(output_path)
