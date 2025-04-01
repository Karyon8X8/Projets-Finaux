import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from collections import deque

class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Explorateur de fichiers")
        self.root.geometry("800x500")

        #Création de la barre latérale
        self.sidebar= tk.Frame(self.root, width=150, bg="lightgray")
        self.sidebar.pack(side="left", fill="y")

        self.sidebar_buttons = {
            "Recents": self.show_recents,
            "Favorites": self.show_favorites,
            "Computer": self.show_message,
            "Tags": self.show_message,
        }
        for text, command in self.sidebar_buttons.items():
            bt= tk.Button(self.sidebar, text=text, relief="flat", bg="lightgray", command=command)
            bt.pack(fill="x", padx=5, pady=2)

        #Conteneur principal
        self.main_frame= tk.Frame(self.root)
        self.main_frame.pack(side="right", expand=True, fill="both")

        #Construction de la barre de chemin d'accè
        self.path_var= tk.StringVar()
        self.path_entry= tk.Entry(self.main_frame, textvariable=self.path_var)
        self.path_entry.pack(fill="x", padx=5, pady=5)
        self.path_entry.bind("<Return>", self.change_directory)

        #Liste des éléments
        self.file_list = tk.Listbox(self.main_frame, selectmode="browse")
        self.file_list.pack(expand=True, fill="both", padx=5, pady=5)
        self.file_list.bind("<Double-Button-1>", self.open_item)


        #Options du menu contextuel
        self.context_menu= tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Ouvrir", command= self.open_item)
        self.context_menu.add_command(label="Renommer", command= self.rename_item)
        self.context_menu.add_command(label="Supprimer", command= self.delete_item)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Copier", command=self.copy_item)
        self.context_menu.add_command(label="Coller", command=self.paste_item)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Ajouter aux favoris", command=self.add_to_favorites)
        self.file_list.bind("<Button-3>", self.show_context_menu)

        #Initialisation
        self.current_path = os.getcwd()
        self.clipboard= None
        self.favorites = set()
        self.recents = deque(maxlen=None) #Stocke les fichiers visités récemment
        self.update_file_list()

    def show_message(self, text= None):
        messagebox.showinfo("Info", f"Section:{text}")

    def update_file_list(self):
        """Met à jour l'affichage de la liste des fichiers.""" 
        self.file_list.delete(0, tk.END)
        self.path_var.set(self.current_path)

        try:
            items = os.listdir(self.current_path)
            for item in items:
                self.file_list.insert(tk.END, item)
        except PermissionError:
            messagebox.showerror("Erreur", "Accès refusé")

    def change_directory(self, event=None):
        """Change de répertoire."""
        new_path= self.path_var.get()
        if os.path.isdir(new_path):
            self.current_path= new_path
            self.update_file_list()
        else:
            messagebox.showerror("Erreur", "Dossier invalide")
    
    def open_item(self, event= None):
        """Ouvre un fichier ou un dossier."""
        try:
            selected = self.file_list.get(self.file_list.curselection())
            path= os.path.join(self.current_path, selected)
            if os.path.isdir(path):
                self.current_path= path
                self.update_file_list()
            else:
                os.startfile(path)
                self.add_to_recent(path) #Ajoute le fichier aux fichiers récemment consusltés
        except:
            pass

    def rename_item(self):
        """Renomme un fichier."""
        try:
            selected = self.file_list.get(self.file_list.curselection())
            new_name= simpledialog.askstring("Renommer", "Nouveau nom :", initialvalue=selected)
            if new_name:
                old_path= os.path.join(self.current_path, selected)
                new_path= os.path.join(self.current_path, new_name)
                os.rename(old_path, new_path)
                self.update_file_list()
        except:
            pass

    def delete_item(self):
        """Supprime un fichier."""
        try:
            selected = self.file_list.get(self.current_path, selected)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
                self.update_file_list()
        except:
            pass

    def add_to_favorites(self):
        """Ajoute un fichier aux favoris."""
        try:
            selected =self.file_list.get(self.file_list.curselection())
            path = os.path.join(self.current_path, selected)
            self.favorites.add(path)
            messagebox.showinfo("Favoris", f"{selected} a été ajouté aux favoris!")
        except:
            pass

    def add_to_recent(self, path):
        """Ajoute un fichier aux fichiers récemment consultés"""
        if path not in self.recent_files:
            self.recents.appendleft(path) #Ajoute le fichier en haut de la liste

    def show_favorites(self):
        """Affiche les fichiers favoris."""
        self.file_list.delete(0, tk.END)
        for item in self.favorites:
            self.file_list.insert(tk.END, item)
    
    def show_recents(self):
        """Affiche les fichiers récents."""
        self.file_list.delete(0, tk.END, os.path.basename(item))

    def show_context_menu(self, event):
        """Affiche le menu contextuel."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def copy_item(self):
        print("Fonction de copie non encore implémentée.")

    def paste_item(self):
        print("Fonction de collage non encore implémentée.")

if __name__=="__main__":
    root= tk.Tk()
    app = FileExplorer(root)
    root.mainloop()