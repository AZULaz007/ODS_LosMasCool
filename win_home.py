import tkinter as tk
from tkinter import ttk
import os
from app.win_canvas import open_win_canvas
from app.win_learning import open_win_learning
from app.win_perfil import open_win_perfil
from app.win_retos import open_win_retos
from app.win_translator import open_win_translator


def open_win_home(parent: tk.Tk, user_email="user@example.com", user_username="Usuario"):
    win = tk.Toplevel(parent)
    win.title("ZignaM")
    win.geometry("360x640+500+150")
    win.resizable(False, False)
    win.config(bg="white")

    #Headerw
    base_path = os.path.dirname(os.path.abspath(__file__)) 

    im_path_top = os.path.join(base_path, "images", "pgder.png")
    im_path_mid = os.path.join(base_path, "images", "titl_yawey_ya.png")

    imagen_top = tk.PhotoImage(file=im_path_top)
    imagen_mid = tk.PhotoImage(file=im_path_mid).subsample(2, 2)

    canvas_top = tk.Canvas(win, width=360, height=100, highlightthickness=0)
    canvas_top.place(x=0, y=0)

    canvas_top.create_image(0, -40, anchor="nw", image=imagen_top)
    canvas_top.image = imagen_top

    btn_perfil = tk.Button(win, text="Perfil", bg="#b7d1d4", fg="#324649", font=("Arial", 10, "bold"), relief="flat", highlightthickness=0,command=lambda: open_win_perfil(parent, user_email, user_username)
)
    btn_perfil.place(x=115, y=60, width=50, height=30)

    btn_retos = tk.Button(win, text="Retos", bg="#b7d1d4", fg="#324649", font=("Arial", 10, "bold"), relief="flat", highlightthickness=0, command=lambda: open_win_retos(parent))
    btn_retos.place(x=200, y=60, width=50, height=30)

    btn_ranking = tk.Button(win, text="Ranking", bg="#b7d1d4", fg="#324649", font=("Arial", 10, "bold"), relief="flat", highlightthickness=0)
    btn_ranking.place(x=258, y=60, width=90, height=30)

    #Imagen del medio
    mid_image_height = 80 
    label_mid_image = tk.Label(win, image=imagen_mid, borderwidth=0, highlightthickness=0)
    label_mid_image.image = imagen_mid
    label_mid_image.config(bg="white")
    label_mid_image.place(x=0, y=100, width=360, height=mid_image_height)

    #area del scroll
    scroll_area_y = 100 + mid_image_height
    scroll_area_height = 640 - scroll_area_y

    scroll_canvas = tk.Canvas(win, bg="white", highlightthickness=0)
    scroll_canvas.place(x=0, y=scroll_area_y, width=345, height=scroll_area_height)

    scrollbar = ttk.Scrollbar(win, orient="vertical", command=scroll_canvas.yview)
    scrollbar.place(x=345, y=scroll_area_y, width=15, height=scroll_area_height) 
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    total_button_rows = 5
    button_spacing = 85
    top_margin = 15 
    bottom_margin = 150 

    calculated_height = top_margin + (total_button_rows * button_spacing) + bottom_margin
    total_content_height = calculated_height
    
    main_frame = tk.Frame(scroll_canvas, bg="white", width=360, height=total_content_height) 
    scroll_canvas.create_window((0, 0), window=main_frame, anchor="nw", width=360, height=total_content_height)

    def open_menu():
        btn_abc.place(x=15, y=270, width=75, height=75)
        btn_hand.place(x=270, y=270, width=75, height=75)
        menu_frame.place(x=90, y=270, width=160, height=75)

    def hide_menu():
        menu_frame.place_forget()
        btn_abc.place(x=100, y=270, width=75, height=75)
        btn_hand.place(x=185, y=270, width=75, height=75)

    def open_lesson():
        open_win_learning(parent)  # CAMBIO: Abre modo aprendizaje
        

    def open_practice():
        open_win_canvas(parent)  # Para práctica libre

    def open_translator():
        open_win_translator(parent)

    btn_fila_y = 15

    # Fila 2 azul osc 4 btn
    textos_azulados = ["PRO", "XIM", "AME", "NTE"]
    for i, texto in enumerate(textos_azulados):
        btnz = tk.Button(main_frame, text=texto, bg="#1a1a47", fg="white", relief="flat", borderwidth=0, font=("Arial", 10, "bold"))
        btnz.place(x=15 + i*85, y=btn_fila_y, width=75, height=75)
    btn_fila_y+=85

    # Fila 3 rosa 4 btn
    textos_rosados = ["✏️", "?", "📅", "📋"]
    for i, texto in enumerate(textos_rosados):
        btnr = tk.Button(main_frame, text=texto, bg="#ff4d6d", fg="black", relief="flat", borderwidth=0, font=("Segoe UI Emoji", 18))
        btnr.place(x=15 + i*85, y=btn_fila_y, width=75, height=75)
    btn_fila_y+=85

    # Fila 4 naranja 4 btn
    textos_naranjosos = ["😀", "123", "🍽️"]
    for i, texto in enumerate(textos_naranjosos):
        btnj = tk.Button(main_frame, text=texto, bg="#ff8b4d", fg="black", relief="flat", font=("Segoe UI Emoji", 18))
        btnj.place(x=60 + i*85, y=btn_fila_y, width=75, height=75)
    
    btn_fila_y+=85
    # Fila 5 azul claro btn (ABC y mano)
    btn_abc = tk.Button(main_frame, text="ABC", bg="#00A5BB", relief="flat", font=("Segoe UI Emoji", 18), command=open_menu)
    btn_abc.place(x=100, y=btn_fila_y, width=75, height=75)

    btn_hand = tk.Button(main_frame, text="🖐️", bg="#00A5BB", relief="flat", font=("Segoe UI Emoji", 18), command=open_practice)
    btn_hand.place(x=185, y=btn_fila_y, width=75, height=75)

    # Menu expandible
    menu_frame = tk.Frame(main_frame, bg="#5DC5D3", highlightthickness=0, borderwidth=0)
    tk.Button(menu_frame, text="ABECEDARIO\n15 min\nModo Aprendizaje", bg="#5DC5D3", fg="#324649", relief="flat", borderwidth=0, font=("Asap", 11), anchor='w', command=open_lesson).place(x=20, y=3, width=120, height=72)

    btn_back = tk.Button(menu_frame, text="←", bg="#5DC5D3", fg="white", relief="flat", font=("Segoe UI Emoji", 10), command=hide_menu)
    btn_back.place(x=3, y=1, width=10, height=10)

    btn_fila_y+=85
    btn_lang = tk.Button(main_frame, text="🌐", bg="#b3cccc", relief="flat", font=("Segoe UI Emoji", 20), command=open_translator)
    btn_lang.place(x=140, y=btn_fila_y, width=75, height=75)

    main_frame.update_idletasks()
    scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))
    scroll_canvas.yview_moveto(0.112)