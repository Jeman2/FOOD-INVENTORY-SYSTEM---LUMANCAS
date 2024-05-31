import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter
from tkinter import Label,PhotoImage
from tkinter import Tk, Entry, Label, Button, Checkbutton, StringVar, IntVar
from datetime import datetime

# Database functions
def create_table():
    conn = sqlite3.connect('resto.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS resto(
                   id TEXT PRIMARY KEY,
                   name TEXT,
                   in_stock INTEGER,
                   description TEXT,
                   price INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS login_logs(
                   id INTEGER PRIMARY KEY,
                   username TEXT,
                   login_time TEXT,
                   logout_time TEXT)''')
    conn.commit()
    conn.close()


def fetch_resto():
    conn = sqlite3.connect('resto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resto')
    resto = cursor.fetchall()
    conn.close()
    return resto

def insert_resto(id, name, stock,description,price):
    conn = sqlite3.connect('resto.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO resto(id, name, in_stock,description,price) VALUES (?, ?, ?, ?, ?)', (id, name, stock,description,price))
    conn.commit()
    conn.close()

def delete_resto(id):
    conn = sqlite3.connect('resto.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM resto WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def update_resto(new_name, new_stock,description,price, id):
    conn = sqlite3.connect('resto.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE resto SET name = ?, in_stock = ? ,  description= ?, price= ? WHERE id = ?', (new_name, new_stock,description,price, id))
    conn.commit()
    conn.close()

def id_exist(id):
    conn = sqlite3.connect('resto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM resto WHERE id = ?', (id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0
def insert_login_log(username, login_time):
    conn = sqlite3.connect('resto.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO login_logs(username, login_time) VALUES (?, ?)', (username, login_time))
    conn.commit()
    conn.close()
def insert_logout_log(username, logout_time):
    conn = sqlite3.connect('resto.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE login_logs SET logout_time = ? WHERE username = ? AND logout_time IS NULL", (logout_time, username))
    conn.commit()
    conn.close()
def delete_user_by_id(user_id):
    conn = sqlite3.connect('resto.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login_logs WHERE id=?", (user_id,))
    user = cursor.fetchone()
    if user:
        cursor.execute("DELETE FROM login_logs WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo(title="Deletion Success", message=f"User with ID {user_id} deleted successfully.")
    else:
        conn.close()
        messagebox.showerror(title="Error", message=f"User with ID {user_id} does not exist.")

def open_delete_user_window():
    global delete_user_window
    delete_user_window = Tk()
    delete_user_window.title("Delete User")
    delete_user_window.geometry("300x150+700+250")
    delete_user_window.resizable(50, 50)

    # Label and Entry for user input
    id_label = Label(delete_user_window, text="User ID:")
    id_label.grid(row=0, column=0, padx=15, pady=15)
    id_entry = Entry(delete_user_window)
    id_entry.grid(row=0, column=1, padx=15, pady=15)

    # Function to delete the user
    def delete_user():
        user_id = id_entry.get()
        if user_id:
            delete_user_by_id(int(user_id))
            delete_user_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter a valid user ID.")

    # Button to confirm deletion
    delete_button = Button(delete_user_window, text="Delete", command=delete_user)
    delete_button.grid(row=1, column=0, columnspan=2, padx=15, pady=15)

    delete_user_window.mainloop()

def display_data(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        id_entry.insert(0, row[0])
        name_entry.insert(0, row[1])
        stock_entry.insert(0, row[2])
        description_entry.insert(0, row[3])
        price_entry.insert(0,row[4])

def add_to_treeview():
    create_table()  # Ensure table exists
    sweetcorns = fetch_resto()
    tree.delete(*tree.get_children())
    for resto in sweetcorns:
        tree.insert('', tk.END, values=resto)

def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
        tree.focus('')
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    stock_entry.delete(0, tk.END)
    description_entry.delete(0,tk.END)
    price_entry.delete(0,tk.END)

def delete():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a product to delete')
    else:
        id = id_entry.get()
        delete_resto(id)
        add_to_treeview()
        clear()
     
        messagebox.showinfo('Success', 'Data has been deleted')

def update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a product to update')
    else:
        id = id_entry.get()
        name = name_entry.get()
        stock = stock_entry.get()
        description=description_entry.get()
        price=price_entry.get()
        update_resto(name, stock,price,description,id)
        add_to_treeview()
        clear()
       
        messagebox.showinfo('Success', 'Data has been updated')

def insert():
    id = id_entry.get()
    name = name_entry.get()
    stock = stock_entry.get()
    description=description_entry.get()
    price=price_entry.get()
    if not (id and name and stock and description and price):
        messagebox.showerror('Error', 'Enter all fields')
    elif id_exist(id):
        messagebox.showerror('Error', 'ID already exists')
    else:
        try:
            stock_value = int(stock)
            insert_resto(id, name, stock_value,description,price)
            add_to_treeview()
            clear()
            
            messagebox.showinfo('Success', 'Data has been inserted')
        except ValueError:
            messagebox.showerror('Error', 'Stock should be an integer')

# Main GUI
app = customtkinter.CTk()
app.title('Inventory Management System')
app.geometry('800x600+350+0')
app.config(bg='black')
app.resizable(False, False)

# Define global variables
login_window = None
authenticated = False

bg_image = PhotoImage(file="jeman.png")
bg_label = Label(app, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)




font1 = ('ARIAL', 12, 'bold')
font2 = ('ARIAL', 10, 'bold')
font3 = ('ARIAL', 12, 'bold')

def logout():
    global authenticated
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        authenticated = False
        logout_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_logout_log("jeman", logout_time)  # Replace "jeman" with the actual username
        app.withdraw()  # Hide the main app window
        open_login_window()  # Reopen the login window
    else:
        pass  # Do nothing if the user clicks "No"

# Listbox to display menu items

title_label = customtkinter.CTkLabel(app, text="INVENTORY OF\nPRODUCTS", font=font1, text_color="blue", fg_color="pink")
title_label.place(x=80, y=15)

frame = customtkinter.CTkFrame(app, bg_color='black', fg_color='pink', corner_radius=10, border_width=2, border_color='white', width=200, height=520)
frame.place(x=25, y=45)

id_label = customtkinter.CTkLabel(frame, font=font2, text='Item Id:', text_color='white', bg_color='black')
id_label.place(x=70, y=5)

id_entry = customtkinter.CTkEntry(frame, font=font2, text_color='#000', fg_color='#fff', border_color='#B2016C', border_width=2, width=160)
id_entry.place(x=20, y=30)

name_label = customtkinter.CTkLabel(frame, font=font2, text='Item Name:', text_color='white', bg_color='black')
name_label.place(x=65, y=60)

name_entry = customtkinter.CTkEntry(frame, font=font2, text_color='#000', fg_color='#fff', border_color='#B2016C', border_width=2, width=160)
name_entry.place(x=20, y=90)

stock_label = customtkinter.CTkLabel(frame, font=font2, text='Item Stock:', text_color='white', bg_color='black')
stock_label.place(x=65, y=120)

stock_entry = customtkinter.CTkEntry(frame, font=font2, text_color='#000', fg_color='#fff', border_color='#B2016C', border_width=2, width=160)
stock_entry.place(x=20, y=150)

description_label = customtkinter.CTkLabel(frame, font=font2, text='description:', text_color='white', bg_color='black')
description_label.place(x=65, y=180)

description_entry = customtkinter.CTkEntry(frame, font=font2, text_color='#000', fg_color='#fff', border_color='#B2016C', border_width=2, width=160)
description_entry.place(x=20, y=210)
price_label = customtkinter.CTkLabel(frame, font=font2, text='PRICE', text_color='white', bg_color='black')
price_label.place(x=75, y=240)

price_entry = customtkinter.CTkEntry(frame, font=font2, text_color='#000', fg_color='#fff', border_color='#B2016C', border_width=2, width=160)
price_entry.place(x=20, y=270)

add_button = customtkinter.CTkButton(frame, command=insert, font=font2, text_color='#fff', text='Add', fg_color='#047E43', hover_color='white', bg_color='pink', cursor='hand2', corner_radius=8, width=80)
add_button.place(x=15, y=380)

clear_button = customtkinter.CTkButton(frame, command=lambda: clear(True), font=font2, text_color='#fff', text='clear', fg_color='#047E43', hover_color='white', bg_color='pink', cursor='hand2', corner_radius=8, width=80)
clear_button.place(x=108, y=380)

update_button = customtkinter.CTkButton(frame, command=update, font=font2, text_color='#fff', text='update', fg_color='#047E43', hover_color='white', bg_color='pink', cursor='hand2', corner_radius=8, width=80)
update_button.place(x=15, y=430)

delete_button = customtkinter.CTkButton(frame, command=delete, font=font2, text_color='#fff', text='delete', fg_color='#047E43', hover_color='white', bg_color='pink', cursor='hand2', corner_radius=8, width=80)
delete_button.place(x=108, y=430)
delete_button1 = customtkinter.CTkButton(frame, command=open_delete_user_window,text_color='#fff', text="Delete user", font=font2,
                                        fg_color="#047e43", bg_color="pink",
                                        hover_color="white",
                                        corner_radius=8, cursor="hand2",width=80)
delete_button1.place(x=15, y=470)
logout_button = customtkinter.CTkButton(frame,command=logout, font=font2, text_color='#fff', text='logout', fg_color='#047E43', hover_color='white', bg_color='pink', cursor='hand2', corner_radius=8, width=80)
logout_button.place(x=108, y=470)

style = ttk.Style(app)
style.theme_use('clam')
style.configure('Treeview', font=font3, foreground='white', background='blue', fieldbackgrounds='white')
style.map('Treeview', background=[('selected', '#AA04A7')])

tree = ttk.Treeview(app, height=27)
tree['columns'] = ('ID', 'Name', 'InStock','Description','price')  # Change 'In stock' to 'InStock'
tree.heading('ID', text='ID')
tree.heading('Name', text='Name')
tree.heading('InStock', text='In Stock')  # Change 'In Stock' to 'InStock'
tree.heading('Description', text='description')
tree.heading('price', text='price')
tree.column('#0', width=0, stretch=tk.NO)
tree.column('ID', anchor=tk.CENTER, width=110)
tree.column('Name', anchor=tk.CENTER, width=110)
tree.column('InStock', anchor=tk.CENTER, width=110)
tree.column('Description', anchor=tk.CENTER, width=110)
tree.column('price', anchor=tk.CENTER, width=110)
tree.place(x=230, y=100)
tree.bind('<ButtonRelease>', display_data)

def authenticate(username, password):
    global authenticated
    if username == "jeman" and password == "jeman123":
        authenticated = True
        login_window.destroy()
        app.deiconify()  # Show the main app window
        login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_login_log(username, login_time)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
def toggle_password_visibility(password_entry, show_password_var):
    if show_password_var.get() == 1:
        password_entry.config(show="")
    else:
        password_entry.config(show="*")
def open_login_window():
    global login_window
    login_window = Tk()
    login_window.title("LUMANCAS FOOD INVENTORY SYSTEM")
    login_window.geometry("400x250+700+250")
    login_window.resizable(0,0)
    username_label = Label(login_window, text="Username:")
    username_label.grid(row=0, column=0, padx=15, pady=15)
    username_entry = Entry(login_window)
    username_entry.grid(row=0, column=1, padx=15, pady=15)

    password_label = Label(login_window, text="Password:")
    password_label.grid(row=1, column=0, padx=15, pady=15)
    password_var = StringVar()
    password_entry = Entry(login_window, show="*", textvariable=password_var)
    password_entry.grid(row=1, column=1, padx=15, pady=15)

    show_password_var = IntVar()
    show_password_checkbox = Checkbutton(login_window, text="Show Password", variable=show_password_var,
                                         command=lambda: toggle_password_visibility(password_entry, show_password_var, password_var))
    show_password_checkbox.grid(row=2, columnspan=2, padx=15, pady=5)

    login_button = Button(login_window, text="Login", command=lambda: authenticate(username_entry.get(), password_entry.get()))
    login_button.grid(row=3, column=0, columnspan=2, padx=15, pady=15)

    # Bind the <Return> key to the login button
    login_window.bind("<Return>", lambda event: login_button.invoke())

    login_window.mainloop()



add_to_treeview()
open_login_window()

app.mainloop()
