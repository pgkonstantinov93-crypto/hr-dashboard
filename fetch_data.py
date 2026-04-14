import requests
import json
import os
import csv
import io
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
    r.encoding = 'utf-8'
    r.raise_for_status()
    reader = csv.DictReader(io.StringIO(r.text))
    rows = []
    seen = set()
    for row in reader:
        clean = {k.strip(): v.strip() for k, v in row.items() if k}
        key = str(clean)
        if key not in seen and any(clean.values()):
            seen.add(key)
            rows.append(clean)
    return rows

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
