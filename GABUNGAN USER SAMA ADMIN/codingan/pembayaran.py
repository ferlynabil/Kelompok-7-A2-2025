import json
import time
import random
import os
import inquirer

BASE_FILE = "pembayaran.json"

def load_pembayaran():
    if not os.path.exists(BASE_FILE):
        with open(BASE_FILE, "w") as f:
            json.dump([], f)
    with open(BASE_FILE, "r") as f:
        return json.load(f)

def save_pembayaran(data):
    with open(BASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def proses_pembayaran(nama_user):
    # Load tiket user
    with open("tiket.json", "r") as f:
        data_tiket = json.load(f)

    # Filter tiket yang belum dibayar
    tiket_user = [t for t in data_tiket if t["user"] == nama_user]

    if not tiket_user:
        print("\n❌ Kamu belum memesan tiket apapun!")
        return

    # Pilih tiket yang ingin dibayar
    choices = [f"{t['kode']} - {t['asal']} ➜ {t['tujuan']} - Rp {t['harga']}" for t in tiket_user]
    pilih = inquirer.prompt([
        inquirer.List("tiket", message="Pilih tiket yang ingin dibayar", choices=choices)
    ])["tiket"]

    # Temukan tiketnya
    tiket = tiket_user[choices.index(pilih)]

    # Pilih metode pembayaran
    metode = inquirer.prompt([
        inquirer.List(
            "bayar",
            message="Pilih metode pembayaran:",
            choices=["Dana", "OVO", "ShopeePay", "Bank Transfer"],
        )
    ])["bayar"]

    # Gimik akun tujuan
    akun = {
        "Dana": "0812-9988-1122 (A/N PT Penerbangan AI)",
        "OVO": "0813-4433-2211 (A/N PT Penerbangan AI)",
        "ShopeePay": "0819-6655-1234 (A/N PT Penerbangan AI)",
        "Bank Transfer": "BRI 1234-5566-7788 (PT Penerbangan AI)"
    }

    print("\n💰 Silakan transfer ke:")
    print(akun[metode])

    # Animasi proses
    print("\n🔄 Memverifikasi pembayaran...")
    for i in range(3):
        print(".", end="", flush=True)
        time.sleep(1)

    # Random success
    if random.choice([True, True, True, False]):  # 75% Sukses
        print("\n✅ Pembayaran Berhasil!")
        
        # Simpan ke json pembayaran
        data = load_pembayaran()
        data.append({
            "user": nama_user,
            "kode_tiket": tiket["kode"],
            "metode": metode,
            "harga": tiket["harga"],
            "status": "Lunas"
        })
        save_pembayaran(data)

        print(f"📄 Tiket {tiket['kode']} telah LUNAS!")
    else:
        print("\n❌ Pembayaran Gagal! Silakan coba lagi.")
