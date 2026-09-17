import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

cases = [
    ('서울', '관악구', 'jobseeker', 'single', 'income60'),
    ('부산', '해운대구', 'jobseeker', 'single', 'income60'),
    ('경기', '수원시', 'employed', 'family', 'income150'),
    ('광주', '북구', 'student', 'single', 'income120'),
    ('인천', '부평구', 'jobseeker', 'single', 'income60')
]

for reg, dist, job, house, inc in cases:
    payload = {
        'age': 24,
        'region': reg,
        'district': dist,
        'jobStatus': job,
        'household': house,
        'income': inc
    }
    res = requests.post('http://127.0.0.1:8000/api/diagnose', json=payload).json()
    prof = res['data']['profile']['summary']
    print(f"==================================================")
    print(f"지역: {reg} {dist}")
    print(f"프로필: {prof}")
    for p in res['data']['policies']:
        print(f"  [{p['rank_label']}] {p['name']} ({p['match_rate']}%) : {p['amount_desc']}")
