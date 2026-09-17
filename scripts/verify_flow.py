import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_flow():
    print("Testing Full Service UX Flow on Local Server...")
    
    # 1. Landing Page
    r1 = requests.get(f"{BASE_URL}/")
    assert r1.status_code == 200, f"Landing page failed: {r1.status_code}"
    print(" [1/5] GET / (Landing Page) -> 200 OK")

    # 2. Diagnosis Survey Page
    r2 = requests.get(f"{BASE_URL}/diagnosis")
    assert r2.status_code == 200, f"Diagnosis page failed: {r2.status_code}"
    assert "만 나이를 입력해 주세요" in r2.text
    assert "서울시 전체 25개 자치구" in r2.text
    print(" [2/5] GET /diagnosis (Survey Page with 25 Districts) -> 200 OK")

    # 3. Post Diagnosis API with User 5-Criteria
    profile = {
        "age": 24,
        "district": "관악구",
        "jobStatus": "jobseeker",
        "household": "single",
        "income": "income60"
    }
    r3 = requests.post(f"{BASE_URL}/api/diagnose", json=profile)
    assert r3.status_code == 200, f"Diagnose API failed: {r3.status_code}"
    res = r3.json()
    assert res.get("status") == "success", "Diagnosis API status not success"
    data = res.get("data", {})
    assert len(data.get("policies", [])) == 4, "Top 4 policies should be returned"
    print(f" [3/5] POST /api/diagnose -> 200 OK (Matched: {len(data['policies'])} policies, Total benefit: {data['total_benefit_formatted']} won)")

    # 4. Loading Page
    r4 = requests.get(f"{BASE_URL}/loading")
    assert r4.status_code == 200, f"Loading page failed: {r4.status_code}"
    print(" [4/5] GET /loading (Neural Match Loading Animation) -> 200 OK")

    # 5. Dashboard Page
    r5 = requests.get(f"{BASE_URL}/dashboard")
    assert r5.status_code == 200, f"Dashboard page failed: {r5.status_code}"
    assert "policy-modal" in r5.text
    print(" [5/5] GET /dashboard (Interactive Bento Dashboard) -> 200 OK")

    print("\nALL 5 STEPS PASSED! The complete web service flow is verified and working flawlessly.")

if __name__ == "__main__":
    test_flow()
