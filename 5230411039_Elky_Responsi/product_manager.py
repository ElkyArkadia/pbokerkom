import mysql.connector

# Konfigurasi koneksi database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "perusahaan_a"
}

# Fungsi untuk menambah produk
def tambah_produk(nama, harga):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO Produk (nama_produk, harga_produk) VALUES (%s, %s)"
    cursor.execute(query, (nama, harga))
    conn.commit()
    conn.close()

# Fungsi untuk membaca daftar produk
def baca_produk():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT id_produk, nama_produk, harga_produk FROM Produk"
    cursor.execute(query)
    hasil = cursor.fetchall()
    conn.close()
    return hasil

# Fungsi untuk mengubah produk
def ubah_produk(id_produk, nama, harga):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "UPDATE Produk SET nama_produk = %s, harga_produk = %s WHERE id_produk = %s"
    cursor.execute(query, (nama, harga, id_produk))
    conn.commit()
    conn.close()

# Fungsi untuk menghapus produk
def hapus_produk(id_produk):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM Produk WHERE id_produk = %s"
    cursor.execute(query, (id_produk,))
    conn.commit()
    conn.close()
