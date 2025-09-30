# guarda como loader_tkinter.py
import tkinter as tk, math, time

class LoadingKnob(tk.Tk):
    def __init__(self, total_ms: int = 6000, auto_close: bool = False, title: str = "Cargando…"):
        super().__init__()
        self.title(title)
        self.configure(bg="#0f1226")
        self.resizable(False, False)

        # tamaño/posicion
        w, h = 360, 460
        self.geometry(f"{w}x{h}")

        # canvas y texto
        self.canvas = tk.Canvas(self, width=340, height=320, bg="#0f1226", highlightthickness=0)
        self.canvas.pack(pady=16)
        self.label = tk.Label(self, text="Cargando… 0%", font=("Segoe UI", 14, "bold"),
                              fg="#E6E8FF", bg="#0f1226")
        self.label.pack()

        # estado/animación
        self.cx, self.cy = 170, 160
        self.r_outer, self.r_needle = 110, 95
        self.angle = 0
        self.start = time.time()
        self.total_ms = total_ms
        self.auto_close = auto_close

        # dial base
        self.canvas.create_oval(self.cx-self.r_outer, self.cy-self.r_outer,
                                self.cx+self.r_outer, self.cy+self.r_outer,
                                outline="#2d3569", width=6)
        self.canvas.create_oval(self.cx-self.r_outer+14, self.cy-self.r_outer+14,
                                self.cx+self.r_outer-14, self.cy+self.r_outer-14,
                                outline="#1c2146", width=3)

        # marcas
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

        # aguja
        self.needle = self.canvas.create_line(self.cx, self.cy, self.cx, self.cy-self.r_needle,
                                              width=5, capstyle=tk.ROUND, fill="#B7C0FF")
        self.canvas.create_oval(self.cx-6, self.cy-6, self.cx+6, self.cy+6, fill="#E6E8FF", outline="")

        # animar
        self.after(16, self._animate)

    def _animate(self):
        # giro de la aguja
        self.angle = (self.angle + 6) % 360
        rad = math.radians(self.angle)
        x = self.cx + self.r_needle * math.cos(rad)
        y = self.cy - self.r_needle * math.sin(rad)
        self.canvas.coords(self.needle, self.cx, self.cy, x, y)

        # progreso %
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
    # << Aquí ajustas la duración >>
    app = LoadingKnob(total_ms=8000, auto_close=True, title="Cargando módulo…")
    app.mainloop()
