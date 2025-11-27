import inquirer
import json
import os
from datetime import datetime

# ===== Helper Functions =====
def validasi_kode(teks):
    teks = teks.strip()
    if not teks:
        print("✖ Kode penerbangan tidak boleh kosong!")
        return False
    if not teks.isalnum():
        print("✖ Kode penerbangan hanya boleh huruf dan angka (tanpa spasi/simbol)!")
        return False
    return True

def validasi_huruf(teks, label):
    teks = teks.strip()
    if not teks:
        print(f"✖ {label} tidak boleh kosong!")
        return False
    if not teks.replace(" ", "").isalpha():
        print(f"✖ {label} hanya boleh huruf dan spasi!")
        return False
    return True

def validasi_tanggal(teks):
    teks = teks.strip()
    if not teks:
        print("✖ Tanggal tidak boleh kosong!")
        return False
    try:
        datetime.strptime(teks, "%d-%m-%Y")
        return True
    except ValueError:
        print("✖ Format tanggal harus DD-MM-YYYY dan valid!")
        return False

def validasi_jam(teks):
    teks = teks.strip()
    if not teks:
        print("✖ Jam tidak boleh kosong!")
        return False
    try:
        datetime.strptime(teks, "%H:%M")
        return True
    except ValueError:
        print("✖ Format jam harus HH:MM dan valid!")
        return False

def validasi_harga(teks):
    teks = teks.strip()
    if not teks:
        print("✖ Harga tidak boleh kosong!")
        return None
    if teks.isdigit() and int(teks) > 0:
        return int(teks)
    print("✖ Harga harus berupa angka positif tanpa huruf/simbol!")
    return None

def validasi_kapasitas(teks):
    teks = teks.strip()
    if not teks:
        print("✖ Kapasitas kursi tidak boleh kosong!")
        return None
    if teks.isdigit() and int(teks) > 0:
        return int(teks)
    print("✖ Kapasitas kursi harus berupa angka positif!")
    return None

def validasi_kolom(teks):
    teks = teks.strip()
    if not teks:
        print("✖ Jumlah kursi per baris tidak boleh kosong!")
        return None
    if teks.isdigit() and 1 <= int(teks) <= 10:
        return int(teks)
    print("✖ Jumlah kursi per baris harus angka 1–10!")
    return None

# ===== Fungsi Utama =====
def tambah_jadwal():
    jadwal_baru = inquirer.prompt([
        inquirer.Text('kode', message="Masukkan Kode Penerbangan"),
        inquirer.Text('asal', message="Masukkan Kota Asal"),
        inquirer.Text('tujuan', message="Masukkan Kota Tujuan"),
        inquirer.Text('tanggal', message="Masukkan Tanggal (DD-MM-YYYY)"),
        inquirer.Text('jam', message="Masukkan Jam (HH:MM)"),
        inquirer.Text('harga', message="Masukkan Harga Tiket (contoh: 25000)"),
        inquirer.Text('nama_maskapai', message="Masukkan Nama Maskapai (contoh: Lion Air)"),
        inquirer.List('jenis_pesawat', message="Pilih Jenis Pesawat", choices=['Ekonomi','Bisnis']),
        inquirer.Text('kapasitas', message="Masukkan Jumlah Kursi Tersedia"),
        inquirer.Text('kolom', message="Masukkan Jumlah Kursi per Baris (contoh: 4)")
    ])

    if jadwal_baru is None:
        print("\n❌ Input dibatalkan.")
        return

    # ===== Validasi =====
    if not validasi_kode(jadwal_baru['kode']): return
    if not validasi_huruf(jadwal_baru['asal'], "Kota asal"): return
    if not validasi_huruf(jadwal_baru['tujuan'], "Kota tujuan"): return
    if not validasi_tanggal(jadwal_baru['tanggal']): return
    if not validasi_jam(jadwal_baru['jam']): return
    harga_int = validasi_harga(jadwal_baru['harga'])
    if harga_int is None: return
    jadwal_baru['harga'] = harga_int
    if not validasi_huruf(jadwal_baru['nama_maskapai'], "Nama maskapai"): return
    kapasitas_int = validasi_kapasitas(jadwal_baru['kapasitas'])
    if kapasitas_int is None: return
    kolom_int = validasi_kolom(jadwal_baru['kolom'])
    if kolom_int is None: return

    jadwal_baru['kapasitas'] = kapasitas_int
    jadwal_baru['kolom'] = kolom_int

    # Buat daftar kursi sesuai kapasitas & kolom (pakai dict)
    kursi_list = []
    for i in range(kapasitas_int):
        kursi_id = f"{(i//kolom_int)+1}{chr(65+(i%kolom_int))}"
        kursi_list.append({"nomor": kursi_id, "status": "kosong"})
    jadwal_baru['kursi'] = kursi_list

    # ===== Load file JSON =====
    try:
        if os.path.exists("jadwal.json"):
            with open("jadwal.json", "r") as f:
                data_jadwal = json.load(f)
        else:
            data_jadwal = []
    except (FileNotFoundError, json.JSONDecodeError):
        data_jadwal = []

    # ===== Cek duplikat kode =====
    for jadwal in data_jadwal:
        if jadwal['kode'] == jadwal_baru['kode']:
            print("✖ Kode penerbangan sudah ada!")
            return

    # ===== Simpan =====
    try:
        data_jadwal.append(jadwal_baru)
        with open("jadwal.json", "w") as f:
            json.dump(data_jadwal, f, indent=4)
    except Exception as e:
        print(f"✖ Gagal menyimpan jadwal: {e}")
        return

    # ===== Feedback =====
    harga_rupiah = "Rp {:,}".format(jadwal_baru['harga']).replace(",", ".")
    print("\n✅ Jadwal penerbangan berhasil ditambahkan!")
    print(f"Kode: {jadwal_baru['kode']}")
    print(f"Asal: {jadwal_baru['asal']} → Tujuan: {jadwal_baru['tujuan']}")
    print(f"Tanggal: {jadwal_baru['tanggal']} | Jam: {jadwal_baru['jam']}")
    print(f"Harga: {harga_rupiah}")
    print(f"Maskapai: {jadwal_baru['nama_maskapai']} ({jadwal_baru['jenis_pesawat']})")
    print(f"Kapasitas Kursi: {jadwal_baru['kapasitas']} (per baris {jadwal_baru['kolom']})")
    print("Kursi tersedia:")
    for k in jadwal_baru['kursi']:
        print(f"[{k['nomor']}]", end=" ")
    print()

