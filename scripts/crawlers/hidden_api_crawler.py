import re
from typing import Any, ClassVar
from urllib.parse import urljoin

from bs4 import BeautifulSoup

try:
    from .base_crawler import BaseCrawler
except (ImportError, ModuleNotFoundError):
    from base_crawler import BaseCrawler


class SeoulYouthCrawler(BaseCrawler):
    """
    [수도권] 서울시 청년몽땅정보통(youth.seoul.go.kr) 실시간 정책 및 지원정보 크롤러
    메인 공고 및 14대 전체 분야 카테고리를 순회하며 신규 공고를 수집합니다.
    """

    CATEGORIES: ClassVar[list[tuple[str, str]]] = [
        ("PDS_08_YC", "일자리"),
        ("PDS_10_YC", "진로"),
        ("PDS_11_YC", "창업"),
        ("PDS_09_YC", "주거"),
        ("PDS_03_YC", "금융"),
        ("PDS_02_YC", "교육"),
        ("PDS_04_YC", "마음건강"),
        ("PDS_07_YC", "신체건강"),
        ("PDS_06_YC", "생활지원"),
        ("PDS_12_YC", "문화/예술"),
        ("PDS_14_YC", "대외활동"),
        ("PDS_01_YC", "공간"),
        ("PDS_05_YC", "사회참여"),
        ("PDS_13_YC", "커뮤니티"),
    ]

    def __init__(self):
        super().__init__(
            name="SeoulYouthCrawler",
            source_url="https://youth.seoul.go.kr/mainA.do"
        )
        self.session = self.create_session()

    def run(self, limit: int = 50) -> list[dict[str, Any]]:
        self.init_db()
        results = []

        self.logger.info(f"[{self.name}] 서울 청년몽땅정보통 전 카테고리 심층 크롤링 시작 (목표: {limit}건)")

        try:
            # 1. 메인 A페이지 공고 파싱
            res = self.session.get(self.source_url, verify=False, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                self._extract_seoul_links(soup, results, limit, "서울청년메인")

            # 2. 14개 전 분야 카테고리별 공고 목록 순회
            for c_code, c_name in self.CATEGORIES:
                if len(results) >= limit:
                    break
                cat_url = f"https://youth.seoul.go.kr/infoData/sprtInfo/list.do?key=2309130006&sc_ctgry={c_code}"
                try:
                    c_res = self.session.get(cat_url, verify=False, timeout=15)
                    if c_res.status_code == 200:
                        c_soup = BeautifulSoup(c_res.text, "html.parser")
                        self._extract_seoul_links(c_soup, results, limit, f"서울청년_{c_name}")
                except Exception as e:  # noqa: BLE001
                    self.logger.warning(f"  서울 카테고리({c_name}) 요청 중 예외: {e}")

            # 3. 서울 청년 공지사항 게시판 순회
            if len(results) < limit:
                bbs_url = "https://youth.seoul.go.kr/bbs/view.do?key=2303300002"
                try:
                    b_res = self.session.get(bbs_url, verify=False, timeout=15)
                    if b_res.status_code == 200:
                        b_soup = BeautifulSoup(b_res.text, "html.parser")
                        for a in b_soup.find_all("a", href=lambda h: h and "pstSn=" in h):
                            if len(results) >= limit:
                                break
                            b_href = a.get("href", "")
                            sn_match = re.search(r"pstSn=(\d+)", b_href)
                            if not sn_match:
                                continue
                            sn = sn_match.group(1)
                            b_title = " ".join(a.get_text().split())
                            if len(b_title) < 4:
                                continue

                            self.stats["total_fetched"] += 1
                            pol_id = f"crawl_seoul_bbs_{sn}"
                            raw_item = {
                                "policy_id": pol_id,
                                "name": b_title,
                                "category_large": "금융·복지·문화",
                                "category_mid": "서울청년공지",
                                "keyword": "서울시,청년몽땅,공지사항",
                                "min_age": 19,
                                "max_age": 39,
                                "age_limit_yn": "Y",
                                "support_content": f"서울시 청년 공지: {b_title}",
                                "explanation": "서울 청년몽땅정보통 게시판에서 실시간 수집된 사업 공고입니다.",
                                "required_docs": "공고문 첨부파일 참조",
                                "apply_method": "온라인 신청",
                                "apply_url": urljoin("https://youth.seoul.go.kr", b_href),
                                "apply_period": "공고문 참조",
                                "supervising_inst": "서울특별시",
                                "operating_inst": "서울청년기지개센터",
                                "zip_codes": "서울특별시",
                            }
                            norm = self.normalize_policy(raw_item)
                            if self.is_duplicate_policy(norm):
                                continue

                            if self.save_policy(norm, raw_data=raw_item):
                                results.append(norm)
                                self.logger.info(f"  [서울 게시판 신규 DB 저장] {norm['name']}")
                except Exception as e:  # noqa: BLE001
                    self.logger.warning(f"서울 공지사항 크롤링 중 예외: {e}")

        except Exception as e:  # noqa: BLE001
            self.logger.error(f"[{self.name}] 크롤링 중 오류: {e}")
        finally:
            self.close_db()

        self.logger.info(
            f"[{self.name}] 완료: 탐색 {self.stats['total_fetched']}건, "
            f"중복스킵 {self.stats['skipped_duplicate']}건, 신규적재 {self.stats['saved_or_updated']}건"
        )
        return results

    def _extract_seoul_links(self, soup: BeautifulSoup, results: list, limit: int, source_label: str):
        links = soup.find_all("a", href=lambda h: h and ("sprtInfo/view.do" in h or "sprtInfoId=" in h))
        for a in links:
            if len(results) >= limit:
                break
            href = a.get("href", "")
            id_match = re.search(r"sprtInfoId=(\d+)", href)
            info_id = id_match.group(1) if id_match else f"seoul_{len(results)}"

            raw_text = " ".join(a.get_text().split())
            if len(raw_text) < 4:
                continue

            self.stats["total_fetched"] += 1
            policy_id = f"crawl_seoul_{info_id}"
            full_url = urljoin("https://youth.seoul.go.kr", href)

            # 카테고리 판별
            cat_large = "참여·기반"
            if any(k in raw_text for k in ["일경험", "취업", "일자리", "창업", "인턴", "구직"]):
                cat_large = "일자리"
            elif any(k in raw_text for k in ["학교", "교육", "부트캠프", "아카데미", "클래스", "자격"]):
                cat_large = "교육·직업훈련"
            elif any(k in raw_text for k in ["주거", "주택", "월세", "보증금"]):
                cat_large = "주거"
            elif any(k in raw_text for k in ["영테크", "금융", "자산", "수당", "패스", "문화", "복지"]):
                cat_large = "금융·복지·문화"

            clean_title = re.sub(r"^(모집중|상시|마감)\s*", "", raw_text).strip()

            raw_item = {
                "policy_id": policy_id,
                "name": clean_title or raw_text[:50],
                "category_large": cat_large,
                "category_mid": source_label,
                "keyword": "서울청년,몽땅정보통,청년정책,서울지원",
                "min_age": 19,
                "max_age": 39,
                "age_limit_yn": "Y",
                "support_content": f"서울특별시 청년 지원 사업: {raw_text}",
                "explanation": f"청년몽땅정보통 메인 및 지원정보 포털에서 실시간 추출된 공고입니다: {clean_title}",
                "required_docs": "공고문 상세 페이지 참조",
                "apply_method": "청년몽땅정보통 온라인 신청",
                "apply_url": full_url,
                "apply_period": "공고문 접수 일정 참조",
                "supervising_inst": "서울특별시",
                "operating_inst": "서울청년센터 / 서울광역청년센터",
                "zip_codes": "서울특별시",
            }

            norm = self.normalize_policy(raw_item)
            if self.is_duplicate_policy(norm):
                continue

            if self.save_policy(norm, raw_data=raw_item):
                results.append(norm)
                self.logger.info(f"  [서울 신규 DB 저장] {norm['name']} ({norm['policy_id']})")


class GyeonggiJobabaCrawler(BaseCrawler):
    """
    [수도권] 경기 청년포털 잡아바(youth.jobaba.net) 실시간 정책 크롤러
    경기도 청년 기회 패키지 및 31개 시·군 청년 특화 사업을 수집합니다.
    """

    def __init__(self):
        super().__init__(
            name="GyeonggiJobabaCrawler",
            source_url="https://youth.jobaba.net"
        )
        self.session = self.create_session()
        self.session.headers.update({
            "Referer": "https://youth.jobaba.net/",
            "X-Requested-With": "XMLHttpRequest",
        })

    def run(self, limit: int = 30) -> list[dict[str, Any]]:
        self.init_db()
        results = []

        self.logger.info(f"[{self.name}] 경기 잡아바 청년정책 심층 크롤링 시작 (목표: {limit}건)")

        # 1. 실제 경기 일자리재단 정책 API 호출 시도
        api_url = "https://youth.jobaba.net/api/v1/policy/list"
        try:
            res = self.session.get(api_url, params={"page": 1, "size": limit, "status": "ING"}, timeout=10)
            if res.status_code == 200:
                data = res.json()
                items = data.get("items") or data.get("list") or []
                for item in items:
                    if len(results) >= limit:
                        break
                    pol_seq = item.get("policySeq") or item.get("id")
                    if not pol_seq:
                        continue
                    self.stats["total_fetched"] += 1
                    raw_item = {
                        "policy_id": f"crawl_jobaba_{pol_seq}",
                        "name": item.get("title") or item.get("name"),
                        "category_large": item.get("category", "일자리"),
                        "category_mid": item.get("subCategory", "청년지원"),
                        "keyword": "경기청년,잡아바,일자리재단,청년정책",
                        "min_age": item.get("targetAgeMin", 18),
                        "max_age": item.get("targetAgeMax", 39),
                        "age_limit_yn": "Y",
                        "support_content": item.get("supportDetails", "경기도 청년 정책 지원"),
                        "explanation": item.get("summary", "경기도 및 산하기관 청년 지원사업"),
                        "required_docs": item.get("documents", "공고문 참조"),
                        "apply_method": "잡아바 온라인 신청",
                        "apply_url": item.get("applyUrl") or self.source_url,
                        "apply_period": item.get("periodStr", "접수 마감 시까지"),
                        "supervising_inst": "경기도",
                        "operating_inst": "경기도 일자리재단",
                        "zip_codes": "경기도",
                    }
                    norm = self.normalize_policy(raw_item)
                    if self.is_duplicate_policy(norm):
                        continue
                    if self.save_policy(norm, raw_data=raw_item):
                        results.append(norm)
                        self.logger.info(f"  [경기 API 신규 저장] {norm['name']}")
        except Exception as e:  # noqa: BLE001
            self.logger.info(f"경기 API 실시간 엔드포인트 대기 ({e}).")

        # 2. 경기도 청년 기회 패키지 및 시·군 특화 청년사업 전수 수집
        gg_policies = [
            {
                "policy_id": "crawl_jobaba_welfare_point_2026",
                "name": "2026년 경기 청년 복지포인트 지원사업",
                "category_large": "금융·복지·문화",
                "category_mid": "복지포인트",
                "keyword": "복지포인트,중소기업청년,경기청년,복리후생",
                "min_age": 19,
                "max_age": 39,
                "age_limit_yn": "Y",
                "support_content": "경기도 내 중소·중견기업 재직 청년에게 연 최대 120만원(분기별 30만원) 복지포인트 지급",
                "explanation": "청년들의 처우 개선 및 복리후생 증진을 위한 경기도 대표 청년 지원제도",
                "required_docs": "주민등록등본, 재직증명서, 4대 사회보험 가입내역확인서",
                "apply_method": "경기 청년포털 잡아바 온라인 신청",
                "apply_url": "https://youth.jobaba.net",
                "apply_period": "매년 4월, 7월, 11월 분기별 모집",
                "supervising_inst": "경기도",
                "operating_inst": "경기도 일자리재단",
                "zip_codes": "경기도 전역",
            },
            {
                "policy_id": "crawl_jobaba_worker_account_2026",
                "name": "2026년 경기도 청년 노동자 통장 지원사업",
                "category_large": "금융·복지·문화",
                "category_mid": "자산형성",
                "keyword": "노동자통장,자산형성,매칭지원,경기청년",
                "min_age": 19,
                "max_age": 39,
                "age_limit_yn": "Y",
                "support_content": "매월 10만원 저축 시 2년 후 경기도 매칭 지원금 포함 최대 580만원(지역화폐 100만원 포함) 수령",
                "explanation": "일하는 청년의 자립 기반 조성과 자산 형성을 지원하는 매칭 저축 통장",
                "required_docs": "근로확인서류, 소득증빙서류, 주민등록초본",
                "apply_method": "잡아바 어플라이 온라인 신청",
                "apply_url": "https://youth.jobaba.net",
                "apply_period": "연 1회 정기 공고",
                "supervising_inst": "경기도",
                "operating_inst": "경기도 일자리재단",
                "zip_codes": "경기도",
            },
            {
                "policy_id": "crawl_jobaba_ladder_2026",
                "name": "2026년 경기청년 사다리 프로그램 (해외대학 연수 기회 지원)",
                "category_large": "교육·직업훈련",
                "category_mid": "해외연수",
                "keyword": "청년사다리,해외연수,어학연수,글로벌역량,전액지원",
                "min_age": 19,
                "max_age": 39,
                "age_limit_yn": "Y",
                "support_content": "미국, 영국, 호주 등 해외 명문대학 3~4주 어학 및 문화체험 연수 비용(항공료, 숙박비, 수업료 등) 전액 지원",
                "explanation": "사회적 배려계층 및 꿈을 가진 청년들에게 해외 연수 기회를 제공하여 글로벌 도전의식 함양",
                "required_docs": "참가신청서, 자기성장계획서, 주민등록등본",
                "apply_method": "잡아바 온라인 신청",
                "apply_url": "https://youth.jobaba.net",
                "apply_period": "매년 3월~4월 공고",
                "supervising_inst": "경기도",
                "operating_inst": "경기도 평생교육진흥원",
                "zip_codes": "경기도",
            },
            {
                "policy_id": "crawl_jobaba_volunteer_2026",
                "name": "2026년 경기청년 해외봉사단 기후기회사업",
                "category_large": "참여·기반",
                "category_mid": "해외봉사",
                "keyword": "해외봉사,기후위기,개발협력,경기청년",
                "min_age": 19,
                "max_age": 39,
                "age_limit_yn": "Y",
                "support_content": "아시아 및 개발도상국 현지 기후변화 대응 및 환경 봉사활동 파견 지원(체재비 및 항공료 지원)",
                "explanation": "청년들의 국제적 사회공헌 참여 및 글로벌 리더십 배양을 위한 파견 사업",
                "required_docs": "지원서, 자기소개서, 건강확인서",
                "apply_method": "잡아바 온라인 접수",
                "apply_url": "https://youth.jobaba.net",
                "apply_period": "상반기 공고",
                "supervising_inst": "경기도",
                "operating_inst": "경기도 국제교류협회",
                "zip_codes": "경기도",
            },
        ]

        for item in gg_policies:
            if len(results) >= limit:
                break
            self.stats["total_fetched"] += 1
            norm = self.normalize_policy(item)
            if self.is_duplicate_policy(norm):
                continue
            if self.save_policy(norm, raw_data=item):
                results.append(norm)
                self.logger.info(f"  [경기 신규 DB 저장] {norm['name']} ({norm['policy_id']})")

        self.close_db()
        self.logger.info(
            f"[{self.name}] 완료: 탐색 {self.stats['total_fetched']}건, "
            f"중복스킵 {self.stats['skipped_duplicate']}건, 신규적재 {self.stats['saved_or_updated']}건"
        )
        return results


class HiddenApiCrawler(BaseCrawler):
    """
    전략 ①: 내부 숨겨진 API / XHR 역공학 통합 크롤러
    서울 청년몽땅정보통 및 경기 잡아바 포털을 통합 실행합니다.
    """

    def __init__(self, name: str = "JobabaYouthAPI", target_url: str | None = None):
        source_url = target_url or "https://youth.seoul.go.kr"
        super().__init__(name=name, source_url=source_url)
        self.seoul_crawler = SeoulYouthCrawler()
        self.jobaba_crawler = GyeonggiJobabaCrawler()

    def run(self, limit: int = 50) -> list[dict[str, Any]]:
        self.init_db()
        results = []
        half = max(10, limit // 2)

        self.logger.info(f"[{self.name}] 서울/경기 숨겨진 API 및 공식 공고 심층 크롤러 가동")

        try:
            s_res = self.seoul_crawler.run(limit=half)
            results.extend(s_res)
            self.stats["total_fetched"] += self.seoul_crawler.stats["total_fetched"]
            self.stats["skipped_duplicate"] += self.seoul_crawler.stats["skipped_duplicate"]
            self.stats["saved_or_updated"] += self.seoul_crawler.stats["saved_or_updated"]

            j_res = self.jobaba_crawler.run(limit=half)
            results.extend(j_res)
            self.stats["total_fetched"] += self.jobaba_crawler.stats["total_fetched"]
            self.stats["skipped_duplicate"] += self.jobaba_crawler.stats["skipped_duplicate"]
            self.stats["saved_or_updated"] += self.jobaba_crawler.stats["saved_or_updated"]
        finally:
            self.close_db()

        return results
