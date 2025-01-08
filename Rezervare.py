import tkinter as tk
from tkinter import messagebox
import os
import json

# Date despre filme
filme = [
    {"titlu": "Film 1", "ora": "12:00 PM", "sala": 1, "pret": 20},
    {"titlu": "Film 2", "ora": "3:00 PM", "sala": 2, "pret": 22},
    {"titlu": "Film 3", "ora": "6:00 PM", "sala": 3, "pret": 25},
]

# Fișier pentru stocarea rezervărilor
fisier_rezervari = "rezervari.json"
if not os.path.exists(fisier_rezervari):
    with open(fisier_rezervari, "w") as fisier:
        json.dump([], fisier)

# Variabile globale
film_selectat = None
locuri_selectate = []

class AplicatieCinema:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicație de Management Cinema")
        self.afiseaza_selectia_filmului()
        root.geometry("700x500")

    def afiseaza_selectia_filmului(self):
        # Curăță fereastra
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Selectează un Film", font=("Arial", 16)).pack(pady=10)

        for film in filme:
            buton = tk.Button(
                self.root,
                text=f"{film['titlu']} - {film['ora']} - Sala {film['sala']} - {film['pret']} RON",
                command=lambda f=film: self.selecteaza_filmul(f),
                font=("Arial", 12)
            )
            buton.pack(pady=5)

    def selecteaza_filmul(self, film):
        global film_selectat
        film_selectat = film
        self.afiseaza_selectia_locurilor()

    def afiseaza_selectia_locurilor(self):
        # Curăță fereastra
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Selectează Locuri pentru {film_selectat['titlu']}", font=("Arial", 16)).pack(pady=10)

        self.butoane_locuri = []
        frame = tk.Frame(self.root)
        frame.pack()

        with open(fisier_rezervari, "r") as fisier:
            rezervari = json.load(fisier)

        locuri_rezervate = set()
        for rezervare in rezervari:
            if rezervare["film"] == film_selectat["titlu"] and rezervare["sala"] == film_selectat["sala"]:
                locuri_rezervate.update(tuple(loc) for loc in rezervare["locuri"])

        for rand in range(8):
            rand_frame = tk.Frame(frame)
            rand_frame.pack()
            for coloana in range(20):
                buton_loc = tk.Button(
                    rand_frame,
                    text=f"{rand+1}-{coloana+1}",
                    bg="red" if (rand, coloana) in locuri_rezervate else "green",
                    width=3,
                    command=lambda r=rand, c=coloana: self.comuta_loc(r, c)
                )
                buton_loc.grid(row=rand, column=coloana, padx=2, pady=2)
                self.butoane_locuri.append((buton_loc, rand, coloana))

        tk.Button(
            self.root, text="Rezervă", command=self.afiseaza_interfata_rezervare, font=("Arial", 12)
        ).pack(pady=10)

        tk.Button(
            self.root, text="Modifică Rezervarea", command=self.arata_modificare_rezervari, font=("Arial", 12)
        ).pack(pady=10)

        tk.Button(
            self.root, text="Înapoi", command=self.afiseaza_selectia_filmului, font=("Arial", 12)
        ).pack(pady=10)

    def comuta_loc(self, rand, coloana):
        global locuri_selectate
        loc = (rand, coloana)
        buton = [btn for btn, r, c in self.butoane_locuri if r == rand and c == coloana][0]

        if buton.cget("bg") == "red":
            messagebox.showerror("Eroare", "Locul este deja rezervat!")
            return

        if loc in locuri_selectate:
            locuri_selectate.remove(loc)
            buton.config(bg="green")
        else:
            locuri_selectate.append(loc)
            buton.config(bg="blue")

    def afiseaza_interfata_rezervare(self):
        if not locuri_selectate:
            messagebox.showerror("Eroare", "Nu ați selectat niciun loc!")
            return

        # Curăță fereastra
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Introduceți Detaliile Rezervării", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Nume:", font=("Arial", 12)).pack()
        caseta_nume = tk.Entry(self.root, font=("Arial", 12))
        caseta_nume.pack(pady=5)

        tk.Label(self.root, text="Număr de Bilete:", font=("Arial", 12)).pack()

        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Label(frame, text="Adulți:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        caseta_adulti = tk.Entry(frame, width=5, font=("Arial", 12))
        caseta_adulti.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Studenți:", font=("Arial", 12)).grid(row=0, column=2, padx=5)
        caseta_studenti = tk.Entry(frame, width=5, font=("Arial", 12))
        caseta_studenti.grid(row=0, column=3, padx=5)

        tk.Label(frame, text="Copii:", font=("Arial", 12)).grid(row=0, column=4, padx=5)
        caseta_copii = tk.Entry(frame, width=5, font=("Arial", 12))
        caseta_copii.grid(row=0, column=5, padx=5)

        def confirma_rezervarea():
            global locuri_selectate
            nume = caseta_nume.get()
            if not nume:
                messagebox.showerror("Eroare", "Numele este obligatoriu!")
                return

            try:
                adulti = int(caseta_adulti.get()) if caseta_adulti.get() else 0
                studenti = int(caseta_studenti.get()) if caseta_studenti.get() else 0
                copii = int(caseta_copii.get()) if caseta_copii.get() else 0
            except ValueError:
                messagebox.showerror("Eroare", "Numărul de bilete nu este valid!")
                return

            total_bilete = adulti + studenti + copii
            if total_bilete != len(locuri_selectate):
                messagebox.showerror("Eroare", "Numărul de bilete trebuie să corespundă cu locurile selectate!")
                return

            pret_total = (
                adulti * film_selectat['pret'] +
                studenti * (film_selectat['pret'] * 0.8) +
                copii * (film_selectat['pret'] * 0.5)
            )

            id_rezervare = f"S{film_selectat['sala']}-" + "_".join([f"{r+1}-{c+1}" for r, c in locuri_selectate])

            rezervare = {
                "nume": nume,
                "film": film_selectat["titlu"],
                "sala": film_selectat["sala"],
                "locuri": locuri_selectate,
                "adulti": adulti,
                "studenti": studenti,
                "copii": copii,
                "pret_total": pret_total,
                "id_rezervare": id_rezervare
            }

            with open(fisier_rezervari, "r") as fisier:
                rezervari = json.load(fisier)

            rezervari.append(rezervare)

            with open(fisier_rezervari, "w") as fisier:
                json.dump(rezervari, fisier, indent=4)

            messagebox.showinfo(
                "Rezervare Confirmată",
                f"Nume: {nume}\n"
                f"Bilete: {total_bilete}\n"
                f"Preț Total: {pret_total:.2f} RON\n"
                f"ID Rezervare: {id_rezervare}"
            )

            locuri_selectate = []  # Resetează locurile selectate
            self.afiseaza_selectia_filmului()

        tk.Button(
            self.root, text="Confirmă Rezervarea", command=confirma_rezervarea, font=("Arial", 12)
        ).pack(pady=10)

        tk.Button(
            self.root, text="Înapoi", command=self.afiseaza_selectia_locurilor, font=("Arial", 12)
        ).pack(pady=5)

    def arata_modificare_rezervari(self):
        # Curăță fereastra
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Modificare Rezervări", font=("Arial", 16)).pack(pady=10)

        # Bară de căutare
        bara_cautare = tk.Frame(self.root)
        bara_cautare.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(bara_cautare, text="Caută după Nume:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        camp_cautare = tk.Entry(bara_cautare, font=("Arial", 12))
        camp_cautare.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        buton_cautare = tk.Button(
            bara_cautare, 
            text="Caută", 
            font=("Arial", 12), 
            command=lambda: self.filtreaza_rezervari(camp_cautare.get())
        )
        buton_cautare.pack(side=tk.LEFT, padx=5)

        # Asociază tasta Enter pentru căutare
        camp_cautare.bind("<Return>", lambda event: self.filtreaza_rezervari(camp_cautare.get()))

        # Creare cadru cu scrollbar
        container = tk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(container, width=500)
        self.scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=700)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.afiseaza_rezervari()

        # Buton Înapoi
        tk.Button(
            self.root, text="Înapoi", command=self.afiseaza_selectia_locurilor, font=("Arial", 12)
        ).pack(pady=10)

    def afiseaza_rezervari(self, rezervari_filtrate=None):
        # Curăță cadrul scrollabil
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Încarcă rezervările din fișier
        with open(fisier_rezervari, "r") as file:
            rezervari = json.load(file)

        # Folosește rezervările filtrate dacă sunt disponibile
        if rezervari_filtrate is not None:
            rezervari_curente = rezervari_filtrate
        else:
            rezervari_curente = [
                r for r in rezervari
                if r["film"] == film_selectat["titlu"] and r["sala"] == film_selectat["sala"]
            ]

        # Afișează rezervările
        for rezervare in rezervari_curente:
            cadru = tk.Frame(self.scrollable_frame, bd=2, relief=tk.RIDGE, bg="lightgray", width=500)
            cadru.pack(fill=tk.X, expand=True, pady=5, padx=10)

            # Afișează ID-ul rezervării
            tk.Label(cadru, text=f"ID: {rezervare['id_rezervare']}", font=("Arial", 10, "bold"), bg="lightgray").pack(anchor="w", fill=tk.X)

            # Afișează alte detalii
            detalii = (
                f"Nume: {rezervare['nume']}\n"
                f"Locuri: {', '.join([f'{r+1}-{c+1}' for r, c in rezervare['locuri']])}\n"
                f"Adulți: {rezervare['adulti']} | Studenți: {rezervare['studenti']} | Copii: {rezervare['copii']}\n"
                f"Preț Total: {rezervare['pret_total']:.2f} RON"
            )
            tk.Label(cadru, text=detalii, font=("Arial", 10), bg="lightgray").pack(anchor="w", fill=tk.X)

            # Butoane pentru editare și ștergere
            cadru_butoane = tk.Frame(cadru, bg="lightgray")
            cadru_butoane.pack(fill=tk.X, pady=5)

            buton_editare = tk.Button(
                cadru_butoane, text="Editează", command=lambda r=rezervare: self.editeaza_rezervare(r), font=("Arial", 10)
            )
            buton_editare.pack(side=tk.LEFT, padx=5)

            buton_stergere = tk.Button(
                cadru_butoane, text="Șterge", command=lambda r=rezervare: self.sterge_rezervare(r), font=("Arial", 10)
            )
            buton_stergere.pack(side=tk.RIGHT, padx=5)

    def filtreaza_rezervari(self, text_cautare):
        # Încarcă rezervările din fișier
        with open(fisier_rezervari, "r") as file:
            rezervari = json.load(file)

        # Filtrează rezervările după textul introdus
        rezervari_filtrate = [
            r for r in rezervari
            if text_cautare.lower() in r["nume"].lower()
            and r["film"] == film_selectat["titlu"]
            and r["sala"] == film_selectat["sala"]
        ]

        # Afișează toate rezervările dacă textul introdus este gol
        if not text_cautare.strip():
            rezervari_filtrate = [
                r for r in rezervari
                if r["film"] == film_selectat["titlu"] and r["sala"] == film_selectat["sala"]
            ]

        # Actualizează rezervările afișate
        self.afiseaza_rezervari(rezervari_filtrate)

    def sterge_rezervare(self, rezervare):
        # Verifică dacă rezervarea conține cheia 'id_rezervare'
        if "id_rezervare" not in rezervare:
            messagebox.showerror("Eroare", "Datele rezervării sunt invalide. Nu se poate șterge.")
            return

        # Încarcă rezervările din fișier
        with open(fisier_rezervari, "r") as file:
            rezervari = json.load(file)

        # Filtrează rezervările, eliminând pe cea selectată
        rezervari = [r for r in rezervari if r.get("id_rezervare") != rezervare["id_rezervare"]]

        # Salvează modificările în fișier
        with open(fisier_rezervari, "w") as file:
            json.dump(rezervari, file, indent=4)

        # Actualizează interfața
        messagebox.showinfo("Succes", "Rezervarea a fost ștearsă cu succes!")
        self.afiseaza_rezervari()

    def editeaza_rezervare(self, rezervare):
        # Curăță fereastra
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Editează Rezervare", font=("Arial", 16)).pack(pady=10)

        # Nume
        tk.Label(self.root, text="Nume:", font=("Arial", 12)).pack()
        camp_nume = tk.Entry(self.root, font=("Arial", 12))
        camp_nume.insert(0, rezervare["nume"])  # Pre-populează cu numele curent
        camp_nume.pack(pady=5)

        # Numărul de bilete
        cadru = tk.Frame(self.root)
        cadru.pack(pady=5)

        tk.Label(cadru, text="Adulți:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        camp_adulti = tk.Entry(cadru, width=5, font=("Arial", 12))
        camp_adulti.insert(0, rezervare["adulti"])
        camp_adulti.grid(row=0, column=1, padx=5)

        tk.Label(cadru, text="Studenți:", font=("Arial", 12)).grid(row=0, column=2, padx=5)
        camp_studenti = tk.Entry(cadru, width=5, font=("Arial", 12))
        camp_studenti.insert(0, rezervare["studenti"])
        camp_studenti.grid(row=0, column=3, padx=5)

        tk.Label(cadru, text="Copii:", font=("Arial", 12)).grid(row=0, column=4, padx=5)
        camp_copii = tk.Entry(cadru, width=5, font=("Arial", 12))
        camp_copii.insert(0, rezervare["copii"])
        camp_copii.grid(row=0, column=5, padx=5)

        def salveaza_modificari():
            # Validare și salvare
            try:
                adulti = int(camp_adulti.get())
                studenti = int(camp_studenti.get())
                copii = int(camp_copii.get())
            except ValueError:
                messagebox.showerror("Eroare", "Numărul biletelor este invalid!")
                return

            total_bilete = adulti + studenti + copii
            if total_bilete != len(rezervare["locuri"]):
                messagebox.showerror("Eroare", "Numărul biletelor trebuie să corespundă cu locurile selectate!")
                return

            pret_total = (
                adulti * film_selectat["pret"] +
                studenti * (film_selectat["pret"] * 0.8) +
                copii * (film_selectat["pret"] * 0.5)
            )

            rezervare["nume"] = camp_nume.get()
            rezervare["adulti"] = adulti
            rezervare["studenti"] = studenti
            rezervare["copii"] = copii
            rezervare["pret_total"] = pret_total

            # Actualizare în fișier
            with open(fisier_rezervari, "r") as file:
                rezervari = json.load(file)

            # Înlocuiește rezervarea actualizată
            for i, r in enumerate(rezervari):
                if r["id_rezervare"] == rezervare["id_rezervare"]:
                    rezervari[i] = rezervare
                    break

            with open(fisier_rezervari, "w") as file:
                json.dump(rezervari, file, indent=4)

            messagebox.showinfo("Succes", "Rezervarea a fost actualizată cu succes!")
            self.arata_modificare_rezervari()

        # Buton pentru salvarea modificărilor
        tk.Button(
            self.root, text="Salvează Modificările", command=salveaza_modificari, font=("Arial", 12)
        ).pack(pady=10)

        # Buton pentru revenire
        tk.Button(
            self.root, text="Înapoi", command=self.arata_modificare_rezervari, font=("Arial", 12)
        ).pack(pady=5)


root = tk.Tk()

root.resizable(False, False)

app = AplicatieCinema(root)
root.mainloop()