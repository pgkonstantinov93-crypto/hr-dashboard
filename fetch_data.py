import requests
import json
import os
from datetime import datetime

SHEET_ID = os.environ.get('SHEET_ID', '1W4CY0Za6M3U7NqjwPjuUcyPr7SCQ__koSPrTi4ECs3I')

SHEETS = {
    'daily_snapshot': '1817386711',
    'vacancies': '0',
    'recruiter_stats': '1663571946',
    'sla_log': '1051732898',
    'funnel_stages': '123456789'
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
        if any(vals):
            rows.append(dict(zip(headers, vals)))
    return rows

data = {}
for name, gid in SHEETS.items():
    try:
        data[name] = fetch_sheet(gid)
        print(f'✅ {name}: {len(data[name])} rows')
    except Exception as e:
        print(f'❌ {name}: {e}')
        data[name] = []

data['updated_at'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'✅ data.json saved, updated_at: {data["updated_at"]}')
