from pyswip import Prolog
import tkinter as tk
from tkinter import ttk, messagebox

prolog = Prolog()
prolog.consult("pakar_tidur.pl")

class PakarTidurApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pakar Gangguan Tidur")
        self.gejala_list = self.get_pertanyaan()
        self.jawaban = {}
        self.current_index = 0

        self.mainframe = ttk.Frame(root, padding="20")
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.mainframe, text="Sistem Sederhana Diagnosa Gangguan Tidur", font=("Arial", 16)).grid(column=0, row=0, columnspan=2, pady=10)

        self.pertanyaan_label = ttk.Label(self.mainframe, text="", wraplength=400)
        self.pertanyaan_label.grid(column=0, row=1, columnspan=2, pady=10)

        self.btn_ya = ttk.Button(self.mainframe, text="Ya", command=lambda: self.jawab("ya"))
        self.btn_tidak = ttk.Button(self.mainframe, text="Tidak", command=lambda: self.jawab("tidak"))

        self.btn_ya.grid(column=0, row=2, padx=10, pady=10)
        self.btn_tidak.grid(column=1, row=2, padx=10, pady=10)

        self.tampilkan_pertanyaan()

    def get_pertanyaan(self):
        pertanyaan = []
        for hasil in prolog.query("pertanyaan(Kode, Teks)"):
            pertanyaan.append((hasil["Kode"], hasil["Teks"]))
        return pertanyaan

    def tampilkan_pertanyaan(self):
        if self.current_index < len(self.gejala_list):
            kode, teks = self.gejala_list[self.current_index]
            self.pertanyaan_label.config(text=teks)
        else:
            self.analisis()

    def jawab(self, pilihan):
        kode, _ = self.gejala_list[self.current_index]
        if pilihan == "ya":
            prolog.assertz(f"gejala_pos({kode})")
        else:
            prolog.assertz(f"gejala_neg({kode})")
        self.current_index += 1
        self.tampilkan_pertanyaan()

    def analisis(self):
        hasil = list(prolog.query("diagnosa(Penyakit)"))
        if hasil:
            nama = hasil[0]["Penyakit"]
            messagebox.showinfo("Hasil Diagnosa", f"Anda kemungkinan mengalami: {nama}")
        else:
            messagebox.showinfo("Hasil Diagnosa", "Tidak ditemukan gangguan tidur yang sesuai.")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = PakarTidurApp(root)
    root.mainloop()
