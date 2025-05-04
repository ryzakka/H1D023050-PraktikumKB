import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pyswip import Prolog

# Inisialisasi Prolog
prolog = Prolog()
prolog.consult("pakar_malaria_gui.pl")

# Variabel Global
penyakit = []
gejala = {}
index_penyakit = 0
index_gejala = 0
current_penyakit = ""
current_gejala = ""

def mulai_diagnosa():
    global penyakit, gejala, index_penyakit, index_gejala

    # Bersihkan database Prolog
    prolog.retractall("gejala_pos(_)")
    prolog.retractall("gejala_neg(_)")

    # Aktifkan tombol jawaban
    start_btn.configure(state=tk.DISABLED)
    yes_btn.configure(state=tk.NORMAL)
    no_btn.configure(state=tk.NORMAL)

    # Dapatkan daftar penyakit
    penyakit = [p["X"] for p in prolog.query("penyakit(X)")]
    for p in penyakit:
        gejala[p] = [g["X"] for g in prolog.query(f"gejala(X, \"{p}\")")]

    index_penyakit = 0
    index_gejala = -1
    pertanyaan_selanjutnya()

def pertanyaan_selanjutnya(ganti_penyakit=False):
    global current_penyakit, current_gejala, index_penyakit, index_gejala

    if ganti_penyakit:
        index_penyakit += 1
        index_gejala = -1

    if index_penyakit >= len(penyakit):
        hasil_diagnosa()
        return

    current_penyakit = penyakit[index_penyakit]
    index_gejala += 1

    if index_gejala >= len(gejala[current_penyakit]):
        hasil_diagnosa(current_penyakit)
        return

    current_gejala = gejala[current_penyakit][index_gejala]

    # Cek status gejala di Prolog
    if list(prolog.query(f"gejala_pos({current_gejala})")):
        pertanyaan_selanjutnya()
        return
    elif list(prolog.query(f"gejala_neg({current_gejala})")):
        pertanyaan_selanjutnya(ganti_penyakit=True)
        return

    # Dapatkan teks pertanyaan
    query_result = list(prolog.query(f"pertanyaan({current_gejala}, Y)"))
    if query_result:
        pertanyaan = query_result[0]["Y"]
        tampilkan_pertanyaan(pertanyaan)
    else:
        tampilkan_pertanyaan("Pertanyaan tidak ditemukan.")

def tampilkan_pertanyaan(pertanyaan):
    kotak_pertanyaan.configure(state=tk.NORMAL)
    kotak_pertanyaan.delete(1.0, tk.END)
    kotak_pertanyaan.insert(tk.END, pertanyaan)
    kotak_pertanyaan.configure(state=tk.DISABLED)

def jawaban(jwb):
    if jwb:
        prolog.assertz(f"gejala_pos({current_gejala})")
        pertanyaan_selanjutnya()
    else:
        prolog.assertz(f"gejala_neg({current_gejala})")
        pertanyaan_selanjutnya(ganti_penyakit=True)

def hasil_diagnosa(penyakit_ditemukan=""):
    if penyakit_ditemukan:
        messagebox.showinfo("Hasil Diagnosa", f"Anda terdeteksi {penyakit_ditemukan}.")
    else:
        messagebox.showinfo("Hasil Diagnosa", "Tidak terdeteksi penyakit.")
    
    # Reset tombol
    yes_btn.configure(state=tk.DISABLED)
    no_btn.configure(state=tk.DISABLED)
    start_btn.configure(state=tk.NORMAL)

# Inisialisasi window utama
root = tk.Tk()
root.title("Sistem Pakar Diagnosis Penyakit Malaria")

# Inisialisasi frame utama
mainframe = ttk.Frame(root, padding="10 10 20 20")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Judul
ttk.Label(mainframe, text="Aplikasi Diagnosa Penyakit Malaria", font=("Arial", 16)).grid(column=0, row=0, columnspan=3, pady=10)

# Label pertanyaan
ttk.Label(mainframe, text="Kolom Pertanyaan:").grid(column=0, row=1, columnspan=3)

# Kotak pertanyaan
kotak_pertanyaan = tk.Text(mainframe, height=4, width=50, state=tk.DISABLED, wrap="word")
kotak_pertanyaan.grid(column=0, row=2, columnspan=3, pady=10)

# Tombol Ya/Tidak
yes_btn = ttk.Button(mainframe, text="Ya", state=tk.DISABLED, command=lambda: jawaban(True))
yes_btn.grid(column=1, row=3, sticky=(tk.W, tk.E), padx=5, pady=5)

no_btn = ttk.Button(mainframe, text="Tidak", state=tk.DISABLED, command=lambda: jawaban(False))
no_btn.grid(column=2, row=3, sticky=(tk.W, tk.E), padx=5, pady=5)

# Tombol Mulai Diagnosa
start_btn = ttk.Button(mainframe, text="Mulai Diagnosa", command=mulai_diagnosa)
start_btn.grid(column=1, row=4, columnspan=2, sticky=(tk.W, tk.E), pady=10)

# Menambahkan padding ke setiap widget
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# Jalankan GUI
root.mainloop()
