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
# LIHAT JADWAL (USER)
# ------------------------------------------------------
def lihat_jadwal():
    os.system("cls")
    data = load_json("jadwal.json")

    if not data:
        print("❌ Belum ada jadwal.")
        return

    table = PrettyTable()
    table.field_names = ["Kode", "Asal", "Tujuan", "Tanggal", "Jam", "Harga", "Maskapai", "Jenis Pesawat", "Kursi Tersedia"]

    for j in data:
        kursi_tersedia = sum(1 for k in j.get("kursi", []) if k.get("status") == "kosong")
        table.add_row([
            j["kode"], j["asal"], j["tujuan"], j["tanggal"], j["jam"],
            f"Rp {j['harga']:,}", j.get("nama_maskapai","-"), j.get("jenis_pesawat","-"),
            kursi_tersedia
        ])

    print("\n📋 DAFTAR JADWAL PENERBANGAN:\n")
    print(table)

# ------------------------------------------------------
# PESAN TIKET (USER)
# ------------------------------------------------------
def pesan_tiket(username):
    os.system("cls")
    jadwal = load_json("jadwal.json")
    if not jadwal:
        print("❌ Jadwal kosong.")
        return

    print("=== PILIH JADWAL ===\n")
    table = PrettyTable()
    table.field_names = ["ID", "Kode", "Asal", "Tujuan", "Tanggal", "Jam", "Harga", "Maskapai", "Jenis Pesawat", "Kursi Tersedia"]

    pilihan_list = []
    for i, j in enumerate(jadwal):
        kursi_tersedia = sum(1 for k in j.get("kursi", []) if k.get("status") == "kosong")
        table.add_row([
            i+1, j["kode"], j["asal"], j["tujuan"], j["tanggal"], j["jam"],
            f"Rp {j['harga']:,}", j.get("nama_maskapai","-"), j.get("jenis_pesawat","-"),
            kursi_tersedia
        ])
        pilihan_list.append(f"{i+1}. {j['asal']} → {j['tujuan']} ({j['tanggal']} {j['jam']}) - Rp {j['harga']} | {j.get('nama_maskapai','-')}")

    print(table)

    jawaban = inquirer.prompt([inquirer.List("pilih", message="Pilih jadwal:", choices=pilihan_list + ["❌ Batal"])])
    if jawaban is None or jawaban["pilih"] == "❌ Batal":
        print("❌ Pemesanan dibatalkan.")
        return

    index = int(jawaban["pilih"].split(".")[0]) - 1
    data = jadwal[index]

    # Pilih kursi kosong
    kursi_tersedia = [k["nomor"] for k in data.get("kursi", []) if k.get("status") == "kosong"]
    if not kursi_tersedia:
        print("❌ Tidak ada kursi tersedia.")
        return

    kursi_jawab = inquirer.prompt([inquirer.List("kursi", message="Pilih kursi:", choices=kursi_tersedia + ["❌ Batal"])])
    if kursi_jawab is None or kursi_jawab["kursi"] == "❌ Batal":
        print("❌ Pemesanan dibatalkan.")
        return

    kursi_dipilih = kursi_jawab["kursi"]

    # Update tiket.json
    tiket = load_json("tiket.json")
    tiket.append({
        "user": username,
        "kode": data["kode"],
        "asal": data["asal"],
        "tujuan": data["tujuan"],
        "tanggal": data["tanggal"],
        "jam": data["jam"],
        "harga": data["harga"],
        "kursi": kursi_dipilih,
        "nama_maskapai": data.get("nama_maskapai","-"),
        "jenis_pesawat": data.get("jenis_pesawat","-"),
        "status": "pending"
    })
    save_json("tiket.json", tiket)

    # Tandai kursi di jadwal.json sebagai X
    for k in data["kursi"]:
        if k["nomor"] == kursi_dipilih:
            k["status"] = "X"
    save_json("jadwal.json", jadwal)

    print("\n✅ Tiket berhasil dipesan!")
    print("Status: PENDING (menunggu konfirmasi admin)\n")

# ------------------------------------------------------
# LIHAT TIKET USER
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
    table.field_names = ["Kode", "Asal", "Tujuan", "Tanggal", "Jam", "Harga", "Kursi", "Maskapai", "Jenis Pesawat", "Status"]

    for t in data:
        status = t["status"].upper()
        if status == "CANCELLED":
            status = "⚠ CANCELLED"
        elif status == "PENDING":
            status = "⏳ PENDING"
        elif status == "CONFIRMED":
            status = "✅ CONFIRMED"
        elif status == "LUNAS":
            status = "💰 LUNAS"
        table.add_row([
            t["kode"], t["asal"], t["tujuan"], t["tanggal"], t["jam"],
            f"Rp {t['harga']:,}", t.get("kursi","-"),
            t.get("nama_maskapai","-"), t.get("jenis_pesawat","-"),
            status
        ])
    print(table)

# ------------------------------------------------------
# TIMBANG BAGASI
# ------------------------------------------------------
def timbang_bagasi(username):
    os.system("cls")
    print("=== MENIMBANG BAGASI ===\n")

    while True:
        jawab = inquirer.prompt([inquirer.Text("berat", message="Masukkan berat bagasi (kg)")])
        if jawab is None:
            print("❌ Dibatalkan.")
            return

        try:
            berat = float(jawab["berat"])
        except ValueError:
            print("❌ Input harus angka!")
            continue

        if berat < 0:
            print("❌ Berat tidak boleh minus!")
            continue

        break

    if berat <= 15:
        print(f"\n✔ Berat: {berat} kg — GRATIS!")
    else:
        kelebihan = berat - 15
        denda = kelebihan * 20000
        print(f"\n⚠ Berat: {berat} kg — Kelebihan {kelebihan} kg")
        print(f"Denda: Rp {denda:,}")

    input("\nEnter untuk kembali...")

# ------------------------------------------------------
# PEMBAYARAN (USER)
# ------------------------------------------------------
def bayar_tiket(username):
    os.system("cls")
    tiket = load_json("tiket.json")

    # Ambil tiket user yang sudah dikonfirmasi admin
    tiket_user = [t for t in tiket if t["user"] == username and t["status"] == "confirmed"]

    if not tiket_user:
        print("⚠ Tidak ada tiket yang bisa dibayar (butuh konfirmasi admin).")
        return

    pilihan = []
    for i, t in enumerate(tiket_user):
        pilihan.append(
            f"{i+1}. {t['asal']} → {t['tujuan']} ({t['tanggal']} {t['jam']}) "
            f"Kursi {t['kursi']} - Rp {t['harga']} | {t.get('nama_maskapai','-')}"
        )

    jawaban = inquirer.prompt([
        inquirer.List("pilih", message="Pilih tiket :", choices=pilihan + ["❌ Batal"])
    ])
    if jawaban is None or jawaban["pilih"] == "❌ Batal":
        print("❌ Dibatalkan.")
        return

    idx = int(jawaban["pilih"].split(".")[0]) - 1
    t = tiket_user[idx]
    harga = t["harga"]

    # Pilih metode pembayaran
    metode_pembayaran = ["Virtual Account", "QRIS", "Minimarket"]
    jawab_metode = inquirer.prompt([
        inquirer.List("metode", message="Pilih metode pembayaran:", choices=metode_pembayaran)
    ])
    if jawab_metode is None:
        print("❌ Dibatalkan.")
        return
    metode = jawab_metode["metode"]

    os.system("cls")
    if metode == "Virtual Account":
        bank = ["BCA", "MANDIRI", "BRI"]
        jawab_bank = inquirer.prompt([inquirer.List("bank", message="Pilih bank:", choices=bank)])
        if jawab_bank is None:
            print("❌ Dibatalkan.")
            return
        b = jawab_bank["bank"]
        kode = {"BCA":"014","MANDIRI":"008","BRI":"002"}
        nomor_va = kode[b] + str(random.randint(1000000000, 9999999999))
        print(f"Maskapai: {t.get('nama_maskapai','-')} ({t.get('jenis_pesawat','-')})")
        print(f"Bank: {b}\nVA Number: {nomor_va}\nTotal: Rp {harga:,}")

    elif metode == "QRIS":
        qris = "000201" + str(random.randint(10000000,99999999))
        print(f"Maskapai: {t.get('nama_maskapai','-')} ({t.get('jenis_pesawat','-')})")
        print(f"QRIS Code: {qris}\nTotal: Rp {harga:,}")

    elif metode == "Minimarket":
        kode_bayar = str(random.randint(100000000000, 999999999999))
        toko = random.choice(["Indomaret", "Alfamart"])
        print(f"Maskapai: {t.get('nama_maskapai','-')} ({t.get('jenis_pesawat','-')})")
        print(f"Bayar di: {toko}\nKode Bayar: {kode_bayar}\nTotal: Rp {harga:,}")

    # Konfirmasi setelah info pembayaran
    yes = inquirer.prompt([inquirer.Confirm("ok", message="Sudah melakukan pembayaran?", default=False)])
    if yes is None or not yes.get("ok", False):
        print("❌ Pembayaran dibatalkan.")
        return

    # Ubah status jadi lunas hanya jika masih "confirmed"
    for item in tiket:
        if (
            item["user"] == username and
            item["kode"] == t["kode"] and
            item.get("kursi") == t.get("kursi") and
            item["status"] == "confirmed"
        ):
            item["status"] = "lunas"

    save_json("tiket.json", tiket)
    print("\n✅ PEMBAYARAN BERHASIL!")
