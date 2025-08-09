import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def choisir_dossier():
    dossier = filedialog.askdirectory(title="Sélectionnez le dossier du projet Git")
    if dossier:
        return dossier
    else:
        messagebox.showwarning("Avertissement", "Aucun dossier sélectionné.")
        return None

def afficher_derniere_branche():
    dossier = choisir_dossier()
    if not dossier:
        return
    try:
        cmd = 'git for-each-ref --sort=creatordate --format="%(creatordate:short) %(refname:short)" refs/heads/ | tail -n 1'
        resultat = subprocess.check_output(cmd, cwd=dossier, shell=True, text=True).strip()
        if resultat:
            messagebox.showinfo("Dernière branche", f"Dernière branche créée :\n{resultat}")
        else:
            messagebox.showwarning("Aucune branche", "Aucune branche trouvée dans ce dossier.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Erreur", "Ce dossier n'est pas un dépôt Git valide.")
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Git n'est pas installé ou n'est pas dans le PATH.")

def afficher_toutes_branches():
    dossier = choisir_dossier()
    if not dossier:
        return
    try:
        cmd = 'git for-each-ref --sort=creatordate --format="%(creatordate:short) %(refname:short)" refs/heads/'
        resultat = subprocess.check_output(cmd, cwd=dossier, shell=True, text=True).strip()
        if resultat:
            # Afficher dans une nouvelle fenêtre scrollable
            fenetre = tk.Toplevel(root)
            fenetre.title("Toutes les branches avec leur date de création")
            fenetre.geometry("400x400")
            text = tk.Text(fenetre, wrap=tk.NONE)
            scrollbar_y = tk.Scrollbar(fenetre, orient=tk.VERTICAL, command=text.yview)
            scrollbar_x = tk.Scrollbar(fenetre, orient=tk.HORIZONTAL, command=text.xview)
            text.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
            scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            text.insert(tk.END, resultat)
            text.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("Aucune branche", "Aucune branche trouvée dans ce dossier.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Erreur", "Ce dossier n'est pas un dépôt Git valide.")
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Git n'est pas installé ou n'est pas dans le PATH.")

root = tk.Tk()
root.title("GitLastBranch - Outil Branches Git")
root.geometry("320x180")

label = tk.Label(root, text="Sélectionnez une option :", font=("Arial", 12))
label.pack(pady=10)

btn_derniere = tk.Button(root, text="Afficher la dernière branche créée", width=30, command=afficher_derniere_branche)
btn_derniere.pack(pady=5)

btn_toutes = tk.Button(root, text="Afficher toutes les branches avec dates", width=30, command=afficher_toutes_branches)
btn_toutes.pack(pady=5)

root.mainloop()
