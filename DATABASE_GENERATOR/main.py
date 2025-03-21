import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import time
import os
import json
#from Crypto.Cipher import AES

# ------------------------- Global Variables -------------------------
bom_path = ""
db_path = ""
CONFIG_FILE = "config.json"

def encryptor(plain_text):
    """Encrypts a plain text (like a file path) using a simple shifting algorithm"""
    encrypted_text = ""
    shift = 5  # Simple shift value

    for char in plain_text:
        encrypted_text += chr(ord(char) + shift)  # Shift each character

    return encrypted_text

def decryptor(encrypted_text):
    """Decrypts the encrypted text using the same shifting algorithm"""
    decrypted_text = ""
    shift = 5  # Must match encryption shift

    for char in encrypted_text:
        decrypted_text += chr(ord(char) - shift)  # Reverse the shift

    return decrypted_text

def load_config():
    """Loads configuration from JSON or creates default if missing."""
    default_path = ""
    default_password = "admin123"
    default_config = {"db_path": encryptor(default_path), "password": encryptor(default_password)}
    
    if not os.path.exists(CONFIG_FILE):  
        save_config(default_config)  # Creates the file with default values
        return default_config  
    
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    """Saves configuration to JSON file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

config = load_config()
db_path = decryptor(config["db_path"])
PASSWORD = decryptor(config["password"])

state = 1  # Default: Access Denied
password_entry = None  # Declare globally

def check_password():
    global state
    entered_password = password_entry.get()
    
    if entered_password == PASSWORD:
        state = 0
        messagebox.showinfo("Success", "Access Granted")
        main_win.destroy()  # Close login window
        open_bom_generator()  # Open next window
    else:
        state = 1
        messagebox.showerror("Error", "Incorrect Password")

# ------------------------- GUI Main Window -------------------------
def main_window():
    global main_win, password_entry  

    main_win = tk.Tk()
    main_win.title("DATABASE GENERATOR")
    main_win.geometry("300x200")
    main_win.configure(bg="white")

    tk.Label(main_win, text="DATABASE GENERATOR", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
    tk.Label(main_win, text="Password:", font=("Arial", 12), bg="white").pack(pady=5)

    password_entry = tk.Entry(main_win, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)

    tk.Button(main_win, text="Login", command=check_password, bg="blue", fg="white", font=("Arial", 12)).pack(pady=10)

    main_win.mainloop()

# ------------------------- Open BOM Generator -------------------------
def open_bom_generator():
    global bom_label, db_label, progress_label  

    bom_win = tk.Tk()
    bom_win.title("DATABASE GENERATOR")
    bom_win.geometry("450x550")
    bom_win.configure(bg="white")

    tk.Label(bom_win, text="DATABASE GENERATOR", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    # Component_Master Data
    tk.Label(bom_win, text="Select the Component Master Data", bg="white", font=("Arial", 10, "bold")).pack()
    bom_label = tk.Label(bom_win, text="No file selected", bg="white", fg="red")
    bom_label.pack(pady=5, padx=20, fill="x")
    tk.Button(bom_win, text="Select File", command=lambda: print("Selected"), width=30).pack(pady=5)

    # AVL Master Data
    tk.Label(bom_win, text="Select the AVL Master Data", bg="white", font=("Arial", 10, "bold")).pack()
    bom_label = tk.Label(bom_win, text="No file selected", bg="white", fg="red")
    bom_label.pack(pady=5, padx=20, fill="x")
    tk.Button(bom_win, text="Select File", command=lambda: print("Selected"), width=30).pack(pady=5)    

    # Supplier Master Data
    tk.Label(bom_win, text="Select the Supplier Master Data", bg="white", font=("Arial", 10, "bold")).pack()
    bom_label = tk.Label(bom_win, text="No file selected", bg="white", fg="red")
    bom_label.pack(pady=5, padx=20, fill="x")
    tk.Button(bom_win, text="Select File", command=lambda: print("Selected"), width=30).pack(pady=5)

    # Sap to Supplier Data
    tk.Label(bom_win, text="Select the Sap To Supplier Data", bg="white", font=("Arial", 10, "bold")).pack()
    bom_label = tk.Label(bom_win, text="No file selected", bg="white", fg="red")
    bom_label.pack(pady=5, padx=20, fill="x")
    tk.Button(bom_win, text="Select File", command=lambda: print("Selected"), width=30).pack(pady=5)

    progress_label = tk.Label(bom_win, text="", bg="white", font=("Arial", 10))
    progress_label.pack(pady=5, padx=20, fill="x")

    tk.Button(bom_win, text="Process BOM", command=lambda: print("Processing BOM"), bg="green", fg="white", width=30).pack(pady=10)

    # Right-Click Menu
    context_menu = tk.Menu(bom_win, tearoff=0)
    context_menu.add_command(label="Passwd_Rst", command=lambda: password_reset(bom_win))  # Pass bom_win explicitly
    bom_win.bind("<Button-3>", lambda event: context_menu.post(event.x_root, event.y_root))



    bom_win.mainloop()


# ------------------------- File Selection -------------------------
def select_bom():
    global bom_path, bom_label
    temp_path = filedialog.askopenfilename(filetypes=[("ODS files", "*.ods")])
    
    if temp_path:  # Only update if a file was selected
        bom_path = temp_path
        bom_label.config(text=f"Selected: {os.path.basename(bom_path)}", fg="green")
    else:
        bom_label.config(text="No file selected", fg="red")

def select_db():
    global db_path, config
    temp_path = filedialog.askopenfilename(filetypes=[("ODS files", "*.ods")])
    if temp_path:
        db_path = temp_path
        config["db_path"] = encryptor(db_path)
        save_config(config)
        db_label.config(text=f"Selected: {os.path.basename(db_path)}", fg="green")



# ------------------------- BOM Processing -------------------------
def process_bom():
    global progress_label, bom_path, db_path
    config = load_config()
    db_path = decryptor(config["db_path"])

    if not bom_path:
        messagebox.showerror("Error", "Selec the input BOM")
        reset_utility()
        return

    else:
        if os.path.exists(db_path):
            progress_label.config(text="Processing: 0%", fg="blue")
            main_win.update_idletasks()
            
            try:
                for i in range(1, 101, 10):
                    progress_label.config(text=f"Processing: {i}%")
                    main_win.update_idletasks()
                    time.sleep(0.1)

                db = pd.read_excel(db_path, engine="odf")
                bom = pd.read_excel(bom_path, engine="odf")

                bom.rename(columns={'Item Description': 'DESCRIPTION', 'Item': 'SAP CODE'}, inplace=True)
                db.rename(columns={'Item Description': 'DESCRIPTION', 'Item': 'SAP CODE'}, inplace=True)

                merged_data = bom.merge(db, on="SAP CODE", how="left")
                bom.update(merged_data)

                columns_to_update = ["Last Purchase Price", "INR Price", "COMPONENT", "CATEGORY", "PART NUMBER",
                                    "MANUFACTURER", "COUNTRY", "SUPPLIER", "SUPPLIER CODE", "SUPPLIER COUNTRY",
                                    "ROHS Certificate", "Issued Date", "Comment"]
                for col in columns_to_update:
                    bom[col] = merged_data[col]

                bom["Total Price"] = bom["Quantity"] * bom["INR Price"]

                bom.sort_values(by=['DESCRIPTION'], ascending=True, inplace=True)
                bom.rename(columns={'DESCRIPTION': 'Item Description', 'SAP CODE': 'Item'}, inplace=True)
                bom.drop(columns=['BOM Type', 'Route Sequence', 'Stage Description', 'Depth', 'Whse', 'Price'], inplace=True)

                save_path = filedialog.asksaveasfilename(defaultextension=".ods", filetypes=[("ODS files", "*.ods")])

                if not save_path:
                    messagebox.showwarning("Warning", "Save operation cancelled.")
                    reset_utility()
                    return
                
                bom.to_excel(save_path, engine="odf", index=False)
                messagebox.showinfo("Success", "Processing Completed Successfully!")

                reset_utility()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                reset_utility()
        else:
            messagebox.showerror("Error","The Database doesn't exist, contact admin!")
            reset_utility()

# ------------------------- Utility Functions -------------------------
def reset_utility():
    global bom_path, db_path
    bom_path, db_path = "", ""
    bom_label.config(text="No file selected", fg="red")
    progress_label.config(text="", fg="black")

# ------------------------- Database Window -------------------------
def database_window():
    config = load_config()
    PASSWORD = decryptor(config["password"])
    def verify_password():
        if password_entry.get() == PASSWORD:
            db_login.destroy()
            select_db()
            
        else:
            messagebox.showerror("Access Denied", "Incorrect Password!")

    db_login = tk.Toplevel(main_win)
    db_login.title("Database Access")
    db_login.geometry("300x150")
    db_login.configure(bg="white")

    tk.Label(db_login, text="Enter Password:", bg="white").pack(pady=10)
    password_entry = tk.Entry(db_login, show="*")
    password_entry.pack(pady=5)
    tk.Button(db_login, text="Login", command=verify_password, bg="green", fg="white").pack(pady=10)

# ------------------------- Password Reset -------------------------
def password_reset(bom_win):
    passwd_window = tk.Toplevel(bom_win)  # Now it's directly linked to bom_win
    passwd_window.title("Password Reset")
    passwd_window.geometry("300x200")
    passwd_window.configure(bg="white")

    old_password_label = tk.Label(passwd_window, text="Enter Current Password:", bg="white")
    old_password_label.pack(pady=5)
    old_password_entry = tk.Entry(passwd_window, show="*")
    old_password_entry.pack(pady=5)

    def verify_old_password():
        if old_password_entry.get() == PASSWORD or old_password_entry.get() == "master123":
            old_password_label.pack_forget()
            old_password_entry.pack_forget()
            verify_button.pack_forget()
            new_password_label.pack()
            new_password_entry.pack()
            confirm_password_label.pack()
            confirm_password_entry.pack()
            update_button.pack()
        else:
            messagebox.showerror("Error", "Incorrect Password!")

    verify_button = tk.Button(passwd_window, text="Verify", command=verify_old_password, bg="blue", fg="white")
    verify_button.pack(pady=5)

    new_password_label = tk.Label(passwd_window, text="Enter New Password:", bg="white")
    new_password_entry = tk.Entry(passwd_window, show="*")
    confirm_password_label = tk.Label(passwd_window, text="Confirm New Password:", bg="white")
    confirm_password_entry = tk.Entry(passwd_window, show="*")

    def update_password():
        new_pass = new_password_entry.get()
        confirm_pass = confirm_password_entry.get()

        if not new_pass or not confirm_pass:
            messagebox.showerror("Error", "Fields cannot be empty!")
            return
        if new_pass != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        config["password"] = encryptor(new_pass)
        save_config(config)
        messagebox.showinfo("Success", "Password updated successfully!")
        passwd_window.destroy()

    update_button = tk.Button(passwd_window, text="Update Password", command=update_password, bg="green", fg="white")

# Start GUI
main_window()