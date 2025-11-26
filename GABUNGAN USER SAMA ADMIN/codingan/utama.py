import os
import json
import inquirer
from colorama import init, Fore

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


# Inisialisasi colorama
init(autoreset=True)

# ====== KONFIGURASI FILE ======
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AKUN_FILE = os.path.join(BASE_DIR, "akun.json")

# ====== FUNGSI HELPER ======
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nTekan Enter untuk melanjutkan...")

# ====== LOAD & SAVE USERS ======
def load_users():
    try:
        with open(AKUN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        default = {
            "admin": {"password": "242637", "role": "admin"}
        }
        with open(AKUN_FILE, "w") as f:
            json.dump(default, f, indent=4)
        return default

def save_users(users):
    with open(AKUN_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ====== REGISTER ======
# ====== REGISTER ======
def register():
    cls()
    print(Fore.CYAN + "=== REGISTER AKUN BARU ===\n")
    
    users = load_users()

    try:
        questions = [
            inquirer.Text("username", message="Username baru"),
            inquirer.Password("password", message="Password")
        ]
        ans = inquirer.prompt(questions)

        if ans is None:  # User cancelled
            print(Fore.YELLOW + "\nRegistrasi dibatalkan.")
            pause()
            return  # balik ke menu utama

        username = ans["username"].strip()
        password = ans["password"].strip()

        # Validasi username kosong
        if not username:
            print(Fore.RED + "✖ Username tidak boleh kosong!")
            pause()
            return

        # Validasi username hanya huruf
        if not username.isalpha():
            print(Fore.RED + "✖ Username hanya boleh huruf (A-Z)!")
            pause()
            return

        # Validasi password kosong
        if not password:
            print(Fore.RED + "✖ Password tidak boleh kosong!")
            pause()
            return

        # Validasi password hanya angka positif dan minimal 3 digit
        if not password.isdigit() or len(password) < 3:
            print(Fore.RED + "✖ Password harus berupa angka positif dan minimal 3 digit!")
            pause()
            return

        # Cek username sudah ada
        if username in users:
            print(Fore.RED + f"✖ Username '{username}' sudah terdaftar!")
            pause()
            return

        # Registrasi berhasil
        users[username] = {"password": password, "role": "user"}
        save_users(users)
        print(Fore.GREEN + f"\n✔ Akun '{username}' berhasil didaftarkan sebagai user!")
        pause()
        return

    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        pause()
        return

# ====== LOGIN ======
def login():
    cls()
    print(Fore.CYAN + "=== LOGIN ===\n")
    
    users = load_users()

    try:
        questions = [
            inquirer.Text("username", message="Masukkan username"),
            inquirer.Password("password", message="Masukkan password")
        ]
        ans = inquirer.prompt(questions)

        if ans is None:  # User cancelled
            print(Fore.YELLOW + "\nLogin dibatalkan.")
            pause()
            return None

        username = ans["username"].strip()
        password = ans["password"].strip()

        # Validasi login
        if username in users and users[username]["password"] == password:
            role = users[username]["role"]
            print(Fore.GREEN + f"\n✔ Login berhasil! Selamat datang, {username} ({role})")
            pause()
            return {"username": username, "role": role}
        else:
            print(Fore.RED + "\n✖ Username atau password salah!")
            pause()
            return None

    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        pause()
        return None

# ====== MENU ADMIN ======
def menu_admin(username):
    while True:
        cls()
        print(Fore.CYAN + f"=== MENU ADMIN ({username}) ===\n")

        pertanyaan_menu = [
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
        
        jawaban = inquirer.prompt(pertanyaan_menu)
        
        if jawaban is None:  # User cancelled
            print(Fore.YELLOW + "\nKembali ke menu utama.")
            pause()
            break

        pilihan = jawaban['pilihan']

        if pilihan == '1. Tambah Jadwal Penerbangan':
            cls()
            tambah_jadwal()
            pause()
        elif pilihan == '2. Ubah Jadwal Penerbangan':
            cls()
            ubah_jadwal()
            pause()
        elif pilihan == '3. Hapus Jadwal Penerbangan':
            cls()
            hapus_jadwal()
            pause()
        elif pilihan == '4. Lihat Jadwal Penerbangan':
            cls()
            lihat_jadwal()
            pause()
        elif pilihan == '5. Lihat Daftar Akun User':
            cls()
            lihat_akun()
            pause()
        elif pilihan == '6. Lihat Daftar Pesanan User':
            cls()
            print(Fore.YELLOW + "Fitur ini belum tersedia.")
            pause()
        elif pilihan == '7. Konfirmasi Pesanan User':
            cls()
            print(Fore.YELLOW + "Fitur ini belum tersedia.")
            pause()
        elif pilihan == '8. Total Pendapatan':
            cls()
            print(Fore.YELLOW + "Fitur ini belum tersedia.")
            pause()
        elif pilihan == '9. Logout':
            print(Fore.GREEN + "\n✔ Logout berhasil.")
            pause()
            break

# ====== MENU USER ======
def menu_user(username):
    while True:
        cls()
        print(Fore.CYAN + f"=== MENU USER ({username}) ===\n")

        pertanyaan_menu = [
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
        
        jawaban = inquirer.prompt(pertanyaan_menu)
        
        if jawaban is None:  # User cancelled
            print(Fore.YELLOW + "\nKembali ke menu utama.")
            pause()
            break

        pilihan = jawaban['pilihan']

        if pilihan == '1. Lihat Jadwal Penerbangan':
            cls()
            user_lihat_jadwal()
            pause()
        elif pilihan == '2. Pesan Tiket':
            cls()
            pesan_tiket(username)
            pause()
        elif pilihan == '3. Menimbang Berat Bagasi':
            cls()
            timbang_bagasi(username)
            pause()
        elif pilihan == "4. Melakukan Pembayaran":
            cls()
            bayar_tiket(username)
            pause()
        elif pilihan == '5. Melihat Tiket yang Sudah Dibeli':
            cls()
            lihat_tiket_user(username)
            pause()
        elif pilihan == '6. Logout':
            print(Fore.GREEN + "\n✔ Logout berhasil.")
            pause()
            break

# ====== MAIN MENU ======
def main():
    while True:
        cls()
        print(Fore.CYAN + "╔═══════════════════════════════════════╗")
        print(Fore.CYAN + "║  SISTEM PEMESANAN TIKET PESAWAT       ║")
        print(Fore.CYAN + "╚═══════════════════════════════════════╝\n")

        menu_utama = [
            inquirer.List(
                'pilihan',
                message="Pilih menu:",
                choices=[
                    '1. Login',
                    '2. Register',
                    '3. Keluar'
                ]
            )
        ]
        
        jawaban = inquirer.prompt(menu_utama)
        
        if jawaban is None:  # User cancelled
            print(Fore.YELLOW + "\nProgram dihentikan.")
            pause()
            break

        pilihan = jawaban['pilihan']

        if pilihan == '1. Login':
            user_data = login()
            if user_data:
                if user_data["role"] == "admin":
                    menu_admin(user_data["username"])
                elif user_data["role"] == "user":
                    menu_user(user_data["username"])

        elif pilihan == '2. Register':
            register()

        elif pilihan == '3. Keluar':
            cls()
            print(Fore.GREEN + "Terima kasih telah menggunakan sistem pemesanan tiket!")
            print(Fore.YELLOW + "Program selesai.\n")
            pause()
            break

if __name__ == "__main__":
    main()