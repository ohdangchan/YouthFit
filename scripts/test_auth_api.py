import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')
BASE_URL = "http://127.0.0.1:8000"

def test_auth_apis():
    print("Testing Full Authentication & DB Integration...")

    # 1. Signup API
    email = f"user_{hash(str(sys.argv)) % 100000}@youthfit.kr"
    payload_signup = {
        "email": email,
        "name": "김청년",
        "password": "securepassword123!"
    }
    r_signup = requests.post(f"{BASE_URL}/api/auth/signup", json=payload_signup)
    assert r_signup.status_code == 200, f"Signup failed: {r_signup.text}"
    data_signup = r_signup.json()["data"]
    print(f" [1] Signup API -> 200 OK (Created User ID: {data_signup['id']}, Email: {data_signup['email']})")

    # 2. Login API (Valid)
    payload_login = {
        "email": email,
        "password": "securepassword123!"
    }
    r_login = requests.post(f"{BASE_URL}/api/auth/login", json=payload_login)
    assert r_login.status_code == 200, f"Login failed: {r_login.text}"
    data_login = r_login.json()["data"]
    assert data_login["token"].startswith("yf_"), "Token format mismatch"
    print(f" [2] Login API -> 200 OK (Session Token: {data_login['token'][:20]}..., Name: {data_login['name']})")

    # 3. Login API (Invalid password)
    payload_wrong = {
        "email": email,
        "password": "wrong_password"
    }
    r_wrong = requests.post(f"{BASE_URL}/api/auth/login", json=payload_wrong)
    assert r_wrong.status_code == 401, f"Should be 401 Unauthorized: {r_wrong.status_code}"
    print(f" [3] Invalid Password Protection -> 401 Unauthorized (Blocked properly)")

    # 4. Google OAuth API
    payload_google = {
        "email": "google_sesac@gmail.com",
        "name": "새싹 구글청년",
        "google_id": "gid_google_123456"
    }
    r_google = requests.post(f"{BASE_URL}/api/auth/google", json=payload_google)
    assert r_google.status_code == 200, f"Google auth failed: {r_google.text}"
    data_google = r_google.json()["data"]
    assert data_google["provider"] == "google"
    print(f" [4] Google Auth API -> 200 OK (Google User: {data_google['name']}, Provider: {data_google['provider']}, ID: {data_google['id']})")

    # 5. Check auth.html status
    r_html = requests.get(f"{BASE_URL}/auth.html")
    assert r_html.status_code == 200
    assert "btn-google-login" in r_html.text
    print(" [5] Web /auth.html -> 200 OK (Google Button & Forms Wired)")

    print("\nALL AUTHENTICATION & DATABASE TESTS PASSED!")

if __name__ == "__main__":
    test_auth_apis()
