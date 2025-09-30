import tkinter as tk
from tkinter import messagebox

# Tamaño fijo de la ventana
WIDTH, HEIGHT = 420, 340

# ---------------- Pantallas ----------------
def show_login():
    clear_window()
    tk.Label(root, text="ZignaM", font=("Arial", 20)).pack(pady=10)
    tk.Label(root, text="Inicia sesión").pack()
    tk.Entry(root).pack(pady=5)
    tk.Entry(root, show="*").pack(pady=5)
    tk.Button(root, text="Sign in", command=show_welcome).pack(pady=10)

def show_welcome():
    clear_window()
    tk.Label(root, text="ZignaM", font=("Arial", 20)).pack(pady=10)
    tk.Label(root, text="¿Sabías que la lengua de señas no es universal?").pack(pady=40)
    tk.Button(root, text="Continuar", command=show_menu).pack(pady=10)

def show_menu():
    clear_window()
    tk.Label(root, text="Menú principal", font=("Arial", 16)).pack(pady=10)
    tk.Button(root, text="Lección: Abecedario", command=show_lesson).pack(pady=5)
    tk.Button(root, text="Perfil", command=lambda: messagebox.showinfo("Info","Sección en construcción")).pack(pady=5)
    tk.Button(root, text="Volver al login", command=show_login).pack(pady=10)

def show_lesson():
    clear_window()
    tk.Label(root, text="Lección 1: Abecedario", font=("Arial", 14)).pack(pady=10)
    tk.Label(root, text="Replica esta seña frente a la cámara:").pack(pady=10)
    tk.Label(root, text="👋 (placeholder)").pack(pady=20)
    tk.Button(root, text="Validar", command=show_feedback).pack(pady=5)
    tk.Button(root, text="Volver al menú", command=show_menu).pack(pady=5)

def show_feedback():
    clear_window()
    tk.Label(root, text="✔️", font=("Arial", 40), fg="green").pack(pady=20)
    tk.Label(root, text="¡Seña reconocida!").pack(pady=10)
    tk.Button(root, text="Repetir", command=show_lesson).pack(pady=5)
    tk.Button(root, text="Continuar", command=show_menu).pack(pady=5)

# ---------------- Utilidad ----------------
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# ---------------- Ventana principal ----------------
root = tk.Tk()
root.title("ZignaM")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

show_login()  # inicia en login

root.mainloop()
