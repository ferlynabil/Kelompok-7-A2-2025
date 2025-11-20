import inquirer
from jadwal_tambah import tambah_jadwal
from jadwal_ubah import ubah_jadwal
from jadwal_hapus import hapus_jadwal
from jadwal_lihat import lihat_jadwal
from akun_lihat import lihat_akun
from login import load_users, login, register   # ambil dari login.py

users = load_users()   # data akun dari akun.json

def main():
    while True:
        print("=== SISTEM LOGIN & REGISTER ===")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            # panggil login() dari login.py
            username = input("Username: ")
            password = input("Password: ")

            if username in users and users[username]["password"] == password:
                role = users[username]["role"]
                print(f"\nLogin berhasil! Selamat datang, {username} ({role})")

                # === Filter role admin ===
                if role == "admin":
                    while True:
                        pertanyaan_menu = [
                            inquirer.List(
                                'pilihan',
                                message="Menu Admin - pilih perintah",
                                choices=[
                                    '1. Tambah Jadwal Penerbangan',
                                    '2. Ubah Jadwal Penerbangan',
                                    '3. Hapus Jadwal Penerbangan',
                                    '4. Lihat Jadwal Penerbangan',
                                    '5. Melihat daftar akun user yang sudah registrasi',
                                    '6. Melihat daftar pesanan user',
                                    '7. Konfirmasi daftar pesanan user',
                                    '8. Total Pendapatan',
                                    '9. Logout'
                                ]
                            )
                        ]
                        jawaban = inquirer.prompt(pertanyaan_menu)

                        if jawaban['pilihan'] == '1. Tambah Jadwal Penerbangan':
                            tambah_jadwal()
                        elif jawaban['pilihan'] == '2. Ubah Jadwal Penerbangan':
                            ubah_jadwal()
                        elif jawaban['pilihan'] == '3. Hapus Jadwal Penerbangan':
                            hapus_jadwal()
                        elif jawaban['pilihan'] == '4. Lihat Jadwal Penerbangan':
                            lihat_jadwal()
                        elif jawaban['pilihan'] == '5. Melihat daftar akun user yang sudah registrasi':
                            lihat_akun()
                        elif jawaban['pilihan'] == '9. Logout':
                            print(" Logout berhasil.")
                            break

                # === Filter role user ===
                elif role == "user":
                    while True:
                        pertanyaan_menu = [
                            inquirer.List(
                                'pilihan',
                                message="Menu User - pilih perintah",
                                choices=[
                                    '1. Lihat Jadwal Penerbangan',
                                    '2. Pesan Tiket (belum dibuat)',
                                    '9. Logout'
                                ]
                            )
                        ]
                        jawaban = inquirer.prompt(pertanyaan_menu)

                        if jawaban['pilihan'] == '1. Lihat Jadwal Penerbangan':
                            lihat_jadwal()
                        elif jawaban['pilihan'] == '2. Pesan Tiket (belum dibuat)':
                            print("Fitur pesan tiket belum tersedia.")
                        elif jawaban['pilihan'] == '9. Logout':
                            print(" Logout berhasil.")
                            break

            else:
                print("\nLogin gagal! Username atau password salah.")

        elif pilih == "2":
            register()

        elif pilih == "3":
            print("Terima kasih! Program selesai.")
            break

        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
