import os
import sys
import json
import requests
import urllib3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db_connection

try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()
except ImportError:
    pass

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = os.getenv("ONTONG_API_KEY", "")
BASE_URL = "https://www.youthcenter.go.kr/go/ythip/getPlcy"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

JSON_OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "youth_policies_19_34.json"
)

def init_db():
    conn, db_type = db_connection.init_db()
    return conn, db_type

def is_eligible_19_34(min_age_str, max_age_str, age_limit_yn):
    """
    만 19세 ~ 34세 청년이 수혜 대상에 포함되는지 검사
    """
    if age_limit_yn == "N" or (not min_age_str and not max_age_str):
        return True
        
    try:
        min_age = int(min_age_str) if min_age_str and min_age_str.isdigit() else 0
    except ValueError:
        min_age = 0
        
    try:
        max_age = int(max_age_str) if max_age_str and max_age_str.isdigit() else 99
    except ValueError:
        max_age = 99
        
    # 만 19세~34세와 겹치는지 확인:
    # 정책의 최소연령 <= 34 이고 최대연령 >= 19
    return min_age <= 34 and max_age >= 19

def normalize_policy(raw):
    """
    온통청년 원본 API 응답 객체를 정제된 표준 스키마 딕셔너리로 변환
    """
    min_age_str = raw.get("sprtTrgtMinAge", "")
    max_age_str = raw.get("sprtTrgtMaxAge", "")
    min_age = int(min_age_str) if min_age_str and min_age_str.isdigit() else 0
    max_age = int(max_age_str) if max_age_str and max_age_str.isdigit() else 99

    # 서류 목록 파싱 (개행, 특수기호 등으로 분리)
    docs_raw = raw.get("sbmsnDcmntCn", "") or ""
    docs_list = [line.strip().lstrip("○-•*1234567890.) ").strip() for line in docs_raw.split("\n") if line.strip()]
    docs_list = [d for d in docs_list if len(d) > 1 and not d.startswith("□") and not d.startswith("※")]

    return {
        "policy_id": raw.get("plcyNo", ""),
        "name": (raw.get("plcyNm") or "").strip(),
        "category_large": raw.get("lclsfNm", "") or "",
        "category_mid": raw.get("mclsfNm", "") or "",
        "keyword": raw.get("plcyKywdNm", "") or "",
        "min_age": min_age,
        "max_age": max_age,
        "age_limit_yn": raw.get("sprtTrgtAgeLmtYn", "Y"),
        "support_content": (raw.get("plcySprtCn") or "").strip(),
        "explanation": (raw.get("plcyExplnCn") or "").strip(),
        "required_docs": docs_raw.strip(),
        "required_docs_parsed": docs_list[:10], # 최대 10개 핵심 서류
        "apply_method": (raw.get("plcyAplyMthdCn") or "").strip(),
        "apply_url": (raw.get("aplyUrlAddr") or raw.get("refUrlAddr1") or "").strip(),
        "apply_period": (raw.get("aplyYmd") or "").strip(),
        "biz_start_date": raw.get("bizPrdBgngYmd", ""),
        "biz_end_date": raw.get("bizPrdEndYmd", ""),
        "supervising_inst": raw.get("sprvsnInstCdNm", "") or "",
        "operating_inst": raw.get("operInstCdNm", "") or "",
        "zip_codes": raw.get("zipCd", "") or "",
        "marriage_status": raw.get("mrgSttsCd", ""),
        "employment_status": raw.get("jobCd", ""),
        "education_status": raw.get("schoolCd", ""),
        "last_modified": raw.get("lastMdfcnDt", "")
    }

def fetch_and_store_policies(max_pages=10, page_size=100):
    if not API_KEY:
        print("[!] 오류: ONTONG_API_KEY가 설정되지 않았습니다. .env 파일에 ONTONG_API_KEY를 입력해주세요.")
        return

    conn, db_type = init_db()
    cur = conn.cursor()
    
    total_fetched = 0
    eligible_count = 0
    all_eligible_policies = []
    
    print(f"[*] 온통청년 Open API 정책 수집 시작 (최대 {max_pages} 페이지, 페이지당 {page_size}건)...")
    print(f"[*] 연결된 데이터베이스 타입: [{db_type.upper()}]")
    
    for page in range(1, max_pages + 1):
        params = {
            "apiKeyNm": API_KEY,
            "pageNum": page,
            "pageSize": page_size,
            "rtnType": "json"
        }
        
        try:
            res = requests.get(BASE_URL, params=params, headers=HEADERS, verify=False, timeout=15)
            if res.status_code != 200:
                print(f"[!] 페이지 {page} 호출 실패: HTTP {res.status_code}")
                break
                
            data = res.json()
            if data.get("resultCode") != 200:
                print(f"[!] 페이지 {page} API 에러: {data.get('resultMessage')}")
                break
                
            policy_list = data.get("result", {}).get("youthPolicyList", [])
            if not policy_list:
                print(f"[*] 페이지 {page}: 더 이상 데이터가 없습니다.")
                break
                
            total_count = data.get("result", {}).get("pagging", {}).get("totCount", 0)
            print(f"[*] 페이지 {page}/{max_pages} 수신 완료 ({len(policy_list)}건) - 전체 등록 정책: {total_count}건")
            
            for raw in policy_list:
                total_fetched += 1
                min_age = raw.get("sprtTrgtMinAge")
                max_age = raw.get("sprtTrgtMaxAge")
                age_limit_yn = raw.get("sprtTrgtAgeLmtYn")
                
                # 만 19세~34세 대상 정책 필터링
                if is_eligible_19_34(min_age, max_age, age_limit_yn):
                    norm = normalize_policy(raw)
                    eligible_count += 1
                    all_eligible_policies.append(norm)
                    
                    # DB 저장 (PostgreSQL / SQLite 호환)
                    db_connection.upsert_policy(cur, norm, raw, db_type=db_type)
                    
            conn.commit()
            
            # 전체 정책 수에 도달하면 중단
            if total_fetched >= total_count:
                break
                
        except Exception as e:
            print(f"[!] 페이지 {page} 처리 중 예외 발생: {e}")
            break
            
    conn.close()
    
    # JSON 파일로도 저장
    with open(JSON_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "source": "온통청년 (youthcenter.go.kr) Open API",
                "target_age_group": "만 19세 ~ 34세",
                "total_fetched": total_fetched,
                "eligible_19_34_count": eligible_count,
                "db_engine": db_type
            },
            "policies": all_eligible_policies
        }, f, ensure_ascii=False, indent=2)
        
    print("\n" + "="*50)
    print(f"[*] 수집 및 DB 변환 완료!")
    print(f" - 온통청년 API 수신 총 정책: {total_fetched}건")
    print(f" - 만 19세 ~ 34세 청년 수혜 가능 정책: {eligible_count}건")
    print(f" - 데이터베이스 엔진: [{db_type.upper()}]")
    print(f" - 정제 JSON 파일 저장: {JSON_OUTPUT_PATH}")
    print("="*50)

if __name__ == "__main__":
    # 500건 또는 5페이지 우선 수집
    fetch_and_store_policies(max_pages=5, page_size=100)
