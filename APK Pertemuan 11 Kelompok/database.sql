-- Membuat database
CREATE DATABASE IF NOT EXISTS crud_sia;

-- Menggunakan database
USE crud_sia;

-- Membuat tabel students (sekarang lebih relevan untuk keuangan)
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,          -- ID Transaksi sebagai primary key
    tanggal DATE NOT NULL,                      -- Tanggal transaksi
    jenis_transaksi ENUM('Debit', 'Kredit') NOT NULL, -- Jenis transaksi: Debit atau Kredit
    jumlah DECIMAL(10, 2) NOT NULL,             -- Jumlah transaksi dengan format desimal
    keterangan TEXT                             -- Keterangan transaksi
);
