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

def validasi_kapasitas(teks):
    teks = teks.strip()
    if not teks:
        return None
    if teks.isdigit() and int(teks) > 0:
        return int(teks)
    print("✖ Kapasitas kursi harus angka positif!")
    return None

def validasi_kolom(teks):
    teks = teks.strip()
    if not teks:
        return None
    if teks.isdigit() and 1 <= int(teks) <= 10:
        return int(teks)
    print("✖ Jumlah kursi per baris harus angka 1–10!")
    return None

# ===== Fungsi Ubah Jadwal =====
def ubah_jadwal():
    # Load file JSON dengan fallback
    try:
        if os.path.exists("jadwal.json"):
            with open("jadwal.json", "r") as f:
                data_jadwal = json.load(f)
        else:
            data_jadwal = []
    except (FileNotFoundError, json.JSONDecodeError):
        data_jadwal = []

    if not data_jadwal:
        print("❌ Belum ada jadwal penerbangan untuk diubah.")
        return

    # Pilihan jadwal
    pilihan_jadwal = [
        f"{j['kode']} | {j['asal']} → {j['tujuan']} | {j['tanggal']} {j['jam']} | Rp{j['harga']}"
        for j in data_jadwal
    ]

    pilih = inquirer.prompt([
        inquirer.List('jadwal', message="Pilih jadwal yang ingin diubah", choices=pilihan_jadwal)
    ])['jadwal']

    index = pilihan_jadwal.index(pilih)
    jadwal_ditemukan = data_jadwal[index]

    print(f"\n📌 Jadwal lama: {jadwal_ditemukan}")

    # fallback nama maskapai/pesawat
    lama_maskapai = jadwal_ditemukan.get("nama_maskapai") or jadwal_ditemukan.get("nama_pesawat","-")

    # Prompt perubahan
    perubahan = inquirer.prompt([
        inquirer.Text('asal', message=f"Ubah Kota Asal (lama: {jadwal_ditemukan['asal']})"),
        inquirer.Text('tujuan', message=f"Ubah Kota Tujuan (lama: {jadwal_ditemukan['tujuan']})"),
        inquirer.Text('tanggal', message=f"Ubah Tanggal (lama: {jadwal_ditemukan['tanggal']})"),
        inquirer.Text('jam', message=f"Ubah Jam (lama: {jadwal_ditemukan['jam']})"),
        inquirer.Text('harga', message=f"Ubah Harga Tiket (lama: {jadwal_ditemukan['harga']})"),
        inquirer.Text('nama_maskapai', message=f"Ubah Nama Maskapai (lama: {lama_maskapai})"),
        inquirer.List('jenis_pesawat', message=f"Ubah Jenis Pesawat (lama: {jadwal_ditemukan.get('jenis_pesawat','-')})", choices=['Ekonomi','Bisnis']),
        inquirer.Text('kapasitas', message=f"Ubah Kapasitas Kursi (lama: {jadwal_ditemukan.get('kapasitas','-')})"),
        inquirer.Text('kolom', message=f"Ubah Jumlah Kursi per Baris (lama: {jadwal_ditemukan.get('kolom','-')})")
    ])

    # Terapkan perubahan dengan validasi
    if perubahan['asal'].strip():
        if not validasi_huruf(perubahan['asal'], "Kota asal"): return
        jadwal_ditemukan['asal'] = perubahan['asal'].strip()

    if perubahan['tujuan'].strip():
        if not validasi_huruf(perubahan['tujuan'], "Kota tujuan"): return
        jadwal_ditemukan['tujuan'] = perubahan['tujuan'].strip()

    if perubahan['tanggal'].strip():
        if not validasi_tanggal(perubahan['tanggal']): return
        jadwal_ditemukan['tanggal'] = perubahan['tanggal'].strip()

    if perubahan['jam'].strip():
        if not validasi_jam(perubahan['jam']): return
        jadwal_ditemukan['jam'] = perubahan['jam'].strip()

    if perubahan['harga'].strip():
        harga_int = validasi_harga(perubahan['harga'])
        if harga_int is None: return
        jadwal_ditemukan['harga'] = harga_int

    if perubahan['nama_maskapai'].strip():
        if not validasi_huruf(perubahan['nama_maskapai'], "Nama maskapai"): return
        jadwal_ditemukan['nama_maskapai'] = perubahan['nama_maskapai'].strip()

    if perubahan['jenis_pesawat']:
        jadwal_ditemukan['jenis_pesawat'] = perubahan['jenis_pesawat']

    if perubahan['kapasitas'].strip():
        kapasitas_int = validasi_kapasitas(perubahan['kapasitas'])
        if kapasitas_int is None: return
        jadwal_ditemukan['kapasitas'] = kapasitas_int

    if perubahan['kolom'].strip():
        kolom_int = validasi_kolom(perubahan['kolom'])
        if kolom_int is None: return
        jadwal_ditemukan['kolom'] = kolom_int

    # regenerate kursi jika kapasitas/kolom berubah
    if 'kapasitas' in jadwal_ditemukan and 'kolom' in jadwal_ditemukan:
        kursi_list = []
        for i in range(jadwal_ditemukan['kapasitas']):
            kursi_id = f"{(i//jadwal_ditemukan['kolom'])+1}{chr(65+(i%jadwal_ditemukan['kolom']))}"
            kursi_list.append({"nomor": kursi_id, "status": "kosong"})
        jadwal_ditemukan['kursi'] = kursi_list

    # Simpan kembali dengan error handling
    try:
        with open("jadwal.json", "w") as f:
            json.dump(data_jadwal, f, indent=4)
    except Exception as e:
        print(f"✖ Gagal menyimpan perubahan: {e}")
        return

    harga_rupiah = "Rp {:,}".format(jadwal_ditemukan['harga']).replace(",", ".")
    print("\n✅ Jadwal penerbangan berhasil diubah!")
    print(f"Kode: {jadwal_ditemukan['kode']}")
    print(f"Asal: {jadwal_ditemukan['asal']} → Tujuan: {jadwal_ditemukan['tujuan']}")
    print(f"Tanggal: {jadwal_ditemukan['tanggal']} | Jam: {jadwal_ditemukan['jam']}")
    print(f"Harga: {harga_rupiah}")
    print(f"Maskapai: {jadwal_ditemukan['nama_maskapai']} ({jadwal_ditemukan['jenis_pesawat']})")
    print(f"Kapasitas Kursi: {jadwal_ditemukan.get('kapasitas','-')} (per baris {jadwal_ditemukan.get('kolom','-')})")
    print("Kursi tersedia:")
    for k in jadwal_ditemukan.get('kursi', []):
        print(f"[{k['nomor']}]", end=" ")
    print()
