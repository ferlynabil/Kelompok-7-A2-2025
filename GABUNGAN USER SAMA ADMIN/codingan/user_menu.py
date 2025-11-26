import os
import json
import random
from prettytable import PrettyTable
import inquirer


# ------------------------------------------------------
# LOAD & SAVE JSON
# ------------------------------------------------------
def load_json(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# ------------------------------------------------------
# LIHAT JADWAL (UNTUK USER)
# ------------------------------------------------------
def lihat_jadwal():
    os.system("cls")

    data = load_json("jadwal.json")

    if not data:
        print("❌ Belum ada jadwal.")
        return

    table = PrettyTable()
    table.field_names = ["Kode", "Asal", "Tujuan", "Tanggal", "Jam", "Harga"]

    for j in data:
        table.add_row([
            j["kode"], j["asal"], j["tujuan"], j["tanggal"], j["jam"], j["harga"]
        ])

    print("\n📋 DAFTAR JADWAL PENERBANGAN:\n")
    print(table)


# ------------------------------------------------------
# PESAN TIKET
# ------------------------------------------------------

def pesan_tiket(username):
    os.system("cls")

    jadwal = load_json("jadwal.json")
    if not jadwal:
        print("❌ Jadwal kosong.")
        return

    print("=== PILIH JADWAL ===\n")

    table = PrettyTable()
    table.field_names = ["ID", "Kode", "Asal", "Tujuan", "Tanggal", "Jam", "Harga"]

    pilihan_list = []
    for i, j in enumerate(jadwal):
        table.add_row([i+1, j["kode"], j["asal"], j["tujuan"], j["tanggal"], j["jam"], j["harga"]])
        pilihan_list.append(f"{i+1}. {j['asal']} → {j['tujuan']} ({j['tanggal']} {j['jam']}) - Rp {j['harga']}")

    print(table)

    pertanyaan = [
        inquirer.List(
            "pilih",
            message="Pilih jadwal:",
            choices=pilihan_list
        )
    ]
    jawaban = inquirer.prompt(pertanyaan)

    if jawaban is None:
        print("❌ Pemesanan dibatalkan.")
        return

    index = int(jawaban["pilih"].split(".")[0]) - 1
    data = jadwal[index]

    tiket = load_json("tiket.json")

    tiket.append({
        "user": username,
        "kode": data["kode"],
        "asal": data["asal"],
        "tujuan": data["tujuan"],
        "tanggal": data["tanggal"],
        "jam": data["jam"],
        "harga": data["harga"],
        "status": "belum"
    })

    save_json("tiket.json", tiket)

    print("\n✅ Tiket berhasil dipesan!")
    print("Status: BELUM DIBAYAR\n")

# ------------------------------------------------------
# TIKET SAYA
# ------------------------------------------------------
def lihat_tiket_user(username):
    os.system("cls")

    tiket = load_json("tiket.json")
    data = [t for t in tiket if t["user"] == username]

    if not data:
        print("⚠ Belum ada tiket.")
        return

    print("=== TIKET KAMU ===\n")

    table = PrettyTable()
    table.field_names = ["Kode", "Asal", "Tujuan", "Tanggal", "Jam", "Harga", "Status"]

    for t in data:
        table.add_row([
            t["kode"], t["asal"], t["tujuan"], t["tanggal"], t["jam"],
            f"Rp {t['harga']:,}", t["status"].upper()
        ])

    print(table)



# ------------------------------------------------------
# TIMBANG BAGASI
# ------------------------------------------------------
def timbang_bagasi(username):
    os.system("cls")
    print("=== MENIMBANG BAGASI ===\n")

    while True:
        pertanyaan = [
            inquirer.Text("berat", message="Masukkan berat bagasi (kg)")
        ]
        jawab = inquirer.prompt(pertanyaan)

        if jawab is None:
            print("❌ Dibatalkan.")
            return

        try:
            berat = float(jawab["berat"])
        except ValueError:
            print("❌ Input harus angka!")
            continue  # ulang khusus input berat

        if berat < 0:
            print("❌ Berat tidak boleh minus!")
            continue

        break  # Keluar loop kalau valid

    # --- Perhitungan ---
    if berat <= 15:
        print(f"\n✔ Berat: {berat} kg — GRATIS!")
    else:
        kelebihan = berat - 15
        denda = kelebihan * 20000
        print(f"\n⚠ Berat: {berat} kg — Kelebihan {kelebihan} kg")
        print(f"Denda: Rp {denda:,}")

    input("\nEnter untuk kembali...")

# ------------------------------------------------------
# PEMBAYARAN
# ------------------------------------------------------
def bayar_tiket(username):
    os.system("cls")

    tiket = load_json("tiket.json")
    tiket_user = [t for t in tiket if t["user"] == username and t["status"] == "belum"]

    if not tiket_user:
        print("⚠ Tidak ada tiket yang perlu dibayar.")
        return

    pilihan = []
    for i, t in enumerate(tiket_user):
        pilihan.append(f"{i+1}. {t['asal']} → {t['tujuan']} ({t['tanggal']} {t['jam']}) - Rp {t['harga']}")

    pertanyaan = [
        inquirer.List("pilih", message="Pilih tiket :", choices=pilihan)
    ]
    jawaban = inquirer.prompt(pertanyaan)

    if jawaban is None:
        print("❌ Dibatalkan.")
        return

    idx = int(jawaban["pilih"].split(".")[0]) - 1
    t = tiket_user[idx]
    harga = t["harga"]

    # PILIH METODE
    metode_pembayaran = [
        "Virtual Account",
        "QRIS",
        "Minimarket"
    ]

    pilih_metode = [
        inquirer.List("metode", message="Pilih metode pembayaran:", choices=metode_pembayaran)
    ]
    metode = inquirer.prompt(pilih_metode)["metode"]

    os.system("cls")

    if metode == "Virtual Account":
        bank = ["BCA", "MANDIRI", "BRI"]

        pilih_bank = [
            inquirer.List("bank", message="Pilih bank:", choices=bank)
        ]
        b = inquirer.prompt(pilih_bank)["bank"]

        kode = {"BCA":"014","MANDIRI":"008","BRI":"002"}
        nomor_va = kode[b] + str(random.randint(1000000000, 9999999999))

        print(f"Bank: {b}")
        print(f"VA Number: {nomor_va}")
        print(f"Total: Rp {harga:,}")

    elif metode == "QRIS":
        qris = "000201" + str(random.randint(10000000,99999999))
        print(f"QRIS Code: {qris}")
        print(f"Total: Rp {harga:,}")

    elif metode == "Minimarket":
        kode_bayar = str(random.randint(100000000000, 999999999999))
        toko = random.choice(["Indomaret", "Alfamart"])

        print(f"Bayar di: {toko}")
        print(f"Kode Bayar: {kode_bayar}")
        print(f"Total: Rp {harga:,}")

    # KONFIRMASI PEMBAYARAN
    konfirmasi = [
        inquirer.Confirm("ok", message="Sudah melakukan pembayaran?", default=False)
    ]
    yes = inquirer.prompt(konfirmasi)

    if not yes["ok"]:
        print("❌ Pembayaran dibatalkan.")
        return

    # Ubah status jadi lunas
    for item in tiket:
        if item == t:
            item["status"] = "lunas"

    save_json("tiket.json", tiket)

    print("\n✅ PEMBAYARAN BERHASIL!")



# ------------------------------------------------------
# MENU USER
# ------------------------------------------------------
def menu_user(username):
    while True:
        os.system("cls")
        print(f"=== MENU USER ({username}) ===")
        print("1. Lihat Jadwal")
        print("2. Pesan Tiket")
        print("3. Timbang Bagasi")
        print("4. Pembayaran")
        print("5. Tiket Saya")
        print("6. Logout")

        pilih = input("\nPilih: ")

        if pilih == "1":
            lihat_jadwal()
            input("\nEnter...")
        elif pilih == "2":
            pesan_tiket(username)
            input("\nEnter...")
        elif pilih == "3":
            timbang_bagasi()
            input("\nEnter...")
        elif pilih == "4":
            bayar_tiket(username)
            input("\nEnter...")
        elif pilih == "5":
            lihat_tiket_user(username)
            input("\nEnter...")
        elif pilih == "6":
            break
        else:
            print("❌ Pilihan tidak ada!")
            input("Enter...")
