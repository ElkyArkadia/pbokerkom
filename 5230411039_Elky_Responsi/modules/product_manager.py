from db_connection import get_connection

def tambah_produk(nama, harga):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Produk (nama_produk, harga_produk) VALUES (%s, %s)"
    cursor.execute(query, (nama, harga))
    conn.commit()
    conn.close()

def baca_produk():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Produk"
    cursor.execute(query)
    hasil = cursor.fetchall()
    conn.close()
    return hasil

def ubah_produk(id_produk, nama, harga):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE Produk SET nama_produk = %s, harga_produk = %s WHERE id_produk = %s"
    cursor.execute(query, (nama, harga, id_produk))
    conn.commit()
    conn.close()

def hapus_produk(id_produk):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Produk WHERE id_produk = %s"
    cursor.execute(query, (id_produk,))
    conn.commit()
    conn.close()
