# ============================
#   MENU USER
# ============================

def menu_user():
    while True:
        print("\n===== MENU USER =====")
        print("1. Lihat Jadwal Penerbangan")
        print("2. Pesan Tiket")
        print("3. Menimbang Berat Bagasi")
        print("4. Melakukan Pembayaran")
        print("5. Melihat Tiket yang Sudah Dibeli")
        print("6. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            lihat_jadwal()

        elif pilihan == "2":
            pesan_tiket()

        elif pilihan == "3":
            timbang_bagasi()

        elif pilihan == "4":
            bayar_tiket()

        elif pilihan == "5":
            lihat_tiket_user()

        elif pilihan == "6":
            print("Logout berhasil...")
            break

        else:
            print("Pilihan tidak valid! Masukkan angka 1-6.")


# ============================
#   FUNGSI-FUNGSI USER
# ============================

# Contoh database sederhana
jadwal = [
    {"kode": "JT01", "asal": "Jakarta", "tujuan": "Surabaya", "harga": 850000},
    {"kode": "GA77", "asal": "Medan", "tujuan": "Jakarta", "harga": 950000},
]

tiket_user = []
keranjang = []


def lihat_jadwal():
    print("\n=== DAFTAR JADWAL PENERBANGAN ===")
    for j in jadwal:
        print(f"{j['kode']} | {j['asal']} -> {j['tujuan']} | Rp{j['harga']}")
    print("---------------------------------")


def pesan_tiket():
    print("\n=== PESAN TIKET ===")
    kode = input("Masukkan kode penerbangan: ")

    data = next((j for j in jadwal if j["kode"] == kode), None)

    if data:
        nama = input("Masukkan nama penumpang: ")
        keranjang.append({"nama": nama, "jadwal": data})
        print("Tiket berhasil ditambahkan ke keranjang.")
    else:
        print("Kode penerbangan tidak ditemukan.")


def timbang_bagasi():
    print("\n=== TIMBANG BAGASI ===")
    try:
        berat = float(input("Masukkan berat bagasi (kg): "))

        if berat <= 20:
            print("Bagasi gratis.")
        else:
            kelebihan = berat - 20
            biaya = kelebihan * 50000
            print(f"Kelebihan {kelebihan} kg | Biaya: Rp{biaya}")

    except ValueError:
        print("Input harus berupa angka!")


def bayar_tiket():
    print("\n=== PEMBAYARAN ===")

    if not keranjang:
        print("Keranjang masih kosong!")
        return

    total = sum(item["jadwal"]["harga"] for item in keranjang)
    print(f"Total pembayaran: Rp{total}")

    konfirmasi = input("Lanjutkan pembayaran? (y/n): ").lower()
    if konfirmasi == "y":
        tiket_user.extend(keranjang.copy())
        keranjang.clear()
        print("Pembayaran berhasil! Tiket tersimpan.")
    else:
        print("Pembayaran dibatalkan.")


def lihat_tiket_user():
    print("\n=== TIKET YANG SUDAH DIBELI ===")
    if not tiket_user:
        print("Belum ada tiket yang dibeli.")
    else:
        for t in tiket_user:
            j = t["jadwal"]
            print(f"{t['nama']} | {j['kode']} {j['asal']} -> {j['tujuan']} (Rp{j['harga']})")
    print("--------------------------------")
