import os
import json
import inquirer
from colorama import init, Fore


# ====== LOAD & SAVE USERS ======
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AKUN_FILE = os.path.join(BASE_DIR, "akun.json")

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

users = load_users()

# ====== UTIL ======
def clean():
    os.system('cls' if os.name == 'nt' else 'clear')
def cls():
    os.system('cls')

def pause():
    input("\nTekan Enter...")

# ====================================
# REGISTER (ulang sampai berhasil)
# ====================================
def register():
    while True:   # <-- LOOP REGISTER
        cls()
        print(Fore.CYAN + "=== REGISTER AKUN BARU ===\n")

        users = load_users()

        questions = [
            inquirer.Text("username", message="Username baru"),
            inquirer.Password("password", message="Password")
        ]
        ans = inquirer.prompt(questions)

        if ans is None:
            print(Fore.YELLOW + "Registrasi dibatalkan.")
            pause()
            return

        username = ans["username"].strip()
        password = ans["password"].strip()

        # VALIDASI
        if not username or not username.isalpha():
            print(Fore.RED + "✖ Username hanya boleh huruf dan tidak boleh kosong!")
            pause()
            continue

        if not password.isdigit() or len(password) < 3:
            print(Fore.RED + "✖ Password harus berupa angka positif minimal 3 digit!")
            pause()
            continue

        if username in users:
            print(Fore.RED + f"✖ Username '{username}' sudah digunakan!")
            pause()
            continue

        # SIMPAN
        users[username] = {"password": password, "role": "user"}
        save_users(users)

        print(Fore.GREEN + f"✔ Akun '{username}' berhasil dibuat!")
        pause()
        return  # keluar setelah berhasil


# ====================================
# LOGIN (ulang sampai benar)
# ====================================
def login():
    users = load_users()

    while True:   # <-- LOOP LOGIN
        cls()
        print(Fore.CYAN + "=== LOGIN ===\n")

        questions = [
            inquirer.Text("username", message="Masukkan username"),
            inquirer.Password("password", message="Masukkan password")
        ]
        ans = inquirer.prompt(questions)

        if ans is None:
            print(Fore.YELLOW + "Login dibatalkan.")
            pause()
            return None

        username = ans["username"].strip()
        password = ans["password"].strip()

        # CEK USER
        if username not in users:
            print(Fore.RED + "✖ Username tidak ditemukan!")
            pause()
            continue

        # CEK PASSWORD
        if users[username]["password"] != password:
            print(Fore.RED + "✖ Password salah!")
            pause()
            continue

        role = users[username]["role"]
        print(Fore.GREEN + f"✔ Login berhasil! Selamat datang, {username} ({role})")
        pause()
        return {"username": username, "role": role}

# ====== MENU ADMIN ======
def admin_menu(username):
    while True:
        clean()
        print(f"=== MENU ADMIN ({username}) ===\n")

        questions = [
            inquirer.List(
                "menu",
                message="Pilih menu:",
                choices=[
                    "Lihat Semua Akun",
                    "Tambah Akun Baru",
                    "Hapus Akun",
                    "Logout"
                ]
            )
        ]

        pilih = inquirer.prompt(questions)["menu"]

        if pilih == "Lihat Semua Akun":
            clean()
            print("=== SEMUA AKUN ===")
            for u, info in users.items():
                print(f"- {u} | role: {info['role']}")
            pause()

        elif pilih == "Tambah Akun Baru":
            register()

        elif pilih == "Hapus Akun":
            clean()
            print("=== HAPUS AKUN ===\n")

            # list semua username kecuali admin utama
            akun_list = [u for u in users.keys() if u != "admin"]

            if not akun_list:
                print("Tidak ada akun untuk dihapus!")
                pause()
                continue

            q = [
                inquirer.List(
                    "pilih",
                    message="Pilih akun yang ingin dihapus:",
                    choices=akun_list
                )
            ]
            target = inquirer.prompt(q)["pilih"]

            confirm = input(f"Yakin hapus akun '{target}'? (y/n): ").lower()
            if confirm == "y":
                del users[target]
                save_users(users)
                print(f"✔ Akun '{target}' dihapus!")
            else:
                print("Dibatalkan.")

            pause()

        elif pilih == "Logout":
            break

# ====== MENU USER ======
def user_menu(username):
    while True:
        clean()
        print(f"=== MENU USER ({username}) ===\n")

        questions = [
            inquirer.List(
                "menu",
                message="Pilih menu:",
                choices=[
                    "Lihat Profil",
                    "Ubah Password",
                    "Logout"
                ]
            )
        ]

        pilih = inquirer.prompt(questions)["menu"]

        if pilih == "Lihat Profil":
            clean()
            print("=== PROFIL ANDA ===")
            print(f"Username : {username}")
            print(f"Role     : {users[username]['role']}")
            pause()

        elif pilih == "Ubah Password":
            clean()
            print("=== UBAH PASSWORD ===\n")

            q = [
                inquirer.Password("pw", message="Password baru")
            ]
            new_pw = inquirer.prompt(q)["pw"]

            if new_pw:
                users[username]["password"] = new_pw
                save_users(users)
                print("✔ Password berhasil diubah!")
            else:
                print("✖ Password tidak boleh kosong!")
            pause()

        elif pilih == "Logout":
            break

# ====== MAIN MENU ======
def main_menu():
    while True:
        clean()
        print("=== SISTEM LOGIN & REGISTER ===\n")

        questions = [
            inquirer.List(
                "menu",
                message="Pilih menu:",
                choices=[
                    "Login",
                    "Register (max 5x)",
                    "Keluar"
                ]
            )
        ]

        pilih = inquirer.prompt(questions)["menu"]

        if pilih == "Login":
            login()
        elif pilih == "Register (max 5x)":
            register()
        else:
            print("Program selesai.")
            break

if __name__ == "__main__":
    main_menu()
