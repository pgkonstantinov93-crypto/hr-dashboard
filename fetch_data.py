import requests
import json
import os
from datetime import datetime

SHEET_ID = os.environ.get('SHEET_ID', '1W4CY0Za6M3U7NqjwPjuUcyPr7SCQ__koSPrTi4ECs3I')

SHEETS = {
    'daily_snapshot': '700832784',
    'vacancies': '1914912702',
    'recruiter_stats': '613309742',
    'sla_log': '934058151',
    'funnel_stages': '1858502204',
    'events_log': '1934468928'
}

def fetch_sheet(sheet_gid):
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={sheet_gid}'
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    lines = r.text.strip().split('\n')
    if len(lines) < 2:
        return []
    headers = [h.strip().strip('"') for h in lines[0].split(',')]
    rows = []
    for line in lines[1:]:
        vals = [v.strip().strip('"') for v in line.split(',')]
        if any(v for v in vals if v):
            rows.append(dict(zip(headers, vals)))
    seen = set()
    unique = []
    for row in rows:
        key = str(row)
        if key not in seen:
            seen.add(key)
            unique.append(row)
    return unique

data = {}
for name, gid in SHEETS.items():
    try:
        rows = fetch_sheet(gid)
        data[name] = rows
        print(f'✅ {name}: {len(rows)} rows')
    except Exception as e:
        print(f'❌ {name}: {e}')
        data[name] = []

data['updated_at'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('✅ data.json saved')
