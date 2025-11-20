import inquirer
import json
import os

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

    print("\n✅ Jadwal penerbangan berhasil ditambahkan!")
