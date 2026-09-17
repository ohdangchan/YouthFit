import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')
from services import diagnosis_engine

tests = [
    {
        'title': '1. 부산 해운대구 취준생 1인가구',
        'profile': {'age': 24, 'region': '부산', 'district': '해운대구', 'jobStatus': 'jobseeker', 'household': 'single', 'income': 'income60'}
    },
    {
        'title': '2. 경기도 수원시 재직자 다인가구',
        'profile': {'age': 28, 'region': '경기', 'district': '수원시', 'jobStatus': 'employed', 'household': 'family', 'income': 'income150'}
    },
    {
        'title': '3. 광주광역시 북구 대학생 1인가구',
        'profile': {'age': 22, 'region': '광주', 'district': '북구', 'jobStatus': 'student', 'household': 'single', 'income': 'income120'}
    },
    {
        'title': '4. 서울 관악구 취준생 1인가구',
        'profile': {'age': 24, 'region': '서울', 'district': '관악구', 'jobStatus': 'jobseeker', 'household': 'single', 'income': 'income60'}
    }
]

for t in tests:
    res = diagnosis_engine.diagnose_policies(t['profile'])
    print("=" * 60)
    print(t['title'])
    print("프로필 요약:", res['profile']['summary'])
    print("총 혜택:", res['total_benefit_formatted'], "원")
    for p in res['policies']:
        rate = p['match_rate']
        print(f" - [{p['rank_label']}] {p['name']} ({rate}%) -> {p['amount_desc']}")
