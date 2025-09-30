# loader_tkinter.py
import tkinter as tk, math, time

class LoadingKnob(tk.Tk):
    def __init__(self, total_ms: int = 6000, auto_close: bool = False, title: str = "Cargando…"):
        super().__init__()
        self.title(title)
        self.configure(bg="#0f1226")
        self.resizable(False, False)

        # ===== Tamaño de ventana: 420 x 340 (centrada) =====
        w, h = 420, 340
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        # ===== Área de dibujo adaptada a la altura =====
        self.canvas = tk.Canvas(self, width=380, height=200, bg="#0f1226", highlightthickness=0)
        self.canvas.pack(pady=(10, 6))

        self.label = tk.Label(self, text="Cargando… 0%", font=("Segoe UI", 13, "bold"),
                              fg="#E6E8FF", bg="#0f1226")
        self.label.pack(pady=(0, 4))

        # Estado/animación
        self.cx, self.cy = 190, 100      # centro del dial dentro del canvas
        self.r_outer, self.r_needle = 90, 78
        self.angle = 0
        self.start = time.time()
        self.total_ms = total_ms
        self.auto_close = auto_close

        # Dial base
        self.canvas.create_oval(self.cx-self.r_outer, self.cy-self.r_outer,
                                self.cx+self.r_outer, self.cy+self.r_outer,
                                outline="#2d3569", width=6)
        self.canvas.create_oval(self.cx-self.r_outer+14, self.cy-self.r_outer+14,
                                self.cx+self.r_outer-14, self.cy+self.r_outer-14,
                                outline="#1c2146", width=3)

        # Marcas
        for deg in range(0, 360, 10):
            rad = math.radians(deg)
            r1 = self.r_outer - 18
            r2 = self.r_outer - (30 if deg % 30 == 0 else 24)
            x1 = self.cx + r1 * math.cos(rad)
            y1 = self.cy - r1 * math.sin(rad)
            x2 = self.cx + r2 * math.cos(rad)
            y2 = self.cy - r2 * math.sin(rad)
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="#5c66a7" if deg % 30 == 0 else "#3c447b",
                width=3 if deg % 30 == 0 else 1
            )

        # Aguja
        self.needle = self.canvas.create_line(self.cx, self.cy, self.cx, self.cy-self.r_needle,
                                              width=5, capstyle=tk.ROUND, fill="#B7C0FF")
        self.canvas.create_oval(self.cx-6, self.cy-6, self.cx+6, self.cy+6, fill="#E6E8FF", outline="")

        # Animación
        self.after(16, self._animate)

    def _animate(self):
        # Giro de la aguja
        self.angle = (self.angle + 6) % 360
        rad = math.radians(self.angle)
        x = self.cx + self.r_needle * math.cos(rad)
        y = self.cy - self.r_needle * math.sin(rad)
        self.canvas.coords(self.needle, self.cx, self.cy, x, y)

        # Progreso %
        elapsed = int((time.time() - self.start) * 1000)
        pct = max(0, min(100, int(100 * elapsed / self.total_ms)))
        self.label.config(text=f"Cargando… {pct}%")

        if pct >= 100:
            self.label.config(text="¡Listo!")
            if self.auto_close:
                self.after(700, self.destroy)
        else:
            self.after(16, self._animate)

if __name__ == "__main__":
    # Ajusta la duración aquí (ms) y si se autocierra
    app = LoadingKnob(total_ms=8000, auto_close=True, title="Cargando módulo…")
    app.mainloop()
