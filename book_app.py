import tkinter as tk
from tkinter import messagebox
import requests

class BookApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Book App")

        self.label = tk.Label(master, text="Laboratorium PAMIW - aplikacja desktopowa")
        self.label.pack()

        self.book_listbox = tk.Listbox(master, width=50, height=10)
        self.book_listbox.pack()

        self.navigation_frame = tk.Frame(master)
        self.navigation_frame.pack()
        self.page_label = tk.Label(self.navigation_frame, text="Numer strony:")
        self.page_label.grid(row=0, column=0, padx=5, pady=5)
        self.page_entry = tk.Entry(self.navigation_frame)
        self.page_entry.grid(row=0, column=1, padx=5, pady=5)
        self.per_page_label = tk.Label(self.navigation_frame, text="Liczba elementów na stronie:")
        self.per_page_label.grid(row=0, column=2, padx=5, pady=5)
        self.per_page_entry = tk.Entry(self.navigation_frame)
        self.per_page_entry.grid(row=0, column=3, padx=5, pady=5)
        self.add_button = tk.Button(self.navigation_frame, text="Pobierz Listę Książek", command=self.fetch_books)
        self.add_button.grid(row=0, column=4, padx=5, pady=5)

        self.add_frame = tk.Frame(master)
        self.add_frame.pack()
        self.title_label = tk.Label(self.add_frame, text="Tytuł:")
        self.title_label.grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.add_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.author_label = tk.Label(self.add_frame, text="Autor:")
        self.author_label.grid(row=0, column=2, padx=5, pady=5)
        self.author_entry = tk.Entry(self.add_frame)
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)
        self.add_button = tk.Button(self.add_frame, text="Dodaj Książkę", command=self.add_book)
        self.add_button.grid(row=0, column=4, padx=5, pady=5)

        self.delete_frame = tk.Frame(master)
        self.delete_frame.pack()
        self.delete_id_label = tk.Label(self.delete_frame, text="ID Książki do usunięcia:")
        self.delete_id_label.grid(row=0, column=0, padx=5, pady=5)
        self.delete_id_entry = tk.Entry(self.delete_frame)
        self.delete_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.delete_button = tk.Button(self.delete_frame, text="Usuń Książkę", command=self.delete_book)
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)

        self.edit_frame = tk.Frame(master)
        self.edit_frame.pack()
        self.edit_id_label = tk.Label(self.edit_frame, text="ID Książki do edycji:")
        self.edit_id_label.grid(row=0, column=0, padx=5, pady=5)
        self.edit_id_entry = tk.Entry(self.edit_frame)
        self.edit_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.new_title_label = tk.Label(self.edit_frame, text="Nowy Tytuł:")
        self.new_title_label.grid(row=0, column=2, padx=5, pady=5)
        self.new_title_entry = tk.Entry(self.edit_frame)
        self.new_title_entry.grid(row=0, column=3, padx=5, pady=5)
        self.new_author_label = tk.Label(self.edit_frame, text="Nowy Autor:")
        self.new_author_label.grid(row=0, column=4, padx=5, pady=5)
        self.new_author_entry = tk.Entry(self.edit_frame)
        self.new_author_entry.grid(row=0, column=5, padx=5, pady=5)
        self.edit_button = tk.Button(self.edit_frame, text="Edytuj Książkę", command=self.edit_book)
        self.edit_button.grid(row=0, column=6, padx=5, pady=5)

    def fetch_books(self):
        page_str = self.page_entry.get()
        per_page_str = self.per_page_entry.get()

        if not page_str or not per_page_str:
            messagebox.showerror("Błąd", "Wprowadź numer strony i liczbę elementów na stronie.")
            return

        try:
            page = int(page_str)
            per_page = int(per_page_str)
            self.fetch_books_by_page(page, per_page)
        except ValueError:
            messagebox.showerror("Błąd", "Numer strony i liczba elementów na stronie muszą być liczbami całkowitymi.")

    def fetch_books_by_page(self, page, per_page):
        try:
            response = requests.get(f'http://localhost:5000/books?page={page}&per_page={per_page}')
            response.raise_for_status()

            books = response.json()

            self.book_listbox.delete(0, tk.END)

            if books:
                for book in books['books']:
                    book_info = f"ID: {book['id']}, Tytuł: {book['title']}, Autor: {book['author']}"
                    self.book_listbox.insert(tk.END, book_info)
            else:
                self.book_listbox.insert(tk.END, "Brak dostępnych książek.")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas pobierania listy książek: {e}")

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()

        if not title or not author:
            messagebox.showwarning("Uwaga", "Wprowadź tytuł i autora książki.")
            return

        try:
            new_book_data = {'title': title, 'author': author}

            response = requests.post('http://localhost:5000/books', json=new_book_data)
            response.raise_for_status()

            new_book = response.json()
            messagebox.showinfo("Sukces", f"Dodano nową książkę: ID={new_book['id']}, Tytuł={new_book['title']}, Autor={new_book['author']}")
            self.fetch_books()

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas dodawania nowej książki: {e}")

    def delete_book(self):
        book_id = self.delete_id_entry.get()

        if not book_id:
            messagebox.showwarning("Uwaga", "Wprowadź ID książki do usunięcia.")
            return

        try:
            response = requests.delete(f'http://localhost:5000/books/{book_id}')
            response.raise_for_status()

            deleted_book = response.json()
            messagebox.showinfo("Sukces", f"Usunięto książkę o ID: {book_id}")

            self.fetch_books()

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas usuwania książki: {e}")

    def edit_book(self):
        book_id = self.edit_id_entry.get()
        new_title = self.new_title_entry.get()
        new_author = self.new_author_entry.get()

        if not book_id or not new_title or not new_author:
            messagebox.showwarning("Uwaga", "Wprowadź ID książki do edycji oraz nowy tytuł i autora.")
            return

        try:
            edited_book_data = {'title': new_title, 'author': new_author}

            response = requests.put(f'http://localhost:5000/books/{book_id}', json=edited_book_data)
            response.raise_for_status()

            edited_book = response.json()
            messagebox.showinfo("Sukces", f"Zaktualizowano książkę o ID: {book_id}")

            self.fetch_books()

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas edycji książki: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookApp(root)
    root.mainloop()
