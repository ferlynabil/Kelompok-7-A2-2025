import re
from datetime import datetime
import os

def clear_screen():
    # langsung pakai cls sesuai permintaan
    try:
        os.system("cls")
    except Exception:
        # jika ada error, ignore (tidak melakukan fallback ke clear)
        pass

def validate_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def parse_datetime(date_str: str, fmt='%Y-%m-%d %H:%M'):
    try:
        return datetime.strptime(date_str, fmt)
    except ValueError:
        raise ValueError(f"Tanggal harus format {fmt}")

def input_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print('Input tidak boleh kosong.')
