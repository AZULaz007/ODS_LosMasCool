import tkinter as tk
from tkinter import messagebox
import os
import random
from PIL import Image, ImageTk

# --- Constantes de Configuración ---
MAIN_BG = "#eaf2f3"
HEADER_DARK = "#324649"
CARD_PINK = "#e85d95"
CARD_ORANGE = "#ffa54f"
CARD_CYAN = "#54a7c0"
CARD_SIZE = 120
CARD_BORDER = 8

class RetosWindow:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("ZignaM - Retos")
        self.win.geometry("360x640+500+100")
        self.win.resizable(False, False)
        self.win.config(bg=MAIN_BG)

        self.base_path = os.path.dirname(os.path.abspath(__file__))

        # challenges/ retos
        self.challenges = [
            {'letter': 'A', 'options': ['A.png', 'E.png', 'B.png'], 'correct_answer': 'A.png'},
            {'letter': 'B', 'options': ['B.png', 'D.png', 'C.png'], 'correct_answer': 'B.png'},
            {'letter': 'C', 'options': ['C.png', 'A.png', 'E.png'], 'correct_answer': 'C.png'},
        ]
        random.shuffle(self.challenges)
        self.current_challenge_index = 0

        self.create_widgets()
        self.setup_challenge()

    def create_widgets(self):
        # header
        im_path_top = os.path.join(self.base_path, "images", "pgder.png")
        self.imagen_top = tk.PhotoImage(file=im_path_top)
        
        # Crea canvas para imagen fondo y botones encima
        canvas_top = tk.Canvas(self.win, width=360, height=120, highlightthickness=0) # altura incrementada a 120
        canvas_top.place(x=0, y=0)
        
        # imagen EN CANVAS
        canvas_top.create_image(0, -40, anchor="nw", image=self.imagen_top)

        # botones SOBRE la imagen EN el canvas (fijos)
        # botones sobre la imagen (en la ventana, no en el canvas)
        tk.Button(self.win, text="Perfil", bg="#b7d1d4", fg="#324649", font=("Arial", 10, "bold"), relief="flat").place(x=110, y=60, width=50, height=30) # ajustado X para centrar mejor
        tk.Button(self.win, text="Retos", bg="#b7d1d4", fg="#324649", font=("Arial", 10, "bold"), relief="flat").place(x=205, y=60, width=50, height=30)
        tk.Button(self.win, text="Ranking", bg="#b7d1d4", fg="#324649", font=("Arial", 10, "bold"), relief="flat").place(x=280, y=60, width=60, height=30)

        # se me acaba el tiempo aaa
        main_frame = tk.Frame(self.win, bg=MAIN_BG)
        main_frame.place(x=0, y=120, width=360, height=520)

        # Letra grande del reto
        self.lbl_letter = tk.Label(main_frame, text="", font=("Arial", 150, "bold"), bg=MAIN_BG, fg=HEADER_DARK)
        self.lbl_letter.place(relx=0.5, y=20, anchor="n")

        # Frame para los cuadros colores
        self.cards_frame = tk.Frame(main_frame, bg=MAIN_BG)
        self.cards_frame.place(x=0, y=230, width=360, height=400)

    def setup_challenge(self):
        """Configura y muestra el reto actual en la interfaz."""
        if self.current_challenge_index >= len(self.challenges):
            messagebox.showinfo("Felicidades!", "Completaste los retos")
            self.win.destroy()
            return

        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        challenge = self.challenges[self.current_challenge_index]
        self.lbl_letter.config(text=challenge['letter'])

        options = challenge['options'][:]
        random.shuffle(options)
        
        # Posiciones y colores para cada cuadro (rosa, naranja, azul cyan)
        card_positions = [
            {'color': CARD_PINK, 'x': 30, 'y': 20},    # cuadro 1 rosa
            {'color': CARD_ORANGE, 'x': 210, 'y': 20}, # cuadro naranja
            {'color': CARD_CYAN, 'x': 120, 'y': 170}   # cuadro azul cyan, # centrar horizontal: (360 - CARD_SIZE) / 2 = 120
        ]

        for i, option_img in enumerate(options):
            pos = card_positions[i]
            self.create_hand_card(self.cards_frame, pos['color'], pos['x'], pos['y'], option_img)

    #crear cuadros colores
    def create_hand_card(self, parent, border_color, x_pos, y_pos, image_filename):
        
        border_frame = tk.Frame(parent, bg=border_color, width=CARD_SIZE, height=CARD_SIZE)
        border_frame.place(x=x_pos, y=y_pos)

        try:
            img_path = os.path.join(self.base_path, "images", "signs", image_filename)
            
            pil_image = Image.open(img_path)
            pil_image = pil_image.resize((CARD_SIZE - CARD_BORDER * 2, CARD_SIZE - CARD_BORDER * 2), Image.LANCZOS)
            photo_image = ImageTk.PhotoImage(pil_image)

            btn = tk.Button(
                border_frame,
                image=photo_image,
                relief="flat",
                bg="white",
                command=lambda img=image_filename: self.check_answer(img)
            )
            btn.image = photo_image 
            btn.pack(padx=CARD_BORDER, pady=CARD_BORDER)
        #error
        except FileNotFoundError:
            btn = tk.Button(
                border_frame,
                text=f"No se\nencontró\n{image_filename}",
                font=("Arial", 10),
                bg="white",
                command=lambda img=image_filename: self.check_answer(img)
            )
            btn.pack(padx=CARD_BORDER, pady=CARD_BORDER, fill="both", expand=True)
        #check answer respuesta
    def check_answer(self, selected_image):
        correct_answer = self.challenges[self.current_challenge_index]['correct_answer']
        
        if selected_image == correct_answer:
            messagebox.showinfo("CORRECTO", "Pasando al siguiente reto")
            self.current_challenge_index += 1
            self.setup_challenge()
        else:
            messagebox.showerror("INCORRECTO", "Inténtalo de nuevo")


def open_win_retos(parent: tk.Tk):
    RetosWindow(parent)


