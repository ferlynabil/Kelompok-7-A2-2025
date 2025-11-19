import matplotlib.pyplot as plt
from flights import list_flights
from transactions import list_transactions
from utils import clear_screen

def plot_tickets_per_flight():
    flights = list_flights()
    names = [f"{f['asal']}-{f['tujuan']} ({f['datetime']})" for f in flights]
    sold = [f.get('terjual',0) for f in flights]
    if not flights:
        print('Belum ada data flight.')
        input('\nTekan Enter untuk kembali...')
        return
    plt.figure()
    plt.bar(names, sold)
    plt.xticks(rotation=45, ha='right')
    plt.title('Tiket terjual per penerbangan')
    plt.tight_layout()
    plt.show()

def plot_revenue_overview():
    txs = list_transactions()
    labels = ['paid','pending','cancel']
    vals = [sum(t['subtotal'] for t in txs if t['status']==lab) for lab in labels]
    plt.figure()
    plt.pie(vals, labels=labels, autopct='%1.1f%%')
    plt.title('Perbandingan revenue berdasarkan status')
    plt.show()
