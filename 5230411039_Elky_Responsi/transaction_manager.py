import mysql.connector
from datetime import date

# Konfigurasi koneksi database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "perusahaan_a"
}

# Fungsi untuk menghitung total harga
def hitung_total(harga, jumlah):
    return harga * jumlah

# Fungsi untuk menambah transaksi
def tambah_transaksi(id_produk, jumlah, total, tanggal):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = """
        INSERT INTO Transaksi (id_produk, jumlah_produk, total_harga, tanggal_transaksi)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (id_produk, jumlah, total, tanggal))
    conn.commit()
    conn.close()

# Fungsi untuk membaca daftar transaksi
def baca_transaksi():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = """
        SELECT 
            p.nama_produk, t.jumlah_produk, t.total_harga, t.tanggal_transaksi
        FROM 
            Transaksi t
        JOIN 
            Produk p ON t.id_produk = p.id_produk
    """
    cursor.execute(query)
    hasil = cursor.fetchall()
    conn.close()
    return hasil
