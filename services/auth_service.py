import os
import sys
import json
import hashlib
import secrets
import datetime
from typing import Optional, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scripts import db_connection
except Exception:
    db_connection = None


def hash_password(password: str) -> str:
    """PBKDF2-HMAC-SHA256 기반 안전한 비밀번호 해싱"""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}:{key.hex()}"

def verify_password(stored_hash: str, password: str) -> bool:
    """저장된 해시값과 입력된 비밀번호 일치 여부 검증"""
    try:
        if not stored_hash or ":" not in stored_hash:
            return False
        salt, key_hex = stored_hash.split(":", 1)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return secrets.compare_digest(key.hex(), key_hex)
    except Exception:
        return False

def generate_session_token(user_id: int, email: str) -> str:
    """간이 세션 토큰 생성 (실제 프로덕션 JWT 호환 형태)"""
    rand = secrets.token_hex(24)
    timestamp = int(datetime.datetime.now().timestamp())
    payload = f"{user_id}:{email}:{timestamp}:{rand}"
    token = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    return f"yf_{user_id}_{token[:32]}"

def signup_user(email: str, name: str, password: str) -> Dict[str, Any]:
    """
    신규 회원가입을 처리하고 DB에 저장합니다.
    """
    email = email.strip().lower()
    name = name.strip()

    if not email or "@" not in email:
        raise ValueError("유효한 이메일 주소를 입력해 주세요.")
    if not name:
        raise ValueError("이름(닉네임)을 입력해 주세요.")
    if not password or len(password) < 6:
        raise ValueError("비밀번호는 최소 6자 이상이어야 합니다.")

    conn, db_type = db_connection.get_connection(allow_sqlite_fallback=True)
    cur = conn.cursor()

    try:
        # 중복 이메일 체크
        cur.execute("SELECT id FROM public.users WHERE email = %s;" if db_type == "postgresql" else "SELECT id FROM users WHERE email = ?;", (email,))
        if cur.fetchone():
            raise ValueError("이미 가입된 이메일 계정입니다. 다른 이메일로 가입하시거나 로그인해 주세요.")

        pwd_hash = hash_password(password)
        now = datetime.datetime.now()

        if db_type == "postgresql":
            cur.execute("""
                INSERT INTO public.users (email, name, password_hash, provider, profile_json, created_at, last_login_at)
                VALUES (%s, %s, %s, 'local', %s, %s, %s)
                RETURNING id;
            """, (email, name, pwd_hash, json.dumps({}), now, now))
            user_id = cur.fetchone()[0]
        else:
            cur.execute("""
                INSERT INTO users (email, name, password_hash, provider, profile_json, created_at, last_login_at)
                VALUES (?, ?, ?, 'local', ?, ?, ?);
            """, (email, name, pwd_hash, json.dumps({}), now, now))
            user_id = cur.lastrowid

        conn.commit()

        token = generate_session_token(user_id, email)

        return {
            "id": user_id,
            "email": email,
            "name": name,
            "provider": "local",
            "token": token,
            "message": "회원가입이 성공적으로 완료되었습니다."
        }
    finally:
        conn.close()

def login_user(email: str, password: str) -> Dict[str, Any]:
    """
    이메일과 비밀번호로 로그인 인증을 수행합니다.
    """
    email = email.strip().lower()

    if not email or not password:
        raise ValueError("이메일과 비밀번호를 모두 입력해 주세요.")

    conn, db_type = db_connection.get_connection(allow_sqlite_fallback=True)
    cur = conn.cursor()

    try:
        query = "SELECT id, email, name, password_hash, provider, profile_json FROM public.users WHERE email = %s;" if db_type == "postgresql" else "SELECT id, email, name, password_hash, provider, profile_json FROM users WHERE email = ?;"
        cur.execute(query, (email,))
        row = cur.fetchone()

        if not row:
            raise ValueError("등록되지 않은 이메일 계정이거나 비밀번호가 일치하지 않습니다.")

        user_id, u_email, u_name, stored_hash, provider, profile_json = row

        if provider == "google" and not stored_hash:
            raise ValueError("해당 계정은 Google 소셜 계정으로 가입되었습니다. 'Google 계정으로 계속하기'를 이용해 주세요.")

        if not verify_password(stored_hash, password):
            raise ValueError("비밀번호가 일치하지 않습니다. 다시 확인해 주세요.")

        # 최근 로그인 일시 갱신
        now = datetime.datetime.now()
        update_query = "UPDATE public.users SET last_login_at = %s WHERE id = %s;" if db_type == "postgresql" else "UPDATE users SET last_login_at = ? WHERE id = ?;"
        cur.execute(update_query, (now, user_id))
        conn.commit()

        token = generate_session_token(user_id, u_email)

        # 프로필 파싱
        prof_data = {}
        if isinstance(profile_json, dict):
            prof_data = profile_json
        elif isinstance(profile_json, str):
            try:
                prof_data = json.loads(profile_json)
            except Exception:
                pass

        return {
            "id": user_id,
            "email": u_email,
            "name": u_name,
            "provider": provider,
            "token": token,
            "profile": prof_data,
            "message": "로그인에 성공했습니다."
        }
    finally:
        conn.close()

def authenticate_google_user(google_email: str, google_name: str, google_id: str = "") -> Dict[str, Any]:
    """
    Google 소셜 계정 로그인을 처리합니다.
    기존 회원이면 로그인, 신규 회원이면 DB에 자동 회원가입 후 로그인 처리합니다.
    """
    email = google_email.strip().lower()
    name = google_name.strip() or "구글 회원"

    if not email or "@" not in email:
        raise ValueError("유효한 Google 이메일 계정이 아닙니다.")

    conn, db_type = db_connection.get_connection(allow_sqlite_fallback=True)
    cur = conn.cursor()

    try:
        query = "SELECT id, email, name, provider, profile_json FROM public.users WHERE email = %s;" if db_type == "postgresql" else "SELECT id, email, name, provider, profile_json FROM users WHERE email = ?;"
        cur.execute(query, (email,))
        row = cur.fetchone()
        now = datetime.datetime.now()

        if row:
            # 기존 회원 로그인
            user_id, u_email, u_name, provider, profile_json = row
            update_query = "UPDATE public.users SET last_login_at = %s WHERE id = %s;" if db_type == "postgresql" else "UPDATE users SET last_login_at = ? WHERE id = ?;"
            cur.execute(update_query, (now, user_id))
            conn.commit()

            prof_data = profile_json if isinstance(profile_json, dict) else {}
            if isinstance(profile_json, str):
                try:
                    prof_data = json.loads(profile_json)
                except Exception:
                    pass

            token = generate_session_token(user_id, u_email)
            return {
                "id": user_id,
                "email": u_email,
                "name": u_name,
                "provider": "google",
                "token": token,
                "profile": prof_data,
                "is_new": False,
                "message": f"Google 계정({u_email})으로 로그인되었습니다."
            }
        else:
            # 신규 Google 계정 회원가입
            initial_profile = {"google_id": google_id, "verified": True}
            if db_type == "postgresql":
                cur.execute("""
                    INSERT INTO public.users (email, name, password_hash, provider, profile_json, created_at, last_login_at)
                    VALUES (%s, %s, NULL, 'google', %s, %s, %s)
                    RETURNING id;
                """, (email, name, json.dumps(initial_profile), now, now))
                user_id = cur.fetchone()[0]
            else:
                cur.execute("""
                    INSERT INTO users (email, name, password_hash, provider, profile_json, created_at, last_login_at)
                    VALUES (?, ?, NULL, 'google', ?, ?, ?);
                """, (email, name, json.dumps(initial_profile), now, now))
                user_id = cur.lastrowid

            conn.commit()

            token = generate_session_token(user_id, email)
            return {
                "id": user_id,
                "email": email,
                "name": name,
                "provider": "google",
                "token": token,
                "profile": initial_profile,
                "is_new": True,
                "message": f"Google 계정으로 환영합니다, {name}님! 회원가입이 완료되었습니다."
            }
    finally:
        conn.close()

def save_user_diagnosis(user_id: int, profile_data: dict, diagnosis_result: dict) -> bool:
    """
    회원의 최근 진단 이력을 DB에 저장합니다.
    """
    conn, db_type = db_connection.get_connection(allow_sqlite_fallback=True)
    cur = conn.cursor()

    try:
        # 기존 프로필 조회
        query = "SELECT profile_json FROM public.users WHERE id = %s;" if db_type == "postgresql" else "SELECT profile_json FROM users WHERE id = ?;"
        cur.execute(query, (user_id,))
        row = cur.fetchone()
        if not row:
            return False

        existing = row[0] if isinstance(row[0], dict) else {}
        if isinstance(row[0], str):
            try:
                existing = json.loads(row[0])
            except Exception:
                pass

        existing["recent_diagnosis"] = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "profile": profile_data,
            "total_benefit": diagnosis_result.get("total_benefit", 0),
            "total_benefit_formatted": diagnosis_result.get("total_benefit_formatted", "0"),
            "matched_count": diagnosis_result.get("matched_count", 0),
            "top_policy_names": [p.get("name") for p in diagnosis_result.get("policies", [])[:3]]
        }
        # 조건 정보도 동기화
        if profile_data:
            existing["user_conditions"] = profile_data

        up_query = "UPDATE public.users SET profile_json = %s WHERE id = %s;" if db_type == "postgresql" else "UPDATE users SET profile_json = ? WHERE id = ?;"
        cur.execute(up_query, (json.dumps(existing), user_id))
        conn.commit()
        return True
    finally:
        conn.close()

def get_user_profile(user_id: int) -> Dict[str, Any]:
    """
    회원의 저장된 프로필 및 최근 진단 이력을 조회합니다.
    """
    conn, db_type = db_connection.get_connection(allow_sqlite_fallback=True)
    cur = conn.cursor()
    try:
        query = "SELECT id, email, name, provider, profile_json FROM public.users WHERE id = %s;" if db_type == "postgresql" else "SELECT id, email, name, provider, profile_json FROM users WHERE id = ?;"
        cur.execute(query, (user_id,))
        row = cur.fetchone()
        if not row:
            return {}
        prof = row[4]
        if isinstance(prof, str):
            try:
                prof = json.loads(prof)
            except Exception:
                prof = {}
        elif not isinstance(prof, dict):
            prof = {}
        return {
            "id": row[0],
            "email": row[1],
            "name": row[2],
            "provider": row[3],
            "profile": prof
        }
    finally:
        conn.close()

def update_user_profile(user_id: int, profile_data: dict) -> bool:
    """
    회원의 설정 조건(연령, 거주지역구, 고용상태 등)을 DB에 저장/갱신합니다.
    """
    conn, db_type = db_connection.get_connection(allow_sqlite_fallback=True)
    cur = conn.cursor()
    try:
        query = "SELECT profile_json FROM public.users WHERE id = %s;" if db_type == "postgresql" else "SELECT profile_json FROM users WHERE id = ?;"
        cur.execute(query, (user_id,))
        row = cur.fetchone()
        if not row:
            return False
        existing = row[0] if isinstance(row[0], dict) else {}
        if isinstance(row[0], str):
            try:
                existing = json.loads(row[0])
            except Exception:
                existing = {}
        existing["user_conditions"] = profile_data
        up_query = "UPDATE public.users SET profile_json = %s WHERE id = %s;" if db_type == "postgresql" else "UPDATE users SET profile_json = ? WHERE id = ?;"
        cur.execute(up_query, (json.dumps(existing), user_id))
        conn.commit()
        return True
    finally:
        conn.close()

