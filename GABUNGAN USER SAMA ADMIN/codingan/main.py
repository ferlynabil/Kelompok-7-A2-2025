import os
from colorama import init, Fore
from user_menu import (
    lihat_jadwal,
    pesan_tiket,
    timbang_bagasi,
    bayar_tiket,
    lihat_tiket_user
)

init(autoreset=True)

def cls():
    os.system("cls" if os.name == "nt" else "clear")

def menu_user():
    while True:
        cls()
        print(Fore.CYAN + "===== MENU USER =====")
        print("1. Lihat Jadwal Penerbangan")
        print("2. Pesan Tiket")
        print("3. Menimbang Berat Bagasi")
        print("4. Melakukan Pembayaran")
        print("5. Melihat Tiket yang Sudah Dibeli")
        print("6. Logout")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            lihat_jadwal()
            input("\nTekan Enter untuk lanjut...")
        elif pilihan == "2":
            pesan_tiket()
            input("\nTekan Enter untuk lanjut...")
        elif pilihan == "3":
            timbang_bagasi()
            input("\nTekan Enter untuk lanjut...")
        elif pilihan == "4":
            bayar_tiket()
            input("\nTekan Enter untuk lanjut...")
        elif pilihan == "5":
            lihat_tiket_user()
            input("\nTekan Enter untuk lanjut...")
        elif pilihan == "6":
            print(Fore.GREEN + "Logout berhasil...")
            break
        else:
            print(Fore.RED + "Pilihan tidak valid!")
            input("\nTekan Enter untuk lanjut...")

if __name__ == "__main__":
    menu_user()
