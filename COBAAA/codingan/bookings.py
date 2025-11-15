from dp import read, write
from flights import find_available
from utils import clear_screen

def create_booking(user, flight_id, passengers, bag_weights, paid=False):
    flights = read('flights')
    txs = read('transactions')
    flight = next((f for f in flights if f['id'] == flight_id), None)
    if not flight:
        raise ValueError('Penerbangan tidak ditemukan')
    available = flight['kapasitas'] - flight.get('terjual', 0)
    if len(passengers) > available:
        raise ValueError('Kursi tidak cukup')
    # hitung biaya tambahan bagasi: asumsi 10kg gratis, >10kg biaya 10k/kg
    extra = 0
    for w in bag_weights:
        if w > 10:
            extra += (w-10) * 10000
    subtotal = flight['harga'] * len(passengers) + extra
    tx = {
        'id': len(txs)+1,
        'user_id': user['id'],
        'flight_id': flight_id,
        'passengers': passengers,
        'bag_weights': bag_weights,
        'subtotal': subtotal,
        'status': 'paid' if paid else 'pending'
    }
    txs.append(tx)
    # update terjual jika immediate paid
    if paid:
        flight['terjual'] = flight.get('terjual', 0) + len(passengers)
        # tulis perubahan flights
        write('flights', flights)
    write('transactions', txs)
    return tx

def pay_transaction(tx_id):
    txs = read('transactions')
    flights = read('flights')
    tx = next((t for t in txs if t['id'] == tx_id), None)
    if not tx:
        raise ValueError('Transaksi tidak ditemukan')
    if tx['status'] == 'paid':
        return tx
    tx['status'] = 'paid'
    # update terjual
    flight = next((f for f in flights if f['id'] == tx['flight_id']), None)
    if flight:
        flight['terjual'] = flight.get('terjual', 0) + len(tx['passengers'])
        write('flights', flights)
    write('transactions', txs)
    return tx
