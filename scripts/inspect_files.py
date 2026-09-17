import json
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

print("="*65)
print("📦 [1] 데이터베이스 상태 및 스키마 검증")
print("="*65)

try:
    conn, db_type = db_connection.get_connection(allow_sqlite_fallback=True)
    cur = conn.cursor()
    print(f"• 연결된 데이터베이스 엔진: [{db_type.upper()}]")
    print(f"• 연결 URL: {db_connection.get_database_url()}")

    if db_type == "postgresql":
        print("\n[PostgreSQL 테이블 컬럼 및 데이터 타입]:")
        cur.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'policies'
            ORDER BY ordinal_position;
        """)
        cols = cur.fetchall()
        if cols:
            for col, dtype, nullable in cols:
                null_str = "NULL" if nullable == "YES" else "NOT NULL"
                print(f" • {col:<20} : {dtype:<25} ({null_str})")
        else:
            print(" [!] 'policies' 테이블이 아직 생성되지 않았습니다.")

        print("\n[PostgreSQL 인덱스 목록]:")
        cur.execute("""
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE tablename = 'policies';
        """)
        for idx_name, idx_def in cur.fetchall():
            print(f" • {idx_name}: {idx_def}")

    else:
        # SQLite
        cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='policies'")
        row = cur.fetchone()
        if row:
            print("\n[SQLite 테이블 스키마 정의 (DDL)]:")
            print(row[0])
            print("\n[SQLite 인덱스 목록]:")
            cur.execute("SELECT name, sql FROM sqlite_master WHERE type='index'")
            for name, sql in cur.fetchall():
                if sql:
                    print(f" • {name}: {sql}")
        else:
            print(" [!] 'policies' 테이블이 존재하지 않습니다.")

    cur.execute("SELECT COUNT(*) FROM policies")
    row_count = cur.fetchone()
    total_rows = row_count[0] if row_count else 0
    print(f"\n총 레코드 건수: {total_rows}건")
    conn.close()

except Exception as e:  # noqa: BLE001
    print(f"[!] 데이터베이스 검증 중 오류: {e}")

print("\n" + "="*65)
print("📄 [2] JSON 데이터셋 (data/youth_policies_19_34.json) 검증")
print("="*65)

json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "youth_policies_19_34.json")

if os.path.exists(json_path):
    with open(json_path, encoding="utf-8") as f:
        jdata = json.load(f)

    meta = jdata.get("metadata", {})
    policies = jdata.get("policies", [])

    print(f"• 데이터 출처   : {meta.get('source')}")
    print(f"• 타겟 연령대   : {meta.get('target_age_group')}")
    print(f"• 유효 정책 건수: {len(policies)}건")

    if policies:
        sample = policies[0]
        print(f"\n[정제된 JSON 정책 샘플 (ID: {sample.get('policy_id')})]")
        print(f"• 정책명       : {sample.get('name')}")
        print(f"• 분류         : {sample.get('category_large')} > {sample.get('category_mid')}")
        print(f"• 연령         : 만 {sample.get('min_age')}세 ~ {sample.get('max_age')}세")
        print(f"• 주관기관     : {sample.get('supervising_inst')}")
        print(f"• 지원내용     : {(sample.get('support_content') or '')[:90]}...")
        print("• 파싱된 서류 목록 (체크리스트용 배열):")
        for doc in sample.get('required_docs_parsed', []):
            print(f"   ☑ {doc}")
else:
    print(f"[!] JSON 파일이 없습니다: {json_path}")
print("="*65 + "\n")
