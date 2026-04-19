"""
Ferramenta interativa de localização de campos.
Clique no formulário para capturar as coordenadas dos campos.
"""
import tkinter as tk
from tkinter import messagebox
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import io

PDF_ORIGINAL = "/Users/clinicabeneser/Downloads/EXAMES UNIMED.pdf"
ROTACAO      = 270    # graus horário para renderizar em paisagem
ESCALA       = 0.25   # zoom de exibição

CAMPOS = ["NOME", "INDICAÇÃO CLÍNICA", "DESCRIÇÃO (1ª linha)"]
CORES  = ["#f38ba8", "#a6e3a1", "#89b4fa"]


def renderizar_pdf():
    doc  = fitz.open(PDF_ORIGINAL)
    page = doc[0]
    mat  = fitz.Matrix(ESCALA, ESCALA).prerotate(ROTACAO)
    pix  = page.get_pixmap(matrix=mat)
    img  = Image.open(io.BytesIO(pix.tobytes("png")))
    return img, pix.width, pix.height


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Localizar Campos — clique sobre cada campo")
        self.configure(bg="#1e1e2e")

        self.campo_idx = 0
        self.coords    = {}

        # Renderiza PDF
        img, self.img_w, self.img_h = renderizar_pdf()
        self.photo = ImageTk.PhotoImage(img)

        # PDF dimensions (landscape após rotação)
        self.pdf_w = self.img_w / ESCALA
        self.pdf_h = self.img_h / ESCALA

        self._build_ui()

    def _build_ui(self):
        # Barra de instrução
        self.lbl_campo = tk.Label(
            self, text=f"► Clique no campo:  {CAMPOS[0]}",
            font=("Helvetica", 14, "bold"), fg="white", bg="#1e1e2e", pady=6
        )
        self.lbl_campo.pack(fill="x")

        self.lbl_pos = tk.Label(
            self, text="Posição do cursor: —",
            font=("Helvetica", 11), fg="#cdd6f4", bg="#1e1e2e"
        )
        self.lbl_pos.pack(fill="x")

        # Canvas com scroll
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)

        sbv = tk.Scrollbar(frame, orient="vertical")
        sbh = tk.Scrollbar(frame, orient="horizontal")
        sbv.pack(side="right",  fill="y")
        sbh.pack(side="bottom", fill="x")

        self.canvas = tk.Canvas(
            frame,
            width=min(self.img_w, 1300),
            height=min(self.img_h, 700),
            bg="gray20", cursor="crosshair",
            xscrollcommand=sbh.set,
            yscrollcommand=sbv.set,
            highlightthickness=0
        )
        self.canvas.pack(side="left", fill="both", expand=True)
        sbv.config(command=self.canvas.yview)
        sbh.config(command=self.canvas.xview)

        # Desenha imagem
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo, tags="img")
        self.canvas.config(scrollregion=(0, 0, self.img_w, self.img_h))

        self.canvas.bind("<Motion>",   self.on_move)
        self.canvas.bind("<Button-1>", self.on_click)

    def on_move(self, event):
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        px = int(cx / ESCALA)
        py = int(self.pdf_h - cy / ESCALA)
        self.lbl_pos.config(text=f"x = {px}   y = {py}")

    def on_click(self, event):
        if self.campo_idx >= len(CAMPOS):
            return

        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        px = int(cx / ESCALA)
        py = int(self.pdf_h - cy / ESCALA)

        campo = CAMPOS[self.campo_idx]
        self.coords[campo] = (px, py)
        cor = CORES[self.campo_idx]

        # Marcador visual
        r = 10
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
                                 fill=cor, outline="black", width=2)
        self.canvas.create_text(cx + 16, cy, text=campo, anchor="w",
                                 font=("Helvetica", 11, "bold"), fill=cor)

        self.campo_idx += 1

        if self.campo_idx < len(CAMPOS):
            self.lbl_campo.config(
                text=f"► Clique no campo:  {CAMPOS[self.campo_idx]}"
            )
        else:
            self.lbl_campo.config(text="✓  Todos os campos marcados!")
            self.after(300, self.mostrar_resultado)

    def mostrar_resultado(self):
        print("\n=== COORDENADAS CAPTURADAS ===")
        linhas = []
        for campo, (x, y) in self.coords.items():
            print(f'  {campo}: x={x}, y={y}')
            linhas.append(f"  {campo}:\n    x={x}, y={y}")
        msg = "Coordenadas capturadas:\n\n" + "\n\n".join(linhas)
        messagebox.showinfo("Coordenadas", msg)


if __name__ == "__main__":
    app = App()
    app.mainloop()
