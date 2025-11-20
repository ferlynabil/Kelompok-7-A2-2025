from dp import read
from utils import clear_screen

def list_transactions():
    return read('transactions')

def summary():
    txs = read('transactions')
    sold = sum(len(t['passengers']) for t in txs if t['status']=='paid')
    revenue = sum(t['subtotal'] for t in txs if t['status']=='paid')
    pending = len([t for t in txs if t['status']=='pending'])
    canceled = len([t for t in txs if t.get('status')=='cancel'])
    return {'sold': sold, 'revenue': revenue, 'pending': pending, 'canceled': canceled}

def print_transactions():
    clear_screen()
    txs = list_transactions()
    print('\n== Daftar Transaksi ==')
    for t in txs:
        print(t)
    input('\nTekan Enter untuk kembali...')
