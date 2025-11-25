import inquirer
import json
import os
from datetime import datetime

# ===== Helper Functions =====
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

# ===== Fungsi Utama =====
def tambah_jadwal():
    jadwal_baru = inquirer.prompt([
        inquirer.Text('kode', message="Masukkan Kode Penerbangan"),
        inquirer.Text('asal', message="Masukkan Kota Asal"),
        inquirer.Text('tujuan', message="Masukkan Kota Tujuan"),
        inquirer.Text('tanggal', message="Masukkan Tanggal (DD-MM-YYYY)"),
        inquirer.Text('jam', message="Masukkan Jam (HH:MM)"),
        inquirer.Text('harga', message="Masukkan Harga Tiket (full angka, contoh: 25000)"),
        inquirer.Text('nama_pesawat', message="Masukkan Nama Pesawat"),
        inquirer.List('jenis_pesawat', message="Pilih Jenis Pesawat", choices=['Ekonomi','Bisnis'])
    ])

    if jadwal_baru is None:
        print("\n❌ Input dibatalkan.")
        return

    # ===== Validasi =====
    if not validasi_huruf(jadwal_baru['asal'], "Kota asal"): return
    if not validasi_huruf(jadwal_baru['tujuan'], "Kota tujuan"): return
    if not validasi_tanggal(jadwal_baru['tanggal']): return
    if not validasi_jam(jadwal_baru['jam']): return
    harga_int = validasi_harga(jadwal_baru['harga'])
    if harga_int is None: return
    jadwal_baru['harga'] = harga_int
    if not validasi_huruf(jadwal_baru['nama_pesawat'], "Nama pesawat"): return

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
    print(f"Pesawat: {jadwal_baru['nama_pesawat']} ({jadwal_baru['jenis_pesawat']})")
