import logging
import os
import sys
from abc import ABC, abstractmethod
from typing import Any, ClassVar

import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 부모 scripts 및 프로젝트 루트 경로 추가 (db_connection 임포트용)
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(PARENT_DIR)
for p in [PARENT_DIR, PROJECT_ROOT]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from scripts import db_connection
except (ImportError, ModuleNotFoundError):
    import db_connection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%H:%M:%S"
)

class BaseCrawler(ABC):
    """
    모든 청년 정책 크롤러의 기본 추상 클래스.
    PostgreSQL 데이터베이스 연결 및 표준 정책 스키마로의 정규화, Upsert 저장 기능을 제공합니다.
    """

    DEFAULT_HEADERS: ClassVar[dict[str, str]] = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }

    def __init__(self, name: str, source_url: str):
        self.name: str = name
        self.source_url: str = source_url
        self.logger: logging.Logger = logging.getLogger(f"Crawler:{name}")
        self.conn: Any = None
        self.db_type: Any = None
        self.cur: Any = None
        self.session: requests.Session = self.create_session()

        # 사전 중복 방지 인메모리 세트 (DB 기존 적재 데이터 캐시)
        self.existing_ids: set[str] = set()
        self.existing_names: set[str] = set()

        # 통계 카운터
        self.stats: dict[str, int] = {
            "total_fetched": 0,
            "saved_or_updated": 0,
            "skipped_duplicate": 0,
            "errors": 0,
            "skipped_youthcenter": 0
        }

    @staticmethod
    def get_tag_text(elem: Any) -> str:
        """BeautifulSoup 태그 또는 요소에서 안전하게 텍스트를 추출합니다."""
        if elem is None:
            return ""
        if hasattr(elem, "get_text"):
            return str(elem.get_text()).strip()
        if hasattr(elem, "text"):
            return str(elem.text).strip()
        return str(elem).strip()

    @staticmethod
    def get_tag_attr(elem: Any, attr: str, default: str = "") -> str:
        """BeautifulSoup 태그에서 속성값을 안전하게 문자열로 추출합니다."""
        if elem is None:
            return default
        if hasattr(elem, "get"):
            val = elem.get(attr, default)
            if isinstance(val, (list, tuple)):
                return str(val[0]) if val else default
            return str(val or default)
        return default

    def create_session(self) -> requests.Session:
        """
        네트워크 불안정 및 재시도를 처리하는 견고한 requests.Session 객체 생성
        """
        session = requests.Session()
        session.headers.update(self.DEFAULT_HEADERS)

        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            raise_on_status=False
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    @staticmethod
    def clean_policy_name(name: str) -> str:
        """
        중복 검사를 위해 제목에서 공백 및 대괄호, 특수기호를 제거하고 정규화합니다.
        """
        if not name:
            return ""
        import re
        # 대괄호 태그 제거 예: [모집중], [부산] 등
        cleaned = re.sub(r"\[.*?\]", "", name)
        # 영문/숫자/한글만 남기고 공백 및 특수문자 제거
        cleaned = re.sub(r"[^가-힣a-zA-Z0-9]", "", cleaned).lower()
        return cleaned

    def load_existing_policies(self):
        """
        데이터베이스에 이미 적재된 모든 정책 ID와 정규화된 정책명을 메모리에 캐싱하여
        완전한 중복 방지(Deduplication)를 보장합니다.
        """
        if not self.cur:
            return

        try:
            self.cur.execute("SELECT policy_id, name FROM policies;")
            rows = self.cur.fetchall()
            for p_id, p_name in rows:
                if p_id:
                    self.existing_ids.add(str(p_id).strip())
                if p_name:
                    cleaned = self.clean_policy_name(str(p_name))
                    if cleaned:
                        self.existing_names.add(cleaned)
            self.logger.info(
                f"[{self.name}] 기존 DB 정책 {len(rows)}건 사전 캐싱 완료 (중복 방지 준비됨)"
            )
        except Exception as e:  # noqa: BLE001
            self.logger.warning(f"[{self.name}] 기존 정책 캐시 로드 중 예외: {e}")

    def is_duplicate_policy(self, norm_data: dict[str, Any]) -> bool:
        """
        수집된 정책이 기존 DB에 이미 존재하는지 정밀 판별합니다.
        존재할 경우 True를 반환하고, 신규 정책이면 캐시에 등록 후 False를 반환합니다.
        """
        policy_id = str(norm_data.get("policy_id", "")).strip()
        cleaned_name = self.clean_policy_name(str(norm_data.get("name", "")))

        # 1. ID 중복 확인
        if policy_id and policy_id in self.existing_ids:
            self.stats["skipped_duplicate"] += 1
            return True

        # 2. 제목 정규화 중복 확인 (5글자 이상인 유의미한 제목 대상)
        if len(cleaned_name) >= 5 and cleaned_name in self.existing_names:
            self.stats["skipped_duplicate"] += 1
            return True

        # 신규 정책인 경우 캐시에 즉시 등록하여 같은 실행 내 중복도 방어
        if policy_id:
            self.existing_ids.add(policy_id)
        if cleaned_name:
            self.existing_names.add(cleaned_name)

        return False

    @staticmethod
    def is_youthcenter_policy(policy_id: str, url: str = "") -> bool:
        """
        온통청년(청년온통, youthcenter.go.kr) 소속 정책인지 확인하여 제외합니다.
        """
        if "youthcenter.go.kr" in (url or "").lower():
            return True
        # 온통청년 정책 ID 패턴 (예: R202409... 또는 온통청년 일련번호)
        return bool(policy_id.startswith("R20") and len(policy_id) >= 12)

    def init_db(self):
        """데이터베이스 연결 초기화 및 기존 정책 로드"""
        try:
            if self.conn is None or self.cur is None:
                self.conn, self.db_type = db_connection.get_connection(allow_sqlite_fallback=True)
                if self.conn is not None:
                    self.cur = self.conn.cursor()
                self.logger.info(f"[{self.name}] DB 연결 성공: {str(self.db_type).upper()}")
                # 기존 적재 데이터 사전 캐싱
                self.load_existing_policies()
        except Exception as e:
            self.logger.error(f"[{self.name}] DB 연결 실패: {e}")
            raise

    def close_db(self):
        """데이터베이스 연결 종료 및 리소스 정리"""
        if self.cur:
            try:
                self.cur.close()
            except (AttributeError, RuntimeError) as e:
                self.logger.debug(f"커서 닫기 중 예외: {e}")
            finally:
                self.cur = None

        if self.conn:
            try:
                self.conn.close()
            except (AttributeError, RuntimeError) as e:
                self.logger.debug(f"연결 닫기 중 예외: {e}")
            finally:
                self.conn = None

        self.logger.info(f"[{self.name}] DB 세션 종료")

    def normalize_policy(self, raw: dict[str, Any]) -> dict[str, Any]:
        """
        수집된 원본 데이터를 PostgreSQL policies 테이블 스키마에 맞게 정규화합니다.
        """
        # 연령 파싱
        min_age = raw.get("min_age", 19)
        max_age = raw.get("max_age", 39)
        try:
            min_age = int(min_age) if min_age is not None else 19
        except (ValueError, TypeError):
            min_age = 19

        try:
            max_age = int(max_age) if max_age is not None else 39
        except (ValueError, TypeError):
            max_age = 39

        policy_id = str(raw.get("policy_id", "")).strip()
        if not policy_id:
            raise ValueError("policy_id는 필수 항목입니다.")

        title = str(raw.get("name", "")).strip()
        if not title:
            title = "제목 미지정 공고"

        return {
            "policy_id": policy_id,
            "name": title,
            "category_large": str(raw.get("category_large") or "기타").strip(),
            "category_mid": str(raw.get("category_mid") or "공고").strip(),
            "keyword": str(raw.get("keyword") or "").strip(),
            "min_age": min_age,
            "max_age": max_age,
            "age_limit_yn": str(raw.get("age_limit_yn") or "Y").strip(),
            "support_content": str(raw.get("support_content") or "").strip(),
            "explanation": str(raw.get("explanation") or "").strip(),
            "required_docs": str(raw.get("required_docs") or "").strip(),
            "apply_method": str(raw.get("apply_method") or "온라인 접수").strip(),
            "apply_url": str(raw.get("apply_url") or self.source_url).strip(),
            "apply_period": str(raw.get("apply_period") or "공고문 참조").strip(),
            "biz_start_date": str(raw.get("biz_start_date") or "").strip(),
            "biz_end_date": str(raw.get("biz_end_date") or "").strip(),
            "supervising_inst": str(raw.get("supervising_inst") or "지자체/공공기관").strip(),
            "operating_inst": str(raw.get("operating_inst") or "").strip(),
            "zip_codes": str(raw.get("zip_codes") or "").strip(),
        }

    def save_policy(self, norm_data: dict[str, Any], raw_data: dict[str, Any]) -> bool:
        """
        정규화된 데이터를 PostgreSQL policies 테이블에 Upsert합니다.
        (ON CONFLICT (policy_id) DO UPDATE)
        """
        if not self.cur or not self.conn:
            self.init_db()

        try:
            db_connection.upsert_policy(
                cur=self.cur,
                norm=norm_data,
                raw=raw_data,
                db_type=self.db_type
            )
            if self.conn:
                self.conn.commit()
            self.stats["saved_or_updated"] += 1
            return True
        except Exception as e:  # noqa: BLE001
            if self.conn:
                self.conn.rollback()
            self.stats["errors"] += 1
            self.logger.error(f"정책 저장 중 오류 [{norm_data.get('policy_id')}]: {e}")
            return False

    @abstractmethod
    def run(self, limit: int = 10) -> list[dict[str, Any]]:
        """
        각 크롤러 구현체가 반드시 구현해야 하는 크롤링 실행 메서드.
        수집된 정규화 데이터 목록을 반환합니다.
        """
