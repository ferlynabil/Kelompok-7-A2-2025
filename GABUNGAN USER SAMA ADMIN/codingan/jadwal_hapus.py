import inquirer
import json
import os

def hapus_jadwal():
    # Load file jadwal.json dengan fallback
    try:
        if os.path.exists("jadwal.json"):
            with open("jadwal.json", "r") as f:
                data_jadwal = json.load(f)
        else:
            data_jadwal = []
    except (FileNotFoundError, json.JSONDecodeError):
        data_jadwal = []

    if not data_jadwal:
        print("❌ Belum ada jadwal penerbangan untuk dihapus.")
        return

    # Buat daftar pilihan jadwal + opsi keluar
    pilihan_jadwal = [
        f"{j['kode']} | {j['asal']} → {j['tujuan']} | {j['tanggal']} {j['jam']} | Rp{j['harga']}"
        for j in data_jadwal
    ]
    pilihan_jadwal.append("❌ Batal / Keluar")

    pilih = inquirer.prompt([
        inquirer.List('jadwal', message="Pilih jadwal yang ingin dihapus", choices=pilihan_jadwal)
    ])

    if pilih is None or pilih['jadwal'] == "❌ Batal / Keluar":
        print("\nℹ Penghapusan dibatalkan, tidak ada jadwal yang dihapus.")
        return

    index = pilihan_jadwal.index(pilih['jadwal'])
    jadwal_dihapus = data_jadwal[index]

    # Konfirmasi sebelum hapus
    konfirmasi = inquirer.prompt([
        inquirer.List('konfirmasi', message=f"Yakin hapus jadwal {jadwal_dihapus['kode']}?", choices=["Ya", "Tidak"])
    ])

    if konfirmasi is None or konfirmasi['konfirmasi'] == "Tidak":
        print("\nℹ Penghapusan dibatalkan, jadwal tetap tersimpan.")
        return

    # Hapus jadwal
    data_jadwal.pop(index)
    try:
        with open("jadwal.json", "w") as f:
            json.dump(data_jadwal, f, indent=4)
    except Exception as e:
        print(f"✖ Gagal menyimpan perubahan jadwal: {e}")
        return

    # Update tiket.json: tandai tiket terkait sebagai cancelled
    try:
        if os.path.exists("tiket.json"):
            with open("tiket.json", "r") as f:
                tiket = json.load(f)
        else:
            tiket = []
    except (FileNotFoundError, json.JSONDecodeError):
        tiket = []

    affected = 0
    for t in tiket:
        if t.get("kode") == jadwal_dihapus["kode"] and t.get("status") != "cancelled":
            t["status"] = "cancelled"
            t["alasan"] = "Jadwal dibatalkan oleh admin"
            affected += 1

    try:
        with open("tiket.json", "w") as f:
            json.dump(tiket, f, indent=4)
    except Exception as e:
        print(f"✖ Jadwal terhapus, tapi gagal memperbarui tiket: {e}")
        return

    # Feedback detail
    harga_rupiah = "Rp {:,}".format(jadwal_dihapus['harga']).replace(",", ".")
    nama_maskapai = jadwal_dihapus.get("nama_maskapai") or jadwal_dihapus.get("nama_pesawat","-")

    print("\n✅ Jadwal penerbangan berhasil dihapus!")
    print(f"Kode: {jadwal_dihapus['kode']}")
    print(f"Asal: {jadwal_dihapus['asal']} → Tujuan: {jadwal_dihapus['tujuan']}")
    print(f"Tanggal: {jadwal_dihapus['tanggal']} | Jam: {jadwal_dihapus['jam']}")
    print(f"Harga: {harga_rupiah}")
    print(f"Maskapai: {nama_maskapai} ({jadwal_dihapus.get('jenis_pesawat','-')})")
    print(f"ℹ {affected} tiket terkait ditandai CANCELLED.")
