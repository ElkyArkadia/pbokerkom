CREATE DATABASE perusahaan_a;

USE perusahaan_a;

CREATE TABLE Produk (
    id_produk INT AUTO_INCREMENT PRIMARY KEY,
    nama_produk VARCHAR(100) NOT NULL,
    harga_produk DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Transaksi (
    id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
    id_produk INT NOT NULL,
    jumlah_produk INT NOT NULL,
    total_harga DECIMAL(10, 2) NOT NULL,
    tanggal_transaksi DATE NOT NULL,
    FOREIGN KEY (id_produk) REFERENCES Produk(id_produk)
);
