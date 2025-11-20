from dp import read, write
from utils import validate_email, clear_screen
import getpass

def register_user():
    clear_screen()
    users = read('users')
    print('\n== Register User ==')
    email = input('Email: ').strip()
    if not validate_email(email):
        print('Email tidak valid.')
        input('\nTekan Enter untuk kembali...')
        return
    if any(u['email'] == email for u in users):
        print('Email sudah terdaftar.')
        input('\nTekan Enter untuk kembali...')
        return
    name = input('Nama: ').strip()
    password = getpass.getpass('Password (min 6): ')
    if len(password) < 6:
        print('Password terlalu pendek.')
        input('\nTekan Enter untuk kembali...')
        return
    user = {'id': len(users)+1, 'email': email, 'name': name, 'password': password, 'role': 'user'}
    users.append(user)
    write('users', users)
    print('Registrasi berhasil.')
    input('\nTekan Enter untuk kembali...')

def login():
    clear_screen()
    users = read('users')
    print('\n== Login ==')
    email = input('Email: ').strip()
    password = getpass.getpass('Password: ')
    for u in users:
        if u['email'] == email and u['password'] == password:
            print(f"Selamat datang, {u['name']} ({u['role']})")
            input('\nTekan Enter untuk melanjutkan...')
            return u
    # default admin account (jika belum ada)
    if email == 'admin@admin' and password == 'admin':
        print("Selamat datang, Admin")
        input('\nTekan Enter untuk melanjutkan...')
        return {'id': 0, 'email': email, 'name': 'Admin', 'role': 'admin'}
    print('Login gagal.')
    input('\nTekan Enter untuk kembali...')
    return None
