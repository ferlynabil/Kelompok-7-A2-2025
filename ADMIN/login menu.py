import os
import json


def load_users():
    try:
        with open("akun.json", "r") as f:  
            return json.load(f)
    except FileNotFoundError:
    
        return {
            "user": {"password": "999", "role": "user"},
            "admin": {"password": "242637", "role": "admin"}
        }

def save_users(users):
    with open("akun.json", "w") as f:      
        json.dump(users, f, indent=4)


users = load_users()

def clean():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nTekan Enter untuk melanjutkan...")

def login():
    clean()
    print("=== LOGIN ===")
    username = input("Username: ")
    password = input("Password: ")

    if username in users and users[username]["password"] == password:
        print(f"\nLogin berhasil! Selamat datang, {username} ({users[username]['role']})")
    else:
        print("\nLogin gagal! Username atau password salah.")
    pause()

def register():
    clean()
    print("=== REGISTER ===")
    attempt = 0

    while attempt < 5:
        username = input("Masukkan username baru: ")
        if username in users:
            print("Username sudah terdaftar!")
            attempt += 1
            continue

        password = input("Masukkan password: ")
        role = "user"

        if username and password:
            users[username] = {"password": password, "role": role}
            save_users(users) 
            print(f"Akun '{username}' berhasil didaftarkan!")
            break
        else:
            print("Username atau password tidak boleh kosong!")
            attempt += 1

        if attempt == 5:
            print("\n Batas percobaan register telah habis!")

    pause()

def main_menu():
    while True:
        clean()
        print("=== SISTEM LOGIN & REGISTER ===")
        print("1. Login")
        print("2. Register (Max 5x percobaan)")
        print("3. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            login()
        elif pilih == "2":
            register()
        elif pilih == "3":
            print("Terima kasih! Program selesai.")
            break
        else:
            print("Pilihan tidak valid!")
            pause()

if __name__ == "__main__":
    main_menu()
