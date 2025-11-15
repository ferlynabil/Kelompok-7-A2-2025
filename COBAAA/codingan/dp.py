import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
DATA_DIR.mkdir(exist_ok=True)

FILES = {
    'flights': DATA_DIR / 'flights.json',
    'users': DATA_DIR / 'users.json',
    'transactions': DATA_DIR / 'transactions.json'
}

# inisialisasi jika belum ada
for p in FILES.values():
    if not p.exists():
        p.write_text('[]')

def read(file_key: str):
    p = FILES[file_key]
    try:
        with p.open('r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def write(file_key: str, data: Any):
    p = FILES[file_key]
    with p.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
