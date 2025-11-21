import json
import os
from datetime import datetime
from prettytable import PrettyTable
from colorama import init, Fore, Style
from visualize import grafik_tiket

# Inisialisasi colorama
init(autoreset=True)

# fungsi cls
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# ----------------------
# Helper JSON
# ----------------------
def load_json(filepath):
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            json.dump([], f)
    with open(filepath, "r") as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


# ----------------------
# 1. Lihat Jadwal Penerbangan
# ----------------------
def lihat_jadwal():
    cls()
    jadwal = load_json("data_jadwal.json")

    print(Fore.CYAN + "\n=== DAFTAR JADWAL PENERBANGAN ===")
    table = PrettyTable()
    table.field_names = ["Kode", "Asal", "Tujuan", "Harga (Rp)"]

    for j in jadwal:
        table.add_row([j["kode"], j["asal"], j["tujuan"], j["harga"]])

    print(table)


# ----------------------
# 2. Pesan Tiket
# ----------------------
def pesan_tiket():
    cls()
    jadwal = load_json("data_jadwal.json")
    keranjang = load_json("keranjang.json")

    print(Fore.CYAN + "\n=== PESAN TIKET ===")
    kode = input("Masukkan kode penerbangan: ").strip()

    data = next((x for x in jadwal if x["kode"].lower() == kode.lower()), None)

    if data:
        nama = input("Masukkan nama penumpang: ").strip()
        waktu_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        keranjang.append({
            "nama": nama,
            "jadwal": data,
            "waktu_pesan": waktu_now
        })
        save_json("keranjang.json", keranjang)
        print(Fore.GREEN + "Tiket berhasil ditambahkan ke keranjang.")
        print(Fore.YELLOW + f"Waktu pesan: {waktu_now}")
    else:
        print(Fore.RED + "Kode penerbangan tidak ditemukan.")


# ----------------------
# 3. Menimbang Berat Bagasi
# ----------------------
def timbang_bagasi():
    cls()
    print(Fore.CYAN + "\n=== TIMBANG BAGASI ===")
    try:
        berat = float(input("Masukkan berat bagasi (kg): ").strip())
    except ValueError:
        print(Fore.RED + "ERROR: Input harus berupa angka.")
        return

    if berat <= 20:
        print(Fore.GREEN + "Bagasi termasuk gratis (<= 20 kg).")
    else:
        kelebihan = berat - 20
        biaya = kelebihan * 50000
        print(Fore.YELLOW + f"Kelebihan: {kelebihan:.2f} kg")
        print(Fore.YELLOW + f"Biaya tambahan: Rp{int(biaya):,}")


# ----------------------
# 4. Melakukan Pembayaran
# ----------------------
def bayar_tiket():
    cls()
    keranjang = load_json("keranjang.json")
    tiket_user = load_json("data_tiket_user.json")

    if not keranjang:
        print(Fore.RED + "Keranjang masih kosong!")
        return

    print(Fore.CYAN + "\n=== PEMBAYARAN ===")
    table = PrettyTable()
    table.field_names = ["No", "Nama", "Kode", "Asal", "Tujuan", "Harga (Rp)", "Waktu Pesan"]

    total = 0
    for idx, item in enumerate(keranjang, start=1):
        j = item["jadwal"]
        table.add_row([
            idx,
            item.get("nama", ""),
            j.get("kode", ""),
            j.get("asal", ""),
            j.get("tujuan", ""),
            j.get("harga", 0),
            item.get("waktu_pesan", "")
        ])
        total += j.get("harga", 0)

    print(table)
    print(Fore.MAGENTA + f"Total pembayaran: Rp{int(total):,}")

    confirm = input("Lanjutkan pembayaran? (y/n): ").strip().lower()
    if confirm not in {"y", "n"}:
        print(Fore.RED + "Input tidak valid.")
        return

    if confirm == "y":
        waktu_bayar = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for item in keranjang:
            item["waktu_bayar"] = waktu_bayar
            tiket_user.append(item)

        keranjang.clear()
        save_json("data_tiket_user.json", tiket_user)
        save_json("keranjang.json", keranjang)

        print(Fore.GREEN + "Pembayaran berhasil! Tiket tersimpan.")
        print(Fore.YELLOW + f"Waktu bayar: {waktu_bayar}")
    else:
        print(Fore.YELLOW + "Pembayaran dibatalkan.")


# ----------------------
# 5. Melihat Tiket yang sudah dibeli
# ----------------------
def lihat_tiket_user():
    cls()
    tiket_user = load_json("data_tiket_user.json")

    print(Fore.CYAN + "\n=== TIKET YANG SUDAH DIBELI ===")
    if not tiket_user:
        print(Fore.YELLOW + "Belum ada tiket yang dibeli.")
        return

    table = PrettyTable()
    table.field_names = ["No", "Nama", "Kode", "Asal", "Tujuan", "Harga (Rp)", "Waktu Pesan", "Waktu Bayar"]

    for idx, t in enumerate(tiket_user, start=1):
        j = t["jadwal"]
        table.add_row([
            idx,
            t.get("nama", ""),
            j.get("kode", ""),
            j.get("asal", ""),
            j.get("tujuan", ""),
            j.get("harga", 0),
            t.get("waktu_pesan", ""),
            t.get("waktu_bayar", "")
        ])

    print(table)
    grafik_tiket()
