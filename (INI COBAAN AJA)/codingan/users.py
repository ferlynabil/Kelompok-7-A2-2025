from dp import read
from utils import clear_screen

def list_users():
    return read('users')

def print_users():
    clear_screen()
    users = list_users()
    print('\n== Daftar Users ==')
    for u in users:
        print(f"ID:{u['id']} - {u['name']} ({u['email']}) - role:{u.get('role','user')}")
    input('\nTekan Enter untuk kembali...')
