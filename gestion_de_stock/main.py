import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import pandas as pd

class Stock:
    def __init__(self, root, mdp):
        self.root = root
        self.root.title("Gestion de Stock")

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mdp,
            database="store"
        )
        self.cursor = self.conn.cursor()

        self.tree = ttk.Treeview(root, columns=("ID", "Nom", "Description", "Prix", "Quantité", "Catégorie"))
        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("ID", text="ID", anchor="w")
        self.tree.heading("Nom", text="Nom", anchor="w")
        self.tree.heading("Description", text="Description", anchor="w")
        self.tree.heading("Prix", text="Prix", anchor="w")
        self.tree.heading("Quantité", text="Quantité", anchor="w")
        self.tree.heading("Catégorie", text="Catégorie", anchor="w")
        self.tree.pack()

        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Ajouter Produit", command=self.add_product).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Modifier Produit", command=self.edit_product).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Supprimer Produit", command=self.delete_product).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Ajouter Categorie", command=self.add_category).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Exporter CSV", command=self.export_csv).grid(row=0, column=4, padx=5)

        self.load_data()

    def run_query(self, query, parameters=()):
        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()

    def load_data(self):
        query = "SELECT product.id, product.name, product.description, product.price, product.quantity, category.name " \
                "FROM product JOIN category ON product.id_category = category.id"
        result = self.run_query(query)

        for record in self.tree.get_children():
            self.tree.delete(record)

        for row in result:
            self.tree.insert("", "end", values=row)

    def add_product(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Ajouter un produit")

        name_var = tk.StringVar()
        description_var = tk.StringVar()
        price_var = tk.DoubleVar()
        quantity_var = tk.IntVar()
        category_var = tk.StringVar()

        ttk.Label(add_window, text="Nom du produit:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(add_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(add_window, textvariable=description_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Prix:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(add_window, textvariable=price_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Quantité:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(add_window, textvariable=quantity_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Catégorie:").grid(row=4, column=0, padx=5, pady=5)

        categories = self.get_categories()
        category_menu = ttk.Combobox(add_window, textvariable=category_var, values=categories)
        category_menu.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(add_window, text="Ajouter", command=lambda: self.add_product_to_db(
            name_var.get(), description_var.get(), price_var.get(), quantity_var.get(), category_var.get())).grid(row=5, column=0, columnspan=2, pady=10)

    def add_category(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Ajouter une categorie")

        name_var = tk.StringVar()

        ttk.Label(add_window, text="Nom de la catégorie:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(add_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(add_window, text="Ajouter", command=lambda: self.add_category_to_db(name_var.get())).grid(row=1, column=0, columnspan=2, pady=10)

    def add_category_to_db(self, name):
        try:
            query = "INSERT INTO category (name) VALUES (%s)"
            value = (name,)
            self.run_query(query, value)
            self.conn.commit()

            self.load_data()

            messagebox.showinfo("Ajout de categorie", "Categorie ajouté avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout d'une categorie : {str(e)}")

    def add_product_to_db(self, name, description, price, quantity, category):
        try:
            category_id = self.get_category_id(category)

            query = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)"
            values = (name, description, price, quantity, category_id)
            self.run_query(query, values)
            self.conn.commit()

            self.load_data()

            messagebox.showinfo("Ajout de produit", "Produit ajouté avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout du produit : {str(e)}")

    def edit_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à modifier")
            return

        selected_values = self.tree.item(selected_item, "values")

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Modifier un produit")

        name_var = tk.StringVar(value=selected_values[1])
        description_var = tk.StringVar(value=selected_values[2])
        price_var = tk.DoubleVar(value=selected_values[3])
        quantity_var = tk.IntVar(value=selected_values[4])
        category_var = tk.StringVar(value=selected_values[5])

        ttk.Label(edit_window, text="Nom du produit:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(edit_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(edit_window, textvariable=description_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Prix:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(edit_window, textvariable=price_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Quantité:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(edit_window, textvariable=quantity_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Catégorie:").grid(row=4, column=0, padx=5, pady=5)

        categories = self.get_categories()
        category_menu = ttk.Combobox(edit_window, textvariable=category_var, values=categories)
        category_menu.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(edit_window, text="Modifier", command=lambda: self.edit_product_in_db(
            selected_values[0], name_var.get(), description_var.get(), price_var.get(), quantity_var.get(),
            category_var.get())).grid(row=5, column=0, columnspan=2, pady=10)

    def edit_product_in_db(self, product_id, name, description, price, quantity, category):
        try:
            category_id = self.get_category_id(category)

            query = "UPDATE product SET name=%s, description=%s, price=%s, quantity=%s, id_category=%s WHERE id=%s"
            values = (name, description, price, quantity, category_id, product_id)
            self.run_query(query, values)
            self.conn.commit()

            self.load_data()

            messagebox.showinfo("Modification de produit", "Produit modifié avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification du produit : {str(e)}")

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à supprimer")
            return

        confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce produit ?")
        if confirmation:
            selected_id = self.tree.item(selected_item, "values")[0]

            query = "DELETE FROM product WHERE id=%s"
            self.run_query(query, (selected_id,))
            self.conn.commit()

            self.load_data()

            messagebox.showinfo("Suppression de produit", "Produit supprimé avec succès.")

    def export_csv(self):
        query = "SELECT * FROM product"
        result = self.run_query(query)

        df = pd.DataFrame(result, columns=["ID", "Nom", "Description", "Prix", "Quantité", "ID Catégorie"])
        df.to_csv("stock_data.csv", index=False)
        messagebox.showinfo("Export CSV", "Les données ont été exportées avec succès")

    def get_categories(self):
        query = "SELECT name FROM category"
        result = self.run_query(query)
        categories = [row[0] for row in result]
        return categories

    def get_category_id(self, category_name):
        query = "SELECT id FROM category WHERE name=%s"
        result = self.run_query(query, (category_name,))
        if result:
            return result[0][0]
        else:
            messagebox.showwarning("Avertissement", f"La catégorie '{category_name}' n'a pas été trouvée")
            return None

root = tk.Tk()
app = Stock(root, input("Quel est votre mot de passe : "))
root.mainloop()
