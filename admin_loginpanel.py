import tkinter as tk
from tkinter import messagebox
import os
import subprocess

def open_file():
    try:
        subprocess.run(['python', 'gestureflow_sc.py'], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file: {e}")

def login(event=None):
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "kaustuvb":
        root.destroy()
        open_file()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

root = tk.Tk()
root.title("Admin Access Control Panel")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width - 2 * 96  
window_height = screen_height - 2 * 96
root.geometry(f"{window_width}x{window_height}+96+96")
root.configure(bg='white')
frame = tk.Frame(root, bg='white')
frame.place(relx=0.5, rely=0.5, anchor='center')
label_title = tk.Label(frame, text="GestureFlow Developer Build v5.1", font=("Helvetica", 30), bg='white')
label_title.pack(pady=10)
label_username = tk.Label(frame, text="Username", font=("Helvetica", 14), bg='white')
label_username.pack(pady=5)
entry_username = tk.Entry(frame, font=("Helvetica", 14), bg='lightgray', bd=0, highlightthickness=0)
entry_username.pack(pady=5)
label_password = tk.Label(frame, text="Password", font=("Helvetica", 14), bg='white')
label_password.pack(pady=5)
entry_password = tk.Entry(frame, font=("Helvetica", 14), show='*', bg='lightgray', bd=0, highlightthickness=0)
entry_password.pack(pady=5)
entry_password.bind('<Return>', login)  # Bind the Enter key to the login function

root.mainloop()
