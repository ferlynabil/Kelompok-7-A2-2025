import inquirer
from jadwal_tambah import tambah_jadwal
from jadwal_ubah import ubah_jadwal
from jadwal_hapus import hapus_jadwal
from jadwal_lihat import lihat_jadwal
from akun_lihat import lihat_akun
from login import load_users   # ✅ ambil fungsi dari login.py

users = load_users()   # ambil data akun dari login.py

def main():
    # === LOGIN dulu ===
    print("=== SISTEM LOGIN ===")
    username = input("Username: ")
    password = input("Password: ")

    if username in users and users[username]["password"] == password:
        role = users[username]["role"]
        print(f"\nLogin berhasil! Selamat datang, {username} ({role})")

        # === Kalau role admin, masuk menu admin ===
        if role == "admin":
            lanjut = False
            while not lanjut:
                pertanyaan_menu = [
                    inquirer.List(
                        'pilihan',
                        message="Pilih perintah anda",
                        choices=[
                            '1. Tambah Jadwal Penerbangan',
                            '2. Ubah Jadwal Penerbangan',
                            '3. Hapus Jadwal Penerbangan',
                            '4. Lihat Jadwal Penerbangan',
                            '5. Melihat daftar akun user yang sudah registrasi',
                            '6. Melihat daftar pesanan user',
                            '7. Melihat dan ubah semua daftar transaksi tiket',
                            '8. Melihat jumlah tiket terjual dan total pendapatan',
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
                    print("✅ Logout berhasil.")
                    break

        # === Kalau role user, bisa diarahkan ke menu user sederhana ===
        else:
            print("Menu user belum tersedia. Silakan hubungi admin.")
    else:
        print("\nLogin gagal! Username atau password salah.")

if __name__ == "__main__":
    main()
