import os
import json
import inquirer
from colorama import init, Fore
from prettytable import PrettyTable

# Import fungsi dari modul yang sudah ada
from jadwal_tambah import tambah_jadwal
from jadwal_ubah import ubah_jadwal
from jadwal_hapus import hapus_jadwal
from jadwal_lihat import lihat_jadwal
from akun_lihat import lihat_akun
from user_menu import (
    lihat_jadwal as user_lihat_jadwal,
    pesan_tiket,
    timbang_bagasi,
    bayar_tiket,
    lihat_tiket_user
)
from konfirmasi_pesanan import konfirmasi_pesanan

# ⬇ Pakai sistem login dari file login.py
from login import login, register

init(autoreset=True)

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nTekan Enter untuk melanjutkan...")


# ====== LIHAT PESANAN USER ======
def lihat_pesanan_user():
    try:
        with open("tiket.json", "r") as f:
            tiket = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tiket = []

    if not tiket:
        print(Fore.YELLOW + "⚠ Belum ada pesanan tiket.")
        return

    print(Fore.CYAN + "=== DAFTAR PESANAN USER ===\n")
    table = PrettyTable()
    table.field_names = [
        "User", "Kode", "Asal", "Tujuan", "Tanggal", "Jam",
        "Harga", "Kursi", "Maskapai", "Jenis Pesawat", "Status"
    ]

    for t in tiket:
        table.add_row([
            t.get("user","-"),
            t.get("kode","-"),
            t.get("asal","-"),
            t.get("tujuan","-"),
            t.get("tanggal","-"),
            t.get("jam","-"),
            f"Rp {t.get('harga',0):,}",
            t.get("kursi","-"),
            t.get("nama_maskapai","-"),
            t.get("jenis_pesawat","-"),
            t.get("status","-").upper()
        ])

    print(table)


# ====== TOTAL PENDAPATAN ======
def total_pendapatan():
    try:
        with open("tiket.json", "r") as f:
            tiket = json.load(f)
    except:
        tiket = []

    if not tiket:
        print(Fore.YELLOW + "⚠ Belum ada tiket.")
        return

    total = sum(t.get("harga", 0) for t in tiket if str(t.get("status","")).lower() == "lunas")

    print(Fore.CYAN + "=== TOTAL PENDAPATAN ===\n")
    print(Fore.GREEN + f"💰 Total Pendapatan: Rp {total:,}")


# ====== MENU ADMIN ======
def menu_admin(username):
    while True:
        cls()
        print(Fore.CYAN + f"=== MENU ADMIN ({username}) ===\n")

        menu = [
            inquirer.List(
                'pilihan',
                message="Pilih menu:",
                choices=[
                    '1. Tambah Jadwal Penerbangan',
                    '2. Ubah Jadwal Penerbangan',
                    '3. Hapus Jadwal Penerbangan',
                    '4. Lihat Jadwal Penerbangan',
                    '5. Lihat Daftar Akun User',
                    '6. Lihat Daftar Pesanan User',
                    '7. Konfirmasi Pesanan User',
                    '8. Total Pendapatan',
                    '9. Logout'
                ]
            )
        ]

        jawab = inquirer.prompt(menu)
        if jawab is None: break

        pilih = jawab["pilihan"]

        if pilih == '1. Tambah Jadwal Penerbangan':
            cls(); tambah_jadwal(); pause()
        elif pilih == '2. Ubah Jadwal Penerbangan':
            cls(); ubah_jadwal(); pause()
        elif pilih == '3. Hapus Jadwal Penerbangan':
            cls(); hapus_jadwal(); pause()
        elif pilih == '4. Lihat Jadwal Penerbangan':
            cls(); lihat_jadwal(); pause()
        elif pilih == '5. Lihat Daftar Akun User':
            cls(); lihat_akun(); pause()
        elif pilih == '6. Lihat Daftar Pesanan User':
            cls(); lihat_pesanan_user(); pause()
        elif pilih == '7. Konfirmasi Pesanan User':
            cls(); konfirmasi_pesanan(); pause()
        elif pilih == '8. Total Pendapatan':
            cls(); total_pendapatan(); pause()
        elif pilih == '9. Logout':
            print(Fore.GREEN + "\n✔ Logout berhasil."); pause(); break


# ====== MENU USER ======
def menu_user(username):
    while True:
        cls()
        print(Fore.CYAN + f"=== MENU USER ({username}) ===\n")

        menu = [
            inquirer.List(
                'pilihan',
                message="Pilih menu:",
                choices=[
                    '1. Lihat Jadwal Penerbangan',
                    '2. Pesan Tiket',
                    '3. Menimbang Berat Bagasi',
                    '4. Melakukan Pembayaran',
                    '5. Melihat Tiket yang Sudah Dibeli',
                    '6. Logout'
                ]
            )
        ]

        jawab = inquirer.prompt(menu)
        if jawab is None: break

        pilih = jawab["pilihan"]

        if pilih == '1. Lihat Jadwal Penerbangan':
            cls(); user_lihat_jadwal(); pause()
        elif pilih == '2. Pesan Tiket':
            cls(); pesan_tiket(username); pause()
        elif pilih == '3. Menimbang Berat Bagasi':
            cls(); timbang_bagasi(username); pause()
        elif pilih == '4. Melakukan Pembayaran':
            cls(); bayar_tiket(username); pause()
        elif pilih == '5. Melihat Tiket yang Sudah Dibeli':
            cls(); lihat_tiket_user(username); pause()
        elif pilih == '6. Logout':
            print(Fore.GREEN + "\n✔ Logout berhasil."); pause(); break


# ====== MAIN ======
def main():
    while True:
        cls()
        print(Fore.CYAN + "╔═══════════════════════════════════════╗")
        print(Fore.CYAN + "║  SISTEM PEMESANAN TIKET FAFAFUFU AIR  ║")
        print(Fore.CYAN + "╚═══════════════════════════════════════╝\n")

        menu = [
            inquirer.List(
                'pilihan',
                message="Pilih menu:",
                choices=['1. Login', '2. Register', '3. Keluar']
            )
        ]

        jawab = inquirer.prompt(menu)
        if jawab is None: break

        pilih = jawab["pilihan"]

        if pilih == '1. Login':
            user_data = login()
            if user_data:
                if user_data["role"] == "admin":
                    menu_admin(user_data["username"])
                else:
                    menu_user(user_data["username"])

        elif pilih == '2. Register':
            register()

        elif pilih == '3. Keluar':
            cls()
            print(Fore.GREEN + "Terima kasih telah menggunakan sistem!")
            pause()
            break


if __name__ == "__main__":
    main()
