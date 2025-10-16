import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

class TranslatorWindow:
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.title("ZignaM - Traductor")
        self.win.geometry("360x640+500+150")
        self.win.resizable(False, False)
        self.win.config(bg="#b7d1d4")
        
        self.process = None
        self.is_running = False
        self.translated_text = ""
        
        # Variable para seguimiento
        self.last_detection_time = 0
        
        # archivo temporal (?)
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            try:
                # directorio
                base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            except IndexError:
                app_dir = os.path.dirname(os.path.abspath(__file__))
                base_dir = os.path.dirname(app_dir)
        
        model_dir = os.path.join(base_dir, "Model")
        self.temp_file = os.path.join(model_dir, "last_detection.txt")
        
        # interfaz
        self.create_widgets()
        
        #cerrar ventana
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        #Crea todos los widgets de la interfaz
        # frame principal
        main_frame = tk.Frame(self.win, bg="#b7d1d4",)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # title
        lbl_title = tk.Label(main_frame, text="Traductor LSM", font=("Arial", 20, "bold"), bg="#b7d1d4", fg="#324649")
        lbl_title.pack(pady=(0, 20))
        
        # Area para ver texto
        self.text_display = tk.Text(main_frame, height=10, width=40, relief="solid", bd=1, font=("Arial", 12))
        self.text_display.pack(pady=10, fill="x", expand=True)
        
        # Iniciar/Detener
        self.btn_toggle = tk.Button(main_frame, text="▶️ Iniciar Traducción", font=("Arial", 12, "bold"), bg="#ff8b4d", fg="white", relief="flat", command=self.toggle_recognition)
        self.btn_toggle.pack(pady=10, fill="x")
        
        # Frame INICIAR COPIAR Y BORRAR
        action_frame = tk.Frame(main_frame, bg="#b7d1d4")
        action_frame.pack(fill="x", pady=10)
        
        # Botone
        btn_clear = tk.Button(action_frame, text="🗑️ Borrar",font=("Arial", 8, "bold"),bg="#b7d1d4", relief="flat", command=self.clear_all)
        btn_clear.pack(side="left", expand=True, padx=5)
        
        btn_copy = tk.Button(action_frame, text="📋 Copiar", font=("Arial", 8, "bold"),bg="#b7d1d4", relief="flat", command=self.copy_text)
        btn_copy.pack(side="right", expand=True, padx=5)
        
        # contador de letras
        self.counter_label = tk.Label(main_frame, text="Letras: 0", font=("Arial", 10), bg="#b7d1d4")
        self.counter_label.pack(pady=(10, 0))

    def toggle_recognition(self):
        """Inicia o detiene el proceso de reconocimiento de señas."""
        if not self.is_running:
            try:
                #Rutas a intErprete y a recognize
                if getattr(sys, 'frozen', False):
                    base_dir = os.path.dirname(sys.executable)
                else:
                    try:
                        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
                    except IndexError:
                        app_dir = os.path.dirname(os.path.abspath(__file__))
                        base_dir = os.path.dirname(app_dir)
                
                model_dir = os.path.join(base_dir, "Model")
                python_path = os.path.join(model_dir, ".venv", "Scripts", "python.exe")
                script_path = os.path.join(model_dir, "recognize.py")
                
                if not os.path.exists(python_path) or not os.path.exists(script_path):
                    messagebox.showerror("Error", "No se encontró el script de reconocimiento o el entorno virtual.")
                    return

                self.process = subprocess.Popen([python_path, script_path], cwd=model_dir)
                
                self.is_running = True
                self.btn_toggle.config(text="⏹️ Detener Traducción", bg="#ff4d6d")
                
                #actualizaciones
                self.check_for_updates()

            except Exception as e:
                messagebox.showerror("Error al iniciar", f"No se pudo iniciar el proceso de reconocimiento:\n{e}")
        else:
            if self.process:
                try:
                    self.process.terminate()
                    self.process.wait() # WAIT (they don't love you like I love you) (espera a que termine el proceso)
                except Exception as e:
                    print(f"Error al terminar el proceso: {e}")
                finally:
                    self.process = None

            self.is_running = False
            self.btn_toggle.config(text="▶️ Iniciar Traducción", bg="#ff8b4d")

    def check_for_updates(self):
        if not self.is_running:
            return

        try:
            if os.path.exists(self.temp_file):
                # comprobar con tiempo de modificación
                mod_time = os.path.getmtime(self.temp_file)
                
                if mod_time > self.last_detection_time:
                    self.last_detection_time = mod_time
                    with open(self.temp_file, "r") as f:
                        content = f.read().strip()
                        if content:
                            detected_letter = content.split(',')[0] #toma solo la letra
                            self.translated_text += detected_letter
                            self.text_display.insert("end", detected_letter)
                            self.text_display.see("end") #autoscroll (no creo ocuparlo)
                            self.update_counter()
                            
        except Exception as e:
            print(f"Error leyendo el archivo de detección: {e}")
        
        # Verifica cada 200 milisegundos
        self.win.after(200, self.check_for_updates)

    def clear_all(self):
        if messagebox.askyesno("Confirmar", "Borrar todo el texto?"):
            self.translated_text = ""
            self.text_display.delete("1.0", "end")
            self.update_counter()
    
    def copy_text(self):
        if self.translated_text:
            self.win.clipboard_clear()
            self.win.clipboard_append(self.translated_text)
            messagebox.showinfo("Copiado", "Texto copiado al clipboard")
        else:
            messagebox.showwarning("Aviso", "No hay texto para copiar")
    
    def update_counter(self):
        count = len(self.translated_text)
        self.counter_label.config(text=f"Letras: {count}")
    
    def on_closing(self):
        self.is_running = False
        if self.process:
            try:
                self.process.terminate()
            except Exception as e:
                print(f"Error al cerrar el proceso: {e}")
        
        self.win.destroy()


def open_win_translator(parent: tk.Tk):
    TranslatorWindow(parent)
