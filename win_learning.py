import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import time
from PIL import Image, ImageTk

# Posición como constantes
CAMERA_X = 235
CAMERA_Y = 130

LEARNING_WINDOW_WIDTH = 360
LEARNING_WINDOW_HEIGHT = 640
LEARNING_X = CAMERA_X + 640 + 20
LEARNING_Y = CAMERA_Y

WINDOW_GEOMETRY = f"{LEARNING_WINDOW_WIDTH}x{LEARNING_WINDOW_HEIGHT}+{LEARNING_X}+{LEARNING_Y}"

class LearningWindow:
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.title("ZignaM - Aprendizaje")
        
        self.win.geometry(WINDOW_GEOMETRY) 
        self.win.resizable(False, False)
        self.win.config(bg="white")
        
        self.lessons = ['A', 'B', 'C', 'D', 'E']
        self.current_lesson_index = 0
        self.process = None  
        self.checking = False
        
        #errores
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            try:
                base_dir = os.path.dirname(os.path.abspath(sys.argv[0])) 
            except IndexError:
                app_dir = os.path.dirname(os.path.abspath(__file__))
                base_dir = os.path.dirname(app_dir)
        
        model_dir = os.path.join(base_dir, "Model")
        self.temp_file = os.path.join(model_dir, "last_detection.txt")
        
        self.start_camera_process(model_dir)
        
        self.create_widgets()
        self.show_current_lesson()
        
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_camera_process(self, model_dir):
        #iniciar cámara (con el debug)
        try:
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
            
            python_path = os.path.join(model_dir, ".venv", "Scripts", "python.exe")
            script_path = os.path.join(model_dir, "recognize.py")
            
            print(f"DEBUG: Python path: {python_path}")
            print(f"DEBUG: Script path: {script_path}")
            print(f"DEBUG: Python exists? {os.path.exists(python_path)}")
            print(f"DEBUG: Script exists? {os.path.exists(script_path)}")
            
            if not os.path.exists(python_path) or not os.path.exists(script_path):
                error_msg = f"No se encontraron los archivos necesarios para la cámara.\n"
                error_msg += f"Buscando Python en: {python_path}\n"
                error_msg += f"Buscando Script en: {script_path}"
                messagebox.showerror("Error de Ruta", error_msg)
                self.win.destroy()  # cierra ventana si no hay camara
                return
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            self.process = subprocess.Popen([python_path, script_path],cwd=model_dir,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar la cámara:\n{e}")
            print(f"DEBUG ERROR: {e}")
            self.process = None
            self.win.destroy()

    def create_widgets(self):
        header_frame = tk.Frame(self.win, bg="#b7d1d4", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        #usar éste formato en códigos futuros, está más legible
        tk.Label(
            header_frame,
            text="ABECEDARIO",
            font=("Arial", 18, "bold"),
            bg="#b7d1d4",
            fg="white"
        ).pack(pady=25)
        
        instruction_frame = tk.Frame(self.win, bg="white", height=200)
        instruction_frame.pack(fill="x", pady=10)
        instruction_frame.pack_propagate(False)
        
        tk.Label(
            instruction_frame,
            text="Haz esta seña:",
            font=("Arial", 14),
            bg="white",
            fg="#707070"
        ).pack(pady=(5, 2))
        
        # imagen seña
        self.sign_image_label = tk.Label(
            instruction_frame,
            bg="white"
        )
        self.sign_image_label.pack(pady=5)
        
        self.letter_label = tk.Label(
            instruction_frame,
            text="",
            font=("Arial", 36, "bold"),
            bg="white",
            fg="#324649"
        )
        self.letter_label.pack()
        
        self.feedback_label = tk.Label(
            self.win,
            text="Cámara lista. Presiona 'Iniciar Verificación'.",
            font=("Arial", 14),
            bg="white",
            fg="#707070",
            wraplength=320
        )
        self.feedback_label.pack(pady=10)
        
        progress_frame = tk.Frame(self.win, bg="white")
        progress_frame.pack(pady=10)
        
        tk.Label(
            progress_frame,
            text="Progreso:",
            font=("Arial", 12),
            bg="white",
            fg="#707070"
        ).pack(side="left", padx=5)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="0/5",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#324649"
        )
        self.progress_label.pack(side="left")
        
        #progreso self-directioned (que avanzan a su ritmo pues)
        self.progress_canvas = tk.Canvas(self.win, width=320, height=20, bg="white", highlightthickness=0)
        self.progress_canvas.pack(pady=10)
        self.update_progress_bar()
        
        button_frame = tk.Frame(self.win, bg="white")
        button_frame.pack(pady=30)
        
        self.btn_start = tk.Button(
            button_frame,
            text="Iniciar Verificación",
            font=("Arial", 14, "bold"),
            bg="#324649",
            fg="white",
            width=15,
            height=2,
            relief="flat",
            command=self.start_lesson
        )
        self.btn_start.pack(pady=5)
        
        self.btn_next = tk.Button(
            button_frame,
            text="Siguiente",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
            height=2,
            relief="flat",
            command=self.next_lesson,
            state="disabled"
        )
        self.btn_next.pack(pady=5)
        
        self.btn_skip = tk.Button(
            button_frame,
            text="Saltar",
            font=("Arial", 12),
            bg="#ff8b4d",
            fg="white",
            width=15,
            height=1,
            relief="flat",
            command=self.skip_lesson
        )
        self.btn_skip.pack(pady=5)

    def show_current_lesson(self):
        if self.current_lesson_index < len(self.lessons):
            current_letter = self.lessons[self.current_lesson_index]
            self.letter_label.config(text=current_letter)
            self.progress_label.config(text=f"{self.current_lesson_index}/{len(self.lessons)}")
            self.update_progress_bar()
            self.load_sign_image(current_letter)
        else:
            self.lesson_complete()
    
    def load_sign_image(self, letter):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_path, "images", "signs", f"{letter}.png")
        
            if not os.path.exists(image_path):
                image_path = os.path.join(base_path, "images", "signs", f"{letter.lower()}.png")
        
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((120, 120), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.sign_image_label.config(image=photo, text="")
                self.sign_image_label.image = photo
            else:
                self.sign_image_label.config(image="", text=f"📷 {letter}", font=("Arial", 30))
        except:
            self.sign_image_label.config(image="", text=f"📷 {letter}", font=("Arial", 30))
    
    def update_progress_bar(self):
        self.progress_canvas.delete("all")
        self.progress_canvas.create_rectangle(0, 0, 320, 20, fill="#E0E0E0", outline="")
        
        if len(self.lessons) > 0:
            progress_width = (self.current_lesson_index / len(self.lessons)) * 320
            self.progress_canvas.create_rectangle(0, 0, progress_width, 20, fill="#00A5BB", outline="")
    
    def start_lesson(self):
        if not self.process or self.process.poll() is not None:
             messagebox.showerror("Error", "La cámara no está activa. Por favor, reinicia")
             return
             
        if self.checking: 
            self.feedback_label.config(text="Ya se está verificando la seña.", fg="orange")
            return
             
        try:
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
            
            self.btn_start.config(state="disabled")
            self.feedback_label.config(
                text=f"Haz la seña '{self.lessons[self.current_lesson_index]}'!\nLa cámara está activa. Manten la seña.",
                fg="#00A5BB"
            )
            
            self.checking = True
            self.check_detection()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar la verificación:\n{e}")
            self.btn_start.config(state="normal") 

    def check_detection(self):
        if not self.checking:
            return
        
        try:
            if os.path.exists(self.temp_file):
                
                with open(self.temp_file, 'r') as f:
                    detected = f.read().strip()
                
                target = self.lessons[self.current_lesson_index]
                
                if detected == target:
                    self.checking = False
                    self.feedback_label.config(
                        text=f"Excelente! Lograste usar '{target}' correctamente ✓",
                        fg="#4CAF50"
                    )
                    self.btn_next.config(state="normal")
                    self.btn_start.config(state="disabled") 
                    
                    os.remove(self.temp_file)
                    return
                
                if detected != '' and detected != target:
                    self.checking = False 
                    self.feedback_label.config(
                        text=f"Detectado: '{detected}'. Intenta la seña '{target}' de nuevo.",
                        fg="red"
                    )
                    self.btn_start.config(state="normal")
                    os.remove(self.temp_file) 
                    return
                
                if detected == '':
                    os.remove(self.temp_file) 
           #errores         
        except FileNotFoundError:
             pass
        except Exception as e:
            self.checking = False
            self.btn_start.config(state="normal")
            self.feedback_label.config(text=f"Error de lectura del archivo: {e}", fg="red")
            return
        
        if self.checking:
            self.win.after(500, self.check_detection)
    
    def next_lesson(self):
        self.current_lesson_index += 1
        self.btn_next.config(state="disabled")
        self.btn_start.config(state="normal") 
        self.checking = False
        
        if self.current_lesson_index < len(self.lessons):
            self.show_current_lesson()
            self.feedback_label.config(
                text="Presiona 'Iniciar Verificación' para la siguiente lección", 
                fg="#707070"
            )
        else:
            self.lesson_complete()
    
    def skip_lesson(self):
        self.checking = False 
        self.btn_start.config(state="normal") 
            
        if messagebox.askyesno("Saltar", "¿Quieres saltar esta lección?"):
            self.next_lesson()
            
    def lesson_complete(self):
        self.letter_label.config(text="🎉")
        self.sign_image_label.config(image="", text="")
        self.feedback_label.config(
            text="Completaste todas las lecciones!",
            fg="#4CAF50"
        )
        self.btn_start.config(state="disabled")
        self.btn_next.config(state="disabled")
        self.btn_skip.config(state="disabled")
        
        messagebox.showinfo(
            "Felicidades!",
            f"Completaste {len(self.lessons)} lecciones!\nSigue practicando!"
        )
    
    def on_closing(self):
        self.checking = False
        
        if self.process:
            try:
                self.process.terminate() 
            except:
                pass
        
        if os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
            except:
                pass
        
        self.win.destroy()


def open_win_learning(parent: tk.Tk):
    LearningWindow(parent)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_win_learning(root)
    root.mainloop()