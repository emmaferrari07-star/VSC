import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
import webbrowser

print("--- TENTATIVO DI APERTURA FINESTRA ---")

# Creiamo la finestra base (usiamo quella standard del Mac per non fallire)
root = tk.Tk()
root.title("Il mio Cacciatore di Notizie")
root.geometry("500x400")

label_titolo = tk.Label(root, text="📰 Le mie Notizie", font=("Arial", 20))
label_titolo.pack(pady=20)

def carica():
    percorso = "Risultati/notizie.xlsx"
    if os.path.exists(percorso):
        df = pd.read_excel(percorso)
        for i, row in df.head(5).iterrows(): # Mostriamo solo le prime 5
            btn = tk.Button(root, text=row['title'][:50] + "...", 
                            command=lambda u=row['url']: webbrowser.open(u))
            btn.pack(pady=5, fill="x")
        print("✅ Notizie caricate nella finestra.")
    else:
        messagebox.showerror("Errore", "File Excel non trovato!")

btn_check = tk.Button(root, text="CARICA ORA", command=carica, bg="blue", fg="white")
btn_check.pack(pady=20)

print("--- SE LEGGI QUESTO, LA FINESTRA DOVREBBE ESSERE APERTA ---")

root.mainloop()