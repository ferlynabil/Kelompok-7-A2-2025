from auth import login, register_user
from flights import add_flight, list_flights, update_flight, delete_flight, find_available
from users import print_users
from bookings import create_booking, pay_transaction
from transactions import list_transactions, summary, print_transactions
from visualize import plot_tickets_per_flight, plot_revenue_overview
from utils import clear_screen

def admin_menu(user):
    while True:
        clear_screen()
        print('\n== Admin Menu ==')
        print('1. Tambah flight')
        print('2. Update flight')
        print('3. Hapus flight')
        print('4. Lihat users')
        print('5. Lihat transaksi')
        print('6. Laporan singkat')
        print('7. Visualisasi')
        print('0. Logout')
        c = input('Pilihan: ').strip()
        if c=='1':
            add_flight()
        elif c=='2':
            update_flight()
        elif c=='3':
            delete_flight()
        elif c=='4':
            print_users()
        elif c=='5':
            print_transactions()
        elif c=='6':
            clear_screen()
            print(summary())
            input('\nTekan Enter untuk kembali...')
        elif c=='7':
            
            plot_tickets_per_flight()
            plot_revenue_overview()
            input('\nTekan Enter untuk kembali...')
        elif c=='0':
            break
        else:
            print('Pilihan tidak valid')
            input('\nTekan Enter untuk kembali...')

def user_menu(user):
    while True:
        clear_screen()
        print('\n== User Menu ==')
        print('1. Cari penerbangan')
        print('2. Pesan tiket')
        print('3. Bayar transaksi (id)')
        print('4. Lihat tiket saya')
        print('0. Logout')
        c = input('Pilihan: ').strip()
        if c=='1':
            asal = input('Asal: ')
            tujuan = input('Tujuan: ')
            tanggal = input('Tanggal (YYYY-MM-DD): ')
            flights = list_flights(lambda f: f['asal'].lower()==asal.lower() and f['tujuan'].lower()==tujuan.lower() and f['datetime'].startswith(tanggal))
            clear_screen()
            print(f'\n== Hasil Pencarian: {asal} -> {tujuan} tanggal {tanggal} ==')
            for f in flights:
                print(f"ID:{f['id']} | {f['asal']} -> {f['tujuan']} | {f['datetime']} | Kelas:{f['kelas']} | Harga:{f['harga']} | Tersisa:{f['kapasitas']-f.get('terjual',0)}")
            input('\nTekan Enter untuk kembali...')
        elif c=='2':
            try:
                fid = int(input('Flight ID: '))
            except ValueError:
                print('ID harus angka.')
                input('\nTekan Enter untuk kembali...')
                continue
            try:
                n = int(input('Jumlah penumpang: '))
            except ValueError:
                print('Jumlah harus angka.')
                input('\nTekan Enter untuk kembali...')
                continue
            passengers = []
            bags = []
            for i in range(n):
                print(f'-- Penumpang {i+1} --')
                name = input('Nama: ')
                passengers.append({'name': name})
                try:
                    w = float(input('Berat bagasi (kg): '))
                except ValueError:
                    w = 0.0
                bags.append(w)
            paid = input('Bayar sekarang? (y/n): ').lower()=='y'
            try:
                tx = create_booking(user, fid, passengers, bags, paid=paid)
                print('Transaksi dibuat:', tx)
            except Exception as e:
                print('Gagal:', e)
            input('\nTekan Enter untuk kembali...')
        elif c=='3':
            try:
                txid = int(input('ID transaksi: '))
            except ValueError:
                print('ID harus angka.')
                input('\nTekan Enter untuk kembali...')
                continue
            try:
                pay_transaction(txid)
                print('Sudah dibayar jika ditemukan')
            except Exception as e:
                print('Gagal bayar:', e)
            input('\nTekan Enter untuk kembali...')
        elif c=='4':
            txs = list_transactions()
            mytx = [t for t in txs if t['user_id']==user['id']]
            clear_screen()
            print('\n== Tiket Saya ==')
            for t in mytx:
                print(t)
            input('\nTekan Enter untuk kembali...')
        elif c=='0':
            break
        else:
            print('Pilihan salah')
            input('\nTekan Enter untuk kembali...')

def main():
    while True:
        clear_screen()
        print('=== Aplikasi Pemesanan Tiket (CLI) ===')
        print('\n1. Login\n2. Register\n0. Exit')
        c = input('Pilihan: ').strip()
        if c=='1':
            u = login()
            if u:
                if u['role']=='admin':
                    admin_menu(u)
                else:
                    user_menu(u)
        elif c=='2':
            register_user()
        elif c=='0':
            clear_screen()
            print('Bye')
            break
        else:
            print('Pilih 1/2/0')
            input('\nTekan Enter untuk kembali...')

if __name__=='__main__':
    main()
