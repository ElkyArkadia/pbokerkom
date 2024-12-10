import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# Fungsi untuk membuat koneksi ke database
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="crud_klp"
    )

# Fungsi untuk menambah transaksi
def add_transaction():
    date = entry_date.get()
    description = entry_description.get()
    transaction_type = transaction_type_var.get()
    amount = entry_amount.get()

    if date and description and transaction_type and amount.isdigit():
        connection = create_connection()
        cursor = connection.cursor()
        
        query = "INSERT INTO transactions (date, description, type, amount) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (date, description, transaction_type, int(amount)))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Transaksi berhasil ditambahkan!")
        clear_fields()
        refresh_transactions()
    else:
        messagebox.showwarning("Input Error", "Isi semua field dengan benar.")

# Fungsi untuk menampilkan daftar transaksi
def refresh_transactions():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()

    listbox_transactions.delete(0, tk.END)
    for row in transactions:
        listbox_transactions.insert(
            tk.END,
            f"ID: {row[0]}, Tanggal: {row[1]}, Deskripsi: {row[2]}, Jenis: {row[3]}, Jumlah: {row[4]}"
        )

    cursor.close()
    connection.close()

# Fungsi untuk memilih transaksi untuk diedit
def select_transaction(event):
    selected = listbox_transactions.curselection()
    if selected:
        transaction_info = listbox_transactions.get(selected).split(", ")
        transaction_id = transaction_info[0].split(": ")[1]
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = %s", (transaction_id,))
        transaction = cursor.fetchone()
        cursor.close()
        connection.close()

        # Isi field input dengan data transaksi
        entry_date.delete(0, tk.END)
        entry_date.insert(0, transaction[1])
        entry_description.delete(0, tk.END)
        entry_description.insert(0, transaction[2])
        transaction_type_var.set(transaction[3])
        entry_amount.delete(0, tk.END)
        entry_amount.insert(0, transaction[4])
        global selected_transaction_id
        selected_transaction_id = transaction_id

# Fungsi untuk mengupdate transaksi
def update_transaction():
    if not selected_transaction_id:
        messagebox.showwarning("Update Error", "Pilih transaksi untuk diperbarui.")
        return

    date = entry_date.get()
    description = entry_description.get()
    transaction_type = transaction_type_var.get()
    amount = entry_amount.get()

    if date and description and transaction_type and amount.isdigit():
        connection = create_connection()
        cursor = connection.cursor()
        
        query = "UPDATE transactions SET date = %s, description = %s, type = %s, amount = %s WHERE id = %s"
        cursor.execute(query, (date, description, transaction_type, int(amount), selected_transaction_id))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Transaksi berhasil diperbarui!")
        clear_fields()
        refresh_transactions()
    else:
        messagebox.showwarning("Input Error", "Isi semua field dengan benar.")

# Fungsi untuk menghapus transaksi
def delete_transaction():
    selected = listbox_transactions.curselection()
    if selected:
        transaction_info = listbox_transactions.get(selected).split(", ")
        transaction_id = transaction_info[0].split(": ")[1]

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))
        connection.commit()
        cursor.close()
        connection.close()

        messagebox.showinfo("Success", "Transaksi berhasil dihapus!")
        refresh_transactions()
    else:
        messagebox.showwarning("Delete Error", "Pilih transaksi untuk dihapus.")

# Fungsi untuk menghapus isi kolom input
def clear_fields():
    entry_date.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    transaction_type_var.set("")
    entry_amount.delete(0, tk.END)

# Fungsi utama untuk membuat tampilan GUI
def create_gui():
    global entry_date, entry_description, transaction_type_var, entry_amount, listbox_transactions, selected_transaction_id

    selected_transaction_id = None

    root = tk.Tk()
    root.title("Manajemen Keuangan")
    root.geometry("700x600")
    root.config(bg="#f5f5f5")

    font_title = ("Helvetica", 16, "bold")
    font_text = ("Helvetica", 12)

    # Header
    tk.Label(root, text="Manajemen Keuangan", font=font_title, bg="#43a047", fg="white", pady=10).pack(fill="x")

    # Input Fields
    frame_input = tk.Frame(root, bg="#f5f5f5")
    frame_input.pack(pady=10)

    tk.Label(frame_input, text="Tanggal (YYYY-MM-DD):", font=font_text, bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_date = tk.Entry(frame_input, font=font_text, width=30)
    entry_date.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_input, text="Deskripsi:", font=font_text, bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_description = tk.Entry(frame_input, font=font_text, width=30)
    entry_description.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame_input, text="Jenis Transaksi:", font=font_text, bg="#f5f5f5").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    transaction_type_var = tk.StringVar()
    tk.Radiobutton(frame_input, text="Debit", variable=transaction_type_var, value="Debit", font=font_text, bg="#f5f5f5").grid(row=2, column=1, sticky="w")
    tk.Radiobutton(frame_input, text="Kredit", variable=transaction_type_var, value="Kredit", font=font_text, bg="#f5f5f5").grid(row=2, column=1, padx=100, sticky="w")

    tk.Label(frame_input, text="Jumlah (Rp):", font=font_text, bg="#f5f5f5").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_amount = tk.Entry(frame_input, font=font_text, width=30)
    entry_amount.grid(row=3, column=1, padx=10, pady=5)

    # Buttons
    frame_buttons = tk.Frame(root, bg="#f5f5f5")
    frame_buttons.pack(pady=10)

    tk.Button(frame_buttons, text="Tambah", command=add_transaction, font=font_text, bg="#43a047", fg="white", width=12).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="Perbarui", command=update_transaction, font=font_text, bg="#fbc02d", fg="white", width=12).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="Hapus", command=delete_transaction, font=font_text, bg="#e53935", fg="white", width=12).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="Hapus Input", command=clear_fields, font=font_text, bg="#757575", fg="white", width=12).pack(side="left", padx=5)

    # Listbox with Scrollbar
    frame_list = tk.Frame(root, bg="#f5f5f5")
    frame_list.pack(pady=10)

    scrollbar = tk.Scrollbar(frame_list, orient=tk.VERTICAL)
    listbox_transactions = tk.Listbox(frame_list, font=font_text, width=60, height=15, yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox_transactions.yview)
    scrollbar.pack(side="right", fill="y")
    listbox_transactions.pack(side="left", fill="both")

    listbox_transactions.bind('<<ListboxSelect>>', select_transaction)

    refresh_transactions()
    root.mainloop()

# Menjalankan aplikasi
if __name__ == "__main__":
    create_gui()
