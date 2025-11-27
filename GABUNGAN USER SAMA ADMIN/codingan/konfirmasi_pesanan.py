import json
import os
import inquirer
from colorama import Fore

def konfirmasi_pesanan():
    # Load tiket.json dengan fallback
    try:
        if os.path.exists("tiket.json"):
            with open("tiket.json", "r") as f:
                tiket = json.load(f)
        else:
            tiket = []
    except (FileNotFoundError, json.JSONDecodeError):
        tiket = []

    # Filter tiket pending
    pending_tiket = [t for t in tiket if t.get("status") == "pending"]

    if not pending_tiket:
        print(Fore.YELLOW + "⚠ Tidak ada tiket pending untuk dikonfirmasi.")
        return

    # Buat daftar pilihan tiket pending
    pilihan = [
        f"{t['user']} | {t['kode']} | Kursi {t['kursi']} | Status: {t['status']}"
        for t in pending_tiket
    ]
    pilihan.append("❌ Batal / Keluar")

    pilih = inquirer.prompt([
        inquirer.List("tiket", message="Pilih tiket pending untuk dikonfirmasi", choices=pilihan)
    ])

    if pilih is None or pilih["tiket"] == "❌ Batal / Keluar":
        print(Fore.YELLOW + "\nℹ Konfirmasi dibatalkan.")
        return

    index = pilihan.index(pilih["tiket"])
    tiket_dipilih = pending_tiket[index]

    # Konfirmasi atau tolak tiket
    aksi = inquirer.prompt([
        inquirer.List(
            "aksi",
            message=f"Apa yang ingin dilakukan untuk tiket {tiket_dipilih['kode']} kursi {tiket_dipilih['kursi']}?",
            choices=["✅ Konfirmasi", "❌ Tolak", "Batal"]
        )
    ])

    if aksi is None or aksi["aksi"] == "Batal":
        print(Fore.YELLOW + "\nℹ Tidak ada aksi dilakukan.")
        return

    if aksi["aksi"] == "✅ Konfirmasi":
        tiket_dipilih["status"] = "confirmed"
        print(Fore.GREEN + f"\n✔ Tiket {tiket_dipilih['kode']} kursi {tiket_dipilih['kursi']} dikonfirmasi!")
    elif aksi["aksi"] == "❌ Tolak":
        tiket_dipilih["status"] = "cancelled"
        tiket_dipilih["alasan"] = "Ditolak oleh admin"
        print(Fore.RED + f"\n✖ Tiket {tiket_dipilih['kode']} kursi {tiket_dipilih['kursi']} ditolak.")

    # Simpan kembali tiket.json
    try:
        with open("tiket.json", "w") as f:
            json.dump(tiket, f, indent=4)
    except Exception as e:
        print(Fore.RED + f"✖ Gagal menyimpan perubahan tiket: {e}")
