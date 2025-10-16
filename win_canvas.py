import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

def open_win_canvas(parent: tk.Tk):
    """
    Abre el reconocedor de lenguaje de señas para Práctica Libre
    """
    try:
        #ruta absoluta, directorio tkint
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
        
        # verificar existencia
        if not os.path.exists(python_path) or not os.path.exists(script_path):
            error_msg = f"No se encontraron los archivos necesarios.\n"
            error_msg += f"Buscando Python en: {python_path}\n"
            error_msg += f"Buscando Script en: {script_path}"
            messagebox.showerror("Error de Ruta", error_msg)
            return
        
        # que no aparezca la terminal
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        subprocess.Popen(
            [python_path, script_path],
            cwd=model_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        messagebox.showinfo(
            "Práctica Libre Iniciada",
            "El reconocedor se ha abierto. Presiona 'q' para cerrar la ventana de la cámara."
        )
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el reconocedor:\n{e}")