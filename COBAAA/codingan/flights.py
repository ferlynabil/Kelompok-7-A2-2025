from dp import read, write
from utils import parse_datetime, clear_screen

def list_flights(filter_func=None):
    flights = read('flights')
    if filter_func:
        flights = [f for f in flights if filter_func(f)]
    return flights

def add_flight():
    clear_screen()
    flights = read('flights')
    print('\n== Tambah Penerbangan ==')
    asal = input('Asal: ').strip()
    tujuan = input('Tujuan: ').strip()
    dt = input('Tanggal & Jam (YYYY-MM-DD HH:MM): ').strip()
    try:
        dt_obj = parse_datetime(dt)
    except ValueError as e:
        print(e)
        input('\nTekan Enter untuk kembali...')
        return
    try:
        durasi_menit = int(input('Durasi (menit): '))
    except ValueError:
        print('Durasi harus angka.')
        input('\nTekan Enter untuk kembali...')
        return
    jenis_pesawat = input('Jenis Pesawat: ')
    kelas = input('Kelas (Ekonomi/Bisnis): ')
    try:
        harga = float(input('Harga: '))
    except ValueError:
        print('Harga harus angka.')
        input('\nTekan Enter untuk kembali...')
        return
    try:
        kapasitas = int(input('Kapasitas kursi: '))
    except ValueError:
        print('Kapasitas harus angka.')
        input('\nTekan Enter untuk kembali...')
        return
    flight = {
        'id': len(flights)+1,
        'asal': asal,
        'tujuan': tujuan,
        'datetime': dt_obj.strftime('%Y-%m-%d %H:%M'),
        'durasi_menit': durasi_menit,
        'jenis_pesawat': jenis_pesawat,
        'kelas': kelas,
        'harga': harga,
        'kapasitas': kapasitas,
        'terjual': 0
    }
    flights.append(flight)
    write('flights', flights)
    print('Penerbangan ditambahkan.')
    input('\nTekan Enter untuk kembali...')

def update_flight():
    clear_screen()
    flights = read('flights')
    try:
        fid = int(input('ID flight yang mau diubah: '))
    except ValueError:
        print('ID harus angka.')
        input('\nTekan Enter untuk kembali...')
        return
    match = next((f for f in flights if f['id'] == fid), None)
    if not match:
        print('Flight tidak ditemukan')
        input('\nTekan Enter untuk kembali...')
        return
    print('Kosongkan input untuk tidak mengubah')
    asal = input(f"Asal [{match['asal']}]: ").strip() or match['asal']
    tujuan = input(f"Tujuan [{match['tujuan']}]: ").strip() or match['tujuan']
    dt = input(f"Tanggal & Jam [{match['datetime']}]: ").strip() or match['datetime']
    try:
        _ = parse_datetime(dt)
    except ValueError as e:
        print(e)
        input('\nTekan Enter untuk kembali...')
        return
    durasi = input(f"Durasi (menit) [{match['durasi_menit']}]: ").strip() or match['durasi_menit']
    jenis = input(f"Jenis Pesawat [{match['jenis_pesawat']}]: ").strip() or match['jenis_pesawat']
    kelas = input(f"Kelas [{match['kelas']}]: ").strip() or match['kelas']
    harga = input(f"Harga [{match['harga']}]: ").strip() or match['harga']
    kapasitas = input(f"Kapasitas [{match['kapasitas']}]: ").strip() or match['kapasitas']
    try:
        match.update({
            'asal': asal,
            'tujuan': tujuan,
            'datetime': dt,
            'durasi_menit': int(durasi),
            'jenis_pesawat': jenis,
            'kelas': kelas,
            'harga': float(harga),
            'kapasitas': int(kapasitas)
        })
    except ValueError:
        print('Tipe data salah pada update.')
        input('\nTekan Enter untuk kembali...')
        return
    write('flights', flights)
    print('Penerbangan diperbarui')
    input('\nTekan Enter untuk kembali...')

def delete_flight():
    clear_screen()
    flights = read('flights')
    try:
        fid = int(input('ID flight yang dihapus: '))
    except ValueError:
        print('ID harus angka.')
        input('\nTekan Enter untuk kembali...')
        return
    flights = [f for f in flights if f['id'] != fid]
    write('flights', flights)
    print('Dihapus (jika ada)')
    input('\nTekan Enter untuk kembali...')

def find_available(asal, tujuan, tanggal_str, seats_needed=1):
    flights = read('flights')
    def cond(f):
        return (f['asal'].lower() == asal.lower() and f['tujuan'].lower() == tujuan.lower() and
                f['datetime'].startswith(tanggal_str) and (f['kapasitas'] - f.get('terjual',0)) >= seats_needed)
    return [f for f in flights if cond(f)]
