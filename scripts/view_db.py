import argparse
import os
import sys
from contextlib import suppress

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
for p in [CURRENT_DIR, PROJECT_ROOT]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from scripts import db_connection
except (ImportError, ModuleNotFoundError):
    import db_connection

if hasattr(sys.stdout, "reconfigure"):
    with suppress(AttributeError, OSError):
        getattr(sys.stdout, "reconfigure")(encoding="utf-8")

def get_db_and_type():
    try:
        conn, db_type = db_connection.get_connection(allow_sqlite_fallback=True)
        return conn, db_type
    except Exception as e:  # noqa: BLE001
        print(f"[!] 데이터베이스 연결 실패: {e}")
        sys.exit(1)

def format_query(query, db_type):
    if db_type == "postgresql":
        return query.replace("?", "%s")
    return query

def show_summary():
    conn, db_type = get_db_and_type()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM policies")
        row_cnt = cur.fetchone()
        total = row_cnt[0] if row_cnt else 0

        print("\n" + "="*65)
        print(f"📊 [YouthFit DB] 정책 데이터 요약 보고서 (엔진: {db_type.upper()}, 총 {total}건)")
        print("="*65)

        print("\n[1] 분야(대분류)별 정책 통계")
        print("-" * 45)
        cur.execute("""
            SELECT category_large, COUNT(*) as cnt
            FROM policies
            GROUP BY category_large
            ORDER BY cnt DESC
        """)
        for cat, cnt in cur.fetchall():
            ratio = (cnt / total * 100) if total > 0 else 0
            bar = "█" * int(ratio / 4)
            cat_name = cat if cat else "미분류"
            print(f" • {cat_name:<16} : {cnt:>3}건 ({ratio:>5.1f}%) {bar}")

        print("\n[2] 연령대별 수혜 커버리지")
        print("-" * 45)
        for age in [19, 24, 29, 34, 39]:
            q = format_query("SELECT COUNT(*) FROM policies WHERE min_age <= ? AND max_age >= ?", db_type)
            cur.execute(q, (age, age))
            age_row = cur.fetchone()
            count = age_row[0] if age_row else 0
            print(f" • 만 {age}세 대상 정책 : {count}건")

        print("\n[3] 주요 4대 분야별 대표 정책 샘플")
        print("-" * 65)
        key_categories = ["주거", "일자리", "금융･복지･문화", "교육･직업훈련"]
        for cat in key_categories:
            q = format_query("""
                SELECT policy_id, name, min_age, max_age, supervising_inst, support_content, required_docs, apply_url
                FROM policies
                WHERE category_large = ?
                ORDER BY RANDOM() LIMIT 1
            """, db_type)
            cur.execute(q, (cat,))
            row = cur.fetchone()
            if row:
                p_id, name, min_a, max_a, inst, support, docs, url = row
                print(f"\n📂 [{cat}] {name}")
                print(f"   • 정책 ID    : {p_id}")
                print(f"   • 대상 연령  : 만 {min_a}세 ~ {max_a}세")
                print(f"   • 주관 기관  : {inst or '지자체/정부부처'}")
                clean_support = (support or "").replace('\n', ' ')[:100]
                print(f"   • 지원 내용  : {clean_support}...")
                clean_docs = (docs or "").replace('\n', ' ')[:70]
                print(f"   • 필수 서류  : {clean_docs}...")
                print(f"   • 신청 링크  : {url if url else '별도 공고 참조'}")

        print("\n" + "="*65 + "\n")
    finally:
        with suppress(Exception):
            cur.close()
        with suppress(Exception):
            conn.close()

def search_policies(keyword=None, category=None, age=None, limit=10):
    conn, db_type = get_db_and_type()
    cur = conn.cursor()
    try:
        query = "SELECT policy_id, name, category_large, min_age, max_age, supervising_inst, apply_url FROM policies WHERE 1=1"
        params = []

        if keyword:
            query += " AND (name LIKE ? OR support_content LIKE ? OR explanation LIKE ?)"
            term = f"%{keyword}%"
            params.extend([term, term, term])

        if category:
            query += " AND category_large LIKE ?"
            params.append(f"%{category}%")

        if age is not None:
            query += " AND min_age <= ? AND max_age >= ?"
            params.extend([age, age])

        query += " ORDER BY policy_id DESC LIMIT ?"
        params.append(limit)

        cur.execute(format_query(query, db_type), params)
        rows = cur.fetchall()

        print(f"\n🔍 검색 결과 (엔진: {db_type.upper()} | 조건: 키워드='{keyword or '-'}', 카테고리='{category or '-'}', 연령='{age or '-'}' / 상위 {len(rows)}건)")
        print("-" * 80)
        for i, row in enumerate(rows, 1):
            p_id, name, cat, min_a, max_a, inst, url = row
            print(f"[{i:02d}] {name} ({cat})")
            print(f"     ID: {p_id} | 연령: 만 {min_a}~{max_a}세 | 주관: {inst}")
            if url:
                print(f"     URL: {url}")
        print("-" * 80 + "\n")
    finally:
        with suppress(Exception):
            cur.close()
        with suppress(Exception):
            conn.close()

def view_detail(policy_id):
    conn, db_type = get_db_and_type()
    cur = conn.cursor()
    try:
        cur.execute(format_query("SELECT * FROM policies WHERE policy_id = ?", db_type), (policy_id,))
        row = cur.fetchone()
        if not row:
            print(f"[!] 정책 ID '{policy_id}'를 찾을 수 없습니다.")
            return

        col_names = [description[0] for description in cur.description]
        item = dict(zip(col_names, row, strict=False))

        print("\n" + "="*70)
        print(f"📋 [정책 상세 정보] {item['name']} (엔진: {db_type.upper()})")
        print("="*70)
        print(f"• 정책 ID       : {item['policy_id']}")
        print(f"• 카테고리      : {item['category_large']} > {item['category_mid']}")
        print(f"• 키워드        : {item['keyword']}")
        print(f"• 지원 대상연령 : 만 {item['min_age']}세 ~ {item['max_age']}세 (연령제한: {item['age_limit_yn']})")
        print(f"• 주관/운영기관 : {item['supervising_inst']} / {item['operating_inst']}")
        print(f"• 신청 기간     : {item['apply_period']}")
        print(f"• 신청 방법     : {item['apply_method']}")
        print(f"• 신청 URL      : {item['apply_url']}")
        print("\n[지원 내용]")
        print(item['support_content'])
        print("\n[필수 제출 서류]")
        print(item['required_docs'])
        print("="*70 + "\n")
    finally:
        with suppress(Exception):
            cur.close()
        with suppress(Exception):
            conn.close()

def view_crawled_policies(limit=20):
    """
    온통청년 외 지자체 및 특화 포털에서 직접 크롤링 수집된 정책 목록 조회
    """
    conn, db_type = get_db_and_type()
    cur = conn.cursor()
    try:
        q = format_query("""
            SELECT policy_id, name, category_large, min_age, max_age, supervising_inst, apply_url
            FROM policies
            WHERE policy_id LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
        """, db_type)
        cur.execute(q, ("crawl_%", limit))
        rows = cur.fetchall()

        cur.execute(format_query("SELECT COUNT(*) FROM policies WHERE policy_id LIKE ?", db_type), ("crawl_%",))
        c_row = cur.fetchone()
        crawled_total = c_row[0] if c_row else 0

        print("\n" + "=" * 75)
        print(f"🌐 [YouthFit 크롤링 전용] 청년온통 제외 지자체/특화기관 수집 정책 (총 {crawled_total}건 중 최근 {len(rows)}건)")
        print("=" * 75)
        for i, row in enumerate(rows, 1):
            p_id, name, cat, min_a, max_a, inst, url = row
            print(f"[{i:02d}] {name} ({cat})")
            print(f"     ID: {p_id} | 연령: 만 {min_a}~{max_a}세 | 주관: {inst}")
            if url:
                print(f"     URL: {url}")
        print("=" * 75 + "\n")
    finally:
        with suppress(Exception):
            cur.close()
        with suppress(Exception):
            conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouthFit DB 정책 데이터 뷰어 (PostgreSQL / SQLite 호환)")
    parser.add_argument("--summary", action="store_true", help="데이터베이스 전체 통계 및 대표 샘플 출력")
    parser.add_argument("--crawled", action="store_true", help="청년온통 제외 지자체/특화기관 크롤링 수집 정책만 보기")
    parser.add_argument("--search", type=str, help="정책명/내용 검색 키워드 (예: 월세, 면접, 청년수당)")
    parser.add_argument("--cat", type=str, help="카테고리 필터 (예: 주거, 일자리, 금융)")
    parser.add_argument("--age", type=int, help="만 나이 필터 (예: 24)")
    parser.add_argument("--detail", type=str, help="정책 ID 상세 보기")
    parser.add_argument("--limit", type=int, default=10, help="출력 건수 제한 (기본: 10)")

    args = parser.parse_args()

    if args.detail:
        view_detail(args.detail)
    elif args.crawled:
        view_crawled_policies(limit=args.limit)
    elif args.search or args.cat or args.age:
        search_policies(keyword=args.search, category=args.cat, age=args.age, limit=args.limit)
    else:
        show_summary()
