import tkinter as tk
from tkinter import ttk
import os


def open_win_perfil(parent: tk.Tk, user_email: str, user_username: str):
    win = tk.Toplevel(parent)
    win.title("ZignaM")
    win.geometry("360x640+500+100")
    win.resizable(False, False)
    win.config(bg="#dbe5e7")

    base_path = os.path.dirname(os.path.abspath(__file__))

    im_path_top = os.path.join(base_path, "images", "pgder.png")

    imagen_top = tk.PhotoImage(file=im_path_top)

    # Crea canvas para imagen fondo y botones encima
    canvas_top = tk.Canvas(win, width=360, height=120, highlightthickness=0)  # altura incrementada a 120
    canvas_top.place(x=0, y=0)

    # imagen EN CANVAS
    canvas_top.create_image(0, -40, anchor="nw", image=imagen_top)
    canvas_top.image = imagen_top

    # botones SOBRE la imagen EN el canvas (fijos)
    btn_perfil = tk.Button(win, text="Perfil", bg="#b7d1d4", fg="#324649", font=("Arial", 10, "bold"), relief="flat", highlightthickness=0)
    btn_perfil.place(x=110, y=60, width=50, height=30)  # ajustado X para centrar mejor

    btn_retos = tk.Button(win, text="Retos", bg="#b7d1d4", fg="#324649", font=("Arial", 10, "bold"), relief="flat", highlightthickness=0)
    btn_retos.place(x=205, y=60, width=50, height=30)

    btn_ranking = tk.Button(win, text="Ranking", bg="#b7d1d4", fg="#324649", font=("Arial", 10, "bold"), relief="flat", highlightthickness=0)
    btn_ranking.place(x=280, y=60, width=60, height=30)

    # botones sobre la imagen (en la ventana, no en el canvas)
    btn_perfil.place(x=110, y=60, width=50, height=30)
    btn_retos.place(x=205, y=60, width=50, height=30)
    btn_ranking.place(x=280, y=60, width=60, height=30)

    # area principal debajo barra superior
    bottom_frame = tk.Frame(win, bg="white")
    bottom_frame.place(x=0, y=120, width=360, height=520) 

    # Icono usuario y correo sin @
    profile_frame = tk.Frame(bottom_frame, bg="white")
    profile_frame.pack(pady=(15, 20), padx=15, anchor="w")
    user_icon = tk.Label(profile_frame, text="👤", font=("Arial", 30), bg="white")
    user_icon.grid(row=0, column=0, rowspan=2, padx=(0, 10))
    correo_sin_arroba = user_email.split("@")[0]
    lbl_email = tk.Label(profile_frame, text=correo_sin_arroba, font=("Arial", 16, "bold"), bg="white")  # tamaño más grande
    lbl_email.grid(row=0, column=1, sticky="w")
    lbl_email_small = tk.Label(profile_frame, text=user_email, fg="gray", font=("Arial", 12), bg="white")  # tamaño más visible
    lbl_email_small.grid(row=1, column=1, sticky="w")

    # estilo
    def create_card(parent, title, bullet_points, bg_color, fg_color="black"):
        card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid", padx=10, pady=10)
        lbl_title = tk.Label(card, text=title, font=("Arial", 14, "bold"), bg=bg_color, fg=fg_color)
        lbl_title.pack(anchor="w")
        for point in bullet_points:
            lbl = tk.Label(card, text=f" {point}", font=("Arial", 11), bg=bg_color, fg=fg_color)
            lbl.pack(anchor="w", padx=15, pady=2)
        return card

    # plan báscio
    bullet_basico = ["Lecciones progresivas", "Retroalimentación inmediata", "Traducciones"]
    card_basico = create_card(bottom_frame, "Plan Básico Gratuito", bullet_basico, "#a9b8b9", fg_color="#324649")
    card_basico.pack(fill="x", padx=15, pady=(5, 8))

    # plan prof
    bullet_pro = ["Salud, Educación, Legal", "Empresas", "Recuersos"]
    card_pro = create_card(bottom_frame, "Plan Profesionalizante", bullet_pro, "#5a9bab", fg_color="black")
    card_pro.pack(fill="x", padx=15, pady=(0, 8))

    # proximamente
    bullet_next = ["Animaciones/Recursos", "Expansión"]
    card_next = create_card(bottom_frame, "Próximamente!", bullet_next, "#394b4e", fg_color="white")
    card_next.pack(fill="x", padx=15, pady=(0, 10))

    win.user_email = user_email
    win.user_username = user_username

    win.mainloop()
