import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from app.win_home import open_win_home



def main():
    root = tk.Tk()
    root.title("ZignaM - LSM")
    root.geometry("360x640+500+100")
    root.resizable(False, False)
    root.config(bg="white")

    #Imagen logo
    base_path = os.path.dirname(os.path.abspath(__file__))
    image_pathl = os.path.join(base_path, "images", "logo.png")
    logo_image = Image.open(image_pathl)
    imagen_midl = ImageTk.PhotoImage(file=image_pathl)

    #Imagen title
    base_path = os.path.dirname(os.path.abspath(__file__))
    image_patht = os.path.join(base_path, "images", "titl_chikito.png")
    logo_image = Image.open(image_patht)
    imagen_midt = ImageTk.PhotoImage(file=image_patht)

    # Imagen logo (fijo)
    mid_image_height = 200 
    label_mid_image = tk.Label(root, image=imagen_midl, borderwidth=0, highlightthickness=0, bg="white")
    label_mid_image.image = imagen_midl
    label_mid_image.place(x=0, y=10, width=360, height=mid_image_height)

    # Imagen title (fijo)
    mid_image_height = 50 
    label_mid_image = tk.Label(root, image=imagen_midt, borderwidth=0, highlightthickness=0, bg="white")
    label_mid_image.image = imagen_midt
    label_mid_image.place(x=0, y=200, width=360, height=mid_image_height)

    # Ubicación absoluta para los demás widgets, con place()

    label_subtitle = tk.Label(root, text="Inicia sesión", font=("Arial", 18), fg="#222", bg="white")
    label_subtitle.place(x=120, y=260)

    label_small = tk.Label(root, text="Listo para expandir tu mente?", font=("Arial", 11), fg="#707070", bg="white")
    label_small.place(x=90, y=300)

    label_email = tk.Label(root, text="Email", font=("Arial", 10, "bold"), fg="#228fa1", bg="white")
    label_email.place(x=20, y=340)

    entry_email = ttk.Entry(root, width=32, font=("Arial", 10))
    entry_email.insert(0, "")
    entry_email.place(x=20, y=365, width=320, height=25)

    label_password = tk.Label(root, text="Contraseña", font=("Arial", 10, "bold"), fg="#228fa1", bg="white")
    label_password.place(x=20, y=400)

    entry_password = ttk.Entry(root, width=32, show="•", font=("Arial", 10))
    entry_password.place(x=20, y=425, width=320, height=25)

    def toggle_password():
        if entry_password.cget('show') == '':
            entry_password.config(show='•')
            btn_toggle.config(text='👁️')
        else:
            entry_password.config(show='')
            btn_toggle.config(text='👁️')

    btn_toggle = tk.Button(root, text='👁️', font=("Arial", 12), bg="white", relief="flat", command=toggle_password)
    btn_toggle.place(x=310, y=425, width=40, height=25)

    label_error = tk.Label(root, text="", font=("Arial", 10), fg="red", bg="white")
    label_error.place(x=20, y=480)
    
    def sign_in():
        email = entry_email.get()
        password = entry_password.get()
    
        # validaciones de entrada
        if "@" not in email:
            label_error.config(text="El correo debe contener '@'.")
            return
        if not any(c.isdigit() for c in password):
            label_error.config(text="La contraseña debe tener al menos un número.")
            return
    
        # Si cumple con todo
        label_error.config(text="Inicio de sesión exitoso.", fg="green")
    
        # tomar user name
        username = email.split('@')[0]
    
        # Ocultar login y abrir Home
        root.withdraw()
        open_win_home(root, user_email=email, user_username=username)  # PASAR DATOS


    btn_sign_in = tk.Button(root, text="Sign in", font=("Arial", 12), bg="#22b7c5", fg="white", height=2, command=sign_in, relief="flat")
    btn_sign_in.place(x=20, y=500, width=320, height=50)

    root.mainloop()

if __name__ == "__main__":
        main()
