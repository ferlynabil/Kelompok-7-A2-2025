import inquirer
import json
import os
from prettytable import PrettyTable   

# === Fungsi untuk tiap menu ===
def tambah_jadwal():
    jadwal_baru = inquirer.prompt([
        inquirer.Text('kode', message="Masukkan Kode Penerbangan"),
        inquirer.Text('asal', message="Masukkan Kota Asal"),
        inquirer.Text('tujuan', message="Masukkan Kota Tujuan"),
        inquirer.Text('tanggal', message="Masukkan Tanggal (DD-MM-YYYY)"),
        inquirer.Text('jam', message="Masukkan Jam (HH:MM)"),
        inquirer.Text('harga', message='Masukkan Harga Tiket'),
    ])

    if os.path.exists("jadwal.json"):
        with open("jadwal.json", "r") as f:
            data_jadwal = json.load(f)
    else:
        data_jadwal = []

    data_jadwal.append(jadwal_baru)

    with open("jadwal.json", "w") as f:
        json.dump(data_jadwal, f, indent=4)

    print("\n Jadwal penerbangan berhasil ditambahkan!")


def ubah_jadwal():
    with open("jadwal.json", "r") as f:
        data_jadwal = json.load(f)

    if not data_jadwal:
        print(" Belum ada jadwal penerbangan untuk diubah.")
    else:
        pilihan_jadwal = [
            f"{j['kode']} | {j['asal']} -> {j['tujuan']} | {j['tanggal']} {j['jam']} | Rp{j['harga']}"
            for j in data_jadwal
        ]

        pilih = inquirer.prompt([
            inquirer.List(
                'jadwal',
                message="Pilih jadwal yang ingin diubah",
                choices=pilihan_jadwal
            )
        ])['jadwal']

        index = pilihan_jadwal.index(pilih)
        jadwal_ditemukan = data_jadwal[index]

        print(f"\nJadwal lama: {jadwal_ditemukan}")

        perubahan = inquirer.prompt([
            inquirer.Text('asal', message=f"Ubah Kota Asal (lama: {jadwal_ditemukan['asal']})"),
            inquirer.Text('tujuan', message=f"Ubah Kota Tujuan (lama: {jadwal_ditemukan['tujuan']})"),
            inquirer.Text('tanggal', message=f"Ubah Tanggal (lama: {jadwal_ditemukan['tanggal']})"),
            inquirer.Text('jam', message=f"Ubah Jam (lama: {jadwal_ditemukan['jam']})"),
            inquirer.Text('harga', message=f"Ubah Harga Tiket (lama: {jadwal_ditemukan['harga']})")
        ])

        for key in ['asal', 'tujuan', 'tanggal', 'jam', 'harga']:
            if perubahan[key].strip():
                jadwal_ditemukan[key] = perubahan[key]

        with open("jadwal.json", "w") as f:
            json.dump(data_jadwal, f, indent=4)

        print("\n Jadwal penerbangan berhasil diubah!")


def hapus_jadwal():
    with open("jadwal.json", "r") as f:
        data_jadwal = json.load(f)

    if not data_jadwal:
        print(" Belum ada jadwal penerbangan untuk dihapus.")
    else:
        pilihan_jadwal = [
            f"{j['kode']} | {j['asal']} -> {j['tujuan']} | {j['tanggal']} {j['jam']} | Rp{j['harga']}"
            for j in data_jadwal
        ]

        pilih = inquirer.prompt([
            inquirer.List(
                'jadwal',
                message="Pilih jadwal yang ingin dihapus",
                choices=pilihan_jadwal
            )
        ])['jadwal']

        index = pilihan_jadwal.index(pilih)
        jadwal_dihapus = data_jadwal.pop(index)

        with open("jadwal.json", "w") as f:
            json.dump(data_jadwal, f, indent=4)

        print(f"\n Jadwal penerbangan {jadwal_dihapus['kode']} berhasil dihapus!")


def lihat_jadwal():
    with open("jadwal.json", "r") as f:
        data_jadwal = json.load(f)

    if not data_jadwal:
        print(" Belum ada jadwal penerbangan.")
    else:
        table = PrettyTable()
        table.field_names = ["Kode", "Asal", "Tujuan", "Tanggal", "Jam", "Harga"]
        for j in data_jadwal:
            table.add_row([j['kode'], j['asal'], j['tujuan'], j['tanggal'], j['jam'], j['harga']])
        print("\n Daftar Jadwal Penerbangan:")
        print(table)


def lihat_akun():
    if os.path.exists("akun.json"):
        with open("akun.json", "r") as f:
            data_akun = json.load(f)
    else:
        data_akun = {}

    if not data_akun:
        print(" Belum ada akun yang terdaftar.")
    else:
        table = PrettyTable()
        table.field_names = ["Username", "Role"]
        for username, info in data_akun.items():
            table.add_row([username, info['role']])
        print("\n Daftar Akun Terdaftar:")
        print(table)


# === Main Program ===
def main():
    inputadmin = inquirer.prompt([
        inquirer.Text('username', message="Masukkan Nama Akun")
    ])['username']

    lanjut = False

    while not lanjut:
        if inputadmin == 'admin':
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
                lanjut = False
            elif jawaban['pilihan'] == '2. Ubah Jadwal Penerbangan':
                ubah_jadwal()
                lanjut = False
            elif jawaban['pilihan'] == '3. Hapus Jadwal Penerbangan':
                hapus_jadwal()
            elif jawaban['pilihan'] == '4. Lihat Jadwal Penerbangan':
                lihat_jadwal()
            elif jawaban['pilihan'] == '5. Melihat daftar akun user yang sudah registrasi':
                lihat_akun()


if __name__ == "__main__":
    main()
