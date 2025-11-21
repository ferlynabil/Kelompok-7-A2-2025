import json
import matplotlib.pyplot as plt

def grafik_tiket():
    """
    Menampilkan grafik jumlah tiket berdasarkan tujuan.
    Dipanggil dari menu 'Lihat tiket yang sudah dibeli'.
    """
    try:
        with open("data_tiket_user.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print("Gagal membaca data_tiket_user.json:", e)
        return

    if not data:
        print("Belum ada tiket, grafik tidak bisa ditampilkan.")
        return

    tujuan_count = {}
    for item in data:
        tujuan = item["jadwal"]["tujuan"]
        tujuan_count[tujuan] = tujuan_count.get(tujuan, 0) + 1

    plt.figure(figsize=(8,5))
    plt.bar(list(tujuan_count.keys()), list(tujuan_count.values()))
    plt.title("Jumlah Tiket Berdasarkan Tujuan")
    plt.xlabel("Tujuan")
    plt.ylabel("Jumlah Tiket")
    plt.tight_layout()
    plt.show()
