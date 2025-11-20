import json
from prettytable import PrettyTable

def lihat_jadwal():
    with open("jadwal.json", "r") as f:
        data_jadwal = json.load(f)

    if not data_jadwal:
        print("❌ Belum ada jadwal penerbangan.")
        return

    table = PrettyTable()
    table.field_names = ["Kode", "Asal", "Tujuan", "Tanggal", "Jam", "Harga"]
    for j in data_jadwal:
        table.add_row([j['kode'], j['asal'], j['tujuan'], j['tanggal'], j['jam'], j['harga']])
    print("\n📋 Daftar Jadwal Penerbangan:")
    print(table)
