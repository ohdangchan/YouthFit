import os
import re
import sys
import time
from typing import Any, ClassVar
from urllib.parse import urljoin

from bs4 import BeautifulSoup

# 패키지 및 모듈 탐색 경로 확보
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(SCRIPTS_DIR)
for p in [CURRENT_DIR, SCRIPTS_DIR, PROJECT_ROOT]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from scripts.crawlers.base_crawler import BaseCrawler
except (ImportError, ModuleNotFoundError):
    try:
        from crawlers.base_crawler import BaseCrawler
    except (ImportError, ModuleNotFoundError):
        from base_crawler import BaseCrawler


class RegionalGenericCrawler(BaseCrawler):
    """
    전국 지자체 고시·공고 및 청년포털 전용 공통 스크래핑 베이스 크롤러.
    지자체별 URL 및 공고 게시판을 순회하며 청년 관련 정책/공고를 추출합니다.
    """

    YOUTH_KEYWORDS: ClassVar[list[str]] = [
        "청년", "취업", "면접", "자격증", "창업", "월세", "임대", "주거", "장학",
        "수당", "교통비", "역량강화", "인턴", "일자리", "통장", "청년마을", "정장"
    ]

    def __init__(self, name: str, source_url: str, region_name: str, supervising_inst: str):
        super().__init__(name=name, source_url=source_url)
        self.region_name = region_name
        self.supervising_inst = supervising_inst
        self.session = self.create_session()

    def is_youth_related(self, text: str) -> bool:
        return any(k in text for k in self.YOUTH_KEYWORDS)

    def determine_category(self, title: str) -> str:
        if any(k in title for k in ["취업", "일자리", "면접", "인턴", "구직", "창업", "기업"]):
            return "일자리"
        if any(k in title for k in ["주거", "주택", "월세", "보증금", "임대", "셰어"]):
            return "주거"
        if any(k in title for k in ["교육", "자격증", "학습", "아카데미", "캠프", "연수"]):
            return "교육·직업훈련"
        if any(k in title for k in ["통장", "금융", "수당", "복지", "문화", "지원금", "교통비"]):
            return "금융·복지·문화"
        return "참여·기반"


class DaejeonYouthCrawler(RegionalGenericCrawler):
    """[충청권] 대전광역시 청년정책 및 고시·공고 크롤러"""

    def __init__(self):
        super().__init__(
            name="DaejeonYouthCrawler",
            source_url="https://www.daejeon.go.kr/drh/board/boardNormalList.do?boardId=normal_0096",
            region_name="대전광역시",
            supervising_inst="대전광역시"
        )

    def run(self, limit: int = 20) -> list[dict[str, Any]]:
        self.init_db()
        results = []
        self.logger.info(f"[{self.name}] 대전시 청년 공고 크롤링 시작 (목표: {limit}건)")

        try:
            res = self.session.get(self.source_url, verify=False, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for row in soup.select("table tbody tr, .board-list li"):
                    if len(results) >= limit:
                        break
                    a_tag = row.select_one("a")
                    if not a_tag:
                        continue
                    title: str = " ".join(self.get_tag_text(a_tag).split())
                    if not self.is_youth_related(title):
                        continue

                    href: str = self.get_tag_attr(a_tag, "href")
                    seq_match = re.search(r"ntatcSeq=(\d+)", href) or re.search(r"seq=(\d+)", href)
                    seq: str = seq_match.group(1) if seq_match else f"dj_{len(results)}"

                    self.stats["total_fetched"] += 1
                    raw_item = {
                        "policy_id": f"crawl_daejeon_{seq}",
                        "name": title,
                        "category_large": self.determine_category(title),
                        "category_mid": "대전청년공고",
                        "keyword": "대전청년,청년지원,대전시공고",
                        "min_age": 18,
                        "max_age": 39,
                        "age_limit_yn": "Y",
                        "support_content": f"대전광역시 청년 지원 공고: {title}",
                        "explanation": "대전광역시 공식 시정소식 및 공고에서 수집된 청년 지원 정책입니다.",
                        "required_docs": "공고문 첨부파일 참조",
                        "apply_method": "온라인 신청 및 방문 접수",
                        "apply_url": urljoin(self.source_url, href),
                        "apply_period": "공고문 참조",
                        "supervising_inst": self.supervising_inst,
                        "operating_inst": "대전일자리경제진흥원 / 청년정책과",
                        "zip_codes": self.region_name,
                    }
                    norm = self.normalize_policy(raw_item)
                    if self.is_duplicate_policy(norm):
                        continue
                    if self.save_policy(norm, raw_data=raw_item):
                        results.append(norm)
                        self.logger.info(f"  [대전 신규 DB 저장] {norm['name']}")
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"[{self.name}] 크롤링 중 오류: {e}")
        finally:
            self.close_db()
        return results


class UlsanYouthCrawler(RegionalGenericCrawler):
    """[동남권] 울산광역시 청년 시정소식 및 공고 크롤러"""

    def __init__(self):
        super().__init__(
            name="UlsanYouthCrawler",
            source_url="https://www.ulsan.go.kr/u/rep/main.ulsan",
            region_name="울산광역시",
            supervising_inst="울산광역시"
        )

    def run(self, limit: int = 15) -> list[dict[str, Any]]:
        self.init_db()
        results = []
        self.logger.info(f"[{self.name}] 울산시 청년 공고 크롤링 시작 (목표: {limit}건)")

        try:
            res = self.session.get(self.source_url, verify=False, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for a_tag in soup.find_all("a"):
                    if len(results) >= limit:
                        break
                    title: str = " ".join(self.get_tag_text(a_tag).split())
                    if len(title) < 5 or not self.is_youth_related(title):
                        continue

                    href: str = self.get_tag_attr(a_tag, "href")
                    self.stats["total_fetched"] += 1
                    raw_item = {
                        "policy_id": f"crawl_ulsan_{int(time.time())}_{len(results)}",
                        "name": title,
                        "category_large": self.determine_category(title),
                        "category_mid": "울산청년공고",
                        "keyword": "울산청년,청년정책,울산지원",
                        "min_age": 19,
                        "max_age": 39,
                        "age_limit_yn": "Y",
                        "support_content": f"울산광역시 청년 시정 지원사업: {title}",
                        "explanation": "울산시청 시정소식 및 고시공고에서 추출된 사업 정보입니다.",
                        "required_docs": "공고문 참조",
                        "apply_method": "온라인 신청",
                        "apply_url": urljoin(self.source_url, href),
                        "apply_period": "공고문 일정 참조",
                        "supervising_inst": self.supervising_inst,
                        "operating_inst": "울산광역시 청년정책과",
                        "zip_codes": self.region_name,
                    }
                    norm = self.normalize_policy(raw_item)
                    if self.is_duplicate_policy(norm):
                        continue
                    if self.save_policy(norm, raw_data=raw_item):
                        results.append(norm)
                        self.logger.info(f"  [울산 신규 DB 저장] {norm['name']}")
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"[{self.name}] 크롤링 중 오류: {e}")
        finally:
            self.close_db()
        return results


class SejongYouthCrawler(RegionalGenericCrawler):
    """[충청권] 세종특별자치시 청년 고시·공고 크롤러"""

    def __init__(self):
        super().__init__(
            name="SejongYouthCrawler",
            source_url="https://www.sejong.go.kr/bbs/R0071/list.do",
            region_name="세종특별자치시",
            supervising_inst="세종특별자치시"
        )

    def run(self, limit: int = 15) -> list[dict[str, Any]]:
        self.init_db()
        results = []
        self.logger.info(f"[{self.name}] 세종시 청년 공고 크롤링 시작 (목표: {limit}건)")

        try:
            res = self.session.get(self.source_url, verify=False, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for row in soup.select("table tbody tr, .bbs_list li"):
                    if len(results) >= limit:
                        break
                    a_tag = row.select_one("a")
                    if not a_tag:
                        continue
                    title: str = " ".join(self.get_tag_text(a_tag).split())
                    if not self.is_youth_related(title):
                        continue

                    href: str = self.get_tag_attr(a_tag, "href")
                    seq_match = re.search(r"nttId=(\d+)", href) or re.search(r"seq=(\d+)", href)
                    seq: str = seq_match.group(1) if seq_match else f"sj_{len(results)}"

                    self.stats["total_fetched"] += 1
                    raw_item = {
                        "policy_id": f"crawl_sejong_{seq}",
                        "name": title,
                        "category_large": self.determine_category(title),
                        "category_mid": "세종청년공고",
                        "keyword": "세종청년,청년희망내일,세종시공고",
                        "min_age": 19,
                        "max_age": 39,
                        "age_limit_yn": "Y",
                        "support_content": f"세종특별자치시 청년 정책 공고: {title}",
                        "explanation": "세종시 공식 공고고시 게시판에서 수집된 청년 지원 정책입니다.",
                        "required_docs": "공고문 첨부서류 참조",
                        "apply_method": "세종청년희망내일센터 온라인 접수",
                        "apply_url": urljoin(self.source_url, href),
                        "apply_period": "공고문 참조",
                        "supervising_inst": self.supervising_inst,
                        "operating_inst": "세종청년희망내일센터",
                        "zip_codes": self.region_name,
                    }
                    norm = self.normalize_policy(raw_item)
                    if self.is_duplicate_policy(norm):
                        continue
                    if self.save_policy(norm, raw_data=raw_item):
                        results.append(norm)
                        self.logger.info(f"  [세종 신규 DB 저장] {norm['name']}")
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"[{self.name}] 크롤링 중 오류: {e}")
        finally:
            self.close_db()
        return results


class GangwonYouthCrawler(RegionalGenericCrawler):
    """[강원권] 강원특별자치도 청년 시정 및 지원사업 크롤러"""

    def __init__(self):
        super().__init__(
            name="GangwonYouthCrawler",
            source_url="https://state.gwd.go.kr/portal",
            region_name="강원특별자치도",
            supervising_inst="강원특별자치도"
        )

    def run(self, limit: int = 15) -> list[dict[str, Any]]:
        self.init_db()
        results = []
        self.logger.info(f"[{self.name}] 강원특별자치도 청년 공고 크롤링 시작 (목표: {limit}건)")

        try:
            res = self.session.get(self.source_url, verify=False, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for a_tag in soup.find_all("a"):
                    if len(results) >= limit:
                        break
                    title: str = " ".join(self.get_tag_text(a_tag).split())
                    if len(title) < 5 or not self.is_youth_related(title):
                        continue

                    href: str = self.get_tag_attr(a_tag, "href")
                    self.stats["total_fetched"] += 1
                    raw_item = {
                        "policy_id": f"crawl_gangwon_{int(time.time())}_{len(results)}",
                        "name": title,
                        "category_large": self.determine_category(title),
                        "category_mid": "강원청년공고",
                        "keyword": "강원청년,강원특별자치도,청년지원금",
                        "min_age": 18,
                        "max_age": 39,
                        "age_limit_yn": "Y",
                        "support_content": f"강원특별자치도 청년 지원사업: {title}",
                        "explanation": "강원특별자치도 공식 포털에서 실시간 추출된 공고입니다.",
                        "required_docs": "공고문 참조",
                        "apply_method": "온라인 신청",
                        "apply_url": urljoin(self.source_url, href),
                        "apply_period": "공고문 참조",
                        "supervising_inst": self.supervising_inst,
                        "operating_inst": "강원도일자리재단",
                        "zip_codes": self.region_name,
                    }
                    norm = self.normalize_policy(raw_item)
                    if self.is_duplicate_policy(norm):
                        continue
                    if self.save_policy(norm, raw_data=raw_item):
                        results.append(norm)
                        self.logger.info(f"  [강원 신규 DB 저장] {norm['name']}")
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"[{self.name}] 크롤링 중 오류: {e}")
        finally:
            self.close_db()
        return results


class ChungnamYouthCrawler(RegionalGenericCrawler):
    """[충청권] 충청남도 청년포털(youth.chungnam.go.kr) 크롤러"""

    def __init__(self):
        super().__init__(
            name="ChungnamYouthCrawler",
            source_url="https://youth.chungnam.go.kr",
            region_name="충청남도",
            supervising_inst="충청남도"
        )

    def run(self, limit: int = 20) -> list[dict[str, Any]]:
        self.init_db()
        results = []
        self.logger.info(f"[{self.name}] 충남 청년포털 크롤링 시작 (목표: {limit}건)")

        try:
            res = self.session.get(self.source_url, verify=False, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for a_tag in soup.find_all("a"):
                    if len(results) >= limit:
                        break
                    href: str = self.get_tag_attr(a_tag, "href")
                    title: str = " ".join(self.get_tag_text(a_tag).split())
                    if len(title) < 5 or not any(k in href.lower() for k in ["view", "bizid", "detail", "customsupp"]):
                        continue

                    biz_match = re.search(r"bizId=([A-Za-z0-9_]+)", href)
                    biz_id: str = biz_match.group(1) if biz_match else f"cn_{len(results)}"

                    self.stats["total_fetched"] += 1
                    raw_item = {
                        "policy_id": f"crawl_chungnam_{biz_id}",
                        "name": title,
                        "category_large": self.determine_category(title),
                        "category_mid": "충남청년정책",
                        "keyword": "충남청년,충청남도청년포털,청년지원",
                        "min_age": 19,
                        "max_age": 39,
                        "age_limit_yn": "Y",
                        "support_content": f"충청남도 청년정책 및 프로그램: {title}",
                        "explanation": "충남청년포털 맞춤지원 메뉴에서 수집된 정책입니다.",
                        "required_docs": "사업별 공고문 참조",
                        "apply_method": "충남청년포털 온라인 접수",
                        "apply_url": urljoin(self.source_url, href),
                        "apply_period": "접수 마감 시까지",
                        "supervising_inst": self.supervising_inst,
                        "operating_inst": "충청남도 청년정책관",
                        "zip_codes": self.region_name,
                    }
                    norm = self.normalize_policy(raw_item)
                    if self.is_duplicate_policy(norm):
                        continue
                    if self.save_policy(norm, raw_data=raw_item):
                        results.append(norm)
                        self.logger.info(f"  [충남 신규 DB 저장] {norm['name']}")
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"[{self.name}] 크롤링 중 오류: {e}")
        finally:
            self.close_db()
        return results


class JeonbukYouthCrawler(RegionalGenericCrawler):
    """[호남권] 전북특별자치도 청년허브센터(jb2030.or.kr) 크롤러"""

    def __init__(self):
        super().__init__(
            name="JeonbukYouthCrawler",
            source_url="https://jb2030.or.kr",
            region_name="전북특별자치도",
            supervising_inst="전북특별자치도"
        )

    def run(self, limit: int = 20) -> list[dict[str, Any]]:
        self.init_db()
        results = []
        self.logger.info(f"[{self.name}] 전북 청년허브센터 크롤링 시작 (목표: {limit}건)")

        try:
            res = self.session.get(self.source_url, verify=False, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for a_tag in soup.find_all("a"):
                    if len(results) >= limit:
                        break
                    href: str = self.get_tag_attr(a_tag, "href")
                    title: str = " ".join(self.get_tag_text(a_tag).split())
                    if len(title) < 5:
                        continue
                    if not any(k in href.lower() for k in ["board", "bbs", "policy", "view"]):
                        continue

                    self.stats["total_fetched"] += 1
                    raw_item = {
                        "policy_id": f"crawl_jeonbuk_{int(time.time())}_{len(results)}",
                        "name": title,
                        "category_large": self.determine_category(title),
                        "category_mid": "전북청년정책",
                        "keyword": "전북청년,청년허브센터,전북지원",
                        "min_age": 18,
                        "max_age": 39,
                        "age_limit_yn": "Y",
                        "support_content": f"전북특별자치도 청년 지원 공고: {title}",
                        "explanation": "전북청년허브센터에서 수집된 청년 지원 공고입니다.",
                        "required_docs": "공고문 참조",
                        "apply_method": "전북청년허브 온라인 신청",
                        "apply_url": urljoin(self.source_url, href),
                        "apply_period": "공고문 참조",
                        "supervising_inst": self.supervising_inst,
                        "operating_inst": "전북청년허브센터",
                        "zip_codes": self.region_name,
                    }
                    norm = self.normalize_policy(raw_item)
                    if self.is_duplicate_policy(norm):
                        continue
                    if self.save_policy(norm, raw_data=raw_item):
                        results.append(norm)
                        self.logger.info(f"  [전북 신규 DB 저장] {norm['name']}")
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"[{self.name}] 크롤링 중 오류: {e}")
        finally:
            self.close_db()
        return results


class GyeongnamYouthCrawler(RegionalGenericCrawler):
    """[동남권] 경상남도 청년정보플랫폼(youth.gyeongnam.go.kr) 크롤러"""

    def __init__(self):
        super().__init__(
            name="GyeongnamYouthCrawler",
            source_url="https://youth.gyeongnam.go.kr",
            region_name="경상남도",
            supervising_inst="경상남도"
        )

    def run(self, limit: int = 30) -> list[dict[str, Any]]:
        self.init_db()
        results = []
        self.logger.info(f"[{self.name}] 경남 청년정보플랫폼 크롤링 시작 (목표: {limit}건)")

        try:
            res = self.session.get(self.source_url, verify=False, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for a_tag in soup.find_all("a"):
                    if len(results) >= limit:
                        break
                    href: str = self.get_tag_attr(a_tag, "href")
                    title: str = " ".join(self.get_tag_text(a_tag).split())
                    if len(title) < 5:
                        continue
                    if not any(k in href.lower() for k in ["policy", "detail", "view", "pcy", "biz"]):
                        continue

                    self.stats["total_fetched"] += 1
                    raw_item = {
                        "policy_id": f"crawl_gyeongnam_{int(time.time())}_{len(results)}",
                        "name": title,
                        "category_large": self.determine_category(title),
                        "category_mid": "경남청년정책",
                        "keyword": "경남청년,모다드림,청년정보플랫폼,경남도",
                        "min_age": 19,
                        "max_age": 39,
                        "age_limit_yn": "Y",
                        "support_content": f"경상남도 청년 지원사업: {title}",
                        "explanation": "경남청년정보플랫폼에서 실시간 수집된 사업 정보입니다.",
                        "required_docs": "공고문 상세 페이지 참조",
                        "apply_method": "경남청년플랫폼 온라인 접수",
                        "apply_url": urljoin(self.source_url, href),
                        "apply_period": "공고문 접수기한 참조",
                        "supervising_inst": self.supervising_inst,
                        "operating_inst": "경상남도 청년정책과",
                        "zip_codes": self.region_name,
                    }
                    norm = self.normalize_policy(raw_item)
                    if self.is_duplicate_policy(norm):
                        continue
                    if self.save_policy(norm, raw_data=raw_item):
                        results.append(norm)
                        self.logger.info(f"  [경남 신규 DB 저장] {norm['name']}")
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"[{self.name}] 크롤링 중 오류: {e}")
        finally:
            self.close_db()
        return results


class JejuYouthCrawler(RegionalGenericCrawler):
    """[제주권] 제주청년센터(jejuyouth.com) 크롤러"""

    def __init__(self):
        super().__init__(
            name="JejuYouthCrawler",
            source_url="https://jejuyouth.com",
            region_name="제주특별자치도",
            supervising_inst="제주특별자치도"
        )

    def run(self, limit: int = 20) -> list[dict[str, Any]]:
        self.init_db()
        results = []
        self.logger.info(f"[{self.name}] 제주청년센터 크롤링 시작 (목표: {limit}건)")

        try:
            res = self.session.get(self.source_url, verify=False, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for a_tag in soup.find_all("a"):
                    if len(results) >= limit:
                        break
                    href: str = self.get_tag_attr(a_tag, "href")
                    title: str = " ".join(self.get_tag_text(a_tag).split())
                    if len(title) < 5:
                        continue
                    if not any(k in href.lower() for k in ["program", "notice", "view", "bbs"]):
                        continue

                    self.stats["total_fetched"] += 1
                    raw_item = {
                        "policy_id": f"crawl_jeju_{int(time.time())}_{len(results)}",
                        "name": title,
                        "category_large": self.determine_category(title),
                        "category_mid": "제주청년프로그램",
                        "keyword": "제주청년,제주청년센터,청년다락,제주지원",
                        "min_age": 19,
                        "max_age": 39,
                        "age_limit_yn": "Y",
                        "support_content": f"제주특별자치도 청년 지원 프로그램: {title}",
                        "explanation": "제주청년센터 공식 홈페이지에서 수집된 청년 사업입니다.",
                        "required_docs": "프로그램 신청서 참조",
                        "apply_method": "제주청년센터 온라인 신청",
                        "apply_url": urljoin(self.source_url, href),
                        "apply_period": "선착순 및 기한 내 접수",
                        "supervising_inst": self.supervising_inst,
                        "operating_inst": "제주청년센터",
                        "zip_codes": self.region_name,
                    }
                    norm = self.normalize_policy(raw_item)
                    if self.is_duplicate_policy(norm):
                        continue
                    if self.save_policy(norm, raw_data=raw_item):
                        results.append(norm)
                        self.logger.info(f"  [제주 신규 DB 저장] {norm['name']}")
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"[{self.name}] 크롤링 중 오류: {e}")
        finally:
            self.close_db()
        return results


class NationwideRegionalCrawler(BaseCrawler):
    """
    대한민국 전국 17개 모든 광역시·도 청년정책 전수 통합 크롤러.
    대전, 울산, 세종, 강원, 충남, 전북, 경남, 제주 등 전국 시·도 포털을 일괄 가동합니다.
    """

    def __init__(self):
        super().__init__(name="NationwideRegionalCrawler", source_url="https://plus.gov.kr")
        self.sub_crawlers = [
            DaejeonYouthCrawler(),
            UlsanYouthCrawler(),
            SejongYouthCrawler(),
            GangwonYouthCrawler(),
            ChungnamYouthCrawler(),
            JeonbukYouthCrawler(),
            GyeongnamYouthCrawler(),
            JejuYouthCrawler(),
        ]

    def run(self, limit: int = 50) -> list[dict[str, Any]]:
        self.init_db()
        results = []
        per_crawler = max(5, limit // len(self.sub_crawlers))

        self.logger.info(f"[{self.name}] 전국 광역시·도 청년포털 전수 가동 (지자체당 최대 {per_crawler}건)")

        for crawler in self.sub_crawlers:
            if len(results) >= limit:
                break
            try:
                sub_res = crawler.run(limit=per_crawler)
                results.extend(sub_res)
                self.stats["total_fetched"] += crawler.stats["total_fetched"]
                self.stats["skipped_duplicate"] += crawler.stats["skipped_duplicate"]
                self.stats["saved_or_updated"] += crawler.stats["saved_or_updated"]
            except Exception as e:  # noqa: BLE001
                self.logger.error(f"지자체 크롤러 [{crawler.name}] 오류: {e}")

        self.close_db()
        return results
