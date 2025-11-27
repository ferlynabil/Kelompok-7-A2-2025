import json
import inquirer
from prettytable import PrettyTable

def lihat_jadwal():
    try:
        with open("jadwal.json", "r") as f:
            data_jadwal = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data_jadwal = []

    if not data_jadwal:
        print("❌ Belum ada jadwal penerbangan.")
        return

    # Tampilkan tabel jadwal
    table = PrettyTable()
    table.field_names = ["Kode", "Asal", "Tujuan", "Tanggal", "Jam", "Harga", "Maskapai", "Jenis Pesawat"]
    for j in data_jadwal:
        table.add_row([
            j['kode'],
            j['asal'],
            j['tujuan'],
            j['tanggal'],
            j['jam'],
            f"Rp {j['harga']:,}",
            j.get('nama_maskapai', '-'),
            j.get('jenis_pesawat', '-')
        ])
    print("\n📋 Daftar Jadwal Penerbangan:")
    print(table)

    # Buat pilihan untuk inquirer
    pilihan = [
        f"{j['kode']} | {j['asal']} → {j['tujuan']} | {j['tanggal']} {j['jam']} | Rp{j['harga']} | {j.get('nama_maskapai','-')}"
        for j in data_jadwal
    ]

    jawaban = inquirer.prompt([
        inquirer.List("pilih", message="Pilih jadwal untuk lihat detail kursi:", choices=pilihan + ["❌ Batal"])
    ])

    if jawaban is None or jawaban["pilih"] == "❌ Batal":
        print("❌ Dibatalkan.")
        return

    # Ambil jadwal yang dipilih
    index = pilihan.index(jawaban["pilih"])
    jadwal = data_jadwal[index]

    # Tampilkan detail jadwal
    print("\n=== DETAIL JADWAL ===")
    print(f"Kode       : {jadwal['kode']}")
    print(f"Asal       : {jadwal['asal']}")
    print(f"Tujuan     : {jadwal['tujuan']}")
    print(f"Tanggal    : {jadwal['tanggal']}")
    print(f"Jam        : {jadwal['jam']}")
    print(f"Harga      : Rp {jadwal['harga']:,}")
    print(f"Maskapai   : {jadwal.get('nama_maskapai','-')} ({jadwal.get('jenis_pesawat','-')})")
    print(f"Kapasitas  : {jadwal['kapasitas']} kursi")

    # Tampilkan kursi dengan layout + tanda X
    kursi = jadwal.get("kursi", [])
    if kursi:
        print("\n🛫 Layout Kursi:")
        kolom = jadwal.get("kolom", 4)  # default 4 kursi per baris
        for i, k in enumerate(kursi, start=1):
            if isinstance(k, dict):
                status = k.get("status", "kosong")
                nomor = k.get("nomor", "?")
                simbol = f"[{nomor}]" if status == "kosong" else "[X]"
            else:
                simbol = f"[{k}]"
            print(simbol, end=" ")
            if i % kolom == 0:
                print()
        print()
    else:
        print("⚠ Kursi belum diatur untuk jadwal ini.")
