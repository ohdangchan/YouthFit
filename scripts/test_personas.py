import json
import sys
from services import diagnosis_engine

sys.stdout.reconfigure(encoding='utf-8')

test_cases = [
    {
        'title': 'Persona 1: 24세 관악구 1인가구 취준생 (중위 60% 이하)',
        'profile': {'age': 24, 'district': '관악구', 'jobStatus': 'jobseeker', 'household': 'single', 'income': 'income60'}
    },
    {
        'title': 'Persona 2: 28세 마포구 다인가구 직장인 (중위 150% 이하)',
        'profile': {'age': 28, 'district': '마포구', 'jobStatus': 'employed', 'household': 'family', 'income': 'income150'}
    },
    {
        'title': 'Persona 3: 21세 강남구 1인가구 대학생 (중위 120% 이하)',
        'profile': {'age': 21, 'district': '강남구', 'jobStatus': 'student', 'household': 'single', 'income': 'income120'}
    }
]

for tc in test_cases:
    res = diagnosis_engine.diagnose_policies(tc['profile'])
    print("=" * 60)
    print(tc['title'])
    print("프로필 요약:", res['profile']['summary'])
    print("총 수혜 예상액:", res['total_benefit_formatted'], "원", f"({res['total_benefit_text']})")
    print("추천 정책 목록:")
    for p in res['policies']:
        rate = p['match_rate']
        print(f"  [{p['rank_label']}] {p['name']} (적합도 {rate}%)")
        print(f"    - 지원금: {p['amount_desc']}")
        print(f"    - AI 리포트: {p['ai_summary']}")
    print("필요 서류 체크리스트:", [d['name'] for d in res['checklist'][:3]])
