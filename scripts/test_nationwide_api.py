import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_nationwide_diagnose():
    print("Testing Nationwide API & Web Endpoints...")

    # 1. Seoul Test
    seoul_payload = {
        "age": 24,
        "region": "서울",
        "district": "관악구",
        "jobStatus": "jobseeker",
        "household": "single",
        "income": "income60"
    }
    r_seoul = requests.post(f"{BASE_URL}/api/diagnose", json=seoul_payload).json()
    assert r_seoul["status"] == "success"
    p_seoul = r_seoul["data"]["policies"]
    print(" [1] Seoul Test Passed:")
    print(f"     Profile: {r_seoul['data']['profile']['summary']}")
    print(f"     Policies: {[p['name'] for p in p_seoul[:2]]}")

    # 2. Busan Test
    busan_payload = {
        "age": 24,
        "region": "부산",
        "district": "해운대구",
        "jobStatus": "jobseeker",
        "household": "single",
        "income": "income60"
    }
    r_busan = requests.post(f"{BASE_URL}/api/diagnose", json=busan_payload).json()
    assert r_busan["status"] == "success"
    p_busan = r_busan["data"]["policies"]
    print(" [2] Busan Test Passed:")
    print(f"     Profile: {r_busan['data']['profile']['summary']}")
    print(f"     Policies: {[p['name'] for p in p_busan[:2]]}")

    # 3. Gyeonggi Test
    gyeonggi_payload = {
        "age": 28,
        "region": "경기",
        "district": "수원시",
        "jobStatus": "employed",
        "household": "family",
        "income": "income150"
    }
    r_gyeonggi = requests.post(f"{BASE_URL}/api/diagnose", json=gyeonggi_payload).json()
    assert r_gyeonggi["status"] == "success"
    p_gyeonggi = r_gyeonggi["data"]["policies"]
    print(" [3] Gyeonggi Test Passed:")
    print(f"     Profile: {r_gyeonggi['data']['profile']['summary']}")
    print(f"     Policies: {[p['name'] for p in p_gyeonggi[:2]]}")

    # 4. Gwangju Test
    gwangju_payload = {
        "age": 22,
        "region": "광주",
        "district": "북구",
        "jobStatus": "student",
        "household": "single",
        "income": "income120"
    }
    r_gwangju = requests.post(f"{BASE_URL}/api/diagnose", json=gwangju_payload).json()
    assert r_gwangju["status"] == "success"
    p_gwangju = r_gwangju["data"]["policies"]
    print(" [4] Gwangju Test Passed:")
    print(f"     Profile: {r_gwangju['data']['profile']['summary']}")
    print(f"     Policies: {[p['name'] for p in p_gwangju[:2]]}")

    # 5. Incheon Test
    incheon_payload = {
        "age": 25,
        "region": "인천",
        "district": "부평구",
        "jobStatus": "jobseeker",
        "household": "single",
        "income": "income60"
    }
    r_incheon = requests.post(f"{BASE_URL}/api/diagnose", json=incheon_payload).json()
    assert r_incheon["status"] == "success"
    p_incheon = r_incheon["data"]["policies"]
    print(" [5] Incheon Test Passed:")
    print(f"     Profile: {r_incheon['data']['profile']['summary']}")
    print(f"     Policies: {[p['name'] for p in p_incheon[:2]]}")

    # 6. Verify HTML Diagnosis Page
    r_diag = requests.get(f"{BASE_URL}/diagnosis")
    assert r_diag.status_code == 200
    assert "1단계: 시·도 선택" in r_diag.text
    assert "2단계" in r_diag.text
    print(" [6] Web /diagnosis HTML Nationwide Selector Verified (200 OK)")

    print("\nALL NATIONWIDE ENDPOINTS & TESTS PASSED!")

if __name__ == "__main__":
    test_nationwide_diagnose()
