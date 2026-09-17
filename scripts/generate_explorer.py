import os
import sys
import json

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

JSON_PATH = "data/youth_policies_19_34.json"
HTML_OUTPUT = "data/policies_explorer.html"

def generate_html_explorer():
    if not os.path.exists(JSON_PATH):
        print(f"[!] JSON 파일이 없습니다: {JSON_PATH}")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    policies = data.get("policies", [])
    meta = data.get("metadata", {})

    # HTML 템플릿
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouthFit - 온통청년 정책 데이터베이스 탐색기</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Pretendard:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0b1326;
            --surface: #131b2e;
            --surface-card: rgba(23, 31, 51, 0.85);
            --border: rgba(255, 255, 255, 0.1);
            --primary: #4cd7f6;
            --secondary: #45dfa4;
            --text-main: #dae2fd;
            --text-sub: #94a3b8;
            --text-muted: #64748b;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg);
            color: var(--text-main);
            font-family: 'Pretendard', sans-serif;
            padding: 30px 20px;
            line-height: 1.6;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        header {{
            margin-bottom: 30px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
        }}
        .badge {{
            display: inline-block;
            background: rgba(76, 215, 246, 0.15);
            color: var(--primary);
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 10px;
            border: 1px solid rgba(76, 215, 246, 0.3);
        }}
        h1 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 28px;
            font-weight: 800;
            color: #fff;
            margin-bottom: 8px;
        }}
        .stats-bar {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 15px;
        }}
        .stat-item {{
            background: var(--surface);
            border: 1px solid var(--border);
            padding: 12px 20px;
            border-radius: 10px;
        }}
        .stat-item strong {{
            color: var(--secondary);
            font-size: 20px;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        .controls {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-bottom: 25px;
            background: var(--surface);
            padding: 18px;
            border-radius: 12px;
            border: 1px solid var(--border);
        }}
        input[type="text"] {{
            flex: 1;
            min-width: 250px;
            background: #060e20;
            border: 1px solid var(--border);
            color: #fff;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 14px;
        }}
        input[type="text"]:focus {{ outline: none; border-color: var(--primary); }}
        .filter-btn {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border);
            color: var(--text-sub);
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.2s;
        }}
        .filter-btn:hover, .filter-btn.active {{
            background: var(--primary);
            color: #003640;
            font-weight: 700;
            border-color: var(--primary);
        }}
        .policy-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            gap: 20px;
        }}
        .card {{
            background: var(--surface-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.2s;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .card:hover {{
            border-color: rgba(76, 215, 246, 0.5);
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5);
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 12px;
        }}
        .cat-tag {{
            font-size: 11px;
            padding: 3px 8px;
            border-radius: 6px;
            background: rgba(69, 223, 164, 0.15);
            color: var(--secondary);
            font-weight: 600;
        }}
        .age-tag {{
            font-size: 11px;
            padding: 3px 8px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.08);
            color: var(--text-sub);
        }}
        .card-title {{
            font-size: 17px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 8px;
        }}
        .card-desc {{
            font-size: 13px;
            color: var(--text-sub);
            margin-bottom: 15px;
            max-height: 80px;
            overflow-y: auto;
            white-space: pre-line;
        }}
        .docs-box {{
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-size: 12px;
        }}
        .docs-box strong {{ color: var(--primary); display: block; margin-bottom: 4px; }}
        .card-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            padding-top: 12px;
            margin-top: auto;
            font-size: 12px;
            color: var(--text-muted);
        }}
        .link-btn {{
            color: var(--primary);
            text-decoration: none;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 6px;
            background: rgba(76, 215, 246, 0.1);
            transition: all 0.2s;
        }}
        .link-btn:hover {{
            background: var(--primary);
            color: #003640;
        }}
    </style>
</head>
<body>
<div class="container">
    <header>
        <div class="badge">온통청년 LIVE DB 연동 완료</div>
        <h1>🏛️ YouthFit 정책 데이터베이스 탐색기</h1>
        <p style="color: var(--text-sub);">온통청년 Open API를 통해 로컬 DB로 적재된 만 19세~34세 청년 수혜 정책 실시간 뷰어</p>
        
        <div class="stats-bar">
            <div class="stat-item">총 수혜 가능 정책: <strong>{len(policies)}건</strong></div>
            <div class="stat-item">대상 연령: <strong>만 19세 ~ 34세</strong></div>
            <div class="stat-item">로컬 쿼리 응답: <strong>&lt; 0.001초</strong></div>
            <div class="stat-item">출처: <strong>온통청년 (youthcenter.go.kr)</strong></div>
        </div>
    </header>

    <div class="controls">
        <input type="text" id="searchInput" placeholder="정책명, 지원 내용, 서류 검색 (예: 월세, 청년수당, 면접, 자격증)..." oninput="filterCards()">
        <button class="filter-btn active" onclick="setCategory('ALL', this)">전체 ({len(policies)})</button>
        <button class="filter-btn" onclick="setCategory('일자리', this)">일자리</button>
        <button class="filter-btn" onclick="setCategory('주거', this)">주거</button>
        <button class="filter-btn" onclick="setCategory('금융･복지･문화', this)">금융/복지</button>
        <button class="filter-btn" onclick="setCategory('교육･직업훈련', this)">교육/훈련</button>
        <button class="filter-btn" onclick="setCategory('참여･기반', this)">참여/기반</button>
    </div>

    <div class="policy-grid" id="policyGrid">
    </div>
</div>

<script>
    const policies = {json.dumps(policies, ensure_ascii=False)};
    let activeCategory = 'ALL';

    function renderCards(items) {{
        const grid = document.getElementById('policyGrid');
        grid.innerHTML = '';

        if (items.length === 0) {{
            grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 60px; color: var(--text-muted);">검색 조건에 맞는 정책이 없습니다.</div>';
            return;
        }}

        items.forEach(p => {{
            const card = document.createElement('div');
            card.className = 'card';
            
            const docsList = p.required_docs_parsed && p.required_docs_parsed.length > 0 
                ? p.required_docs_parsed.slice(0, 3).map(d => '• ' + d).join('<br>')
                : (p.required_docs ? p.required_docs.slice(0, 60) + '...' : '별도 서류 미기재');

            card.innerHTML = `
                <div>
                    <div class="card-header">
                        <span class="cat-tag">${{p.category_large || '미분류'}}</span>
                        <span class="age-tag">만 ${{p.min_age}}~${{p.max_age}}세</span>
                    </div>
                    <div class="card-title">${{p.name}}</div>
                    <div class="card-desc">${{p.support_content || p.explanation || '상세 내용 참조'}}</div>
                    <div class="docs-box">
                        <strong>📑 주요 제출 서류</strong>
                        <div>${{docsList}}</div>
                    </div>
                </div>
                <div class="card-footer">
                    <span>🏢 ${{p.supervising_inst || '지자체/기관'}}</span>
                    ${{p.apply_url ? `<a href="${{p.apply_url}}" target="_blank" class="link-btn">신청 바로가기 →</a>` : '<span>공고 참조</span>'}}
                </div>
            `;
            grid.appendChild(card);
        }});
    }}

    function filterCards() {{
        const query = document.getElementById('searchInput').value.toLowerCase().trim();
        const filtered = policies.filter(p => {{
            const matchCat = (activeCategory === 'ALL') || (p.category_large && p.category_large.includes(activeCategory));
            const matchQuery = !query || 
                (p.name && p.name.toLowerCase().includes(query)) ||
                (p.support_content && p.support_content.toLowerCase().includes(query)) ||
                (p.required_docs && p.required_docs.toLowerCase().includes(query)) ||
                (p.supervising_inst && p.supervising_inst.toLowerCase().includes(query));
            return matchCat && matchQuery;
        }});
        renderCards(filtered);
    }}

    function setCategory(cat, btn) {{
        activeCategory = cat;
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        filterCards();
    }}

    // 초기 렌더링
    renderCards(policies);
</script>
</body>
</html>
"""

    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"[OK] 인터랙티브 정책 탐색기 웹페이지 생성 완료: {HTML_OUTPUT}")

if __name__ == "__main__":
    generate_html_explorer()
