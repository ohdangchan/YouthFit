import os
import sys
import json
import sqlite3
import argparse
import time

# UTF-8 출력 보정
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db_connection

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "youth_policies_19_34.json")
SQLITE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "youthfit.db")

def migrate_from_json(conn, dry_run=False):
    if not os.path.exists(JSON_PATH):
        print(f"[!] JSON 파일을 찾을 수 없습니다: {JSON_PATH}")
        return 0
        
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    policies = data.get("policies", [])
    total = len(policies)
    print(f"[*] JSON 데이터셋에서 {total}건의 정책을 읽었습니다.")
    
    if dry_run:
        print("[*] --dry-run 모드입니다. 실제 데이터베이스에 쓰지 않습니다.")
        return total
        
    cur = conn.cursor()
    success = 0
    start_time = time.time()
    
    for i, norm in enumerate(policies, 1):
        # raw json 구조 복원 또는 생성
        raw = norm.copy()
        db_connection.upsert_policy(cur, norm, raw, db_type="postgresql")
        success += 1
        if i % 100 == 0 or i == total:
            conn.commit()
            print(f"[*] 진행률: {i}/{total}건 ({i/total*100:.1f}%) 완료...")
            
    elapsed = time.time() - start_time
    print(f"\n[OK] PostgreSQL 마이그레이션 완료: 총 {success}건 반영 ({elapsed:.2f}초 소요)")
    return success

def migrate_from_sqlite(conn, dry_run=False):
    if not os.path.exists(SQLITE_PATH):
        print(f"[!] SQLite DB 파일을 찾을 수 없습니다: {SQLITE_PATH}")
        print("[*] JSON 파일로부터 마이그레이션을 대신 시도합니다.")
        return migrate_from_json(conn, dry_run)
        
    sq_conn = sqlite3.connect(SQLITE_PATH)
    sq_cur = sq_conn.cursor()
    sq_cur.execute("SELECT * FROM policies")
    rows = sq_cur.fetchall()
    col_names = [d[0] for d in sq_cur.description]
    
    total = len(rows)
    print(f"[*] SQLite DB ({SQLITE_PATH})에서 {total}건의 정책을 읽었습니다.")
    
    if dry_run:
        print("[*] --dry-run 모드입니다. 실제 데이터베이스에 쓰지 않습니다.")
        sq_conn.close()
        return total
        
    cur = conn.cursor()
    success = 0
    start_time = time.time()
    
    for i, row in enumerate(rows, 1):
        item = dict(zip(col_names, row))
        raw_json_val = item.get("raw_json")
        try:
            raw_obj = json.loads(raw_json_val) if raw_json_val else item
        except Exception:
            raw_obj = item
            
        db_connection.upsert_policy(cur, item, raw_obj, db_type="postgresql")
        success += 1
        if i % 100 == 0 or i == total:
            conn.commit()
            print(f"[*] 진행률: {i}/{total}건 ({i/total*100:.1f}%) 완료...")
            
    sq_conn.close()
    elapsed = time.time() - start_time
    print(f"\n[OK] PostgreSQL 마이그레이션 완료: 총 {success}건 반영 ({elapsed:.2f}초 소요)")
    return success

def main():
    parser = argparse.ArgumentParser(description="YouthFit SQLite/JSON -> PostgreSQL 마이그레이션 도구")
    parser.add_argument("--source", choices=["sqlite", "json"], default="sqlite", help="데이터 원본 선택 (기본: sqlite)")
    parser.add_argument("--dry-run", action="store_true", help="실제 DB에 쓰지 않고 마이그레이션 대상 검증만 수행")
    args = parser.parse_args()
    
    print("\n" + "="*65)
    print("🐘 [YouthFit] PostgreSQL 데이터 마이그레이션 시작")
    print("="*65)
    print(f"• 데이터 원본: {args.source.upper()}")
    print(f"• 연결 대상 URL: {db_connection.get_database_url()}")
    
    if args.dry_run:
        if args.source == "json":
            migrate_from_json(None, dry_run=True)
        else:
            migrate_from_sqlite(None, dry_run=True)
        return
        
    try:
        conn, db_type = db_connection.get_connection(allow_sqlite_fallback=False)
        if db_type != "postgresql":
            print("[!] PostgreSQL 연결이 아닙니다. DATABASE_URL 설정을 확인하세요.")
            sys.exit(1)
            
        print("[*] PostgreSQL 테이블 스키마 및 인덱스 초기화...")
        db_connection.init_db(conn)
        
        if args.source == "json":
            migrate_from_json(conn, dry_run=False)
        else:
            migrate_from_sqlite(conn, dry_run=False)
            
        conn.close()
    except Exception as e:
        print(f"\n[!] 마이그레이션 중 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
