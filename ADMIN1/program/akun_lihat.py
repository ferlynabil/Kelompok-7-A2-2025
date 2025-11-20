import json
import os
from prettytable import PrettyTable

# pastikan path file akun.json selalu di folder yang sama dengan script ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AKUN_FILE = os.path.join(BASE_DIR, "akun.json")

def lihat_akun():
    if os.path.exists(AKUN_FILE):
        with open(AKUN_FILE, "r") as f:
            data_akun = json.load(f)
    else:
        data_akun = {}

    if not data_akun:
        print("Belum ada akun yang terdaftar.")
        return

    table = PrettyTable()
    table.field_names = ["Username", "Password", "Role"]   # ✅ tambahin kolom Password

    for username, info in data_akun.items():
        table.add_row([username, info['password'], info['role']])   # ✅ tampilkan password juga

    print("\n Daftar Akun Terdaftar:")
    print(table)
