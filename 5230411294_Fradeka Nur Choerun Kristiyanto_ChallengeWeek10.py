import mysql.connector

# Koneksi ke database
conn = mysql.connector.connect(
    user="root",
    host="localhost",
    password="",
    database="penjualan"
)

cur = conn.cursor()

# # Membuat tabel Pegawai
# cur.execute("""
# CREATE TABLE IF NOT EXISTS Pegawai (
#     NIK INT NOT NULL PRIMARY KEY,
#     Nama VARCHAR(100),
#     Alamat VARCHAR(255)
# )
# """)

# # Membuat tabel Produk
# cur.execute("""
# CREATE TABLE IF NOT EXISTS Produk (
#     Kode_Produk INT NOT NULL PRIMARY KEY,
#     Nama_Produk VARCHAR(100),
#     Jenis_Produk VARCHAR(50),
#     Harga DECIMAL(10, 2)
# )
# """)



# # Membuat tabel Struk
# cur.execute("""
# CREATE TABLE IF NOT EXISTS Struk (
#     No_Struk INT NOT NULL PRIMARY KEY,
#     Nama_Pegawai VARCHAR(100),
#     No_Transaksi INT,
#     Nama_Produk VARCHAR(100),
#     Jumlah_Produk INT,
#     Total_Harga DECIMAL(10, 2),
#     FOREIGN KEY (No_Transaksi) REFERENCES Transaksi(No_Transaksi)
# )
# """)

# Fungsi untuk menambahkan Pegawai
def create_pegawai(nik, nama, alamat):
    cur.execute("INSERT INTO Pegawai (NIK, Nama, Alamat) VALUES (%s, %s, %s)", (nik, nama, alamat))
    conn.commit()
    print("Pegawai ditambahkan.")

# Fungsi untuk membaca data Pegawai
def read_pegawai():
    cur.execute("SELECT * FROM Pegawai")
    for row in cur.fetchall():
        print(row)

# Fungsi untuk memperbarui data Pegawai
def update_pegawai(nik, nama, alamat):
    cur.execute("UPDATE Pegawai SET Nama = %s, Alamat = %s WHERE NIK = %s", (nama, alamat, nik))
    conn.commit()
    print("Data Pegawai diperbarui.")

def delete_pegawai(nik):
    # Cek apakah pegawai memiliki transaksi terkait
    cur.execute("SELECT COUNT(*) FROM Transaksi WHERE NIK = %s", (nik,))
    if cur.fetchone()[0] > 0:
        print("Error: Tidak dapat menghapus pegawai karena ada transaksi terkait.")
        return
    
    cur.execute("DELETE FROM Pegawai WHERE NIK = %s", (nik,))
    conn.commit()
    print("Pegawai dihapus.")

# Fungsi untuk menambahkan Produk
def create_produk(kode_produk, nama_produk, jenis_produk, harga):
    cur.execute("INSERT INTO Produk (Kode_Produk, Nama_Produk, Jenis_Produk, Harga) VALUES (%s, %s, %s, %s)", 
                (kode_produk, nama_produk, jenis_produk, harga))
    conn.commit()
    print("Produk ditambahkan.")

# Fungsi untuk membaca data Produk
def read_produk():
    cur.execute("SELECT * FROM Produk")
    for row in cur.fetchall():
        print(row)

# Fungsi untuk memperbarui data Produk
def update_produk(kode_produk, nama_produk, jenis_produk, harga):
    cur.execute("UPDATE Produk SET Nama_Produk = %s, Jenis_Produk = %s, Harga = %s WHERE Kode_Produk = %s", 
                (nama_produk, jenis_produk, harga, kode_produk))
    conn.commit()
    print("Data Produk diperbarui.")

def delete_produk(kode_produk):
    # Cek apakah ada transaksi yang menggunakan kode produk tersebut
    cur.execute("SELECT COUNT(*) FROM Transaksi WHERE Kode_Produk = %s", (kode_produk,))
    if cur.fetchone()[0] > 0:
        print("Error: Tidak dapat menghapus produk karena ada transaksi terkait.")
        return
    
    cur.execute("DELETE FROM Produk WHERE Kode_Produk = %s", (kode_produk,))
    conn.commit()
    print("Produk dihapus.")


# Fungsi untuk menambahkan Transaksi
def create_transaksi(no_transaksi, nik, kode_produk, detail_transaksi):
    cur.execute("INSERT INTO Transaksi (No_Transaksi, NIK, Kode_Produk, Detail_Transaksi) VALUES (%s, %s, %s, %s)", 
                (no_transaksi, nik, kode_produk, detail_transaksi))
    conn.commit()
    print("Transaksi ditambahkan.")

# Fungsi untuk membaca data Transaksi
def read_transaksi():
    cur.execute("SELECT * FROM Transaksi")
    for row in cur.fetchall():
        print(row)

# Fungsi untuk memperbarui data Transaksi
def update_transaksi(no_transaksi, nik=None, kode_produk=None, detail_transaksi=None):
    query = "UPDATE Transaksi SET "
    params = []
    
    if nik is not None:
        query += "NIK = %s,"
        params.append(nik)
    
    if kode_produk is not None:
        query += "Kode_Produk = %s,"
        params.append(kode_produk)
        
    if detail_transaksi is not None:
        query += "Detail_Transaksi = %s,"
        params.append(detail_transaksi)
    
    query = query.rstrip(',') + " WHERE No_Transaksi = %s"
    params.append(no_transaksi)
    
    cur.execute(query, tuple(params))
    conn.commit()
    print("Data Transaksi diperbarui.")

def delete_transaksi(no_transaksi):
    # Cek apakah ada struk yang menggunakan no transaksi tersebut
    cur.execute("SELECT COUNT(*) FROM Struk WHERE No_Transaksi = %s", (no_transaksi,))
    if cur.fetchone()[0] > 0:
        print("Error: Tidak dapat menghapus transaksi karena ada struk terkait.")
        return
    
    cur.execute("DELETE FROM Transaksi WHERE No_Transaksi = %s", (no_transaksi,))
    conn.commit()
    print("Transaksi dihapus.")


# Fungsi untuk menambahkan Struk
def create_struk(no_struk, nama_pegawai, no_transaksi, nama_produk, jumlah_produk, harga_per_unit):
    total_harga = jumlah_produk * harga_per_unit  # Menghitung total harga
    cur.execute("INSERT INTO Struk (No_Struk, Nama_Pegawai, No_Transaksi, Nama_Produk, Jumlah_Produk, Total_Harga) VALUES (%s,%s,%s,%s,%s,%s)", 
                (no_struk, nama_pegawai, no_transaksi, nama_produk, jumlah_produk, total_harga))
    conn.commit()
    print("Struk ditambahkan.")


# Fungsi untuk membaca data Struk
def read_struk():
    cur.execute("SELECT * FROM Struk")
    for row in cur.fetchall():
        print(row)

# Fungsi untuk memperbarui data Struk
def update_struk(no_struk,nama_pegawai=None,no_transaksi=None,nama_produk=None,jumlah_produk=None,total_harga=None):
    
  query = "UPDATE Struk SET "
  params = []

  if nama_pegawai is not None:
      query += "Nama_Pegawai = %s,"
      params.append(nama_pegawai)

  if no_transaksi is not None:
      query += "No_Transaksi = %s,"
      params.append(no_transaksi)

  if nama_produk is not None:
      query += "Nama_Produk = %s,"
      params.append(nama_produk)

  if jumlah_produk is not None:
      query += "Jumlah_Produk = %s,"
      params.append(jumlah_produk)

  if total_harga is not None:
      query += "Total_Harga = %s,"
      params.append(total_harga)

  query = query.rstrip(',') + " WHERE No_Struk = %s"
  params.append(no_struk)

  cur.execute(query , tuple(params))
  conn.commit()
  print("Data Struk diperbarui.")

# Fungsi untuk menghapus Struk
def delete_struk(no_struk):
    cur.execute("DELETE FROM Struk WHERE No_Struk = %s", (no_struk,))
    conn.commit()
    print("Struk dihapus.")

# Fungsi untuk menampilkan menu
def show_menu():
    print("\nMenu:")
    print("1. Tampil Data Pegawai")
    print("2. Tampil Data Produk")
    print("3. Tampil Data Transaksi")
    print("4. Tampil Data Struk")
    print("5. Input Pegawai")
    print("6. Input Produk")
    print("7. Input Transaksi")
    print("8. Input Struk")
    print("9. Ubah Pegawai")
    print("10. Ubah Produk")
    print("11. Ubah Transaksi")
    print("12. Ubah Struk")
    print("13. Hapus Pegawai")
    print("14. Hapus Produk")
    print("15. Hapus Transaksi")
    print("16. Hapus Struk")
    print("0. Keluar")

while True:
    show_menu()
    
    menu = input("Pilihan Menu: ")

    if menu == '1':
        read_pegawai()
        
    elif menu == '2':
        read_produk()
        
    elif menu == '3':
        read_transaksi()
        
    elif menu == '4':
        read_struk()
        
    elif menu == '5':
        nik = int(input("Masukkan NIK: "))
        nama = input("Masukkan Nama: ")
        alamat = input("Masukkan Alamat: ")
        create_pegawai(nik, nama, alamat)
        
    elif menu == '6':
        kode_produk = int(input("Masukkan Kode Produk: "))
        nama_produk = input("Masukkan Nama Produk: ")
        jenis_produk = input("Masukkan Jenis Produk: ")
        harga = float(input("Masukkan Harga: "))
        create_produk(kode_produk, nama_produk, jenis_produk, harga)
        
    elif menu == '7':
        no_transaksi = int(input("Masukkan No Transaksi: "))
        nik = int(input("Masukkan NIK Pegawai: "))
        kode_produk = int(input("Masukkan Kode Produk: "))
        detail_transaksi = input("Masukkan Detail Transaksi: ")
        create_transaksi(no_transaksi, nik, kode_produk, detail_transaksi)
        
    elif menu == '8':
        no_struk = int(input("Masukkan No Struk: "))
        nama_pegawai = input("Masukkan Nama Pegawai: ")
        no_transaksi = int(input("Masukkan No Transaksi: "))
        nama_produk = input("Masukkan Nama Produk: ")
        jumlah_produk = int(input("Masukkan Jumlah Produk: "))
        harga_per_unit = float(input("Masukkan Harga per Unit: "))
        create_struk(no_struk, nama_pegawai, no_transaksi, nama_produk, jumlah_produk, harga_per_unit)
        
    elif menu == '9':
        nik = int(input("Masukkan NIK Pegawai yang ingin diubah: "))
        nama = input("Masukkan Nama baru: ")
        alamat = input("Masukkan Alamat baru: ")
        update_pegawai(nik, nama, alamat)
        
    elif menu == '10':
        kode_produk = int(input("Masukkan Kode Produk yang ingin diubah: "))
        nama_produk = input("Masukkan Nama baru: ")
        jenis_produk = input("Masukkan Jenis baru: ")
        harga = float(input("Masukkan Harga baru: "))
        update_produk(kode_produk, nama_produk, jenis_produk, harga)
        
    elif menu == '11':
        no_transaksi = int(input("Masukkan No Transaksi yang ingin diubah: "))
        nik = int(input("Masukkan NIK baru (tekan Enter jika tidak ingin mengubah): ") or "None") or None
        kode_produk = int(input("Masukkan Kode Produk baru (tekan Enter jika tidak ingin mengubah): ") or "None") or None
        detail_transaksi = input("Masukkan Detail Transaksi baru (tekan Enter jika tidak ingin mengubah): ") or None
        update_transaksi(no_transaksi, nik, kode_produk, detail_transaksi)
        
    elif menu == '12':
        no_struk = int(input("Masukkan No Struk yang ingin diubah: "))
        nama_pegawai = input("Nama Pegawai baru (tekan Enter jika tidak ingin mengubah): ") or None
        no_transaksi = int(input("No Transaksi baru (tekan Enter jika tidak ingin mengubah): ") or "None") or None
        nama_produk = input("Nama Produk baru (tekan Enter jika tidak ingin mengubah): ") or None
        jumlah_produk = int(input("Jumlah Produk baru (tekan Enter jika tidak ingin mengubah): ") or "None") or None
        total_harga = float(input("Total Harga baru (tekan Enter jika tidak ingin mengubah): ") or "None") or None
        update_struk(no_struk, nama_pegawai, no_transaksi, nama_produk, jumlah_produk, total_harga)

    elif menu == '13':
        nik = int(input("Masukkan NIK Pegawai yang ingin dihapus: "))
        delete_pegawai(nik)

    elif menu == '14':
        kode_produk = int(input("Masukkan Kode Produk yang ingin dihapus: "))
        delete_produk(kode_produk)

    elif menu == '15':
        no_transaksi = int(input("Masukkan No Transaksi yang ingin dihapus: "))
        delete_transaksi(no_transaksi)

    elif menu == '16':
        no_struk = int(input("Masukkan No Struk yang ingin dihapus: "))
        delete_struk(no_struk)

    elif menu == '0':
        print("Keluar dari program.")
        break

    else:
        print("Pilihan tidak valid! Silakan coba lagi.")

# Menutup koneksi setelah semua operasi selesai
cur.close()
conn.close()