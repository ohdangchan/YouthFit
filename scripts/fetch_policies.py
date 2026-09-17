import json
import os
import sys
from contextlib import suppress

import requests
import urllib3

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
    with suppress(AttributeError, OSError):
        sys.stdout.reconfigure(encoding='utf-8')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = os.getenv("ONTONG_API_KEY", "")
BASE_URL = "https://www.youthcenter.go.kr/go/ythip/getPlcy"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

def test_fetch_sample():
    if not API_KEY:
        print("[!] 오류: ONTONG_API_KEY가 설정되지 않았습니다. .env 파일에 ONTONG_API_KEY를 입력해주세요.")
        return
        
    params = {
        "apiKeyNm": API_KEY,
        "pageNum": 1,
        "pageSize": 2,
        "rtnType": "json"
    }
    
    res = requests.get(BASE_URL, params=params, headers=HEADERS, verify=False, timeout=10)
    data = res.json()
    
    print("=== API Response Header Info ===")
    print("Result Code:", data.get("resultCode"))
    print("Result Message:", data.get("resultMessage"))
    paging = data.get("result", {}).get("pagging", {})
    print(f"Total Policy Count: {paging.get('totCount')}")
    
    policies = data.get("result", {}).get("youthPolicyList", [])
    if policies:
        os.makedirs("data", exist_ok=True)
        with open("data/raw_sample.json", "w", encoding="utf-8") as f:
            json.dump(policies[0], f, ensure_ascii=False, indent=2)
        print("\n[OK] Raw sample saved to data/raw_sample.json")
        print("\n=== Sample Policy Summary ===")
        sample = policies[0]
        print(f"Policy No: {sample.get('plcyNo')}")
        print(f"Policy Name: {sample.get('plcyNm')}")
        print(f"Category: {sample.get('lclsfNm')} > {sample.get('mclsfNm')}")
        print(f"Age Range: 만 {sample.get('sprtTrgtMinAge')}세 ~ {sample.get('sprtTrgtMaxAge')}세")
        print(f"Support Content: {sample.get('plcySprtCn')[:120]}...")
        print(f"Documents: {sample.get('sbmsnDcmntCn')[:80]}...")

if __name__ == "__main__":
    test_fetch_sample()
