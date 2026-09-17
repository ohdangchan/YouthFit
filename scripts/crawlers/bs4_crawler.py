import os
import re
import sys
import time
from typing import Any
from urllib.parse import urljoin

import requests
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


class BusanYouthCrawler(BaseCrawler):
    """
    [동남권] 부산 청년플랫폼(young.busan.go.kr) 실시간 정책 및 프로그램 크롤러
    다중 페이징(1~10페이지)을 순회하며 기존 DB와 중복되지 않는 신규 정책을 수집합니다.
    """

    def __init__(self):
        super().__init__(
            name="BusanYouthCrawler",
            source_url="https://young.busan.go.kr/policySupport/list.nm?menuCd=12"
        )
        self.session = self.create_session()

    def run(self, limit: int = 50) -> list[dict[str, Any]]:
        self.init_db()
        results = []
        page = 1
        max_pages = 10  # 최대 10페이지 심층 순회

        self.logger.info(f"[{self.name}] 부산 청년플랫폼 심층 크롤링 시작 (최대 10페이지, 목표: {limit}건)")

        try:
            while len(results) < limit and page <= max_pages:
                url = f"{self.source_url}&pageIndex={page}"
                try:
                    res = self.session.get(url, verify=False, timeout=15)
                    if res.status_code != 200:
                        self.logger.warning(f"  부산 페이지 {page} 응답 코드 {res.status_code}")
                        break

                    soup = BeautifulSoup(res.text, "html.parser")
                    page_items_found: int = 0
                    seen_sids: set[str] = set()

                    for a in soup.find_all("a"):
                        if len(results) >= limit:
                            break

                        href: str = self.get_tag_attr(a, "href")
                        if not ("bizSid=" in href or "view.nm" in href):
                            continue

                        match = re.search(r"bizSid=([A-Za-z0-9_]+)", href)
                        sid: str = match.group(1) if match else f"busan_p{page}_{len(results)}"
                        if sid in seen_sids:
                            continue
                        seen_sids.add(sid)

                        raw_text: str = " ".join(self.get_tag_text(a).split())
                        if len(raw_text) < 5:
                            continue

                        page_items_found += 1
                        self.stats["total_fetched"] += 1
                        policy_id = f"crawl_busan_{sid}"

                        # 분야 카테고리 추출
                        cat_large = "금융·복지·문화"
                        cat_match = re.search(r"\[(.*?)분야?\]", raw_text)
                        if cat_match:
                            extracted_cat = cat_match.group(1)
                            if "일자리" in extracted_cat or "취업" in extracted_cat:
                                cat_large = "일자리"
                            elif "교육" in extracted_cat:
                                cat_large = "교육·직업훈련"
                            elif "주거" in extracted_cat:
                                cat_large = "주거"
                            elif "참여" in extracted_cat:
                                cat_large = "참여·기반"

                        # 신청 기간 추출
                        period_match = re.search(r"(\d{4}-\d{2}-\d{2}\s*~\s*\d{4}-\d{2}-\d{2})", raw_text)
                        apply_period = period_match.group(1) if period_match else "상시 접수"

                        # 제목 정리
                        clean_title = re.sub(r"\[.*?\]", "", raw_text)
                        clean_title = re.sub(r"신청기간.*$", "", clean_title)
                        clean_title = re.sub(r"\s+", " ", clean_title).strip()
                        if not clean_title:
                            clean_title = raw_text[:50]

                        full_url = urljoin(self.source_url, href)

                        raw_item = {
                            "policy_id": policy_id,
                            "name": clean_title,
                            "category_large": cat_large,
                            "category_mid": "부산청년지원",
                            "keyword": "부산청년,역량강화,청년프로그램,부산지원",
                            "min_age": 18,
                            "max_age": 39,
                            "age_limit_yn": "Y",
                            "support_content": f"부산광역시 청년정책 및 프로그램 지원 (신청기간: {apply_period})",
                            "explanation": f"부산청년플랫폼에서 실시간 수집된 사업 공고입니다: {raw_text}",
                            "required_docs": "상세 링크 웹페이지 참조",
                            "apply_method": "부산청년플랫폼 온라인 신청",
                            "apply_url": full_url,
                            "apply_period": apply_period,
                            "supervising_inst": "부산광역시",
                            "operating_inst": "부산광역시 청년정책과",
                            "zip_codes": "부산광역시",
                        }

                        norm = self.normalize_policy(raw_item)

                        # 사전 중복 검증: 기존 DB 또는 동일 실행 내 중복이면 건너뜀
                        if self.is_duplicate_policy(norm):
                            continue

                        if self.save_policy(norm, raw_data=raw_item):
                            results.append(norm)
                            self.logger.info(f"  [부산 신규 DB 저장] {norm['name']} ({norm['policy_id']})")

                    if page_items_found == 0:
                        break

                    page += 1
                    time.sleep(0.3)
                except requests.RequestException as req_err:
                    self.logger.warning(f"  부산 페이지 {page} 요청 중 네트워크 지연 ({req_err})")
                    break

        finally:
            self.close_db()

        self.logger.info(
            f"[{self.name}] 완료: 탐색 {self.stats['total_fetched']}건, "
            f"중복스킵 {self.stats['skipped_duplicate']}건, 신규적재 {self.stats['saved_or_updated']}건"
        )
        return results


class IncheonYouthCrawler(BaseCrawler):
    """
    [수도권] 인천 청년정책 유스톡톡(youth.incheon.go.kr) 실시간 정책 크롤러
    정책 목록 및 4대 공지 게시판(공지사항, 유유기지, 자료실 등)을 전수 순회합니다.
    """

    def __init__(self):
        super().__init__(
            name="IncheonYouthCrawler",
            source_url="https://youth.incheon.go.kr/youthpolicy/youthPolicyInfoList.do"
        )
        self.session = self.create_session()

    def run(self, limit: int = 40) -> list[dict[str, Any]]:
        self.init_db()
        results = []

        self.logger.info(f"[{self.name}] 인천 유스톡톡 심층 정책 크롤링 시작 (목표: {limit}건)")

        try:
            # 1. 정책 목록 페이지 크롤링
            res = self.session.get(self.source_url, verify=False, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                seen_seqs: set[str] = set()

                for a in soup.find_all("a"):
                    if len(results) >= limit:
                        break

                    href: str = self.get_tag_attr(a, "href")
                    if "poly_seq=" not in href:
                        continue

                    seq_match = re.search(r"poly_seq=(\d+)", href)
                    if not seq_match:
                        continue
                    seq: str = seq_match.group(1)
                    if seq in seen_seqs:
                        continue
                    seen_seqs.add(seq)

                    title: str = " ".join(self.get_tag_text(a).split())
                    if not title or len(title) < 4:
                        continue

                    self.stats["total_fetched"] += 1
                    policy_id = f"crawl_incheon_{seq}"
                    full_url = urljoin(self.source_url, href)

                    cat_large = "금융·복지·문화"
                    if any(k in title for k in ["일자리", "취업", "인재", "인턴", "구직"]):
                        cat_large = "일자리"
                    elif any(k in title for k in ["주택", "임차", "월세", "보증금", "주거"]):
                        cat_large = "주거"
                    elif any(k in title for k in ["교육", "아카데미", "부트캠프", "연수"]):
                        cat_large = "교육·직업훈련"
                    elif any(k in title for k in ["참여", "공동체", "네트워크", "위원회"]):
                        cat_large = "참여·기반"

                    raw_item = {
                        "policy_id": policy_id,
                        "name": title,
                        "category_large": cat_large,
                        "category_mid": "인천청년정책",
                        "keyword": "인천청년,유스톡톡,인천시,청년지원",
                        "min_age": 18,
                        "max_age": 39,
                        "age_limit_yn": "Y",
                        "support_content": f"인천광역시 청년 대상 지원사업: {title}",
                        "explanation": "인천 유스톡톡 청년포털에서 실시간 수집된 지원 정책 공고입니다.",
                        "required_docs": "공고 상세 및 신청 사이트 안내 참조",
                        "apply_method": "인천 유스톡톡 온라인 접수",
                        "apply_url": full_url,
                        "apply_period": "접수 마감 시까지",
                        "supervising_inst": "인천광역시",
                        "operating_inst": "인천광역시 청년정책담당관",
                        "zip_codes": "인천광역시",
                    }

                    norm = self.normalize_policy(raw_item)
                    if self.is_duplicate_policy(norm):
                        continue

                    if self.save_policy(norm, raw_data=raw_item):
                        results.append(norm)
                        self.logger.info(f"  [인천 신규 DB 저장] {norm['name']} ({norm['policy_id']})")

            # 2. 인천 유스톡톡 다중 게시판 순회 (notice, ysg_notice, yic_notice, data)
            board_codes = ["notice", "ysg_notice", "yic_notice", "data"]
            for bcd in board_codes:
                if len(results) >= limit:
                    break
                notice_url = f"https://youth.incheon.go.kr/bbs/bbsMsgList.do?bcd={bcd}"
                try:
                    n_res = self.session.get(notice_url, verify=False, timeout=15)
                    if n_res.status_code == 200:
                        n_soup = BeautifulSoup(n_res.text, "html.parser")
                        for tr in n_soup.select("table tbody tr, .bbs-list li"):
                            if len(results) >= limit:
                                break
                            a_tag = tr.select_one("a[href*='msg_seq=']")
                            if not a_tag:
                                 continue
                            n_title: str = " ".join(self.get_tag_text(a_tag).split())
                            n_href: str = self.get_tag_attr(a_tag, "href")
                            m_match = re.search(r"msg_seq=(\d+)", n_href)
                            if not m_match or len(n_title) < 4:
                                 continue
                            m_seq: str = m_match.group(1)
                            pol_id = f"crawl_incheon_msg_{bcd}_{m_seq}"

                            self.stats["total_fetched"] += 1
                            raw_item = {
                                "policy_id": pol_id,
                                "name": n_title,
                                "category_large": "참여·기반",
                                "category_mid": f"인천청년_{bcd}",
                                "keyword": "인천청년,유스톡톡,공지안내,프로그램",
                                "min_age": 18,
                                "max_age": 39,
                                "age_limit_yn": "Y",
                                "support_content": f"인천광역시 청년 프로그램 및 공고: {n_title}",
                                "explanation": f"인천 청년포털 {bcd} 게시판에서 수집된 정보입니다.",
                                "required_docs": "공고문 첨부파일 참조",
                                "apply_method": "온라인 신청 또는 방문 접수",
                                "apply_url": urljoin(notice_url, n_href),
                                "apply_period": "공고문 접수기한 참조",
                                "supervising_inst": "인천광역시",
                                "operating_inst": "인천청년센터 / 청년정책과",
                                "zip_codes": "인천광역시",
                            }
                            norm = self.normalize_policy(raw_item)
                            if self.is_duplicate_policy(norm):
                                continue

                            if self.save_policy(norm, raw_data=raw_item):
                                results.append(norm)
                                self.logger.info(f"  [인천 게시판 신규 DB 저장] {norm['name']}")
                except Exception as e:  # noqa: BLE001
                    self.logger.warning(f"인천 게시판({bcd}) 크롤링 중 예외: {e}")

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"[{self.name}] 크롤링 중 오류: {e}")
        finally:
            self.close_db()

        self.logger.info(
            f"[{self.name}] 완료: 탐색 {self.stats['total_fetched']}건, "
            f"중복스킵 {self.stats['skipped_duplicate']}건, 신규적재 {self.stats['saved_or_updated']}건"
        )
        return results


class ShHousingCrawler(BaseCrawler):
    """
    [주거 특화] 서울주택도시공사(SH) 청년·신혼부부 행복주택/임대주택 공고 크롤러
    1~5페이지 청약공고를 심층 순회하며 신규 주거 공고를 수집합니다.
    """

    def __init__(self):
        super().__init__(
            name="ShHousingCrawler",
            source_url="https://www.i-sh.co.kr/main/lay2/program/S1T294C297/www/brd/m_247/list.do"
        )
        self.session = self.create_session()

    def run(self, limit: int = 30) -> list[dict[str, Any]]:
        self.init_db()
        results = []
        max_pages = 5  # 최대 5페이지 순회

        self.logger.info(f"[{self.name}] SH 서울주택도시공사 심층 청약공고 크롤링 시작 (목표: {limit}건)")

        try:
            for page in range(1, max_pages + 1):
                if len(results) >= limit:
                    break

                page_url = f"{self.source_url}?pageIndex={page}"
                res = self.session.get(page_url, verify=False, timeout=15)
                if res.status_code != 200:
                    break

                soup = BeautifulSoup(res.text, "html.parser")
                rows = soup.select("tbody tr")
                if not rows:
                    break

                for row in rows:
                    if len(results) >= limit:
                        break

                    a_tag = row.select_one("a")
                    if not a_tag:
                        continue

                    title: str = " ".join(self.get_tag_text(a_tag).split())
                    onclick: str = self.get_tag_attr(a_tag, "onclick")
                    seq_match = re.search(r"getDetailView\('(\d+)'\)", onclick)
                    seq: str = seq_match.group(1) if seq_match else f"sh_p{page}_{len(results)}"

                    tds = row.select("td")
                    date_str: str = self.get_tag_text(tds[-2]) if len(tds) >= 4 else "상시"

                    policy_id = f"crawl_sh_{seq}"
                    detail_url = f"https://www.i-sh.co.kr/main/lay2/program/S1T294C297/www/brd/m_247/detail.do?seq={seq}"

                    self.stats["total_fetched"] += 1

                    raw_item = {
                        "policy_id": policy_id,
                        "name": title,
                        "category_large": "주거",
                        "category_mid": "공공임대주택",
                        "keyword": "SH,서울주택도시공사,청년안심주택,행복주택,임대공고,장기전세",
                        "min_age": 19,
                        "max_age": 39,
                        "age_limit_yn": "Y",
                        "support_content": f"서울주택도시공사 공공/민간 임대주택 입주 및 청약 (공고일: {date_str})",
                        "explanation": f"SH 청약정보 게시판에서 실시간 수집된 주택 공급 공고입니다: {title}",
                        "required_docs": "공고문 첨부파일 및 입주자격 증빙서류",
                        "apply_method": "SH 인터넷 청약시스템(i-sh.co.kr/app)",
                        "apply_url": detail_url,
                        "apply_period": date_str,
                        "supervising_inst": "서울특별시",
                        "operating_inst": "서울주택도시공사",
                        "zip_codes": "서울특별시",
                    }

                    norm = self.normalize_policy(raw_item)
                    if self.is_duplicate_policy(norm):
                        continue

                    if self.save_policy(norm, raw_data=raw_item):
                        results.append(norm)
                        self.logger.info(f"  [SH 신규 주거 DB 저장] {norm['name']} ({norm['policy_id']})")

                time.sleep(0.3)

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"[{self.name}] 크롤링 중 오류: {e}")
        finally:
            self.close_db()

        self.logger.info(
            f"[{self.name}] 완료: 탐색 {self.stats['total_fetched']}건, "
            f"중복스킵 {self.stats['skipped_duplicate']}건, 신규적재 {self.stats['saved_or_updated']}건"
        )
        return results


class DaeguYouthCrawler(BaseCrawler):
    """
    [대경권] 대구광역시 청년정책 포털(daegu.go.kr/YouthPolicy) 크롤러
    """

    def __init__(self):
        super().__init__(
            name="DaeguYouthCrawler",
            source_url="https://www.daegu.go.kr/YouthPolicy/index.do"
        )
        self.session = self.create_session()

    def run(self, limit: int = 30) -> list[dict[str, Any]]:
        self.init_db()
        results = []

        self.logger.info(f"[{self.name}] 대구광역시 청년정책 크롤링 시작 (목표: {limit}건)")

        try:
            res = self.session.get(self.source_url, verify=False, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                seen_menus: set[str] = set()
                for a in soup.find_all("a"):
                    if len(results) >= limit:
                        break

                    href: str = self.get_tag_attr(a, "href")
                    if "menu_id=" not in href:
                        continue

                    m_match = re.search(r"menu_id=(\d+)", href)
                    if not m_match:
                        continue
                    menu_id: str = m_match.group(1)
                    if menu_id in seen_menus:
                        continue
                    seen_menus.add(menu_id)

                    title: str = " ".join(self.get_tag_text(a).split())
                    if len(title) < 3 or title in ["대구청년정책", "바로가기", "홈"]:
                        continue

                    self.stats["total_fetched"] += 1
                    policy_id = f"crawl_daegu_{menu_id}"
                    full_url = urljoin(self.source_url, href)

                    cat_large = "금융·복지·문화"
                    if "참여" in title or "기반" in title:
                        cat_large = "참여·기반"
                    elif "일자리" in title or "진입" in title:
                        cat_large = "일자리"

                    raw_item = {
                        "policy_id": policy_id,
                        "name": f"대구 청년 {title} 지원사업",
                        "category_large": cat_large,
                        "category_mid": "대구청년정책",
                        "keyword": "대구청년,탄탄대로,청년정책,대구시",
                        "min_age": 19,
                        "max_age": 39,
                        "age_limit_yn": "Y",
                        "support_content": f"대구광역시 청년 정책 세부 프로그램 ({title})",
                        "explanation": "대구시 공식 청년정책 포털에서 실시간 수집된 사업 정보입니다.",
                        "required_docs": "공고문 및 온라인 신청 안내 참조",
                        "apply_method": "대구청년포털 온라인 신청",
                        "apply_url": full_url,
                        "apply_period": "상시 및 분기별 모집",
                        "supervising_inst": "대구광역시",
                        "operating_inst": "대구광역시 청년정책과",
                        "zip_codes": "대구광역시",
                    }

                    norm = self.normalize_policy(raw_item)
                    if self.is_duplicate_policy(norm):
                        continue

                    if self.save_policy(norm, raw_data=raw_item):
                        results.append(norm)
                        self.logger.info(f"  [대구 신규 DB 저장] {norm['name']} ({norm['policy_id']})")

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"[{self.name}] 크롤링 중 오류: {e}")
        finally:
            self.close_db()

        self.logger.info(
            f"[{self.name}] 완료: 탐색 {self.stats['total_fetched']}건, "
            f"중복스킵 {self.stats['skipped_duplicate']}건, 신규적재 {self.stats['saved_or_updated']}건"
        )
        return results


class GwangjuYouthCrawler(BaseCrawler):
    """
    [호남권] 광주광역시 청년정책플랫폼(youth.gwangju.go.kr) 실시간 정책 크롤러
    """

    def __init__(self):
        super().__init__(
            name="GwangjuYouthCrawler",
            source_url="https://youth.gwangju.go.kr"
        )
        self.session = self.create_session()

    def run(self, limit: int = 20) -> list[dict[str, Any]]:
        self.init_db()
        results = []

        self.logger.info(f"[{self.name}] 광주 청년정책플랫폼 크롤링 시작 (목표: {limit}건)")

        try:
            res = self.session.get(self.source_url, verify=False, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                seen_hrefs: set[str] = set()
                for a in soup.find_all("a"):
                    if len(results) >= limit:
                        break
                    href: str = self.get_tag_attr(a, "href")
                    title: str = " ".join(self.get_tag_text(a).split())
                    if len(title) < 4 or href in seen_hrefs:
                        continue
                    if not any(k in href.lower() for k in ["policy", "pcy", "view", "bbs", "board", "detail"]):
                        continue

                    seen_hrefs.add(href)
                    self.stats["total_fetched"] += 1
                    full_url = urljoin(self.source_url, href)

                    # ID 추출
                    id_match = re.search(r"(?:policyId|seq|msg_seq|id)=(\d+)", href)
                    item_id = id_match.group(1) if id_match else f"gj_{len(results)}"
                    policy_id = f"crawl_gwangju_{item_id}"

                    raw_item = {
                        "policy_id": policy_id,
                        "name": f"광주 청년 {title}",
                        "category_large": "참여·기반",
                        "category_mid": "광주청년정책",
                        "keyword": "광주청년,광주광역시,청년정책플랫폼",
                        "min_age": 19,
                        "max_age": 39,
                        "age_limit_yn": "Y",
                        "support_content": f"광주광역시 청년 지원사업 및 프로그램 ({title})",
                        "explanation": "광주 청년정책플랫폼에서 실시간 수집된 사업 정보입니다.",
                        "required_docs": "공고문 및 온라인 신청 안내 참조",
                        "apply_method": "광주 청년정책플랫폼 온라인 접수",
                        "apply_url": full_url,
                        "apply_period": "공고문 참조",
                        "supervising_inst": "광주광역시",
                        "operating_inst": "광주청년센터",
                        "zip_codes": "광주광역시",
                    }

                    norm = self.normalize_policy(raw_item)
                    if self.is_duplicate_policy(norm):
                        continue

                    if self.save_policy(norm, raw_data=raw_item):
                        results.append(norm)
                        self.logger.info(f"  [광주 신규 DB 저장] {norm['name']}")

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"[{self.name}] 크롤링 중 오류: {e}")
        finally:
            self.close_db()

        self.logger.info(
            f"[{self.name}] 완료: 탐색 {self.stats['total_fetched']}건, "
            f"중복스킵 {self.stats['skipped_duplicate']}건, 신규적재 {self.stats['saved_or_updated']}건"
        )
        return results


class Bs4Crawler(BaseCrawler):
    """
    전략 ③: 정적 페이지 크롤링 (BeautifulSoup4 통합 관리 크롤러)
    부산, 인천, SH, 대구, 광주 등 각 지역별 크롤러를 통합 실행합니다.
    """

    def __init__(self, name: str = "ClassicBoardCrawler", target_url: str | None = None):
        source_url = target_url or "https://young.busan.go.kr"
        super().__init__(name=name, source_url=source_url)
        self.sub_crawlers = [
            BusanYouthCrawler(),
            IncheonYouthCrawler(),
            ShHousingCrawler(),
            DaeguYouthCrawler(),
            GwangjuYouthCrawler(),
        ]

    def run(self, limit: int = 50) -> list[dict[str, Any]]:
        self.init_db()
        results = []
        per_crawler = max(10, limit // len(self.sub_crawlers))

        self.logger.info(f"[{self.name}] 전국 정적 지자체/기관 크롤러 일괄 가동 (크롤러당 최대 {per_crawler}건)")

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
                self.logger.error(f"하위 크롤러 [{crawler.name}] 실행 중 예외: {e}")

        self.close_db()
        return results
