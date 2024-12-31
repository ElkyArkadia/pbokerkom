import tkinter as tk
from tkinter import ttk, messagebox
from modules.product_manager import tambah_produk, baca_produk, ubah_produk, hapus_produk
from modules.transaction_manager import tambah_transaksi, hitung_total, baca_transaksi
from datetime import date

def run_app():
    # Setup Window
    root = tk.Tk()
    root.title("Manajemen Produk dan Transaksi")

    # Produk Management Frame
    product_frame = ttk.LabelFrame(root, text="Manajemen Produk")
    product_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    tk.Label(product_frame, text="Nama Produk").grid(row=0, column=0, padx=5, pady=5)
    nama_entry = tk.Entry(product_frame)
    nama_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(product_frame, text="Harga Produk").grid(row=1, column=0, padx=5, pady=5)
    harga_entry = tk.Entry(product_frame)
    harga_entry.grid(row=1, column=1, padx=5, pady=5)

    def add_product():
        nama = nama_entry.get().strip()
        if not nama:
            messagebox.showerror("Input Error", "Nama produk tidak boleh kosong.")
            return
        try:
            harga = float(harga_entry.get())
            if harga <= 0:
                raise ValueError("Harga harus lebih dari nol.")
            tambah_produk(nama, harga)
            refresh_products()
            nama_entry.delete(0, tk.END)
            harga_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    ttk.Button(product_frame, text="Tambah Produk", command=add_product).grid(row=2, column=0, columnspan=2, pady=10)

    product_list = ttk.Treeview(product_frame, columns=("ID", "Nama", "Harga"), show="headings")
    product_list.heading("ID", text="ID")
    product_list.heading("Nama", text="Nama")
    product_list.heading("Harga", text="Harga")
    product_list.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def refresh_products():
        for item in product_list.get_children():
            product_list.delete(item)
        for row in baca_produk():
            product_list.insert("", "end", values=row)

    refresh_products()

    # Fungsi untuk menghapus produk
    def delete_product():
        selected_item = product_list.selection()
        if not selected_item:
            messagebox.showerror("Input Error", "Pilih produk yang ingin dihapus.")
            return
        product_id = product_list.item(selected_item)["values"][0]  # ID produk yang dipilih
        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus produk ini?")
        if confirm:
            hapus_produk(product_id)
            refresh_products()

    ttk.Button(product_frame, text="Hapus Produk", command=delete_product).grid(row=4, column=0, pady=10)

    # Fungsi untuk mengubah produk
    def edit_product():
        selected_item = product_list.selection()
        if not selected_item:
            messagebox.showerror("Input Error", "Pilih produk yang ingin diubah.")
            return
        product_id = product_list.item(selected_item)["values"][0]  # ID produk yang dipilih
        product_name = product_list.item(selected_item)["values"][1]  # Nama produk
        product_price = product_list.item(selected_item)["values"][2]  # Harga produk

        # Masukkan nilai produk ke dalam entry untuk diedit
        nama_entry.delete(0, tk.END)
        nama_entry.insert(0, product_name)
        harga_entry.delete(0, tk.END)
        harga_entry.insert(0, str(product_price))

        def update_product():
            new_name = nama_entry.get().strip()
            try:
                new_price = float(harga_entry.get())
                if new_price <= 0:
                    raise ValueError("Harga harus lebih dari nol.")
                ubah_produk(product_id, new_name, new_price)
                refresh_products()
                nama_entry.delete(0, tk.END)
                harga_entry.delete(0, tk.END)
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))

        ttk.Button(product_frame, text="Update Produk", command=update_product).grid(row=5, column=0, columnspan=2, pady=10)

    ttk.Button(product_frame, text="Ubah Produk", command=edit_product).grid(row=4, column=1, pady=10)

    # Transaction Frame
    transaction_frame = ttk.LabelFrame(root, text="Proses Transaksi")
    transaction_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    tk.Label(transaction_frame, text="Pilih Produk").grid(row=0, column=0, padx=5, pady=5)
    product_dropdown = ttk.Combobox(transaction_frame)
    product_dropdown.grid(row=0, column=1, padx=5, pady=5)

    def load_products():
        # Format: Nama Produk - Harga
        product_dropdown["values"] = [f"{row[1]}" for row in baca_produk()]  # Ambil hanya nama produk

    load_products()

    tk.Label(transaction_frame, text="Jumlah").grid(row=1, column=0, padx=5, pady=5)
    jumlah_entry = tk.Entry(transaction_frame)
    jumlah_entry.grid(row=1, column=1, padx=5, pady=5)

    total_label = tk.Label(transaction_frame, text="Total: 0.00")
    total_label.grid(row=2, column=0, columnspan=2, pady=5)

    def calculate_total():
        selected = product_dropdown.get()
        if selected and jumlah_entry.get():
            try:
                # Cari harga produk berdasarkan nama
                product = next((row for row in baca_produk() if row[1] == selected), None)
                if product:
                    harga = product[2]  # Ambil harga produk
                    jumlah = int(jumlah_entry.get())
                    if jumlah <= 0:
                        raise ValueError("Jumlah harus lebih dari nol.")
                    total = hitung_total(harga, jumlah)
                    total_label.config(text=f"Total: {total:.2f}")
                else:
                    total_label.config(text="Total: 0.00")
            except ValueError:
                total_label.config(text="Total: 0.00")

    jumlah_entry.bind("<KeyRelease>", lambda e: calculate_total())

    def save_transaction():
        selected = product_dropdown.get()
        if selected and jumlah_entry.get():
            try:
                # Cari ID produk berdasarkan nama produk yang dipilih
                product = next((row for row in baca_produk() if row[1] == selected), None)
                if not product:
                    raise ValueError("Pilih produk yang valid dari dropdown.")
                id_produk = product[0]  # ID produk
                harga = product[2]  # Harga produk
                jumlah = int(jumlah_entry.get())
                if jumlah <= 0:
                    raise ValueError("Jumlah harus lebih dari nol.")
                total = hitung_total(harga, jumlah)
                tambah_transaksi(id_produk, jumlah, total, date.today())
                refresh_transactions()
                jumlah_entry.delete(0, tk.END)
                total_label.config(text="Total: 0.00")
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))

    ttk.Button(transaction_frame, text="Simpan Transaksi", command=save_transaction).grid(row=3, column=0, columnspan=2, pady=10)

    # Transaction List
    transaction_list = ttk.Treeview(transaction_frame, columns=("Produk", "Jumlah", "Total", "Tanggal"), show="headings")
    transaction_list.heading("Produk", text="Produk")
    transaction_list.heading("Jumlah", text="Jumlah")
    transaction_list.heading("Total", text="Total")
    transaction_list.heading("Tanggal", text="Tanggal")
    transaction_list.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def refresh_transactions():
        for item in transaction_list.get_children():
            transaction_list.delete(item)
        for row in baca_transaksi():
            transaction_list.insert("", "end", values=row)

    refresh_transactions()

    root.mainloop()

if __name__ == "__main__":
    run_app()
