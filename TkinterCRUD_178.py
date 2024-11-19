# Mengimpor modul sqlite3 untuk menghubungkan dan berinteraksi dengan database SQLite 
import sqlite3  
# Mengimpor elemen-elemen untuk membuat antarmuka grafis dengan Tkinter
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  

# Fungsi untuk membuat database dan tabel
def create_database():
    # Membuka koneksi ke database SQLite (atau membuat baru jika belum ada)
    conn = sqlite3.connect('nilai_siswa.db') 
     # Membuat cursor untuk mengeksekusi perintah SQL
    cursor = conn.cursor() 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            nama_siswa TEXT,  
            biologi INTEGER,  
            fisika INTEGER,  
            inggris INTEGER,  
            prediksi_fakultas TEXT  
        )
    ''')  # Membuat tabel jika belum ada
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk mengambil semua data dari tabel
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor untuk mengeksekusi perintah SQL
    cursor.execute("SELECT * FROM nilai_siswa")  # Mengambil semua data dari tabel nilai_siswa
    rows = cursor.fetchall()  # Menyimpan hasil query dalam bentuk list
    conn.close()  # Menutup koneksi ke database
    return rows  # Mengembalikan data yang diambil

# Fungsi untuk menyimpan data siswa baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor untuk mengeksekusi perintah SQL
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)  
    ''', (nama, biologi, fisika, inggris, prediksi))  # Menyertakan data yang ingin dimasukkan
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk memperbarui data siswa yang sudah ada
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor untuk mengeksekusi perintah SQL
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?  
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))  # Menyertakan data yang ingin diperbarui
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk menghapus data siswa berdasarkan ID
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor untuk mengeksekusi perintah SQL
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus data berdasarkan ID
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:  # Jika nilai biologi lebih tinggi
        return "Kedokteran"  # Prediksi fakultas Kedokteran
    elif fisika > biologi and fisika > inggris:  # Jika nilai fisika lebih tinggi
        return "Teknik"  # Prediksi fakultas Teknik
    elif inggris > biologi and inggris > fisika:  # Jika nilai inggris lebih tinggi
        return "Bahasa"  # Prediksi fakultas Bahasa
    else:
        return "Tidak Diketahui"  # Jika tidak ada nilai yang dominan

# Fungsi untuk menangani tombol "Submit" untuk menambah data siswa baru
def submit():
    try:
        nama = nama_var.get()  # Mengambil input nama siswa
        biologi = int(biologi_var.get())  # Mengambil input nilai biologi
        fisika = int(fisika_var.get())  # Mengambil input nilai fisika
        inggris = int(inggris_var.get())  # Mengambil input nilai inggris

        if not nama:  # Memeriksa apakah nama kosong
            raise Exception("Nama siswa tidak boleh kosong.")  # Menampilkan pesan error jika kosong

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Menyimpan data siswa ke database
        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")  
        populate_table()  # Memperbarui tampilan tabel dengan data terbaru
    except ValueError as e:  # Menangani kesalahan input
        # Menampilkan pesan error jika ada input tidak valid
        messagebox.showerror("Error", f"Input tidak valid: {e}")  
# Fungsi untuk menangani tombol "Update" untuk memperbarui data siswa
def update():
    try:
        if not selected_record_id.get():  # Memeriksa apakah ada data yang dipilih untuk diperbarui
            # Menampilkan pesan error jika tidak ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk di-update!") 
        record_id = int(selected_record_id.get())  # Mengambil ID record yang dipilih
        nama = nama_var.get()  # Mengambil input nama siswa
        biologi = int(biologi_var.get())  # Mengambil input nilai biologi
        fisika = int(fisika_var.get())  # Mengambil input nilai fisika
        inggris = int(inggris_var.get())  # Mengambil input nilai inggris

        if not nama:  # Memeriksa apakah nama kosong
            raise ValueError("Nama siswa tidak boleh kosong.")  # Menampilkan pesan error jika kosong

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Memperbarui data di database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")  # Menampilkan pesan sukses
        clear_inputs()  # Mengosongkan input setelah diperbarui
        populate_table()  # Memperbarui tampilan tabel dengan data terbaru
    except ValueError as e:  # Menangani kesalahan input
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menampilkan pesan error jika ada kesalahan

# Fungsi untuk menangani tombol "Delete" untuk menghapus data siswa
def delete():
    try:
        if not selected_record_id.get():  # Memeriksa apakah ada data yang dipilih untuk dihapus
            # Menampilkan pesan error jika tidak ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk dihapus!")  

        record_id = int(selected_record_id.get())  # Mengambil ID record yang dipilih
        delete_database(record_id)  # Menghapus data di database
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")  # Menampilkan pesan sukses
        clear_inputs()  # Mengosongkan input setelah dihapus
        populate_table()  # Memperbarui tampilan tabel dengan data terbaru
    except ValueError as e:  # Menangani kesalahan input
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menampilkan pesan error jika ada kesalahan

# Fungsi untuk mengosongkan semua input pada form
def clear_inputs():
    nama_var.set("")  # Mengosongkan input nama
    biologi_var.set("")  # Mengosongkan input nilai biologi
    fisika_var.set("")  # Mengosongkan input nilai fisika
    inggris_var.set("")  # Mengosongkan input nilai inggris
    selected_record_id.set("")  # Mengosongkan ID record yang dipilih

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():  # Menghapus semua baris dari tabel
        tree.delete(row)
    for row in fetch_data():  # Mengambil data dari database
        tree.insert('', 'end', values=row)  # Menambahkan data ke dalam tabel

# Fungsi untuk mengisi input dengan data yang dipilih dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Mendapatkan item yang dipilih dari tabel
        selected_row = tree.item(selected_item)['values']  # Mendapatkan nilai dari baris yang dipilih

        selected_record_id.set(selected_row[0])  # Mengisi ID record yang dipilih
        nama_var.set(selected_row[1])  # Mengisi input nama dengan data yang dipilih
        biologi_var.set(selected_row[2])  # Mengisi input nilai biologi dengan data yang dipilih
        fisika_var.set(selected_row[3])  # Mengisi input nilai fisika dengan data yang dipilih
        inggris_var.set(selected_row[4])  # Mengisi input nilai inggris dengan data yang dipilih
    except IndexError:
        # Menampilkan pesan error jika tidak ada data yang dipilih
        messagebox.showerror("Error", "Pilih data yang valid!")  
create_database()  # Membuat database dan tabel jika belum ada

# Membuat GUI dengan tkinter
root = Tk()  # Membuat jendela utama
root.title("Prediksi Fakultas Siswa")  # Menentukan judul jendela
root.configure(bg="lightblue")  # Mengatur warna latar belakang jendela utama

# Variabel tkinter untuk menyimpan data input
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Variabel untuk menyimpan ID record yang dipilih

# Membuat Label dan Entry untuk form input data siswa
Label(root, text="Nama Siswa", bg="lightblue").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var, bg="white").grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi", bg="lightblue").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var, bg="white").grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika", bg="lightblue").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var, bg="white").grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris", bg="lightblue").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var, bg="white").grid(row=3, column=1, padx=10, pady=5)

# Membuat tombol aksi untuk tambah, update, dan delete data
Button(root, text="Add", command=submit, bg="skyblue").grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update, bg="skyblue").grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete, bg="skyblue").grid(row=4, column=2, pady=10)

# Membuat tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')  # Tabel tanpa menampilkan kolom ID

# Styling tabel agar sesuai dengan warna GUI
style = ttk.Style()
style.configure("Treeview", background="lightblue", foreground="black", rowheight=25, fieldbackground="lightblue")
style.map('Treeview', background=[('selected', 'blue')])

# Mengatur posisi kolom tabel dan pengaturan lainnya
for col in columns:
    tree.heading(col, text=col.capitalize())  # Mengatur teks judul kolom
    tree.column(col, anchor='center')  # Mengatur agar teks kolom rata tengah

# Menampilkan tabel pada window
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Menghubungkan event klik pada tabel dengan fungsi pengisian input
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Memuat data awal ke tabel
populate_table()  # Memperbarui tampilan tabel dengan data dari database

# Menjalankan aplikasi Tkinter
root.mainloop()  # Memulai loop utama aplikasi Tkinter


