import mysql.connector

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Ganti dengan username database Anda
            password="",  # Ganti dengan password database Anda
            database="perusahaan_a"  # Pastikan nama database sesuai
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
