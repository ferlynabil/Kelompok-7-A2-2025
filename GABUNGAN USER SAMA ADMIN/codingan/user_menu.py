import json
import os
from datetime import datetime
from prettytable import PrettyTable
from colorama import init, Fore
import inquirer

init(autoreset=True)

# ---------------------------
# Helper
# ---------------------------
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)
    with open(file, "r") as f:
        return json.load(f)


def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------
# 1. Lihat Jadwal
# ---------------------------
def lihat_jadwal():
    cls()
    try:
        with open("jadwal.json", "r") as f:
            data_jadwal = json.load(f)
    except:
        print(Fore.RED + "❌ File jadwal.json tidak ditemukan.")
        return

    if not data_jadwal:
        print(Fore.YELLOW + "❌ Belum ada jadwal penerbangan.")
        return

    table = PrettyTable()
    table.field_names = ["Kode", "Asal", "Tujuan", "Tanggal", "Jam", "Harga"]

    for j in data_jadwal:
        table.add_row([j['kode'], j['asal'], j['tujuan'], j['tanggal'], j['jam'], j['harga']])

    print(Fore.CYAN + "\n📋 DAFTAR JADWAL PENERBANGAN:")
    print(table)


# ---------------------------
# 2. Pesan Tiket (Pakai Inquirer)
# ---------------------------
def pesan_tiket(username=None):
    cls()

    # load jadwal
    try:
        with open("jadwal.json", "r") as f:
            jadwal = json.load(f)
    except:
        print(Fore.RED + "❌ File jadwal.json tidak ditemukan.")
        return

    if not jadwal:
        print(Fore.YELLOW + "❌ Belum ada jadwal.")
        return

    # tampilkan tabel jadwal
    table = PrettyTable()
    table.field_names = ["Kode", "Asal", "Tujuan", "Tanggal", "Jam", "Harga"]
    for j in jadwal:
        table.add_row([j["kode"], j["asal"], j["tujuan"], j["tanggal"], j["jam"], j["harga"]])

    print(Fore.CYAN + "\n📋 DAFTAR JADWAL PENERBANGAN:")
    print(table)

    # buat pilihan inquirer
    pilihan = []
    for j in jadwal:
        pilihan.append(
            f"{j['kode']} - {j['asal']} → {j['tujuan']} | {j['tanggal']} {j['jam']} | Rp{j['harga']}"
        )

    # pilih penerbangan
    jawab = inquirer.prompt([
        inquirer.List(
            "pilih",
            message="✈ Pilih jadwal penerbangan:",
            choices=pilihan
        )
    ])

    if not jawab:
        print(Fore.YELLOW + "❌ Pemesanan dibatalkan.")
        return

    teks = jawab["pilih"]
    kode = teks.split(" - ")[0]

    # ambil jadwal berdasarkan kode
    data = next((x for x in jadwal if x["kode"] == kode), None)

    if not data:
        print(Fore.RED + "❌ Jadwal tidak ditemukan.")
        return

    # minta nama
    nama = input("Masukkan nama penumpang: ").strip()
    while not nama:
        nama = input("Nama tidak boleh kosong, masukkan lagi: ").strip()

    # simpan tiket ke keranjang
    keranjang = load_json("keranjang.json")
    waktu_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    keranjang.append({
        "nama": nama,
        "jadwal": data,
        "waktu_pesan": waktu_now
    })

    save_json("keranjang.json", keranjang)

    print(Fore.GREEN + "\n✔ Tiket berhasil dimasukkan ke keranjang!")
    print(Fore.YELLOW + f"Waktu pesan: {waktu_now}")


# ---------------------------
# 3. Timbang Bagasi
# ---------------------------
def timbang_bagasi():
    cls()
    print(Fore.CYAN + "\n=== TIMBANG BAGASI ===")

    while True:
        try:
            berat = float(input("Masukkan berat bagasi (kg): ").strip())
            if berat < 0:
                print(Fore.RED + "❌ Tidak boleh minus! Masukkan ulang.\n")
                continue
            break
        except:
            print(Fore.RED + "❌ Input harus angka! Coba lagi.\n")

    if berat <= 20:
        print(Fore.GREEN + "✔ Bagasi gratis (≤20 kg).")
    else:
        kelebihan = berat - 20
        biaya = kelebihan * 50000
        print(Fore.YELLOW + f"Kelebihan {kelebihan:.1f} kg → Biaya Rp{int(biaya):,}")


# ---------------------------
# 4. Bayar Tiket
# ---------------------------
def bayar_tiket():
    cls()
    keranjang = load_json("keranjang.json")
    tiket_user = load_json("data_tiket_user.json")

    if not keranjang:
        print(Fore.YELLOW + "❌ Keranjang kosong!")
        return

    print(Fore.CYAN + "\n=== PEMBAYARAN ===")

    table = PrettyTable()
    table.field_names = ["No", "Nama", "Kode", "Asal", "Tujuan", "Harga", "Pesan"]

    total = 0
    for i, t in enumerate(keranjang, start=1):
        j = t["jadwal"]
        total += j["harga"]
        table.add_row([i, t["nama"], j["kode"], j["asal"], j["tujuan"], j["harga"], t["waktu_pesan"]])

    print(table)
    print(Fore.MAGENTA + f"Total pembayaran: Rp{int(total):,}")

    konfirm = input("Lanjutkan pembayaran? (y/n): ").lower()
    while konfirm not in ("y", "n"):
        konfirm = input("Input salah. Pilih y/n: ").lower()

    if konfirm == "n":
        print(Fore.YELLOW + "❌ Pembayaran dibatalkan.")
        return

    waktu_bayar = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for t in keranjang:
        t["waktu_bayar"] = waktu_bayar
        tiket_user.append(t)

    keranjang.clear()
    save_json("data_tiket_user.json", tiket_user)
    save_json("keranjang.json", keranjang)

    print(Fore.GREEN + "✔ Pembayaran berhasil!")
    print(Fore.YELLOW + f"Waktu bayar: {waktu_bayar}")


# ---------------------------
# 5. Lihat Tiket User
# ---------------------------
def lihat_tiket_user():
    cls()
    tiket = load_json("data_tiket_user.json")

    print(Fore.CYAN + "\n=== TIKET YANG SUDAH DIBELI ===")

    if not tiket:
        print(Fore.YELLOW + "Belum ada tiket.")
        return

    table = PrettyTable()
    table.field_names = ["No", "Nama", "Kode", "Asal", "Tujuan",
                         "Harga", "Pesan", "Bayar"]

    for i, t in enumerate(tiket, start=1):
        j = t["jadwal"]
        table.add_row([
            i,
            t["nama"],
            j["kode"],
            j["asal"],
            j["tujuan"],
            j["harga"],
            t["waktu_pesan"],
            t.get("waktu_bayar", "-")
        ])

    print(table)
