import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

from services import auth_service

print("Testing Auth Service Functions...")

# 1. Signup Test
try:
    test_email = "tester1@youthfit.kr"
    res_signup = auth_service.signup_user(test_email, "홍길동", "testpass1234!")
    print("1. Signup Test: SUCCESS ->", res_signup["name"], res_signup["email"])
except Exception as e:
    print("1. Signup Notice (Already exists or error):", e)

# 2. Login Test (Success)
try:
    res_login = auth_service.login_user("tester1@youthfit.kr", "testpass1234!")
    print("2. Login Test: SUCCESS -> User ID:", res_login["id"], "Token:", res_login["token"][:15], "...")
except Exception as e:
    print("2. Login Failed:", e)

# 3. Login Test (Wrong Password)
try:
    auth_service.login_user("tester1@youthfit.kr", "wrongpass!")
    print("3. Wrong Password Test: FAILED (Should have raised error)")
except Exception as e:
    print("3. Wrong Password Test: SUCCESS (Blocked properly) ->", e)

# 4. Google Auth Test
try:
    res_google = auth_service.authenticate_google_user("google_user@gmail.com", "구글테스터", "gid_987654321")
    print("4. Google Auth Test: SUCCESS ->", res_google["name"], f"(New: {res_google['is_new']})")
except Exception as e:
    print("4. Google Auth Failed:", e)
