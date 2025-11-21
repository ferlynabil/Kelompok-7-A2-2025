import os
import json
import inquirer
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

def pause():
    input("\nTekan Enter...")

# ====== LOGIN ======
def login():
    clean()
    print("=== LOGIN ===\n")

    questions = [
        inquirer.Text("username", message="Masukkan username"),
        inquirer.Password("password", message="Masukkan password")
    ]

    ans = inquirer.prompt(questions)
    u = ans["username"]
    p = ans["password"]

    if u in users and users[u]["password"] == p:
        print(f"\n✔ Login berhasil! Selamat datang, {u} ({users[u]['role']})")
        pause()
        if users[u]["role"] == "admin":
            admin_menu(u)
        else:
            user_menu(u)
    else:
        print("\n✖ Username atau password salah!")
        pause()

# ====== REGISTER ======
def register():
    clean()
    print("=== REGISTER (5 percobaan) ===\n")

    attempt = 0

    while attempt < 5:
        questions = [
            inquirer.Text("username", message="Username baru"),
            inquirer.Password("password", message="Password")
        ]
        ans = inquirer.prompt(questions)

        u = ans["username"]
        p = ans["password"]

        if u in users:
            print("✖ Username sudah ada!")
            attempt += 1
            continue

        if not u or not p:
            print("✖ Username/password tidak boleh kosong!")
            attempt += 1
            continue

        users[u] = {"password": p, "role": "user"}
        save_users(users)
        print(f"\n✔ Akun '{u}' berhasil didaftarkan!")
        break

    if attempt == 5:
        print("\n⚠ Batas percobaan habis!")
    pause()

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
