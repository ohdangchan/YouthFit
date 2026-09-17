import argparse
import logging
import os
import sys
from contextlib import suppress

# 현재 스크립트 디렉토리 및 프로젝트 루트 디렉토리를 sys.path에 등록
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
for p in [CURRENT_DIR, PROJECT_ROOT]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from scripts import db_connection
    from scripts.crawlers.bs4_crawler import (
        Bs4Crawler,
        BusanYouthCrawler,
        DaeguYouthCrawler,
        GwangjuYouthCrawler,
        IncheonYouthCrawler,
        ShHousingCrawler,
    )
    from scripts.crawlers.hidden_api_crawler import (
        GyeonggiJobabaCrawler,
        HiddenApiCrawler,
        SeoulYouthCrawler,
    )
    from scripts.crawlers.playwright_crawler import PlaywrightCrawler
except (ImportError, ModuleNotFoundError):
    import db_connection
    from crawlers.bs4_crawler import (
        Bs4Crawler,
        BusanYouthCrawler,
        DaeguYouthCrawler,
        GwangjuYouthCrawler,
        IncheonYouthCrawler,
        ShHousingCrawler,
    )
    from crawlers.hidden_api_crawler import (
        GyeonggiJobabaCrawler,
        HiddenApiCrawler,
        SeoulYouthCrawler,
    )
    from crawlers.playwright_crawler import PlaywrightCrawler

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, OSError):
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("CrawlerRunner")


def get_crawlers_by_target(target: str):
    """
    대상 기관/전략에 따른 크롤러 인스턴스 목록 반환
    """
    mapping = {
        "seoul": [SeoulYouthCrawler()],
        "busan": [BusanYouthCrawler()],
        "incheon": [IncheonYouthCrawler()],
        "daegu": [DaeguYouthCrawler()],
        "gwangju": [GwangjuYouthCrawler()],
        "sh": [ShHousingCrawler()],
        "jobaba": [GyeonggiJobabaCrawler()],
        "playwright": [PlaywrightCrawler()],
        "bs4": [Bs4Crawler()],
        "hidden_api": [HiddenApiCrawler()],
        "all": [
            SeoulYouthCrawler(),
            BusanYouthCrawler(),
            IncheonYouthCrawler(),
            DaeguYouthCrawler(),
            GwangjuYouthCrawler(),
            ShHousingCrawler(),
            GyeonggiJobabaCrawler(),
            PlaywrightCrawler(),
        ],
    }
    return mapping.get(target.lower(), mapping["all"])


def run_pipeline(target: str = "all", limit: int = 50):
    """
    지정된 대상(온통청년 제외 전국 지자체 및 특화 포털) 크롤러를 가동하고
    기존 적재 데이터와의 엄격한 중복 검증을 거쳐 신규 정책만 PostgreSQL에 적재합니다.
    """
    print("\n" + "=" * 75)
    print("🚀 [YouthFit] 청년온통 제외 전국 지자체/기관 심층 크롤러 파이프라인")
    print(f" • 수집 대상: {target.upper()}")
    print(f" • 크롤러당 최대 신규 수집 목표: {limit}건 (중복 데이터는 자동 스킵)")
    print("=" * 75)

    # 1. DB 연결 사전 점검
    try:
        conn, db_type = db_connection.get_connection(allow_sqlite_fallback=True)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM policies")
        current_total = cur.fetchone()[0]
        cur.close()
        conn.close()
        print(f"[*] 데이터베이스 연결 확인 완료: [{db_type.upper()}] (현재 DB 적재: {current_total}건)")
    except Exception as e:  # noqa: BLE001
        print(f"[!] 데이터베이스 연결 실패: {e}")
        return

    crawlers = get_crawlers_by_target(target)
    total_saved = 0
    total_skipped = 0
    stats_by_crawler = {}

    for crawler in crawlers:
        doc = (crawler.__class__.__doc__ or "").strip()
        doc_summary = doc.splitlines()[0] if doc else crawler.name
        print(f"\n>>> 실행 중: [{crawler.name}] ({doc_summary})")
        try:
            results = crawler.run(limit=limit)
            saved_cnt = len(results)
            skip_cnt = crawler.stats.get("skipped_duplicate", 0)
            total_saved += saved_cnt
            total_skipped += skip_cnt
            stats_by_crawler[crawler.name] = (saved_cnt, skip_cnt)
            print(f"  └─ 결과: 신규 저장 {saved_cnt}건 / 기존 중복 스킵 {skip_cnt}건")
        except Exception as e:  # noqa: BLE001
            print(f"  └─ [오류 발생 및 복구] {e}")
            stats_by_crawler[crawler.name] = (0, 0)

    print("\n" + "=" * 75)
    print(f"🎉 크롤러 파이프라인 전체 완료! (신규 {total_saved}건 추가 적재 / 중복 {total_skipped}건 안전 스킵)")
    print("-" * 75)
    for name, (saved, skipped) in stats_by_crawler.items():
        print(f"  • {name:25s}: 신규 {saved:>3}건 저장 | 중복 {skipped:>3}건 스킵")
    print("=" * 75)

    # 방금 저장된 크롤링 데이터 요약 조회
    print_crawled_summary()


def print_crawled_summary():
    """
    DB에서 'crawl_' 접두사를 가진 최신 수집 정책 목록을 조회하여 출력합니다.
    """
    conn = None
    cur = None
    try:
        conn, db_type = db_connection.get_connection(allow_sqlite_fallback=True)
        cur = conn.cursor()

        placeholder = "%s" if db_type == "postgresql" else "?"
        cur.execute(f"""
            SELECT policy_id, name, category_large, min_age, max_age, supervising_inst, apply_url
            FROM policies
            WHERE policy_id LIKE {placeholder}
            ORDER BY created_at DESC
            LIMIT 15;
        """, ("crawl_%",))

        rows = cur.fetchall()
        if rows:
            print("\n📋 [최근 크롤링 수집된 정책 목록 샘플 (최대 15건)]")
            print("-" * 75)
            for i, row in enumerate(rows, 1):
                p_id, name, cat, min_a, max_a, inst, url = row
                print(f"[{i:02d}] {name} ({cat})")
                print(f"     ID: {p_id} | 연령: 만 {min_a}~{max_a}세 | 주관: {inst}")
                print(f"     URL: {url}")
            print("-" * 75)
    except Exception as e:  # noqa: BLE001
        print(f"결과 조회 중 오류: {e}")
    finally:
        if cur:
            with suppress(Exception):
                cur.close()
        if conn:
            with suppress(Exception):
                conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouthFit 지자체/특화 청년 공고 크롤러 실행기")
    parser.add_argument(
        "--strategy",
        "--target",
        dest="target",
        type=str,
        default="all",
        choices=["all", "seoul", "busan", "incheon", "daegu", "gwangju", "sh", "jobaba", "playwright", "bs4", "hidden_api"],
        help="크롤링 대상 선택 (기본값: all - 서울, 부산, 인천, 대구, 광주, SH, 경기, K-Startup 전수 크롤링)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=40,
        help="각 크롤러당 최대 신규 수집 목표 건수 (기본값: 40)"
    )

    args = parser.parse_args()
    run_pipeline(target=args.target, limit=args.limit)
