import inquirer
import json

def ubah_jadwal():
    with open("jadwal.json", "r") as f:
        data_jadwal = json.load(f)

    if not data_jadwal:
        print(" Belum ada jadwal penerbangan untuk diubah.")
        return

    pilihan_jadwal = [
        f"{j['kode']} | {j['asal']} -> {j['tujuan']} | {j['tanggal']} {j['jam']} | Rp{j['harga']}"
        for j in data_jadwal
    ]

    pilih = inquirer.prompt([
        inquirer.List('jadwal', message="Pilih jadwal yang ingin diubah", choices=pilihan_jadwal)
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
