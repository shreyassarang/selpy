#pyinstaller --onefile --noconsole --icon=your_icon.ico your_script.py
import tkinter as tk
from tkinter import messagebox, filedialog
import barcode
from barcode.writer import ImageWriter 
import os
import json

CONFIG_FILE = "bar_code_destinationpath.json"

def load_config():
    """Loads the saved destination folder from config.json or creates one if missing."""
    if not os.path.exists(CONFIG_FILE):
        save_config("")  # Create config.json with empty path if it doesn't exist
    with open(CONFIG_FILE, "r") as file:
        data = json.load(file)
        return data.get("folder_path", "")

def save_config(folder_path):
    """Saves the selected destination folder to config.json."""
    with open(CONFIG_FILE, "w") as file:
        json.dump({"folder_path": folder_path}, file)

def select_destination():
    """Allows the user to select a folder and stores the path."""
    global folder_path
    folder_path = filedialog.askdirectory(title="Select Destination Folder")
    if folder_path:
        save_config(folder_path)
        messagebox.showinfo("Success", f"Folder Selected: {folder_path}")
        reset_gui()
    else:
        messagebox.showwarning("Warning", "No folder selected. Please set a path.")
        reset_gui()

def save_barcode_as_png(code):
    """Generates and saves the barcode as a PNG file in the stored directory."""
    global folder_path
    if not folder_path:
        messagebox.showwarning("Warning", "No folder selected. Please set a destination folder first.")
        return
    
    barcode_class = barcode.get_barcode_class('code128')
    generated_barcode = barcode_class(code, writer=ImageWriter())

    filename = os.path.join(folder_path, f"{code}")
    generated_barcode.save(filename)
    
    messagebox.showinfo("Success", f"Barcode saved at:\n{filename}")

def generate_barcode():
    """Handles user input, validation, and barcode generation."""
    code = entry.get().strip()
    folder_path = load_config()
    if not code:
        messagebox.showerror("Error", "Enter a code")
        return
    
    if folder_path == "" :
        #select_destination()  # Prompt user to select a folder if none set
        messagebox.showerror("Error", "No Destination Folder Selected")
        reset_gui()

    if folder_path:
        save_barcode_as_png(code)
        entry.delete(0, tk.END)  # Clear the text box

def reset_gui():
    """Clears the entry field and resets the GUI to its initial state."""
    entry.delete(0, tk.END)  # Clear the text

def main_window():
    """Sets up the GUI."""
    global entry, folder_path
    
    folder_path = load_config()  # Load or initialize config

    root = tk.Tk()
    #root.iconbitmap("icon/barcode.ico")
    root.title("Barcode Generator")
    root.geometry("400x250")

    # Destination Folder Button
    path_button = tk.Button(root, text="Destination Path", command=select_destination, bg="blue", fg="white", font=("Arial", 10))
    path_button.pack(pady=5, anchor="w", padx=10)

    tk.Label(root, text="Enter Code:", font=("Arial", 12)).pack(pady=5)
    entry = tk.Entry(root, font=("Arial", 12), width=20)
    entry.pack(pady=5)

    # Button Frame
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    process_button = tk.Button(button_frame, text="Generate", command=generate_barcode, bg="green", fg="white", font=("Arial", 12))
    process_button.pack(side=tk.LEFT, padx=5)

    #reset_button = tk.Button(button_frame, text="Reset", command=reset_gui, bg="gray", fg="white", font=("Arial", 12))
    #reset_button.pack(side=tk.LEFT, padx=5)

    exit_button = tk.Button(button_frame, text="Exit", command=root.quit, bg="red", fg="white", font=("Arial", 12))
    exit_button.pack(side=tk.LEFT, padx=5)

    root.mainloop()

# Run the application
main_window()
