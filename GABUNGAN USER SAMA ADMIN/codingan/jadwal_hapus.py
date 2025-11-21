import inquirer
import json

def hapus_jadwal():
    with open("jadwal.json", "r") as f:
        data_jadwal = json.load(f)

    if not data_jadwal:
        print(" Belum ada jadwal penerbangan untuk dihapus.")
        return

    pilihan_jadwal = [
        f"{j['kode']} | {j['asal']} -> {j['tujuan']} | {j['tanggal']} {j['jam']} | Rp{j['harga']}"
        for j in data_jadwal
    ]

    pilih = inquirer.prompt([
        inquirer.List('jadwal', message="Pilih jadwal yang ingin dihapus", choices=pilihan_jadwal)
    ])['jadwal']

    index = pilihan_jadwal.index(pilih)
    jadwal_dihapus = data_jadwal.pop(index)

    with open("jadwal.json", "w") as f:
        json.dump(data_jadwal, f, indent=4)

    print(f"\n Jadwal penerbangan {jadwal_dihapus['kode']} berhasil dihapus!")
