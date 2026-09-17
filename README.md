# 🏛️ 유스핏 AI (YouthFit AI)
> **"서류 읽느라 놓친 청년 지원금, 1분 진단으로 찾아주는 AI 복지 비서"**  
> *48-Hour Hackathon Project Plan & Production Design System*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![OpenAPI](https://img.shields.io/badge/온통청년_OpenAPI-LIVE_연동-0053DB.svg)](https://www.youthcenter.go.kr)
[![Gemini AI](https://img.shields.io/badge/AI_Engine-Gemini_LLM-4285F4.svg?logo=google&logoColor=white)](https://ai.google.dev/)
[![UI/UX Dual Theme](https://img.shields.io/badge/UI%2FUX-Kinetic_Glass_&_Fintech_Civic-06B6D4.svg)](#-듀얼-디자인-시스템-uiux-명세-dark--light)

---

## 📌 목차
1. [프로젝트 개요](#-프로젝트-개요)
2. [핵심 문제의식 및 솔루션](#-핵심-문제의식-및-솔루션)
3. [주요 기능 & 3-Step 사용자 경험](#-주요-기능--3-step-사용자-경험)
4. [듀얼 디자인 시스템 UI/UX 명세 (Dark & Light)](#-듀얼-디자인-시스템-uiux-명세-dark--light)
   - [다크 모드: Kinetic Glass AI (`stitch_ui_dark`)](#1-다크-모드-kinetic-glass-ai-stitch_ui_dark)
   - [라이트 모드: Fintech-Grade Civic Service (`stitch_ui_light`)](#2-라이트-모드-fintech-grade-civic-service-stitch_ui_light)
   - [디자인 토큰 & 테마 비교 매트릭스](#3-디자인-토큰--테마-비교-매트릭스)
5. [시스템 아키텍처 & AI 파이프라인](#-시스템-아키텍처--ai-파이프라인)
6. [데이터셋 & 온통청년 Open API 규격](#-데이터셋--온통청년-open-api-규격)
7. [프로젝트 폴더 구조](#-프로젝트-폴더-구조)
8. [시작 가이드 (Quick Start)](#-시작-가이드-quick-start)
9. [데모 시나리오 (페르소나 2종)](#-데모-시나리오-페르소나-2종)
10. [팀 역할 분담 (48시간 마일스톤)](#-팀-역할-분담-48시간-마일스톤)

---

## 💡 프로젝트 개요

수백 페이지에 달하는 난해하고 파편화된 정부·지자체 청년 정책 공고문! 신청 자격이 되는지, 어떤 서류를 준비해야 하는지 몰라 청년들이 수백만 원 상당의 혜택을 놓치고 있습니다.

**유스핏 AI(YouthFit AI)**는 사용자의 핵심 프로필(나이, 거주 자치구, 소득분위, 가구형태, 취업상태)을 바탕으로 **1분 진단**을 거쳐:
- 정부 **'온통청년' Open API**와 서울시 핵심 정책 DB를 실시간 교차 검증
- **1차 룰 기반 초고속 필터링** + **2차 LLM(Gemini) 심층 자격 판정**
- 단순 링크 제공을 넘어 **"올해 예상 수혜액 합산(예: 약 320만원)"**, **"AI 판별 이유(2문장 요약 + 단서조항)"**, **"필수 서류 체크리스트"**를 원스톱 리포트로 제공하는 지능형 복지 비서 웹 서비스입니다.

---

## 🎯 핵심 문제의식 및 솔루션

| 기존 청년 정책 탐색의 페인포인트 | 유스핏 AI (YouthFit AI)의 솔루션 |
| :--- | :--- |
| **정보의 파편화**: 정부24, 온통청년, 서울청년몽땅정보통 등 수십 개 사이트에 분산 | **원스톱 통합 파이프라인**: 온통청년 Open API + 20대 핵심 정책 DB 통합 수집 |
| **복잡한 자격 요건**: 기준 중위소득, 단서 조항, 예외 규정 등 20~30페이지 공고문 | **2단계 지능형 엔진**: 룰 기반 연령·지역 필터링 + LLM 심층 적격도 판정 (오차율 0.02% 미만) |
| **수혜 가치 체감 불가**: 내가 정확히 얼마를 받을 수 있는지 알기 어려움 | **올해 예상 수혜액 배너**: "₩3,200,000 (약 320만원)" 시각화 및 정책별 기여도 게이지 |
| **서류 준비의 막막함**: 신청 시 누락 서류로 인한 반려 리스크 | **인터랙티브 서류 체크리스트**: 개인별 맞춤 제출 서류 패키지 및 준비율 실시간 추적 |

---

## 🚀 주요 기능 & 3-Step 사용자 경험

```
[ Step 1. 1분 온보딩 문진 ] ───▶ [ Step 2. AI 매칭 분석 로딩 ] ───▶ [ Step 3. 진단 리포트 대시보드 ]
  • 프로그레스 바 (진행률 0~100%)       • 실시간 온통청년 API 동기화           • 올해 예상 수혜액 (₩3,200,000)
  • 만 나이, 지역구, 소득, 가구          • 360° 원형 텔레메트리 게이지           • AI 매칭 신뢰도 (98.4% Match)
  • 원클릭 페르소나 체험 프리셋           • 연산 지연시간 0.38초 초고속          • 정책별 AI 판별이유 & 서류 체크리스트
```

### 1. 1분 온보딩 문진 폼 (`/`)
- **실시간 프로그레스 추적**: 총 4단계 문진 진행률(Step Progress Bar) 표시로 이탈 방지.
- **최소 입력 극대화**: 만 나이(19~39세), 거주 지역구(서울시 25개 자치구), 취업상태(취준생/재직자/대학생/창업자), 가구 형태(1인가구 여부), 중위소득 구간(60% 이하, 100% 이하 등).
- **원클릭 페르소나 프리셋**: 시연 및 심사위원을 위한 페르소나 즉시 입력 버튼(관악구 24세 알바 취준생 / 마포구 28세 중소기업 재직자).

### 2. AI 매칭 분석 콘솔 (`/loading`)
- **Neural Matching Telemetry**: 실시간 데이터 동기화 및 3단계 분석 파이프라인 시각화.
  1. `[완료]` 1차 자격 필터링 (연령, 거주지, 고용상태 교차 검증)
  2. `[연산 중]` AI 심층 자격 정밀 대조 및 단서 조항 추출
  3. `[대기]` 개인 맞춤 수혜액 집계 및 서류 체크리스트 패키징
- **원형 SVG 게이지 & 지연시간 카운터**: 실시간 연산 지연(`0.38s`) 및 매칭 진척률(`85% -> 100%`) 시각화.

### 3. 진단 리포트 대시보드 (`/result`)
- **2026 Estimated Benefit Hero Banner**: 큼직한 디스플레이 타이포그래피로 올해 수혜 가능 총액 표기 (`₩3,200,000`).
- **정책별 수혜액 분할 바**: 청년수당(93.7%), 대중교통비 환급(3.1%), 자산형성 매칭(3.2%) 등 멀티 세그먼트 프로그레스.
- **적격 뱃지 & 마감 카운트다운**: 확실 적격(Verified), 마감 임박(`D-5`), AI 추천 배지.
- **AI 판별 이유 아코디언**: 해당 정책이 사용자에게 적합한 이유를 2문장으로 명쾌하게 요약 및 필수 단서 조항 안내.
- **인터랙티브 서류 체크리스트**: 주민등록초본, 소득금액증명원, 임대차계약서 등 원클릭 체크 및 로컬 상태 저장.

---

## 🎨 듀얼 디자인 시스템 UI/UX 명세 (Dark & Light)

본 프로젝트는 고도화된 UI/UX 설계를 위해 **다크 모드(`stitch_ui_dark`)**와 **라이트 모드(`stitch_ui_light`)**의 명확한 독립 디자인 시스템을 구축하고 완벽하게 지원합니다.

---

### 1. 다크 모드: Kinetic Glass AI (`stitch_ui_dark`)
> **"Intelligent, High-Velocity Civic Tech Canvas"**  
> 차세대 알고리즘의 정밀함과 예측력을 상징하는 다크 글래스모피즘 인터페이스

- **디자인 철학**:
  - 심야 복지 탐색 및 복잡한 데이터 분석 시 눈의 피로를 최소화하는 딥 스페이스 캔버스.
  - 불투명 스큐어모피즘을 배제하고, 반투명 블러 레이어로 정보의 위계를 표현.
  - 전력감 있는 네온 사이버 시안과 키네틱 에메랄드 액센트로 AI 신뢰도와 주요 수혜 지표를 강조.
- **색상 팔레트**:
  - `Base Canvas`: 딥 스페이스 네이비 (`#0b1120`, `#0b1326`)
  - `Surface Elevation 1 (Card)`: 차콜 슬레이트 (`#0f172a`, opacity `40%~70%`)
  - `Surface Elevation 2 (Modal)`: 미드나잇 옵시디언 (`#1e293b`, opacity `80%`)
  - `Primary Cyber Cyan`: `#06b6d4` / `#4cd7f6` (주요 인터랙션, AI 텔레메트리)
  - `Secondary Kinetic Emerald`: `#34d399` / `#45dfa4` (적격 인증 뱃지, 신뢰도 98%+)
  - `Tertiary Coral/Amber`: `#ffb873` (임박 알림, 보조 혜택)
  - `Text Hierarchy`: `#f8fafc` (Primary White), `#94a3b8` (Secondary Slate), `#64748b` (Muted)
- **표면 및 글래스모피즘 (Elevation & Glow)**:
  - `Tier 1 Frosted Surface`: `background: rgba(15, 23, 42, 0.65)`, `backdrop-filter: blur(16px) saturate(180%)`, `border: 1px solid rgba(255, 255, 255, 0.08)`
  - `Cyan Signal Glow`: `box-shadow: 0 0 20px -2px rgba(6, 182, 212, 0.35)`
  - `Emerald Signal Glow`: `box-shadow: 0 0 20px -2px rgba(52, 211, 153, 0.35)`
- **타이포그래피**:
  - 헤드라인: `Plus Jakarta Sans` (800 / 700 Display Weight)
  - 본문: `Inter` (고밀도 가독성 최적화)
  - 수치 및 텔레메트리: `JetBrains Mono` (고정폭 엔지니어링 메트릭 표기)

---

### 2. 라이트 모드: Fintech-Grade Civic Service (`stitch_ui_light`)
> **"Clean Modern / High-Trust Fintech Civic Experience"**  
> 토스·카카오뱅크 수준의 명쾌함과 재정적 신뢰감을 전달하는 라이트 핀테크 인터페이스

- **디자인 철학**:
  - 관공서 사이트의 관료주의적 답답함을 걷어내고, 금융 앱 수준의 직관적인 자산·지원금 가치 체감 제공.
  - 장식적 요소를 배제하고 순수한 정보 아키텍처와 명확한 보더라인으로 시각적 피로도 제거.
  - 한글 폰트(Pretendard)의 시각적 안정성과 숫자 폰트(Plus Jakarta Sans)의 정렬 미학 극대화.
- **색상 팔레트**:
  - `Background Canvas`: 소프트 슬레이트 페이퍼 (`#F8FAFC`, 눈부심 없는 안정적 캔버스)
  - `Surface Containers`: 퓨어 화이트 (`#FFFFFF`, 모듈형 카드 및 타일)
  - `Hairline Borders`: `#E2E8F0` (Slate-200) & Hover 시 `#CBD5E1`
  - `Primary Electric Blue`: `#2563EB` / `#004AC6` (진단 CTA, 검증 완료 인디케이터)
  - `Secondary Emerald`: `#059669` / `#10B981` (실제 현금 수혜금액, 매칭 성공)
  - `Status Alerts`: 경고 `#F59E0B` (Amber-500), 결격 `#EF4444` (Rose-500)
  - `Text Hierarchy`: `#0F172A` (Slate-900), `#334155` (Slate-700), `#64748B` (Slate-500)
- **표면 및 입체감 (Elevation & Diffusion)**:
  - 무거운 드롭 섀도우를 지양하고 1px 헤어라인 보더와 은은한 앰비언트 디퓨전 활용.
  - `Resting Card`: `1px solid #E2E8F0`, `box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.04)`
  - `Hover Card`: `1px solid #CBD5E1`, `box-shadow: 0 8px 16px -4px rgba(37, 99, 235, 0.06)`, `transform: translateY(-1px)`
- **타이포그래피**:
  - 한글 본문: `Pretendard` (행간 1.5배, 자간 -0.015em 최적화)
  - 통화/숫자: `Plus Jakarta Sans` (`font-variant-numeric: tabular-nums` 지원으로 금액 정렬 고정)

---

### 3. 디자인 토큰 & 테마 비교 매트릭스

| 디자인 속성 | 🌙 다크 모드 (`Kinetic Glass AI`) | ☀️ 라이트 모드 (`Fintech Civic`) |
| :--- | :--- | :--- |
| **핵심 무드** | 미래지향적 AI 랩, 정밀 텔레메트리 | 신뢰도 높은 금융·복지 서비스 |
| **캔버스 배경** | `#0b1120` / `#0b1326` (딥 스페이스) | `#F8FAFC` (슬레이트 페이퍼) |
| **카드 표면** | `rgba(15, 23, 42, 0.65)` (블러 글래스) | `#FFFFFF` (솔리드 화이트) |
| **프라이머리 컬러**| `#06b6d4` (Cyber Cyan) | `#2563EB` (Electric Blue) |
| **수혜액 하이라이트**| `#45dfa4` (Kinetic Emerald Glow) | `#059669` (Fintech Emerald Green) |
| **테두리 경계선** | `1px solid rgba(255, 255, 255, 0.08)` | `1px solid #E2E8F0` (Hairline) |
| **깊이감 표현** | Backdrop Blur (16~24px) + Photon Glow | 정밀 헤어라인 보더 + 마이크로 디퓨전 |
| **폰트 조합** | Plus Jakarta Sans + Inter + JetBrains Mono | Plus Jakarta Sans + Pretendard |
| **적용 CSS 클래스** | `.dark` 캔버스 및 틴트 변수 | 기본 루트 라이트 토큰 |

---

## ⚙️ 시스템 아키텍처 & AI 파이프라인

```
┌────────────────────────────────────────────────────────────────────────┐
│                        클라이언트 (Front-End)                           │
│  - 3-Step 온보딩 / AI 분석 콘솔 / 진단 결과 대시보드                   │
│  - 다크(Kinetic Glass) & 라이트(Fintech Civic) 듀얼 테마 토글          │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ POST /api/diagnose (문진 데이터)
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      백엔드 서비스 (FastAPI Engine)                    │
│                                                                        │
│   [1] 데이터 어댑터 계층                                                │
│       ├── 온통청년 Open API (youthcenter.go.kr XML/JSON 실시간 연동)   │
│       └── 서울시/전국 핵심 20선 고도화 DB (policies.json 자동 Fallback) │
│                                                                        │
│   [2] 1차 룰 기반 고속 필터링 (Rule Filter)                             │
│       └── 연령 (19~39세) ∩ 거주지 (자치구) ∩ 취업 상태 불일치 사전 제거 │
│                                                                        │
│   [3] 2차 LLM 심층 자격 진단 (Gemini Engine)                           │
│       ├── 소득분위 (중위소득 %) 및 1인가구 가중치 판별                  │
│       ├── 예상 수혜 금액 정밀 합산 (단위: 원)                          │
│       ├── 맞춤 판별 사유 2문장 요약 + 필수 단서 조항 추출              │
│       └── 제출 필수 서류 체크리스트 구조화                              │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Strict JSON Response
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       최종 진단 리포트 반환                            │
│  { total_benefit: "320만원", match_rate: 98.4, recommendations: [...] }│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 데이터셋 & 온통청년 Open API 규격

### 1. 온통청년 청년정책 오픈 API 명세 (`youthPlcyList.do`)
- **요청 URL**: `https://www.youthcenter.go.kr/opi/youthPlcyList.do`
- **주요 파라미터**:
  - `openApiVlak`: 오픈 API 발급 인증키
  - `pageIndex`: 페이지 번호 (기본 1)
  - `display`: 페이지당 출력 건수 (10~50)
  - `bizTycdSel`: 정책 유형 (023010 취업, 023020 창업, 023030 주거·금융, 023040 생활·복지)
- **주요 응답 필드 매핑**:
  - `polyBizSjnm`: 정책 사업명 (예: "청년월세지원")
  - `sporCn`: 지원 내용 및 금액 (예: "월 20만원 지원, 최대 12개월")
  - `ageInfo`: 연령 제한 요건 (예: "만 19세 ~ 34세")
  - `prcpCn`: 거주지 및 소득 요건
  - `empmSttsCn`: 취업 상태 요건 (취업자, 미취업자 등)
  - `pstnPaprCn`: 필수 제출 서류 목록
  - `rqutUrla`: 온라인 신청 URL

### 2. 고도화 정밀 JSON DB (`policies.json`)
외부 API 지연이나 인증키 미발급 상황에서도 100% 정상 작동하도록, 기획서(Member C)의 지침에 따라 **서울시 핵심 청년 정책 20선**을 사전 가공하여 포함합니다:
- **주거/금융**: 청년월세지원, 청년 임차보증금 이자지원, 희망두배 청년통장, 청년도약계좌 등
- **취업/소득**: 서울시 청년수당, 구직활동지원금, 국민취업지원제도 1·2유형 등
- **생활/교통**: 청년 대중교통비 지원, K-패스 청년 환급, 청년 마음건강 지원 등

---

## 📁 프로젝트 폴더 구조

```bash
YouthFit/
├── README.md                      # 프로젝트 공식 통합 가이드 (본 문서)
├── requirements.txt               # 파이썬 핵심 의존성 (FastAPI, uvicorn, requests 등)
├── main.py                        # FastAPI 앱 엔트리포인트 및 라우터 정의
│
├── services/                      # 비즈니스 로직 & AI 파이프라인
│   ├── __init__.py
│   ├── ontong_api.py              # 온통청년 Open API 클라이언트 & XML/JSON 파서
│   ├── filter_engine.py           # 1차 룰 기반 고속 필터링 모듈
│   └── ai_diagnose.py             # 2차 Gemini LLM 자격 검증 & 수혜액 계산 엔진
│
├── data/
│   └── policies.json              # 서울시 & 전국 핵심 청년정책 20선 고도화 DB
│
├── static/                        # 웹 클라이언트 리소스
│   ├── css/
│   │   ├── style.css              # 듀얼 테마 (Kinetic Glass / Fintech) 통합 CSS
│   │   └── tailwind_tokens.css    # 디자인 시스템 컬러, 타이포그래피, 블러 토큰
│   └── js/
│       ├── app.js                 # 폼 제어, API 통신, 서류 체크박스 인터랙션
│       └── theme.js               # 다크/라이트 모드 실시간 토글러
│
├── templates/
│   └── index.html                 # 3-Step 단일 페이지 통합 웹 애플리케이션
│
├── stitch_ui_dark/                # [Reference] 다크 모드 UI 레퍼런스 에셋
│   └── stitch_ui/
│       ├── kinetic_glass_ai/DESIGN.md  # 다크 모드 공식 디자인 명세서
│       ├── youthfit_ai/                # 진단 대시보드 화면 코드 & 스크린샷
│       └── youthfit_ai_1/              # 온보딩 및 텔레메트리 보조 화면
│
└── stitch_ui_light/               # [Reference] 라이트 모드 UI 레퍼런스 에셋
    └── stitch_ui/
        ├── youthfit_ai/DESIGN.md       # 라이트 모드 공식 디자인 명세서
        ├── 1/                          # 1분 온보딩 문진 화면 코드 & 스크린샷
        ├── ai/                         # AI 연산 로딩 화면 코드 & 스크린샷
        └── code.html                   # 라이트 모드 진단 리포트 대시보드
```

---

## ⚡ 시작 가이드 (Quick Start)

### 1. 가상환경 및 패키지 설치
```bash
# 가상환경 생성 (권장)
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux

# 필수 패키지 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정 (`.env`)
프로젝트 루트 디렉토리에 `.env` 파일을 생성하거나 `.env.example`을 복사하여 환경변수를 등록합니다:
```env
# Gemini AI API Key (필수)
GEMINI_API_KEY=your_gemini_api_key_here

# 온통청년 Open API Key (선택: 미입력 시 내장 policies.json 고도화 DB 자동 활성화)
ONTONG_API_KEY=your_youthcenter_openapi_key_here

# PostgreSQL Database URL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/youthfit
```

### 3. PostgreSQL 데이터베이스 초기화 및 마이그레이션
```bash
# PostgreSQL로 423건 청년 정책 데이터 원클릭 마이그레이션
python scripts/migrate_sqlite_to_pg.py

# 또는 온통청년 API에서 최신 정책 실시간 동기화
python scripts/sync_policies_db.py
```

### 4. 로컬 개발 서버 실행
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
브라우저에서 `http://localhost:8000`에 접속하여 서비스를 이용할 수 있습니다.

---

## 🎭 데모 시나리오 (페르소나 2종)

| 페르소나 | 프로필 요약 | 핵심 매칭 정책 및 예상 수혜액 |
| :--- | :--- | :--- |
| **페르소나 A (알바 취준생)** | • 관악구 거주 만 24세<br>• 미취업 (아르바이트 병행)<br>• 1인 가구, 중위소득 60% 이하 | • **서울시 청년수당**: 300만원 (월 50만원 × 6개월)<br>• **청년 대중교통비 지원**: 약 10만원<br>• **청년월세지원**: 최대 240만원 (월 20만원)<br>👉 **총 예상 수혜액: 약 320만 ~ 550만원** |
| **페르소나 B (중소기업 재직자)** | • 마포구 거주 만 28세<br>• 중소기업 2년차 재직<br>• 1인 가구, 중위소득 120% 이하 | • **희망두배 청년통장**: 연 최대 360만원 매칭<br>• **K-패스 청년 환급**: 연 약 21만원<br>• **청년 임차보증금 대출 이자지원**: 연 100만원 상당<br>👉 **총 예상 수혜액: 약 480만원** |

---

## 👥 팀 역할 분담 (48시간 마일스톤)

```
[Day 1 (00h~24h)]
  00h~02h : 킥오프 ── API 입출력 JSON 규격 확정 및 레포지토리 세팅
  02h~08h : [Member A] 1분 온보딩 폼 제작 / [Member B] 1차 룰 필터링 / [Member C] policies.json 구축
  08h~14h : [Member B] Gemini 프롬프트 엔지니어링 / [Member C] 온통청년 API 스키마 검증
  14h~20h : 프론트-백 `/api/diagnose` 로컬 연동 테스트

[Day 2 (24h~48h)]
  20h~28h : [Member A] Kinetic Glass & Fintech 듀얼 UI 완성 / [Member B] 예외처리 및 응답 3초 최적화
  28h~36h : 페르소나 A/B 실기기 검증 및 네트워크 Fallback 안전장치 점검
  36h~44h : 5분 피칭 슬라이드(7장) 및 시연 백업 비디오 준비
  44h~48h : 최종 Q&A 리허설 및 제출
```

- **Member A (Frontend / UI/UX Lead)**:
  - 3-Step 온보딩 및 대시보드 인터페이스 구현
  - `stitch_ui_dark`(Kinetic Glass AI) 및 `stitch_ui_light`(Fintech Civic) 듀얼 테마 구축
  - 인터랙티브 서류 체크리스트 및 상태 관리
- **Member B (Backend / AI Engineering Lead)**:
  - 온통청년 Open API 클라이언트 및 XML 파서 구축
  - 1차 룰 필터 + 2차 Gemini LLM 자격 진단 파이프라인 개발
  - 3초 이내 응답 레이턴시 최적화 및 Strict JSON 검증
- **Member C (Data / PM / Presentation Lead)**:
  - 서울시 및 전국 핵심 청년정책 20선 정밀 데이터셋(`policies.json`) 구축
  - 페르소나 2종 시연 시나리오 설계 및 데이터 QA
  - 5분 피칭 덱 제작 및 최종 발표 총괄

---

<div align="center">
  <sub>YouthFit AI · 48-Hour Hackathon Project · Powered by 온통청년 OpenAPI & Gemini AI</sub>
</div>
