from db_connection import get_connection

def tambah_transaksi(id_produk, jumlah, total, tanggal):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Transaksi (id_produk, jumlah_produk, total_harga, tanggal_transaksi) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (id_produk, jumlah, total, tanggal))
    conn.commit()
    conn.close()

def hitung_total(harga, jumlah):
    return harga * jumlah

def baca_transaksi():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT Produk.nama_produk, Transaksi.jumlah_produk, Transaksi.total_harga, Transaksi.tanggal_transaksi
    FROM Transaksi
    JOIN Produk ON Transaksi.id_produk = Produk.id_produk
    """
    cursor.execute(query)
    hasil = cursor.fetchall()
    conn.close()
    return hasil
